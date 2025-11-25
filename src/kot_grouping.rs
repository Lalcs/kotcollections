use pyo3::prelude::*;
use pyo3::types::PyDict;

/// A structure for group-and-fold operations on collections.
/// KotGrouping is an intermediate representation that groups elements by key.
#[pyclass]
#[derive(Clone)]
pub struct KotGrouping {
    elements: Vec<PyObject>,
    key_selector: PyObject,
}

#[pymethods]
impl KotGrouping {
    #[new]
    fn new(py: Python<'_>, elements: &PyAny, key_selector: &PyAny) -> PyResult<Self> {
        let mut elems = Vec::new();
        let iter = elements.iter()?;
        for item in iter {
            elems.push(item?.into_py(py));
        }

        Ok(KotGrouping {
            elements: elems,
            key_selector: key_selector.into_py(py),
        })
    }

    /// Returns a Map where keys are elements from keySelector and values are the number of elements in each group.
    fn each_count(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_map_class = module.getattr("KotMap")?;

        let dict = PyDict::new(py);
        let selector = self.key_selector.as_ref(py);

        for element in &self.elements {
            let key = selector.call1((element.as_ref(py),))?;
            let current_count: i64 = match dict.get_item(&key)? {
                Some(v) => v.extract().unwrap_or(0),
                None => 0,
            };
            dict.set_item(&key, current_count + 1)?;
        }

        Ok(kot_map_class.call1((dict,))?.into_py(py))
    }

    /// Returns a Map where keys are elements from keySelector and values are elements in each group.
    fn each_count_to(&self, py: Python<'_>, destination: &PyAny) -> PyResult<PyObject> {
        let selector = self.key_selector.as_ref(py);

        for element in &self.elements {
            let key = selector.call1((element.as_ref(py),))?;

            // Try to get existing count
            let current_count: i64 = if let Ok(value) = destination.call_method1("get", (key,)) {
                if value.is_none() { 0 } else { value.extract().unwrap_or(0) }
            } else {
                0
            };

            destination.call_method1("put", (key, current_count + 1))?;
        }

        Ok(destination.into_py(py))
    }

    /// Groups elements from the source by key and applies operation to each group.
    fn fold(
        &self,
        py: Python<'_>,
        initial_value_selector: &PyAny,
        operation: &PyAny,
    ) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_map_class = module.getattr("KotMap")?;

        let dict = PyDict::new(py);
        let selector = self.key_selector.as_ref(py);

        // Track which keys we've seen to initialize accumulators
        let mut seen_keys: Vec<PyObject> = Vec::new();

        for element in &self.elements {
            let key = selector.call1((element.as_ref(py),))?.into_py(py);

            // Check if we've seen this key before
            let key_exists = seen_keys.iter().any(|k| {
                k.as_ref(py).eq(key.as_ref(py)).unwrap_or(false)
            });

            if !key_exists {
                // First element with this key - initialize the accumulator
                let initial = initial_value_selector.call1((key.as_ref(py),))?;
                let result = operation.call1((key.as_ref(py), initial, element.as_ref(py)))?;
                dict.set_item(key.as_ref(py), result)?;
                seen_keys.push(key);
            } else {
                // Subsequent element - use existing accumulator
                let accumulator = dict.get_item(&key).unwrap();
                let result = operation.call1((key.as_ref(py), accumulator, element.as_ref(py)))?;
                dict.set_item(key.as_ref(py), result)?;
            }
        }

        Ok(kot_map_class.call1((dict,))?.into_py(py))
    }

    /// Groups elements from the source by key and applies operation to each group, storing results in destination.
    fn fold_to(
        &self,
        py: Python<'_>,
        destination: &PyAny,
        initial_value_selector: &PyAny,
        operation: &PyAny,
    ) -> PyResult<PyObject> {
        let selector = self.key_selector.as_ref(py);

        for element in &self.elements {
            let key = selector.call1((element.as_ref(py),))?;

            // Check if key exists in destination
            let has_key = destination.call_method1("contains_key", (key,))?.is_true()?;

            if !has_key {
                // First element with this key - initialize the accumulator
                let initial = initial_value_selector.call1((key,))?;
                let result = operation.call1((key, initial, element.as_ref(py)))?;
                destination.call_method1("put", (key, result))?;
            } else {
                // Subsequent element - use existing accumulator
                let accumulator = destination.call_method1("get", (key,))?;
                let result = operation.call1((key, accumulator, element.as_ref(py)))?;
                destination.call_method1("put", (key, result))?;
            }
        }

        Ok(destination.into_py(py))
    }

    /// Groups elements from the source by key and applies operation to accumulate results.
    fn aggregate(
        &self,
        py: Python<'_>,
        operation: &PyAny,
    ) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_map_class = module.getattr("KotMap")?;

        let dict = PyDict::new(py);
        let selector = self.key_selector.as_ref(py);

        // Track first occurrence for each key
        let mut first_for_key: Vec<(PyObject, bool)> = Vec::new();

        for element in &self.elements {
            let key = selector.call1((element.as_ref(py),))?.into_py(py);

            // Find or create entry for this key
            let mut key_idx = None;
            for (i, (k, _)) in first_for_key.iter().enumerate() {
                if k.as_ref(py).eq(key.as_ref(py))? {
                    key_idx = Some(i);
                    break;
                }
            }

            if key_idx.is_none() {
                // First time seeing this key
                first_for_key.push((key.clone_ref(py), true));
                let accumulator = py.None();
                let result = operation.call1((key.as_ref(py), accumulator, element.as_ref(py), true))?;
                dict.set_item(key.as_ref(py), result)?;
            } else {
                // Subsequent element with this key
                let accumulator = dict.get_item(&key)?.unwrap();
                let result = operation.call1((key.as_ref(py), accumulator, element.as_ref(py), false))?;
                dict.set_item(key.as_ref(py), result)?;
            }
        }

        Ok(kot_map_class.call1((dict,))?.into_py(py))
    }

    /// Groups elements from the source by key and applies operation to accumulate results in destination.
    fn aggregate_to(
        &self,
        py: Python<'_>,
        destination: &PyAny,
        operation: &PyAny,
    ) -> PyResult<PyObject> {
        let selector = self.key_selector.as_ref(py);

        for element in &self.elements {
            let key = selector.call1((element.as_ref(py),))?;

            // Check if key exists in destination
            let has_key = destination.call_method1("contains_key", (key,))?.is_true()?;

            if !has_key {
                // First time seeing this key
                let accumulator = py.None();
                let result = operation.call1((key, accumulator, element.as_ref(py), true))?;
                destination.call_method1("put", (key, result))?;
            } else {
                // Subsequent element with this key
                let accumulator = destination.call_method1("get", (key,))?;
                let result = operation.call1((key, accumulator, element.as_ref(py), false))?;
                destination.call_method1("put", (key, result))?;
            }
        }

        Ok(destination.into_py(py))
    }

    /// Groups elements and applies a reducing operation.
    fn reduce(&self, py: Python<'_>, operation: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_map_class = module.getattr("KotMap")?;

        let dict = PyDict::new(py);
        let selector = self.key_selector.as_ref(py);

        // Track which keys we've seen
        let mut seen_keys: Vec<PyObject> = Vec::new();

        for element in &self.elements {
            let key = selector.call1((element.as_ref(py),))?.into_py(py);

            // Check if we've seen this key before
            let key_exists = seen_keys.iter().any(|k| {
                k.as_ref(py).eq(key.as_ref(py)).unwrap_or(false)
            });

            if !key_exists {
                // First element with this key becomes the accumulator
                dict.set_item(key.as_ref(py), element.as_ref(py))?;
                seen_keys.push(key);
            } else {
                // Apply the operation
                let accumulator = dict.get_item(&key)?.unwrap();
                let result = operation.call1((key.as_ref(py), accumulator, element.as_ref(py)))?;
                dict.set_item(key.as_ref(py), result)?;
            }
        }

        Ok(kot_map_class.call1((dict,))?.into_py(py))
    }

    /// Groups elements and applies a reducing operation, storing results in destination.
    fn reduce_to(
        &self,
        py: Python<'_>,
        destination: &PyAny,
        operation: &PyAny,
    ) -> PyResult<PyObject> {
        let selector = self.key_selector.as_ref(py);

        for element in &self.elements {
            let key = selector.call1((element.as_ref(py),))?;

            // Check if key exists in destination
            let has_key = destination.call_method1("contains_key", (key,))?.is_true()?;

            if !has_key {
                // First element with this key becomes the accumulator
                destination.call_method1("put", (key, element.as_ref(py)))?;
            } else {
                // Apply the operation
                let accumulator = destination.call_method1("get", (key,))?;
                let result = operation.call1((key, accumulator, element.as_ref(py)))?;
                destination.call_method1("put", (key, result))?;
            }
        }

        Ok(destination.into_py(py))
    }
}
