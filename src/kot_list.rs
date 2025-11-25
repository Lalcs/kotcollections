use pyo3::prelude::*;
use pyo3::types::{PyList, PyTuple, PyDict, PySet, PyType};
use pyo3::exceptions::{PyIndexError, PyValueError, PyTypeError};

/// A read-only list implementation that reproduces Kotlin's List interface.
#[pyclass(subclass)]
#[derive(Clone)]
pub struct KotList {
    elements: Vec<PyObject>,
    element_type: Option<PyObject>,
}

impl KotList {
    fn check_type(&mut self, py: Python<'_>, element: &PyObject) -> PyResult<()> {
        if let Some(ref expected_type) = self.element_type {
            let expected = expected_type.as_ref(py);
            let elem = element.as_ref(py);

            if let Ok(expected_type) = expected.downcast::<PyType>() {
                if !elem.is_instance(expected_type)? {
                    let elem_type_name = elem.get_type().name()?;
                    let expected_type_name = expected.getattr("__name__")
                        .map(|n| n.to_string())
                        .unwrap_or_else(|_| expected.to_string());
                    return Err(PyTypeError::new_err(format!(
                        "KotList expected element of type {}, got {}",
                        expected_type_name, elem_type_name
                    )));
                }
            }
        } else {
            let elem = element.as_ref(py);
            self.element_type = Some(elem.get_type().into());
        }
        Ok(())
    }

    pub fn new_with_type(elements: Vec<PyObject>, element_type: Option<PyObject>) -> Self {
        KotList { elements, element_type }
    }
}

#[pymethods]
impl KotList {
    #[new]
    #[pyo3(signature = (elements=None))]
    fn new(py: Python<'_>, elements: Option<&PyAny>) -> PyResult<Self> {
        let mut list = KotList {
            elements: Vec::new(),
            element_type: None,
        };

        if let Some(elems) = elements {
            for item in elems.iter()? {
                let obj: PyObject = item?.into();
                list.check_type(py, &obj)?;
                list.elements.push(obj);
            }
        }

        Ok(list)
    }

    #[classmethod]
    fn of_type(
        _cls: &PyType,
        py: Python<'_>,
        element_type: &PyType,
        elements: Option<&PyAny>,
    ) -> PyResult<Self> {
        let mut list = KotList {
            elements: Vec::new(),
            element_type: Some(element_type.into()),
        };

        if let Some(elems) = elements {
            for item in elems.iter()? {
                let obj: PyObject = item?.into();
                list.check_type(py, &obj)?;
                list.elements.push(obj);
            }
        }

        Ok(list)
    }

    fn __repr__(&self, py: Python<'_>) -> PyResult<String> {
        let items: Vec<String> = self.elements.iter()
            .map(|e| e.as_ref(py).repr().map(|r| r.to_string()).unwrap_or_else(|_| "?".to_string()))
            .collect();
        Ok(format!("KotList([{}])", items.join(", ")))
    }

    fn __str__(&self, py: Python<'_>) -> PyResult<String> {
        let items: Vec<String> = self.elements.iter()
            .map(|e| e.as_ref(py).str().map(|s| s.to_string()).unwrap_or_else(|_| "?".to_string()))
            .collect();
        Ok(format!("[{}]", items.join(", ")))
    }

    fn __eq__(&self, py: Python<'_>, other: &PyAny) -> PyResult<bool> {
        if let Ok(other_list) = other.extract::<PyRef<KotList>>() {
            if self.elements.len() != other_list.elements.len() {
                return Ok(false);
            }
            for (a, b) in self.elements.iter().zip(other_list.elements.iter()) {
                if !a.as_ref(py).eq(b.as_ref(py))? {
                    return Ok(false);
                }
            }
            Ok(true)
        } else {
            Ok(false)
        }
    }

    fn __hash__(&self, py: Python<'_>) -> PyResult<isize> {
        let mut hash: isize = 0;
        for elem in &self.elements {
            hash = hash.wrapping_add(elem.as_ref(py).hash()? as isize);
        }
        Ok(hash)
    }

    fn __iter__(&self, py: Python<'_>) -> PyResult<Py<KotListIterator>> {
        Py::new(py, KotListIterator {
            elements: self.elements.clone(),
            index: 0,
        })
    }

    fn __getitem__(&self, py: Python<'_>, index: isize) -> PyResult<PyObject> {
        let idx = if index < 0 {
            (self.elements.len() as isize + index) as usize
        } else {
            index as usize
        };

        self.elements.get(idx)
            .map(|e| e.clone())
            .ok_or_else(|| PyIndexError::new_err(format!(
                "Index {} out of bounds for list of size {}", index, self.elements.len()
            )))
    }

    fn __len__(&self) -> usize {
        self.elements.len()
    }

    fn __contains__(&self, py: Python<'_>, element: &PyAny) -> PyResult<bool> {
        for e in &self.elements {
            if e.as_ref(py).eq(element)? {
                return Ok(true);
            }
        }
        Ok(false)
    }

    fn __add__(&self, py: Python<'_>, other: &PyAny) -> PyResult<KotList> {
        self.plus(py, other)
    }

    fn __sub__(&self, py: Python<'_>, other: &PyAny) -> PyResult<KotList> {
        self.minus(py, other)
    }

    // Properties
    #[getter]
    fn size(&self) -> usize {
        self.elements.len()
    }

    #[getter]
    fn indices(&self, py: Python<'_>) -> PyResult<PyObject> {
        let builtins = py.import("builtins")?;
        let range = builtins.getattr("range")?;
        Ok(range.call1((self.elements.len(),))?.into())
    }

    #[getter]
    fn last_index(&self) -> isize {
        if self.elements.is_empty() {
            -1
        } else {
            (self.elements.len() - 1) as isize
        }
    }

    // Basic methods
    fn is_empty(&self) -> bool {
        self.elements.is_empty()
    }

    fn is_not_empty(&self) -> bool {
        !self.elements.is_empty()
    }

    fn get(&self, py: Python<'_>, index: usize) -> PyResult<PyObject> {
        self.elements.get(index)
            .map(|e| e.clone())
            .ok_or_else(|| PyIndexError::new_err(format!(
                "Index {} out of bounds for list of size {}", index, self.elements.len()
            )))
    }

    fn get_or_null(&self, index: usize) -> Option<PyObject> {
        self.elements.get(index).cloned()
    }

    fn get_or_none(&self, index: usize) -> Option<PyObject> {
        self.get_or_null(index)
    }

    fn get_or_else(&self, py: Python<'_>, index: usize, default_value: &PyAny) -> PyResult<PyObject> {
        if index < self.elements.len() {
            Ok(self.elements[index].clone())
        } else {
            Ok(default_value.call1((index,))?.into())
        }
    }

    // First/Last element methods
    fn first(&self) -> PyResult<PyObject> {
        self.elements.first()
            .cloned()
            .ok_or_else(|| PyIndexError::new_err("List is empty"))
    }

    fn first_predicate(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<PyObject> {
        for element in &self.elements {
            let result = predicate.call1((element.as_ref(py),))?;
            if result.is_true()? {
                return Ok(element.clone());
            }
        }
        Err(PyValueError::new_err("No element matching predicate found"))
    }

    fn first_or_null(&self) -> Option<PyObject> {
        self.elements.first().cloned()
    }

    fn first_or_none(&self) -> Option<PyObject> {
        self.first_or_null()
    }

    fn first_or_null_predicate(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<Option<PyObject>> {
        for element in &self.elements {
            let result = predicate.call1((element.as_ref(py),))?;
            if result.is_true()? {
                return Ok(Some(element.clone()));
            }
        }
        Ok(None)
    }

    fn first_or_none_predicate(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<Option<PyObject>> {
        self.first_or_null_predicate(py, predicate)
    }

    fn last(&self) -> PyResult<PyObject> {
        self.elements.last()
            .cloned()
            .ok_or_else(|| PyIndexError::new_err("List is empty"))
    }

    fn last_predicate(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<PyObject> {
        for element in self.elements.iter().rev() {
            let result = predicate.call1((element.as_ref(py),))?;
            if result.is_true()? {
                return Ok(element.clone());
            }
        }
        Err(PyValueError::new_err("No element matching predicate found"))
    }

    fn last_or_null(&self) -> Option<PyObject> {
        self.elements.last().cloned()
    }

    fn last_or_none(&self) -> Option<PyObject> {
        self.last_or_null()
    }

    fn last_or_null_predicate(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<Option<PyObject>> {
        for element in self.elements.iter().rev() {
            let result = predicate.call1((element.as_ref(py),))?;
            if result.is_true()? {
                return Ok(Some(element.clone()));
            }
        }
        Ok(None)
    }

    fn last_or_none_predicate(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<Option<PyObject>> {
        self.last_or_null_predicate(py, predicate)
    }

    fn element_at(&self, py: Python<'_>, index: usize) -> PyResult<PyObject> {
        self.get(py, index)
    }

    fn element_at_or_else(&self, py: Python<'_>, index: usize, default_value: &PyAny) -> PyResult<PyObject> {
        self.get_or_else(py, index, default_value)
    }

    fn element_at_or_null(&self, index: usize) -> Option<PyObject> {
        self.get_or_null(index)
    }

    fn element_at_or_none(&self, index: usize) -> Option<PyObject> {
        self.element_at_or_null(index)
    }

    // Contains methods
    fn contains(&self, py: Python<'_>, element: &PyAny) -> PyResult<bool> {
        self.__contains__(py, element)
    }

    fn contains_all(&self, py: Python<'_>, elements: &PyAny) -> PyResult<bool> {
        for item in elements.iter()? {
            let item = item?;
            if !self.__contains__(py, item)? {
                return Ok(false);
            }
        }
        Ok(true)
    }

    // Index methods
    fn index_of(&self, py: Python<'_>, element: &PyAny) -> PyResult<isize> {
        for (i, e) in self.elements.iter().enumerate() {
            if e.as_ref(py).eq(element)? {
                return Ok(i as isize);
            }
        }
        Ok(-1)
    }

    fn last_index_of(&self, py: Python<'_>, element: &PyAny) -> PyResult<isize> {
        for i in (0..self.elements.len()).rev() {
            if self.elements[i].as_ref(py).eq(element)? {
                return Ok(i as isize);
            }
        }
        Ok(-1)
    }

    fn index_of_first(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<isize> {
        for (i, element) in self.elements.iter().enumerate() {
            let result = predicate.call1((element.as_ref(py),))?;
            if result.is_true()? {
                return Ok(i as isize);
            }
        }
        Ok(-1)
    }

    fn index_of_last(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<isize> {
        for i in (0..self.elements.len()).rev() {
            let result = predicate.call1((self.elements[i].as_ref(py),))?;
            if result.is_true()? {
                return Ok(i as isize);
            }
        }
        Ok(-1)
    }

    // Transformation methods
    fn map(&self, py: Python<'_>, transform: &PyAny) -> PyResult<KotList> {
        let mut result = Vec::with_capacity(self.elements.len());
        for element in &self.elements {
            let transformed = transform.call1((element.as_ref(py),))?;
            result.push(transformed.into());
        }
        Ok(KotList::new_with_type(result, None))
    }

    fn map_indexed(&self, py: Python<'_>, transform: &PyAny) -> PyResult<KotList> {
        let mut result = Vec::with_capacity(self.elements.len());
        for (i, element) in self.elements.iter().enumerate() {
            let transformed = transform.call1((i, element.as_ref(py)))?;
            result.push(transformed.into());
        }
        Ok(KotList::new_with_type(result, None))
    }

    fn map_not_null(&self, py: Python<'_>, transform: &PyAny) -> PyResult<KotList> {
        let mut result = Vec::new();
        for element in &self.elements {
            let transformed = transform.call1((element.as_ref(py),))?;
            if !transformed.is_none() {
                result.push(transformed.into());
            }
        }
        Ok(KotList::new_with_type(result, None))
    }

    fn map_not_none(&self, py: Python<'_>, transform: &PyAny) -> PyResult<KotList> {
        self.map_not_null(py, transform)
    }

    fn flat_map(&self, py: Python<'_>, transform: &PyAny) -> PyResult<KotList> {
        let mut result = Vec::new();
        for element in &self.elements {
            let transformed = transform.call1((element.as_ref(py),))?;
            for item in transformed.iter()? {
                result.push(item?.into());
            }
        }
        Ok(KotList::new_with_type(result, None))
    }

    fn flatten(&self, py: Python<'_>) -> PyResult<KotList> {
        let mut result = Vec::new();
        for element in &self.elements {
            let elem = element.as_ref(py);
            // Check if element is iterable but not a string or bytes
            if elem.is_instance_of::<pyo3::types::PyString>() || elem.is_instance_of::<pyo3::types::PyBytes>() {
                result.push(element.clone());
            } else if let Ok(iter) = elem.iter() {
                for item in iter {
                    result.push(item?.into());
                }
            } else {
                result.push(element.clone());
            }
        }
        Ok(KotList::new_with_type(result, None))
    }

    // Filter methods
    fn filter(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<KotList> {
        let mut result = Vec::new();
        for element in &self.elements {
            let keep = predicate.call1((element.as_ref(py),))?;
            if keep.is_true()? {
                result.push(element.clone());
            }
        }
        Ok(KotList::new_with_type(result, self.element_type.clone()))
    }

    fn filter_indexed(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<KotList> {
        let mut result = Vec::new();
        for (i, element) in self.elements.iter().enumerate() {
            let keep = predicate.call1((i, element.as_ref(py)))?;
            if keep.is_true()? {
                result.push(element.clone());
            }
        }
        Ok(KotList::new_with_type(result, self.element_type.clone()))
    }

    fn filter_not(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<KotList> {
        let mut result = Vec::new();
        for element in &self.elements {
            let keep = predicate.call1((element.as_ref(py),))?;
            if !keep.is_true()? {
                result.push(element.clone());
            }
        }
        Ok(KotList::new_with_type(result, self.element_type.clone()))
    }

    fn filter_not_null(&self, py: Python<'_>) -> KotList {
        let result: Vec<PyObject> = self.elements.iter()
            .filter(|e| !e.as_ref(py).is_none())
            .cloned()
            .collect();
        KotList::new_with_type(result, self.element_type.clone())
    }

    fn filter_not_none(&self, py: Python<'_>) -> KotList {
        self.filter_not_null(py)
    }

    fn filter_is_instance(&self, py: Python<'_>, klass: &PyType) -> PyResult<KotList> {
        let mut result = Vec::new();
        for element in &self.elements {
            if element.as_ref(py).is_instance(klass)? {
                result.push(element.clone());
            }
        }
        Ok(KotList::new_with_type(result, None))
    }

    fn partition(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<(KotList, KotList)> {
        let mut matching = Vec::new();
        let mut non_matching = Vec::new();

        for element in &self.elements {
            let result = predicate.call1((element.as_ref(py),))?;
            if result.is_true()? {
                matching.push(element.clone());
            } else {
                non_matching.push(element.clone());
            }
        }

        Ok((
            KotList::new_with_type(matching, self.element_type.clone()),
            KotList::new_with_type(non_matching, self.element_type.clone())
        ))
    }

    // Predicate methods
    #[pyo3(signature = (predicate=None))]
    fn any(&self, py: Python<'_>, predicate: Option<&PyAny>) -> PyResult<bool> {
        match predicate {
            None => Ok(!self.elements.is_empty()),
            Some(pred) => {
                for element in &self.elements {
                    let result = pred.call1((element.as_ref(py),))?;
                    if result.is_true()? {
                        return Ok(true);
                    }
                }
                Ok(false)
            }
        }
    }

    fn all(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<bool> {
        for element in &self.elements {
            let result = predicate.call1((element.as_ref(py),))?;
            if !result.is_true()? {
                return Ok(false);
            }
        }
        Ok(true)
    }

    #[pyo3(signature = (predicate=None))]
    fn none(&self, py: Python<'_>, predicate: Option<&PyAny>) -> PyResult<bool> {
        match predicate {
            None => Ok(self.elements.is_empty()),
            Some(pred) => {
                for element in &self.elements {
                    let result = pred.call1((element.as_ref(py),))?;
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
            None => Ok(self.elements.len()),
            Some(pred) => {
                let mut count = 0;
                for element in &self.elements {
                    let result = pred.call1((element.as_ref(py),))?;
                    if result.is_true()? {
                        count += 1;
                    }
                }
                Ok(count)
            }
        }
    }

    // Aggregation methods
    fn sum_of(&self, py: Python<'_>, selector: &PyAny) -> PyResult<PyObject> {
        let mut sum = 0f64;
        for element in &self.elements {
            let value = selector.call1((element.as_ref(py),))?;
            sum += value.extract::<f64>()?;
        }
        Ok(sum.into_py(py))
    }

    fn max(&self, py: Python<'_>) -> PyResult<PyObject> {
        if self.elements.is_empty() {
            return Err(PyValueError::new_err("List is empty"));
        }

        let builtins = py.import("builtins")?;
        let max_fn = builtins.getattr("max")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        Ok(max_fn.call1((py_list,))?.into())
    }

    fn max_or_null(&self, py: Python<'_>) -> PyResult<Option<PyObject>> {
        if self.elements.is_empty() {
            return Ok(None);
        }
        Ok(Some(self.max(py)?))
    }

    fn max_or_none(&self, py: Python<'_>) -> PyResult<Option<PyObject>> {
        self.max_or_null(py)
    }

    fn min(&self, py: Python<'_>) -> PyResult<PyObject> {
        if self.elements.is_empty() {
            return Err(PyValueError::new_err("List is empty"));
        }

        let builtins = py.import("builtins")?;
        let min_fn = builtins.getattr("min")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        Ok(min_fn.call1((py_list,))?.into())
    }

    fn min_or_null(&self, py: Python<'_>) -> PyResult<Option<PyObject>> {
        if self.elements.is_empty() {
            return Ok(None);
        }
        Ok(Some(self.min(py)?))
    }

    fn min_or_none(&self, py: Python<'_>) -> PyResult<Option<PyObject>> {
        self.min_or_null(py)
    }

    fn max_by(&self, py: Python<'_>, selector: &PyAny) -> PyResult<PyObject> {
        if self.elements.is_empty() {
            return Err(PyValueError::new_err("Cannot find max of empty list"));
        }

        let builtins = py.import("builtins")?;
        let max_fn = builtins.getattr("max")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        let kwargs = PyDict::new(py);
        kwargs.set_item("key", selector)?;
        Ok(max_fn.call((py_list,), Some(kwargs))?.into())
    }

    fn min_by(&self, py: Python<'_>, selector: &PyAny) -> PyResult<PyObject> {
        if self.elements.is_empty() {
            return Err(PyValueError::new_err("Cannot find min of empty list"));
        }

        let builtins = py.import("builtins")?;
        let min_fn = builtins.getattr("min")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        let kwargs = PyDict::new(py);
        kwargs.set_item("key", selector)?;
        Ok(min_fn.call((py_list,), Some(kwargs))?.into())
    }

    fn max_by_or_null(&self, py: Python<'_>, selector: &PyAny) -> PyResult<Option<PyObject>> {
        if self.elements.is_empty() {
            return Ok(None);
        }
        Ok(Some(self.max_by(py, selector)?))
    }

    fn max_by_or_none(&self, py: Python<'_>, selector: &PyAny) -> PyResult<Option<PyObject>> {
        self.max_by_or_null(py, selector)
    }

    fn min_by_or_null(&self, py: Python<'_>, selector: &PyAny) -> PyResult<Option<PyObject>> {
        if self.elements.is_empty() {
            return Ok(None);
        }
        Ok(Some(self.min_by(py, selector)?))
    }

    fn min_by_or_none(&self, py: Python<'_>, selector: &PyAny) -> PyResult<Option<PyObject>> {
        self.min_by_or_null(py, selector)
    }

    fn average(&self, py: Python<'_>) -> PyResult<f64> {
        if self.elements.is_empty() {
            return Ok(f64::NAN);
        }

        let mut sum = 0f64;
        for element in &self.elements {
            sum += element.as_ref(py).extract::<f64>()?;
        }
        Ok(sum / self.elements.len() as f64)
    }

    // Sorting methods
    #[pyo3(signature = (key=None, reverse=false))]
    fn sorted(&self, py: Python<'_>, key: Option<&PyAny>, reverse: bool) -> PyResult<KotList> {
        let builtins = py.import("builtins")?;
        let sorted_fn = builtins.getattr("sorted")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));

        let kwargs = PyDict::new(py);
        if let Some(k) = key {
            kwargs.set_item("key", k)?;
        }
        kwargs.set_item("reverse", reverse)?;

        let result = sorted_fn.call((py_list,), Some(kwargs))?;
        let mut elements = Vec::new();
        for item in result.iter()? {
            elements.push(item?.into());
        }

        Ok(KotList::new_with_type(elements, self.element_type.clone()))
    }

    fn sorted_descending(&self, py: Python<'_>) -> PyResult<KotList> {
        self.sorted(py, None, true)
    }

    fn sorted_by(&self, py: Python<'_>, selector: &PyAny) -> PyResult<KotList> {
        self.sorted(py, Some(selector), false)
    }

    fn sorted_by_descending(&self, py: Python<'_>, selector: &PyAny) -> PyResult<KotList> {
        self.sorted(py, Some(selector), true)
    }

    fn reversed(&self) -> KotList {
        let elements: Vec<PyObject> = self.elements.iter().rev().cloned().collect();
        KotList::new_with_type(elements, self.element_type.clone())
    }

    // Distinct method
    fn distinct(&self, py: Python<'_>) -> PyResult<KotList> {
        let mut seen: Vec<PyObject> = Vec::new();
        let mut result = Vec::new();

        for element in &self.elements {
            let mut found = false;
            for s in &seen {
                if element.as_ref(py).eq(s.as_ref(py))? {
                    found = true;
                    break;
                }
            }
            if !found {
                seen.push(element.clone());
                result.push(element.clone());
            }
        }

        Ok(KotList::new_with_type(result, self.element_type.clone()))
    }

    fn distinct_by(&self, py: Python<'_>, selector: &PyAny) -> PyResult<KotList> {
        let mut seen_keys: Vec<PyObject> = Vec::new();
        let mut result = Vec::new();

        for element in &self.elements {
            let key: PyObject = selector.call1((element.as_ref(py),))?.into();
            let mut found = false;
            for s in &seen_keys {
                if key.as_ref(py).eq(s.as_ref(py))? {
                    found = true;
                    break;
                }
            }
            if !found {
                seen_keys.push(key);
                result.push(element.clone());
            }
        }

        Ok(KotList::new_with_type(result, self.element_type.clone()))
    }

    // Plus/Minus operations
    fn plus(&self, py: Python<'_>, element: &PyAny) -> PyResult<KotList> {
        let mut result = self.elements.clone();

        // Check if element is iterable (but not string or bytes)
        if element.is_instance_of::<pyo3::types::PyString>() || element.is_instance_of::<pyo3::types::PyBytes>() {
            result.push(element.into());
        } else if let Ok(iter) = element.iter() {
            for item in iter {
                result.push(item?.into());
            }
        } else {
            result.push(element.into());
        }

        Ok(KotList::new_with_type(result, self.element_type.clone()))
    }

    fn minus(&self, py: Python<'_>, element: &PyAny) -> PyResult<KotList> {
        let mut result = self.elements.clone();

        // Check if element is iterable (but not string or bytes)
        if element.is_instance_of::<pyo3::types::PyString>() || element.is_instance_of::<pyo3::types::PyBytes>() {
            // Remove first occurrence
            for i in 0..result.len() {
                if result[i].as_ref(py).eq(element)? {
                    result.remove(i);
                    break;
                }
            }
        } else if let Ok(iter) = element.iter() {
            for item in iter {
                let item = item?;
                for i in 0..result.len() {
                    if result[i].as_ref(py).eq(item)? {
                        result.remove(i);
                        break;
                    }
                }
            }
        } else {
            // Remove first occurrence
            for i in 0..result.len() {
                if result[i].as_ref(py).eq(element)? {
                    result.remove(i);
                    break;
                }
            }
        }

        Ok(KotList::new_with_type(result, self.element_type.clone()))
    }

    fn sub_list(&self, from_index: usize, to_index: usize) -> PyResult<KotList> {
        if from_index > to_index || to_index > self.elements.len() {
            return Err(PyIndexError::new_err("Invalid sublist range"));
        }

        let elements: Vec<PyObject> = self.elements[from_index..to_index]
            .iter()
            .cloned()
            .collect();

        Ok(KotList::new_with_type(elements, self.element_type.clone()))
    }

    // Zip methods
    fn zip(&self, py: Python<'_>, other: &PyAny) -> PyResult<KotList> {
        let mut result = Vec::new();

        for (a, b) in self.elements.iter().zip(other.iter()?) {
            let b = b?;
            let tuple = PyTuple::new(py, &[a.as_ref(py), b]);
            result.push(tuple.into());
        }

        Ok(KotList::new_with_type(result, None))
    }

    fn zip_transform(&self, py: Python<'_>, other: &PyAny, transform: &PyAny) -> PyResult<KotList> {
        let mut result = Vec::new();

        for (a, b) in self.elements.iter().zip(other.iter()?) {
            let b = b?;
            let transformed = transform.call1((a.as_ref(py), b))?;
            result.push(transformed.into());
        }

        Ok(KotList::new_with_type(result, None))
    }

    fn unzip(&self, py: Python<'_>) -> PyResult<(KotList, KotList)> {
        let mut first = Vec::new();
        let mut second = Vec::new();

        for element in &self.elements {
            let elem = element.as_ref(py);
            first.push(elem.get_item(0)?.into());
            second.push(elem.get_item(1)?.into());
        }

        Ok((
            KotList::new_with_type(first, None),
            KotList::new_with_type(second, None)
        ))
    }

    // Fold/Reduce methods
    fn fold(&self, py: Python<'_>, initial: &PyAny, operation: &PyAny) -> PyResult<PyObject> {
        let mut result: PyObject = initial.into();
        for element in &self.elements {
            result = operation.call1((result.as_ref(py), element.as_ref(py)))?.into();
        }
        Ok(result)
    }

    fn reduce(&self, py: Python<'_>, operation: &PyAny) -> PyResult<PyObject> {
        if self.elements.is_empty() {
            return Err(PyValueError::new_err("Cannot reduce empty list"));
        }

        let mut result = self.elements[0].clone();
        for element in &self.elements[1..] {
            result = operation.call1((result.as_ref(py), element.as_ref(py)))?.into();
        }
        Ok(result)
    }

    fn reduce_or_null(&self, py: Python<'_>, operation: &PyAny) -> PyResult<Option<PyObject>> {
        if self.elements.is_empty() {
            return Ok(None);
        }
        Ok(Some(self.reduce(py, operation)?))
    }

    fn reduce_or_none(&self, py: Python<'_>, operation: &PyAny) -> PyResult<Option<PyObject>> {
        self.reduce_or_null(py, operation)
    }

    fn scan(&self, py: Python<'_>, initial: &PyAny, operation: &PyAny) -> PyResult<KotList> {
        let mut result = vec![initial.into()];
        let mut acc: PyObject = initial.into();

        for element in &self.elements {
            acc = operation.call1((acc.as_ref(py), element.as_ref(py)))?.into();
            result.push(acc.clone());
        }

        Ok(KotList::new_with_type(result, None))
    }

    // ForEach methods
    fn for_each(&self, py: Python<'_>, action: &PyAny) -> PyResult<()> {
        for element in &self.elements {
            action.call1((element.as_ref(py),))?;
        }
        Ok(())
    }

    fn for_each_indexed(&self, py: Python<'_>, action: &PyAny) -> PyResult<()> {
        for (i, element) in self.elements.iter().enumerate() {
            action.call1((i, element.as_ref(py)))?;
        }
        Ok(())
    }

    fn on_each(&self, py: Python<'_>, action: &PyAny) -> PyResult<KotList> {
        for element in &self.elements {
            action.call1((element.as_ref(py),))?;
        }
        Ok(self.clone())
    }

    fn on_each_indexed(&self, py: Python<'_>, action: &PyAny) -> PyResult<KotList> {
        for (i, element) in self.elements.iter().enumerate() {
            action.call1((i, element.as_ref(py)))?;
        }
        Ok(self.clone())
    }

    // Conversion methods
    fn to_list(&self, py: Python<'_>) -> Py<PyList> {
        PyList::new(py, self.elements.iter().map(|e| e.as_ref(py))).into()
    }

    fn to_set(&self, py: Python<'_>) -> PyResult<Py<PySet>> {
        let set = PySet::empty(py)?;
        for element in &self.elements {
            set.add(element.as_ref(py))?;
        }
        Ok(set.into())
    }

    fn to_kot_list(&self) -> KotList {
        KotList::new_with_type(self.elements.clone(), self.element_type.clone())
    }

    fn to_kot_mutable_list(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let class = module.getattr("KotMutableList")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        Ok(class.call1((py_list,))?.into())
    }

    fn to_kot_set(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let class = module.getattr("KotSet")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        Ok(class.call1((py_list,))?.into())
    }

    fn to_kot_mutable_set(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let class = module.getattr("KotMutableSet")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        Ok(class.call1((py_list,))?.into())
    }

    // String methods
    #[pyo3(signature = (separator=", ", prefix="", postfix="", limit=-1, truncated="...", transform=None))]
    fn join_to_string(
        &self,
        py: Python<'_>,
        separator: &str,
        prefix: &str,
        postfix: &str,
        limit: i32,
        truncated: &str,
        transform: Option<&PyAny>,
    ) -> PyResult<String> {
        let mut result = prefix.to_string();
        let mut count = 0;

        for (i, element) in self.elements.iter().enumerate() {
            if limit >= 0 && count >= limit {
                result.push_str(truncated);
                break;
            }

            if i > 0 {
                result.push_str(separator);
            }

            let elem_str = if let Some(trans) = transform {
                trans.call1((element.as_ref(py),))?.str()?.to_string()
            } else {
                element.as_ref(py).str()?.to_string()
            };

            result.push_str(&elem_str);
            count += 1;
        }

        result.push_str(postfix);
        Ok(result)
    }

    // Component methods (for destructuring)
    fn component1(&self) -> PyResult<PyObject> {
        self.first()
    }

    fn component2(&self, py: Python<'_>) -> PyResult<PyObject> {
        self.get(py, 1)
    }

    fn component3(&self, py: Python<'_>) -> PyResult<PyObject> {
        self.get(py, 2)
    }

    fn component4(&self, py: Python<'_>) -> PyResult<PyObject> {
        self.get(py, 3)
    }

    fn component5(&self, py: Python<'_>) -> PyResult<PyObject> {
        self.get(py, 4)
    }

    // Single element methods
    fn single(&self) -> PyResult<PyObject> {
        if self.elements.is_empty() {
            return Err(PyValueError::new_err("List is empty"));
        }
        if self.elements.len() > 1 {
            return Err(PyValueError::new_err("List has more than one element"));
        }
        Ok(self.elements[0].clone())
    }

    fn single_or_null(&self) -> Option<PyObject> {
        if self.elements.len() == 1 {
            Some(self.elements[0].clone())
        } else {
            None
        }
    }

    fn single_or_none(&self) -> Option<PyObject> {
        self.single_or_null()
    }

    fn single_predicate(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<PyObject> {
        let mut found: Option<PyObject> = None;

        for element in &self.elements {
            let result = predicate.call1((element.as_ref(py),))?;
            if result.is_true()? {
                if found.is_some() {
                    return Err(PyValueError::new_err("More than one element matching predicate found"));
                }
                found = Some(element.clone());
            }
        }

        found.ok_or_else(|| PyValueError::new_err("No element matching predicate found"))
    }

    fn single_or_null_predicate(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<Option<PyObject>> {
        let mut found: Option<PyObject> = None;

        for element in &self.elements {
            let result = predicate.call1((element.as_ref(py),))?;
            if result.is_true()? {
                if found.is_some() {
                    return Ok(None);
                }
                found = Some(element.clone());
            }
        }

        Ok(found)
    }

    fn single_or_none_predicate(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<Option<PyObject>> {
        self.single_or_null_predicate(py, predicate)
    }

    // Random methods
    #[pyo3(signature = (random_instance=None))]
    fn random(&self, py: Python<'_>, random_instance: Option<&PyAny>) -> PyResult<PyObject> {
        if self.elements.is_empty() {
            return Err(PyIndexError::new_err("List is empty"));
        }

        let random_module = py.import("random")?;
        let index: usize = if let Some(rng) = random_instance {
            rng.call_method1("randint", (0, self.elements.len() - 1))?.extract()?
        } else {
            random_module.call_method1("randint", (0, self.elements.len() - 1))?.extract()?
        };

        Ok(self.elements[index].clone())
    }

    #[pyo3(signature = (random_instance=None))]
    fn random_or_null(&self, py: Python<'_>, random_instance: Option<&PyAny>) -> PyResult<Option<PyObject>> {
        if self.elements.is_empty() {
            return Ok(None);
        }
        Ok(Some(self.random(py, random_instance)?))
    }

    #[pyo3(signature = (random_instance=None))]
    fn random_or_none(&self, py: Python<'_>, random_instance: Option<&PyAny>) -> PyResult<Option<PyObject>> {
        self.random_or_null(py, random_instance)
    }

    // Take/Drop methods
    fn take(&self, n: usize) -> KotList {
        let elements: Vec<PyObject> = self.elements.iter()
            .take(n)
            .cloned()
            .collect();
        KotList::new_with_type(elements, self.element_type.clone())
    }

    fn take_last(&self, n: usize) -> KotList {
        let skip = self.elements.len().saturating_sub(n);
        let elements: Vec<PyObject> = self.elements.iter()
            .skip(skip)
            .cloned()
            .collect();
        KotList::new_with_type(elements, self.element_type.clone())
    }

    fn take_while(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<KotList> {
        let mut result = Vec::new();

        for element in &self.elements {
            let keep = predicate.call1((element.as_ref(py),))?;
            if keep.is_true()? {
                result.push(element.clone());
            } else {
                break;
            }
        }

        Ok(KotList::new_with_type(result, self.element_type.clone()))
    }

    fn drop(&self, n: usize) -> KotList {
        let elements: Vec<PyObject> = self.elements.iter()
            .skip(n)
            .cloned()
            .collect();
        KotList::new_with_type(elements, self.element_type.clone())
    }

    fn drop_last(&self, n: usize) -> KotList {
        let take = self.elements.len().saturating_sub(n);
        let elements: Vec<PyObject> = self.elements.iter()
            .take(take)
            .cloned()
            .collect();
        KotList::new_with_type(elements, self.element_type.clone())
    }

    fn drop_while(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<KotList> {
        let mut dropping = true;
        let mut result = Vec::new();

        for element in &self.elements {
            if dropping {
                let drop = predicate.call1((element.as_ref(py),))?;
                if !drop.is_true()? {
                    dropping = false;
                    result.push(element.clone());
                }
            } else {
                result.push(element.clone());
            }
        }

        Ok(KotList::new_with_type(result, self.element_type.clone()))
    }

    // Search methods
    fn find(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<Option<PyObject>> {
        self.first_or_null_predicate(py, predicate)
    }

    fn find_last(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<Option<PyObject>> {
        self.last_or_null_predicate(py, predicate)
    }

    // Utility methods
    fn as_reversed(&self) -> KotList {
        self.reversed()
    }

    fn if_empty(&self, py: Python<'_>, default_value: &PyAny) -> PyResult<PyObject> {
        if self.elements.is_empty() {
            Ok(default_value.call0()?.into())
        } else {
            Ok(self.clone().into_py(py))
        }
    }

    #[pyo3(signature = (index=0))]
    fn list_iterator(&self, py: Python<'_>, index: usize) -> PyResult<Py<KotListIterator>> {
        if index > self.elements.len() {
            return Err(PyIndexError::new_err(format!(
                "Index {} out of bounds for list of size {}", index, self.elements.len()
            )));
        }
        Py::new(py, KotListIterator {
            elements: self.elements[index..].iter().cloned().collect(),
            index: 0,
        })
    }

    // Grouping methods
    fn group_by(&self, py: Python<'_>, key_selector: &PyAny) -> PyResult<PyObject> {
        let kot_map_module = py.import("kotcollections")?;
        let kot_map_class = kot_map_module.getattr("KotMap")?;

        let dict = PyDict::new(py);
        for element in &self.elements {
            let elem = element.as_ref(py);
            let key = key_selector.call1((elem,))?;

            if let Ok(Some(list)) = dict.get_item(key) {
                list.downcast::<PyList>()?.append(elem)?;
            } else {
                let list = PyList::new(py, &[elem]);
                dict.set_item(key, list)?;
            }
        }

        // Convert lists to KotLists
        let result_dict = PyDict::new(py);
        for (key, value) in dict.iter() {
            let kot_list_class = kot_map_module.getattr("KotList")?;
            let kot_list = kot_list_class.call1((value,))?;
            result_dict.set_item(key, kot_list)?;
        }

        Ok(kot_map_class.call1((result_dict,))?.into())
    }

    fn grouping_by(&self, py: Python<'_>, key_selector: &PyAny) -> PyResult<PyObject> {
        let kot_grouping_module = py.import("kotcollections")?;
        let kot_grouping_class = kot_grouping_module.getattr("KotGrouping")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        Ok(kot_grouping_class.call1((py_list, key_selector))?.into())
    }

    // Chunking methods
    fn chunked(&self, py: Python<'_>, size: usize) -> PyResult<KotList> {
        if size == 0 {
            return Err(PyValueError::new_err("Size must be positive"));
        }

        let mut chunks = Vec::new();
        for chunk in self.elements.chunks(size) {
            let chunk_list = KotList::new_with_type(
                chunk.iter().cloned().collect(),
                self.element_type.clone()
            );
            chunks.push(chunk_list.into_py(py));
        }

        Ok(KotList::new_with_type(chunks, None))
    }

    #[pyo3(signature = (size, step=1, partial_windows=false))]
    fn windowed(&self, py: Python<'_>, size: usize, step: usize, partial_windows: bool) -> PyResult<KotList> {
        if size == 0 || step == 0 {
            return Err(PyValueError::new_err("Size and step must be positive"));
        }

        let mut windows = Vec::new();
        let mut i = 0;

        while i < self.elements.len() {
            let end = std::cmp::min(i + size, self.elements.len());
            let window_size = end - i;

            if window_size == size || (partial_windows && window_size > 0) {
                let window = KotList::new_with_type(
                    self.elements[i..end].iter().cloned().collect(),
                    self.element_type.clone()
                );
                windows.push(window.into_py(py));
            }

            if window_size < size && !partial_windows {
                break;
            }

            i += step;
        }

        Ok(KotList::new_with_type(windows, None))
    }

    // Associate methods
    fn associate_with(&self, py: Python<'_>, value_selector: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_map_class = module.getattr("KotMap")?;
        let dict = PyDict::new(py);

        for element in &self.elements {
            let elem = element.as_ref(py);
            let value = value_selector.call1((elem,))?;
            dict.set_item(elem, value)?;
        }

        Ok(kot_map_class.call1((dict,))?.into())
    }

    fn associate_by(&self, py: Python<'_>, key_selector: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_map_class = module.getattr("KotMap")?;
        let dict = PyDict::new(py);

        for element in &self.elements {
            let elem = element.as_ref(py);
            let key = key_selector.call1((elem,))?;
            dict.set_item(key, elem)?;
        }

        Ok(kot_map_class.call1((dict,))?.into())
    }

    fn associate(&self, py: Python<'_>, transform: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_map_class = module.getattr("KotMap")?;
        let dict = PyDict::new(py);

        for element in &self.elements {
            let pair = transform.call1((element.as_ref(py),))?;
            let key = pair.get_item(0)?;
            let value = pair.get_item(1)?;
            dict.set_item(key, value)?;
        }

        Ok(kot_map_class.call1((dict,))?.into())
    }

    // Set operations
    fn intersect(&self, py: Python<'_>, other: &PyAny) -> PyResult<PyObject> {
        let kot_set_module = py.import("kotcollections")?;
        let kot_set_class = kot_set_module.getattr("KotSet")?;

        let mut other_elements = Vec::new();
        for item in other.iter()? {
            other_elements.push(item?);
        }

        let mut result = Vec::new();
        let mut seen: Vec<PyObject> = Vec::new();
        for element in &self.elements {
            let elem = element.as_ref(py);
            for other_elem in &other_elements {
                if elem.eq(*other_elem)? {
                    // Check for duplicates in result
                    let mut dup = false;
                    for s in &seen {
                        if elem.eq(s.as_ref(py))? {
                            dup = true;
                            break;
                        }
                    }
                    if !dup {
                        result.push(element.clone());
                        seen.push(element.clone());
                    }
                    break;
                }
            }
        }

        let py_list = PyList::new(py, result.iter().map(|e| e.as_ref(py)));
        Ok(kot_set_class.call1((py_list,))?.into())
    }

    fn union(&self, py: Python<'_>, other: &PyAny) -> PyResult<PyObject> {
        let kot_set_module = py.import("kotcollections")?;
        let kot_set_class = kot_set_module.getattr("KotSet")?;

        let mut result = self.elements.clone();

        for item in other.iter()? {
            let item = item?;
            let item_obj: PyObject = item.into();
            let mut found = false;
            for r in &result {
                if item_obj.as_ref(py).eq(r.as_ref(py))? {
                    found = true;
                    break;
                }
            }
            if !found {
                result.push(item_obj);
            }
        }

        let py_list = PyList::new(py, result.iter().map(|e| e.as_ref(py)));
        Ok(kot_set_class.call1((py_list,))?.into())
    }

    fn subtract(&self, py: Python<'_>, other: &PyAny) -> PyResult<PyObject> {
        let kot_set_module = py.import("kotcollections")?;
        let kot_set_class = kot_set_module.getattr("KotSet")?;

        let mut other_elements = Vec::new();
        for item in other.iter()? {
            other_elements.push(item?);
        }

        let mut result = Vec::new();
        let mut seen: Vec<PyObject> = Vec::new();
        for element in &self.elements {
            let mut found = false;
            for other_elem in &other_elements {
                if element.as_ref(py).eq(*other_elem)? {
                    found = true;
                    break;
                }
            }
            if !found {
                // Check for duplicates in result
                let mut dup = false;
                for s in &seen {
                    if element.as_ref(py).eq(s.as_ref(py))? {
                        dup = true;
                        break;
                    }
                }
                if !dup {
                    result.push(element.clone());
                    seen.push(element.clone());
                }
            }
        }

        let py_list = PyList::new(py, result.iter().map(|e| e.as_ref(py)));
        Ok(kot_set_class.call1((py_list,))?.into())
    }
}

// Iterator for KotList
#[pyclass]
pub struct KotListIterator {
    elements: Vec<PyObject>,
    index: usize,
}

#[pymethods]
impl KotListIterator {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(&mut self) -> Option<PyObject> {
        if self.index < self.elements.len() {
            let result = self.elements[self.index].clone();
            self.index += 1;
            Some(result)
        } else {
            None
        }
    }
}
