use pyo3::prelude::*;
use pyo3::types::{PyList, PyDict, PyTuple, PyType};
use pyo3::exceptions::{PyKeyError, PyValueError};

/// A read-only map implementation that reproduces Kotlin's Map interface.
#[pyclass(subclass)]
#[derive(Clone)]
pub struct KotMap {
    keys: Vec<PyObject>,
    values: Vec<PyObject>,
    key_type: Option<PyObject>,
    value_type: Option<PyObject>,
}

impl KotMap {
    pub fn new_with_types(
        keys: Vec<PyObject>,
        values: Vec<PyObject>,
        key_type: Option<PyObject>,
        value_type: Option<PyObject>,
    ) -> Self {
        KotMap { keys, values, key_type, value_type }
    }

    fn find_key_index(&self, py: Python<'_>, key: &PyAny) -> PyResult<Option<usize>> {
        for (i, k) in self.keys.iter().enumerate() {
            if k.as_ref(py).eq(key)? {
                return Ok(Some(i));
            }
        }
        Ok(None)
    }
}

#[pymethods]
impl KotMap {
    #[new]
    #[pyo3(signature = (elements=None))]
    fn new(py: Python<'_>, elements: Option<&PyAny>) -> PyResult<Self> {
        let mut map = KotMap {
            keys: Vec::new(),
            values: Vec::new(),
            key_type: None,
            value_type: None,
        };

        if let Some(elems) = elements {
            // Check if it's a dict
            if let Ok(dict) = elems.downcast::<PyDict>() {
                for (key, value) in dict.iter() {
                    map.keys.push(key.into_py(py));
                    map.values.push(value.into_py(py));
                }
            } else {
                // Assume it's an iterable of (key, value) pairs
                let iter = elems.iter()?;
                for item in iter {
                    let item = item?;
                    let key = item.get_item(0)?;
                    let value = item.get_item(1)?;
                    map.keys.push(key.into_py(py));
                    map.values.push(value.into_py(py));
                }
            }
        }

        Ok(map)
    }

    #[classmethod]
    fn of_types(
        _cls: &PyType,
        py: Python<'_>,
        key_type: &PyType,
        value_type: &PyType,
        elements: Option<&PyAny>,
    ) -> PyResult<Self> {
        let mut map = KotMap {
            keys: Vec::new(),
            values: Vec::new(),
            key_type: Some(key_type.into_py(py)),
            value_type: Some(value_type.into_py(py)),
        };

        if let Some(elems) = elements {
            if let Ok(dict) = elems.downcast::<PyDict>() {
                for (key, value) in dict.iter() {
                    map.keys.push(key.into_py(py));
                    map.values.push(value.into_py(py));
                }
            } else {
                let iter = elems.iter()?;
                for item in iter {
                    let item = item?;
                    let key = item.get_item(0)?;
                    let value = item.get_item(1)?;
                    map.keys.push(key.into_py(py));
                    map.values.push(value.into_py(py));
                }
            }
        }

        Ok(map)
    }

    fn __repr__(&self, py: Python<'_>) -> PyResult<String> {
        let items: Vec<String> = self.keys.iter()
            .zip(self.values.iter())
            .map(|(k, v)| {
                let key_str = k.as_ref(py).repr().map(|r| r.to_string()).unwrap_or_else(|_| "?".to_string());
                let val_str = v.as_ref(py).repr().map(|r| r.to_string()).unwrap_or_else(|_| "?".to_string());
                format!("{}: {}", key_str, val_str)
            })
            .collect();
        Ok(format!("KotMap({{{}}})", items.join(", ")))
    }

    fn __str__(&self, py: Python<'_>) -> PyResult<String> {
        let items: Vec<String> = self.keys.iter()
            .zip(self.values.iter())
            .map(|(k, v)| {
                let key_str = k.as_ref(py).str().map(|s| s.to_string()).unwrap_or_else(|_| "?".to_string());
                let val_str = v.as_ref(py).str().map(|s| s.to_string()).unwrap_or_else(|_| "?".to_string());
                format!("{}: {}", key_str, val_str)
            })
            .collect();
        Ok(format!("{{{}}}", items.join(", ")))
    }

    fn __eq__(&self, py: Python<'_>, other: &PyAny) -> PyResult<bool> {
        if let Ok(other_map) = other.extract::<PyRef<KotMap>>() {
            if self.keys.len() != other_map.keys.len() {
                return Ok(false);
            }
            for (k, v) in self.keys.iter().zip(self.values.iter()) {
                let mut found = false;
                for (ok, ov) in other_map.keys.iter().zip(other_map.values.iter()) {
                    if k.as_ref(py).eq(ok.as_ref(py))? && v.as_ref(py).eq(ov.as_ref(py))? {
                        found = true;
                        break;
                    }
                }
                if !found {
                    return Ok(false);
                }
            }
            Ok(true)
        } else {
            Ok(false)
        }
    }

    fn __iter__(&self, py: Python<'_>) -> PyResult<Py<KotMapKeyIterator>> {
        Py::new(py, KotMapKeyIterator {
            keys: self.keys.clone(),
            index: 0,
        })
    }

    fn __len__(&self) -> usize {
        self.keys.len()
    }

    fn __contains__(&self, py: Python<'_>, key: &PyAny) -> PyResult<bool> {
        self.contains_key(py, key)
    }

    fn __getitem__(&self, py: Python<'_>, key: &PyAny) -> PyResult<PyObject> {
        match self.find_key_index(py, key)? {
            Some(idx) => Ok(self.values[idx].clone_ref(py)),
            None => Err(PyKeyError::new_err(format!("Key not found: {:?}", key)))
        }
    }

    // Properties
    #[getter]
    fn size(&self) -> usize {
        self.keys.len()
    }

    #[getter]
    fn keys(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_set_class = module.getattr("KotSet")?;
        let py_list = PyList::new(py, self.keys.iter().map(|k| k.as_ref(py)));
        Ok(kot_set_class.call1((py_list,))?.into_py(py))
    }

    #[getter]
    fn values(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_list_class = module.getattr("KotList")?;
        let py_list = PyList::new(py, self.values.iter().map(|v| v.as_ref(py)));
        Ok(kot_list_class.call1((py_list,))?.into_py(py))
    }

    #[getter]
    fn entries(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_set_class = module.getattr("KotSet")?;

        let mut pairs = Vec::new();
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let tuple = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            pairs.push(tuple);
        }

        let py_list = PyList::new(py, pairs);
        Ok(kot_set_class.call1((py_list,))?.into_py(py))
    }

    // Basic methods
    fn is_empty(&self) -> bool {
        self.keys.is_empty()
    }

    fn is_not_empty(&self) -> bool {
        !self.keys.is_empty()
    }

    fn contains_key(&self, py: Python<'_>, key: &PyAny) -> PyResult<bool> {
        Ok(self.find_key_index(py, key)?.is_some())
    }

    fn contains_value(&self, py: Python<'_>, value: &PyAny) -> PyResult<bool> {
        for v in &self.values {
            if v.as_ref(py).eq(value)? {
                return Ok(true);
            }
        }
        Ok(false)
    }

    // Access methods
    fn get(&self, py: Python<'_>, key: &PyAny) -> PyResult<Option<PyObject>> {
        match self.find_key_index(py, key)? {
            Some(idx) => Ok(Some(self.values[idx].clone_ref(py))),
            None => Ok(None)
        }
    }

    fn get_or_default(&self, py: Python<'_>, key: &PyAny, default_value: &PyAny) -> PyResult<PyObject> {
        match self.find_key_index(py, key)? {
            Some(idx) => Ok(self.values[idx].clone_ref(py)),
            None => Ok(default_value.into_py(py))
        }
    }

    fn get_or_else(&self, py: Python<'_>, key: &PyAny, default_value: &PyAny) -> PyResult<PyObject> {
        match self.find_key_index(py, key)? {
            Some(idx) => Ok(self.values[idx].clone_ref(py)),
            None => Ok(default_value.call0()?.into_py(py))
        }
    }

    fn get_value(&self, py: Python<'_>, key: &PyAny) -> PyResult<PyObject> {
        match self.find_key_index(py, key)? {
            Some(idx) => Ok(self.values[idx].clone_ref(py)),
            None => Err(PyKeyError::new_err(format!("Key not found: {:?}", key)))
        }
    }

    fn get_or_null(&self, py: Python<'_>, key: &PyAny) -> PyResult<Option<PyObject>> {
        self.get(py, key)
    }

    fn get_or_none(&self, py: Python<'_>, key: &PyAny) -> PyResult<Option<PyObject>> {
        self.get(py, key)
    }

    // Transformation methods
    fn map(&self, py: Python<'_>, transform: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_list_class = module.getattr("KotList")?;

        let mut result = Vec::new();
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            let transformed = transform.call1((entry,))?;
            result.push(transformed);
        }

        let py_list = PyList::new(py, result);
        Ok(kot_list_class.call1((py_list,))?.into_py(py))
    }

    fn map_keys(&self, py: Python<'_>, transform: &PyAny) -> PyResult<KotMap> {
        let mut new_keys = Vec::new();
        let mut new_values = Vec::new();

        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            let new_key = transform.call1((entry,))?;
            new_keys.push(new_key.into_py(py));
            new_values.push(v.clone_ref(py));
        }

        Ok(KotMap::new_with_types(new_keys, new_values, None, self.value_type.clone()))
    }

    fn map_values(&self, py: Python<'_>, transform: &PyAny) -> PyResult<KotMap> {
        let mut new_keys = Vec::new();
        let mut new_values = Vec::new();

        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            let new_value = transform.call1((entry,))?;
            new_keys.push(k.clone_ref(py));
            new_values.push(new_value.into_py(py));
        }

        Ok(KotMap::new_with_types(new_keys, new_values, self.key_type.clone(), None))
    }

    fn map_not_null(&self, py: Python<'_>, transform: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_list_class = module.getattr("KotList")?;

        let mut result = Vec::new();
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            let transformed = transform.call1((entry,))?;
            if !transformed.is_none() {
                result.push(transformed);
            }
        }

        let py_list = PyList::new(py, result);
        Ok(kot_list_class.call1((py_list,))?.into_py(py))
    }

    fn map_not_none(&self, py: Python<'_>, transform: &PyAny) -> PyResult<PyObject> {
        self.map_not_null(py, transform)
    }

    fn flat_map(&self, py: Python<'_>, transform: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_list_class = module.getattr("KotList")?;

        let mut result = Vec::new();
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            let transformed = transform.call1((entry,))?;
            let iter = transformed.iter()?;
            for item in iter {
                result.push(item?);
            }
        }

        let py_list = PyList::new(py, result);
        Ok(kot_list_class.call1((py_list,))?.into_py(py))
    }

    // Filter methods
    fn filter(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<KotMap> {
        let mut new_keys = Vec::new();
        let mut new_values = Vec::new();

        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            let keep = predicate.call1((entry,))?;
            if keep.is_true()? {
                new_keys.push(k.clone_ref(py));
                new_values.push(v.clone_ref(py));
            }
        }

        Ok(KotMap::new_with_types(new_keys, new_values, self.key_type.clone(), self.value_type.clone()))
    }

    fn filter_keys(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<KotMap> {
        let mut new_keys = Vec::new();
        let mut new_values = Vec::new();

        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let keep = predicate.call1((k.as_ref(py),))?;
            if keep.is_true()? {
                new_keys.push(k.clone_ref(py));
                new_values.push(v.clone_ref(py));
            }
        }

        Ok(KotMap::new_with_types(new_keys, new_values, self.key_type.clone(), self.value_type.clone()))
    }

    fn filter_values(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<KotMap> {
        let mut new_keys = Vec::new();
        let mut new_values = Vec::new();

        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let keep = predicate.call1((v.as_ref(py),))?;
            if keep.is_true()? {
                new_keys.push(k.clone_ref(py));
                new_values.push(v.clone_ref(py));
            }
        }

        Ok(KotMap::new_with_types(new_keys, new_values, self.key_type.clone(), self.value_type.clone()))
    }

    fn filter_not(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<KotMap> {
        let mut new_keys = Vec::new();
        let mut new_values = Vec::new();

        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            let keep = predicate.call1((entry,))?;
            if !keep.is_true()? {
                new_keys.push(k.clone_ref(py));
                new_values.push(v.clone_ref(py));
            }
        }

        Ok(KotMap::new_with_types(new_keys, new_values, self.key_type.clone(), self.value_type.clone()))
    }

    // Predicate methods
    #[pyo3(signature = (predicate=None))]
    fn any(&self, py: Python<'_>, predicate: Option<&PyAny>) -> PyResult<bool> {
        match predicate {
            None => Ok(!self.keys.is_empty()),
            Some(pred) => {
                for (k, v) in self.keys.iter().zip(self.values.iter()) {
                    let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
                    let result = pred.call1((entry,))?;
                    if result.is_true()? {
                        return Ok(true);
                    }
                }
                Ok(false)
            }
        }
    }

    fn all(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<bool> {
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            let result = predicate.call1((entry,))?;
            if !result.is_true()? {
                return Ok(false);
            }
        }
        Ok(true)
    }

    #[pyo3(signature = (predicate=None))]
    fn none(&self, py: Python<'_>, predicate: Option<&PyAny>) -> PyResult<bool> {
        match predicate {
            None => Ok(self.keys.is_empty()),
            Some(pred) => {
                for (k, v) in self.keys.iter().zip(self.values.iter()) {
                    let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
                    let result = pred.call1((entry,))?;
                    if result.is_true()? {
                        return Ok(false);
                    }
                }
                Ok(true)
            }
        }
    }

    #[pyo3(signature = (predicate=None))]
    fn count(&self, py: Python<'_>, predicate: Option<&PyAny>) -> PyResult<usize> {
        match predicate {
            None => Ok(self.keys.len()),
            Some(pred) => {
                let mut count = 0;
                for (k, v) in self.keys.iter().zip(self.values.iter()) {
                    let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
                    let result = pred.call1((entry,))?;
                    if result.is_true()? {
                        count += 1;
                    }
                }
                Ok(count)
            }
        }
    }

    // Aggregation methods
    fn max_by(&self, py: Python<'_>, selector: &PyAny) -> PyResult<PyObject> {
        if self.keys.is_empty() {
            return Err(PyValueError::new_err("Cannot find max of empty map"));
        }

        let mut max_entry: Option<(PyObject, PyObject, PyObject)> = None;

        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            let key_value = selector.call1((entry.clone(),))?.into_py(py);

            match &max_entry {
                None => max_entry = Some((k.clone_ref(py), v.clone_ref(py), key_value)),
                Some((_, _, max_key_value)) => {
                    if key_value.as_ref(py).gt(max_key_value.as_ref(py))? {
                        max_entry = Some((k.clone_ref(py), v.clone_ref(py), key_value));
                    }
                }
            }
        }

        let (k, v, _) = max_entry.unwrap();
        Ok(PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]).into_py(py))
    }

    fn min_by(&self, py: Python<'_>, selector: &PyAny) -> PyResult<PyObject> {
        if self.keys.is_empty() {
            return Err(PyValueError::new_err("Cannot find min of empty map"));
        }

        let mut min_entry: Option<(PyObject, PyObject, PyObject)> = None;

        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            let key_value = selector.call1((entry.clone(),))?.into_py(py);

            match &min_entry {
                None => min_entry = Some((k.clone_ref(py), v.clone_ref(py), key_value)),
                Some((_, _, min_key_value)) => {
                    if key_value.as_ref(py).lt(min_key_value.as_ref(py))? {
                        min_entry = Some((k.clone_ref(py), v.clone_ref(py), key_value));
                    }
                }
            }
        }

        let (k, v, _) = min_entry.unwrap();
        Ok(PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]).into_py(py))
    }

    fn max_by_or_null(&self, py: Python<'_>, selector: &PyAny) -> PyResult<Option<PyObject>> {
        if self.keys.is_empty() {
            return Ok(None);
        }
        Ok(Some(self.max_by(py, selector)?))
    }

    fn max_by_or_none(&self, py: Python<'_>, selector: &PyAny) -> PyResult<Option<PyObject>> {
        self.max_by_or_null(py, selector)
    }

    fn min_by_or_null(&self, py: Python<'_>, selector: &PyAny) -> PyResult<Option<PyObject>> {
        if self.keys.is_empty() {
            return Ok(None);
        }
        Ok(Some(self.min_by(py, selector)?))
    }

    fn min_by_or_none(&self, py: Python<'_>, selector: &PyAny) -> PyResult<Option<PyObject>> {
        self.min_by_or_null(py, selector)
    }

    // Plus/Minus operations
    fn plus(&self, py: Python<'_>, other: &PyAny) -> PyResult<KotMap> {
        let mut new_keys: Vec<PyObject> = self.keys.iter().map(|k| k.clone_ref(py)).collect();
        let mut new_values: Vec<PyObject> = self.values.iter().map(|v| v.clone_ref(py)).collect();

        // Check if other is a dict or map-like
        if let Ok(dict) = other.downcast::<PyDict>() {
            for (k, v) in dict.iter() {
                let key = k.into_py(py);
                let mut found = false;
                for (i, existing_key) in new_keys.iter().enumerate() {
                    if existing_key.as_ref(py).eq(&k)? {
                        new_values[i] = v.into_py(py);
                        found = true;
                        break;
                    }
                }
                if !found {
                    new_keys.push(key);
                    new_values.push(v.into_py(py));
                }
            }
        } else if let Ok(map) = other.extract::<PyRef<KotMap>>() {
            for (k, v) in map.keys.iter().zip(map.values.iter()) {
                let mut found = false;
                for (i, existing_key) in new_keys.iter().enumerate() {
                    if existing_key.as_ref(py).eq(k.as_ref(py))? {
                        new_values[i] = v.clone_ref(py);
                        found = true;
                        break;
                    }
                }
                if !found {
                    new_keys.push(k.clone_ref(py));
                    new_values.push(v.clone_ref(py));
                }
            }
        } else {
            // Assume it's a tuple (key, value)
            let key = other.get_item(0)?.into_py(py);
            let value = other.get_item(1)?.into_py(py);

            let mut found = false;
            for (i, existing_key) in new_keys.iter().enumerate() {
                if existing_key.as_ref(py).eq(key.as_ref(py))? {
                    new_values[i] = value.clone_ref(py);
                    found = true;
                    break;
                }
            }
            if !found {
                new_keys.push(key);
                new_values.push(value);
            }
        }

        Ok(KotMap::new_with_types(new_keys, new_values, self.key_type.clone(), self.value_type.clone()))
    }

    fn minus(&self, py: Python<'_>, keys_to_remove: &PyAny) -> PyResult<KotMap> {
        let mut remove_keys = Vec::new();

        // Check if it's iterable (but not string)
        if keys_to_remove.is_instance_of::<pyo3::types::PyString>() {
            remove_keys.push(keys_to_remove.into_py(py));
        } else if let Ok(iter) = keys_to_remove.iter() {
            for item in iter {
                remove_keys.push(item?.into_py(py));
            }
        } else {
            remove_keys.push(keys_to_remove.into_py(py));
        }

        let mut new_keys = Vec::new();
        let mut new_values = Vec::new();

        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let mut should_remove = false;
            for rk in &remove_keys {
                if k.as_ref(py).eq(rk.as_ref(py))? {
                    should_remove = true;
                    break;
                }
            }
            if !should_remove {
                new_keys.push(k.clone_ref(py));
                new_values.push(v.clone_ref(py));
            }
        }

        Ok(KotMap::new_with_types(new_keys, new_values, self.key_type.clone(), self.value_type.clone()))
    }

    // ForEach methods
    fn for_each(&self, py: Python<'_>, action: &PyAny) -> PyResult<()> {
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            action.call1((entry,))?;
        }
        Ok(())
    }

    fn on_each(&self, py: Python<'_>, action: &PyAny) -> PyResult<KotMap> {
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            action.call1((entry,))?;
        }
        Ok(self.clone())
    }

    // Conversion methods
    fn to_list(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_list_class = module.getattr("KotList")?;

        let mut pairs = Vec::new();
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let tuple = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            pairs.push(tuple);
        }

        let py_list = PyList::new(py, pairs);
        Ok(kot_list_class.call1((py_list,))?.into_py(py))
    }

    fn to_dict(&self, py: Python<'_>) -> PyResult<Py<PyDict>> {
        let dict = PyDict::new(py);
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            dict.set_item(k.as_ref(py), v.as_ref(py))?;
        }
        Ok(dict.into())
    }

    fn to_kot_map(&self, py: Python<'_>) -> KotMap {
        KotMap::new_with_types(
            self.keys.iter().map(|k| k.clone_ref(py)).collect(),
            self.values.iter().map(|v| v.clone_ref(py)).collect(),
            self.key_type.clone(),
            self.value_type.clone()
        )
    }

    fn to_kot_mutable_map(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let class = module.getattr("KotMutableMap")?;
        let dict = PyDict::new(py);
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            dict.set_item(k.as_ref(py), v.as_ref(py))?;
        }
        Ok(class.call1((dict,))?.into_py(py))
    }

    // Utility methods
    fn if_empty(&self, py: Python<'_>, default_value: &PyAny) -> PyResult<PyObject> {
        if self.keys.is_empty() {
            Ok(default_value.call0()?.into_py(py))
        } else {
            Ok(self.clone().into_py(py))
        }
    }

    // Default value wrapper
    fn with_default(&self, py: Python<'_>, default_value: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let dict = PyDict::new(py);
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            dict.set_item(k.as_ref(py), v.as_ref(py))?;
        }
        let kot_map = module.getattr("KotMapWithDefault")?;
        Ok(kot_map.call1((dict, default_value))?.into_py(py))
    }
}

// Key iterator for KotMap
#[pyclass]
pub struct KotMapKeyIterator {
    keys: Vec<PyObject>,
    index: usize,
}

#[pymethods]
impl KotMapKeyIterator {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(&mut self, py: Python<'_>) -> Option<PyObject> {
        if self.index < self.keys.len() {
            let result = self.keys[self.index].clone_ref(py);
            self.index += 1;
            Some(result)
        } else {
            None
        }
    }
}
