use pyo3::prelude::*;
use pyo3::types::{PyList, PySet, PyDict, PyTuple, PyType};
use pyo3::exceptions::{PyIndexError, PyValueError, PyTypeError};

/// A mutable set implementation that reproduces Kotlin's MutableSet interface.
#[pyclass(subclass)]
#[derive(Clone)]
pub struct KotMutableSet {
    elements: Vec<PyObject>,
    element_type: Option<PyObject>,
}

impl KotMutableSet {
    fn check_type(&mut self, py: Python<'_>, element: &PyObject) -> PyResult<()> {
        if let Some(ref expected_type) = self.element_type {
            let expected = expected_type.as_ref(py);
            let elem = element.as_ref(py);

            if !elem.is_instance(expected.downcast::<PyType>().map_err(|_| {
                PyTypeError::new_err("element_type must be a type")
            })?)? {
                let elem_type_name = elem.get_type().name()?;
                let expected_type_name = expected.getattr("__name__")
                    .map(|n| n.to_string())
                    .unwrap_or_else(|_| expected.to_string());
                return Err(PyTypeError::new_err(format!(
                    "KotMutableSet expected element of type {}, got {}",
                    expected_type_name, elem_type_name
                )));
            }
        } else {
            let elem = element.as_ref(py);
            self.element_type = Some(elem.get_type().into_py(py));
        }
        Ok(())
    }

    fn contains_element(&self, py: Python<'_>, element: &PyAny) -> PyResult<bool> {
        for e in &self.elements {
            if e.as_ref(py).eq(element)? {
                return Ok(true);
            }
        }
        Ok(false)
    }

    fn add_if_not_present(&mut self, py: Python<'_>, element: PyObject) -> PyResult<bool> {
        for e in &self.elements {
            if e.as_ref(py).eq(element.as_ref(py))? {
                return Ok(false);
            }
        }
        self.elements.push(element);
        Ok(true)
    }

    pub fn new_with_type(elements: Vec<PyObject>, element_type: Option<PyObject>) -> Self {
        KotMutableSet { elements, element_type }
    }
}

#[pymethods]
impl KotMutableSet {
    #[new]
    #[pyo3(signature = (elements=None))]
    fn new(py: Python<'_>, elements: Option<&PyAny>) -> PyResult<Self> {
        let mut set = KotMutableSet {
            elements: Vec::new(),
            element_type: None,
        };

        if let Some(elems) = elements {
            let iter = elems.iter()?;
            for item in iter {
                let item = item?;
                let obj = item.into_py(py);
                set.check_type(py, &obj)?;
                set.add_if_not_present(py, obj)?;
            }
        }

        Ok(set)
    }

    #[classmethod]
    fn of_type(
        _cls: &PyType,
        py: Python<'_>,
        element_type: &PyType,
        elements: Option<&PyAny>,
    ) -> PyResult<Self> {
        let mut set = KotMutableSet {
            elements: Vec::new(),
            element_type: Some(element_type.into_py(py)),
        };

        if let Some(elems) = elements {
            let iter = elems.iter()?;
            for item in iter {
                let item = item?;
                let obj = item.into_py(py);
                set.check_type(py, &obj)?;
                set.add_if_not_present(py, obj)?;
            }
        }

        Ok(set)
    }

    fn __repr__(&self, py: Python<'_>) -> PyResult<String> {
        let items: Vec<String> = self.elements.iter()
            .map(|e| e.as_ref(py).repr().map(|r| r.to_string()).unwrap_or_else(|_| "?".to_string()))
            .collect();
        Ok(format!("KotMutableSet({{{}}})", items.join(", ")))
    }

    fn __str__(&self, py: Python<'_>) -> PyResult<String> {
        let items: Vec<String> = self.elements.iter()
            .map(|e| e.as_ref(py).str().map(|s| s.to_string()).unwrap_or_else(|_| "?".to_string()))
            .collect();
        Ok(format!("{{{}}}", items.join(", ")))
    }

    fn __iter__(&self, py: Python<'_>) -> PyResult<Py<KotMutableSetIterator>> {
        Py::new(py, KotMutableSetIterator {
            elements: self.elements.clone(),
            index: 0,
        })
    }

    fn __len__(&self) -> usize {
        self.elements.len()
    }

    fn __contains__(&self, py: Python<'_>, element: &PyAny) -> PyResult<bool> {
        self.contains_element(py, element)
    }

    // Properties
    #[getter]
    fn size(&self) -> usize {
        self.elements.len()
    }

    fn is_empty(&self) -> bool {
        self.elements.is_empty()
    }

    fn is_not_empty(&self) -> bool {
        !self.elements.is_empty()
    }

    fn contains(&self, py: Python<'_>, element: &PyAny) -> PyResult<bool> {
        self.contains_element(py, element)
    }

    fn contains_all(&self, py: Python<'_>, elements: &PyAny) -> PyResult<bool> {
        let iter = elements.iter()?;
        for item in iter {
            let item = item?;
            if !self.contains_element(py, &item)? {
                return Ok(false);
            }
        }
        Ok(true)
    }

    // Mutable methods
    fn add(&mut self, py: Python<'_>, element: &PyAny) -> PyResult<bool> {
        let obj = element.into_py(py);
        self.check_type(py, &obj)?;
        self.add_if_not_present(py, obj)
    }

    fn add_all(&mut self, py: Python<'_>, elements: &PyAny) -> PyResult<bool> {
        let mut added = false;
        let iter = elements.iter()?;
        for item in iter {
            let item = item?;
            let obj = item.into_py(py);
            self.check_type(py, &obj)?;
            if self.add_if_not_present(py, obj)? {
                added = true;
            }
        }
        Ok(added)
    }

    fn remove(&mut self, py: Python<'_>, element: &PyAny) -> PyResult<bool> {
        for i in 0..self.elements.len() {
            if self.elements[i].as_ref(py).eq(element)? {
                self.elements.remove(i);
                return Ok(true);
            }
        }
        Ok(false)
    }

    fn remove_all(&mut self, py: Python<'_>, elements: &PyAny) -> PyResult<bool> {
        let mut to_remove = Vec::new();
        for item in elements.iter()? {
            to_remove.push(item?.into_py(py));
        }

        let initial_len = self.elements.len();
        self.elements.retain(|e| {
            for r in &to_remove {
                if e.as_ref(py).eq(r.as_ref(py)).unwrap_or(false) {
                    return false;
                }
            }
            true
        });

        Ok(self.elements.len() < initial_len)
    }

    fn retain_all(&mut self, py: Python<'_>, elements: &PyAny) -> PyResult<bool> {
        let mut to_keep = Vec::new();
        for item in elements.iter()? {
            to_keep.push(item?.into_py(py));
        }

        let initial_len = self.elements.len();
        self.elements.retain(|e| {
            for k in &to_keep {
                if e.as_ref(py).eq(k.as_ref(py)).unwrap_or(false) {
                    return true;
                }
            }
            false
        });

        Ok(self.elements.len() < initial_len)
    }

    fn remove_if(&mut self, py: Python<'_>, filter_predicate: &PyAny) -> PyResult<bool> {
        let initial_len = self.elements.len();
        let mut new_elements = Vec::new();

        for element in &self.elements {
            let result = filter_predicate.call1((element.as_ref(py),))?;
            if !result.is_true()? {
                new_elements.push(element.clone_ref(py));
            }
        }

        self.elements = new_elements;
        Ok(self.elements.len() < initial_len)
    }

    fn clear(&mut self) {
        self.elements.clear();
    }

    // Access methods
    fn first(&self, py: Python<'_>) -> PyResult<PyObject> {
        self.elements.first()
            .map(|e| e.clone_ref(py))
            .ok_or_else(|| PyValueError::new_err("Set is empty"))
    }

    fn first_or_null(&self, py: Python<'_>) -> Option<PyObject> {
        self.elements.first().map(|e| e.clone_ref(py))
    }

    fn first_or_none(&self, py: Python<'_>) -> Option<PyObject> {
        self.first_or_null(py)
    }

    fn last(&self, py: Python<'_>) -> PyResult<PyObject> {
        self.elements.last()
            .map(|e| e.clone_ref(py))
            .ok_or_else(|| PyValueError::new_err("Set is empty"))
    }

    fn last_or_null(&self, py: Python<'_>) -> Option<PyObject> {
        self.elements.last().map(|e| e.clone_ref(py))
    }

    fn last_or_none(&self, py: Python<'_>) -> Option<PyObject> {
        self.last_or_null(py)
    }

    // Set operations
    fn intersect(&self, py: Python<'_>, other: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_set_class = module.getattr("KotSet")?;

        let mut other_elements = Vec::new();
        for item in other.iter()? {
            other_elements.push(item?.into_py(py));
        }

        let mut result = Vec::new();
        for element in &self.elements {
            for other_elem in &other_elements {
                if element.as_ref(py).eq(other_elem.as_ref(py))? {
                    result.push(element.as_ref(py));
                    break;
                }
            }
        }

        let py_list = PyList::new(py, result);
        Ok(kot_set_class.call1((py_list,))?.into_py(py))
    }

    fn union(&self, py: Python<'_>, other: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_set_class = module.getattr("KotSet")?;

        let mut result: Vec<PyObject> = self.elements.iter().map(|e| e.clone_ref(py)).collect();

        for item in other.iter()? {
            let item = item?.into_py(py);
            let mut found = false;
            for r in &result {
                if item.as_ref(py).eq(r.as_ref(py))? {
                    found = true;
                    break;
                }
            }
            if !found {
                result.push(item);
            }
        }

        let py_list = PyList::new(py, result.iter().map(|e| e.as_ref(py)));
        Ok(kot_set_class.call1((py_list,))?.into_py(py))
    }

    fn subtract(&self, py: Python<'_>, other: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_set_class = module.getattr("KotSet")?;

        let mut other_elements = Vec::new();
        for item in other.iter()? {
            other_elements.push(item?.into_py(py));
        }

        let mut result = Vec::new();
        for element in &self.elements {
            let mut found = false;
            for other_elem in &other_elements {
                if element.as_ref(py).eq(other_elem.as_ref(py))? {
                    found = true;
                    break;
                }
            }
            if !found {
                result.push(element.as_ref(py));
            }
        }

        let py_list = PyList::new(py, result);
        Ok(kot_set_class.call1((py_list,))?.into_py(py))
    }

    fn plus(&self, py: Python<'_>, element: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_set_class = module.getattr("KotSet")?;

        let mut result: Vec<PyObject> = self.elements.iter().map(|e| e.clone_ref(py)).collect();

        if element.is_instance_of::<pyo3::types::PyString>() || element.is_instance_of::<pyo3::types::PyBytes>() {
            let obj = element.into_py(py);
            let mut found = false;
            for r in &result {
                if obj.as_ref(py).eq(r.as_ref(py))? {
                    found = true;
                    break;
                }
            }
            if !found {
                result.push(obj);
            }
        } else if let Ok(iter) = element.iter() {
            for item in iter {
                let item = item?.into_py(py);
                let mut found = false;
                for r in &result {
                    if item.as_ref(py).eq(r.as_ref(py))? {
                        found = true;
                        break;
                    }
                }
                if !found {
                    result.push(item);
                }
            }
        } else {
            let obj = element.into_py(py);
            let mut found = false;
            for r in &result {
                if obj.as_ref(py).eq(r.as_ref(py))? {
                    found = true;
                    break;
                }
            }
            if !found {
                result.push(obj);
            }
        }

        let py_list = PyList::new(py, result.iter().map(|e| e.as_ref(py)));
        Ok(kot_set_class.call1((py_list,))?.into_py(py))
    }

    fn minus(&self, py: Python<'_>, element: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_set_class = module.getattr("KotSet")?;

        let mut to_remove = Vec::new();

        if element.is_instance_of::<pyo3::types::PyString>() || element.is_instance_of::<pyo3::types::PyBytes>() {
            to_remove.push(element.into_py(py));
        } else if let Ok(iter) = element.iter() {
            for item in iter {
                to_remove.push(item?.into_py(py));
            }
        } else {
            to_remove.push(element.into_py(py));
        }

        let mut result = Vec::new();
        for elem in &self.elements {
            let mut should_remove = false;
            for r in &to_remove {
                if elem.as_ref(py).eq(r.as_ref(py))? {
                    should_remove = true;
                    break;
                }
            }
            if !should_remove {
                result.push(elem.as_ref(py));
            }
        }

        let py_list = PyList::new(py, result);
        Ok(kot_set_class.call1((py_list,))?.into_py(py))
    }

    // Transformation methods
    fn map(&self, py: Python<'_>, transform: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_list_class = module.getattr("KotList")?;

        let mut result = Vec::new();
        for element in &self.elements {
            let transformed = transform.call1((element.as_ref(py),))?;
            result.push(transformed);
        }

        let py_list = PyList::new(py, result);
        Ok(kot_list_class.call1((py_list,))?.into_py(py))
    }

    fn filter(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_set_class = module.getattr("KotSet")?;

        let mut result = Vec::new();
        for element in &self.elements {
            let keep = predicate.call1((element.as_ref(py),))?;
            if keep.is_true()? {
                result.push(element.as_ref(py));
            }
        }

        let py_list = PyList::new(py, result);
        Ok(kot_set_class.call1((py_list,))?.into_py(py))
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

    // Fold/Reduce methods
    fn fold(&self, py: Python<'_>, initial: &PyAny, operation: &PyAny) -> PyResult<PyObject> {
        let mut result = initial.into_py(py);
        for element in &self.elements {
            result = operation.call1((result.as_ref(py), element.as_ref(py)))?.into_py(py);
        }
        Ok(result)
    }

    fn reduce(&self, py: Python<'_>, operation: &PyAny) -> PyResult<PyObject> {
        if self.elements.is_empty() {
            return Err(PyValueError::new_err("Cannot reduce empty set"));
        }

        let mut result = self.elements[0].clone_ref(py);
        for element in &self.elements[1..] {
            result = operation.call1((result.as_ref(py), element.as_ref(py)))?.into_py(py);
        }
        Ok(result)
    }

    // ForEach methods
    fn for_each(&self, py: Python<'_>, action: &PyAny) -> PyResult<()> {
        for element in &self.elements {
            action.call1((element.as_ref(py),))?;
        }
        Ok(())
    }

    // Conversion methods
    fn to_list(&self, py: Python<'_>) -> PyResult<Py<PyList>> {
        Ok(PyList::new(py, self.elements.iter().map(|e| e.as_ref(py))).into())
    }

    fn to_set(&self, py: Python<'_>) -> PyResult<Py<PySet>> {
        let set = PySet::empty(py)?;
        for element in &self.elements {
            set.add(element.as_ref(py))?;
        }
        Ok(set.into())
    }

    fn to_kot_list(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_list_class = module.getattr("KotList")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        Ok(kot_list_class.call1((py_list,))?.into_py(py))
    }

    fn to_kot_mutable_list(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let class = module.getattr("KotMutableList")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        Ok(class.call1((py_list,))?.into_py(py))
    }

    fn to_kot_set(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let class = module.getattr("KotSet")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        Ok(class.call1((py_list,))?.into_py(py))
    }

    fn to_kot_mutable_set(&self, py: Python<'_>) -> KotMutableSet {
        KotMutableSet::new_with_type(
            self.elements.iter().map(|e| e.clone_ref(py)).collect(),
            self.element_type.clone()
        )
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
}

// Iterator for KotMutableSet
#[pyclass]
pub struct KotMutableSetIterator {
    elements: Vec<PyObject>,
    index: usize,
}

#[pymethods]
impl KotMutableSetIterator {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(&mut self, py: Python<'_>) -> Option<PyObject> {
        if self.index < self.elements.len() {
            let result = self.elements[self.index].clone_ref(py);
            self.index += 1;
            Some(result)
        } else {
            None
        }
    }
}
