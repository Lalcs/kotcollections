use pyo3::prelude::*;
use pyo3::types::{PyList, PyDict, PyType};
use pyo3::exceptions::{PyIndexError, PyValueError, PyTypeError, PyRuntimeError};

/// A mutable list implementation that reproduces Kotlin's MutableList interface.
#[pyclass(subclass)]
#[derive(Clone)]
pub struct KotMutableList {
    elements: Vec<PyObject>,
    element_type: Option<PyObject>,
}

impl KotMutableList {
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
                    "KotMutableList expected element of type {}, got {}",
                    expected_type_name, elem_type_name
                )));
            }
        } else {
            let elem = element.as_ref(py);
            self.element_type = Some(elem.get_type().into_py(py));
        }
        Ok(())
    }

    pub fn new_with_type(elements: Vec<PyObject>, element_type: Option<PyObject>) -> Self {
        KotMutableList { elements, element_type }
    }
}

#[pymethods]
impl KotMutableList {
    #[new]
    #[pyo3(signature = (elements=None))]
    fn new(py: Python<'_>, elements: Option<&PyAny>) -> PyResult<Self> {
        let mut list = KotMutableList {
            elements: Vec::new(),
            element_type: None,
        };

        if let Some(elems) = elements {
            let iter = elems.iter()?;
            for item in iter {
                let item = item?;
                let obj = item.into_py(py);
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
        let mut list = KotMutableList {
            elements: Vec::new(),
            element_type: Some(element_type.into_py(py)),
        };

        if let Some(elems) = elements {
            let iter = elems.iter()?;
            for item in iter {
                let item = item?;
                let obj = item.into_py(py);
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
        Ok(format!("KotMutableList([{}])", items.join(", ")))
    }

    fn __str__(&self, py: Python<'_>) -> PyResult<String> {
        let items: Vec<String> = self.elements.iter()
            .map(|e| e.as_ref(py).str().map(|s| s.to_string()).unwrap_or_else(|_| "?".to_string()))
            .collect();
        Ok(format!("[{}]", items.join(", ")))
    }

    fn __eq__(&self, py: Python<'_>, other: &PyAny) -> PyResult<bool> {
        if let Ok(other_list) = other.extract::<PyRef<KotMutableList>>() {
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

    fn __iter__(&self, py: Python<'_>) -> PyResult<Py<KotMutableListIterator>> {
        Py::new(py, KotMutableListIterator {
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
            .map(|e| e.clone_ref(py))
            .ok_or_else(|| PyIndexError::new_err(format!(
                "Index {} out of bounds for list of size {}", index, self.elements.len()
            )))
    }

    fn __setitem__(&mut self, py: Python<'_>, index: isize, value: &PyAny) -> PyResult<()> {
        let idx = if index < 0 {
            (self.elements.len() as isize + index) as usize
        } else {
            index as usize
        };

        if idx >= self.elements.len() {
            return Err(PyIndexError::new_err(format!(
                "Index {} out of bounds for list of size {}", index, self.elements.len()
            )));
        }

        let obj = value.into_py(py);
        self.check_type(py, &obj)?;
        self.elements[idx] = obj;
        Ok(())
    }

    fn __delitem__(&mut self, index: isize) -> PyResult<()> {
        let idx = if index < 0 {
            (self.elements.len() as isize + index) as usize
        } else {
            index as usize
        };

        if idx >= self.elements.len() {
            return Err(PyIndexError::new_err(format!(
                "Index {} out of bounds for list of size {}", index, self.elements.len()
            )));
        }

        self.elements.remove(idx);
        Ok(())
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

    // Properties
    #[getter]
    fn size(&self) -> usize {
        self.elements.len()
    }

    #[getter]
    fn indices(&self, py: Python<'_>) -> PyResult<PyObject> {
        let range = py.import("builtins")?.getattr("range")?;
        Ok(range.call1((self.elements.len(),))?.into_py(py))
    }

    #[getter]
    fn last_index(&self) -> isize {
        if self.elements.is_empty() {
            -1
        } else {
            (self.elements.len() - 1) as isize
        }
    }

    fn is_empty(&self) -> bool {
        self.elements.is_empty()
    }

    fn is_not_empty(&self) -> bool {
        !self.elements.is_empty()
    }

    fn get(&self, py: Python<'_>, index: usize) -> PyResult<PyObject> {
        self.elements.get(index)
            .map(|e| e.clone_ref(py))
            .ok_or_else(|| PyIndexError::new_err(format!(
                "Index {} out of bounds for list of size {}", index, self.elements.len()
            )))
    }

    fn get_or_null(&self, py: Python<'_>, index: usize) -> Option<PyObject> {
        self.elements.get(index).map(|e| e.clone_ref(py))
    }

    fn get_or_none(&self, py: Python<'_>, index: usize) -> Option<PyObject> {
        self.get_or_null(py, index)
    }

    // Mutable-specific methods
    fn add(&mut self, py: Python<'_>, element: &PyAny) -> PyResult<bool> {
        let obj = element.into_py(py);
        self.check_type(py, &obj)?;
        self.elements.push(obj);
        Ok(true)
    }

    fn add_at(&mut self, py: Python<'_>, index: usize, element: &PyAny) -> PyResult<()> {
        if index > self.elements.len() {
            return Err(PyIndexError::new_err(format!(
                "Index {} out of bounds for insertion", index
            )));
        }

        let obj = element.into_py(py);
        self.check_type(py, &obj)?;
        self.elements.insert(index, obj);
        Ok(())
    }

    fn add_all(&mut self, py: Python<'_>, elements: &PyAny) -> PyResult<bool> {
        let mut added = false;
        let iter = elements.iter()?;
        for item in iter {
            let item = item?;
            let obj = item.into_py(py);
            self.check_type(py, &obj)?;
            self.elements.push(obj);
            added = true;
        }
        Ok(added)
    }

    fn add_all_at(&mut self, py: Python<'_>, index: usize, elements: &PyAny) -> PyResult<bool> {
        if index > self.elements.len() {
            return Err(PyIndexError::new_err(format!(
                "Index {} out of bounds for insertion", index
            )));
        }

        let mut items = Vec::new();
        let iter = elements.iter()?;
        for item in iter {
            let item = item?;
            let obj = item.into_py(py);
            self.check_type(py, &obj)?;
            items.push(obj);
        }

        if items.is_empty() {
            return Ok(false);
        }

        for (i, item) in items.into_iter().enumerate() {
            self.elements.insert(index + i, item);
        }
        Ok(true)
    }

    fn set(&mut self, py: Python<'_>, index: usize, element: &PyAny) -> PyResult<PyObject> {
        if index >= self.elements.len() {
            return Err(PyIndexError::new_err(format!(
                "Index {} out of bounds for list of size {}", index, self.elements.len()
            )));
        }

        let obj = element.into_py(py);
        self.check_type(py, &obj)?;
        let old = self.elements[index].clone_ref(py);
        self.elements[index] = obj;
        Ok(old)
    }

    fn remove_at(&mut self, py: Python<'_>, index: usize) -> PyResult<PyObject> {
        if index >= self.elements.len() {
            return Err(PyIndexError::new_err(format!(
                "Index {} out of bounds for list of size {}", index, self.elements.len()
            )));
        }

        Ok(self.elements.remove(index))
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

    fn remove_first(&mut self, py: Python<'_>) -> PyResult<PyObject> {
        if self.elements.is_empty() {
            return Err(PyIndexError::new_err("List is empty"));
        }
        Ok(self.elements.remove(0))
    }

    fn remove_last(&mut self, py: Python<'_>) -> PyResult<PyObject> {
        self.elements.pop()
            .ok_or_else(|| PyIndexError::new_err("List is empty"))
    }

    fn remove_first_or_null(&mut self, py: Python<'_>) -> Option<PyObject> {
        if self.elements.is_empty() {
            None
        } else {
            Some(self.elements.remove(0))
        }
    }

    fn remove_first_or_none(&mut self, py: Python<'_>) -> Option<PyObject> {
        self.remove_first_or_null(py)
    }

    fn remove_last_or_null(&mut self, py: Python<'_>) -> Option<PyObject> {
        self.elements.pop()
    }

    fn remove_last_or_none(&mut self, py: Python<'_>) -> Option<PyObject> {
        self.remove_last_or_null(py)
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

    fn replace_all(&mut self, py: Python<'_>, operator: &PyAny) -> PyResult<()> {
        for i in 0..self.elements.len() {
            let new_element = operator.call1((self.elements[i].as_ref(py),))?;
            let obj = new_element.into_py(py);
            self.check_type(py, &obj)?;
            self.elements[i] = obj;
        }
        Ok(())
    }

    fn clear(&mut self) {
        self.elements.clear();
    }

    #[pyo3(signature = (key=None, reverse=false))]
    fn sort(&mut self, py: Python<'_>, key: Option<&PyAny>, reverse: bool) -> PyResult<()> {
        let builtins = py.import("builtins")?;
        let sorted_fn = builtins.getattr("sorted")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));

        let kwargs = PyDict::new(py);
        if let Some(k) = key {
            kwargs.set_item("key", k)?;
        }
        kwargs.set_item("reverse", reverse)?;

        let result = sorted_fn.call((py_list,), Some(kwargs))?;
        self.elements.clear();
        for item in result.iter()? {
            self.elements.push(item?.into_py(py));
        }

        Ok(())
    }

    fn sort_descending(&mut self, py: Python<'_>) -> PyResult<()> {
        self.sort(py, None, true)
    }

    fn sort_by(&mut self, py: Python<'_>, selector: &PyAny) -> PyResult<()> {
        self.sort(py, Some(selector), false)
    }

    fn sort_by_descending(&mut self, py: Python<'_>, selector: &PyAny) -> PyResult<()> {
        self.sort(py, Some(selector), true)
    }

    fn sort_with(&mut self, py: Python<'_>, comparator: &PyAny) -> PyResult<()> {
        let functools = py.import("functools")?;
        let cmp_to_key = functools.getattr("cmp_to_key")?;
        let key = cmp_to_key.call1((comparator,))?;
        self.sort(py, Some(key), false)
    }

    fn reverse(&mut self) {
        self.elements.reverse();
    }

    #[pyo3(signature = (random_instance=None))]
    fn shuffle(&mut self, py: Python<'_>, random_instance: Option<&PyAny>) -> PyResult<()> {
        let random_module = py.import("random")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));

        if let Some(rng) = random_instance {
            rng.call_method1("shuffle", (py_list,))?;
        } else {
            random_module.call_method1("shuffle", (py_list,))?;
        }

        self.elements.clear();
        for item in py_list.iter() {
            self.elements.push(item.into_py(py));
        }

        Ok(())
    }

    fn fill(&mut self, py: Python<'_>, value: &PyAny) -> PyResult<()> {
        let obj = value.into_py(py);
        self.check_type(py, &obj)?;
        for i in 0..self.elements.len() {
            self.elements[i] = obj.clone_ref(py);
        }
        Ok(())
    }

    // Inherited methods from KotList that need to be re-implemented
    fn first(&self, py: Python<'_>) -> PyResult<PyObject> {
        self.elements.first()
            .map(|e| e.clone_ref(py))
            .ok_or_else(|| PyIndexError::new_err("List is empty"))
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
            .ok_or_else(|| PyIndexError::new_err("List is empty"))
    }

    fn last_or_null(&self, py: Python<'_>) -> Option<PyObject> {
        self.elements.last().map(|e| e.clone_ref(py))
    }

    fn last_or_none(&self, py: Python<'_>) -> Option<PyObject> {
        self.last_or_null(py)
    }

    fn contains(&self, py: Python<'_>, element: &PyAny) -> PyResult<bool> {
        self.__contains__(py, element)
    }

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

    // Transformation methods returning new KotList
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
        let kot_list_class = module.getattr("KotList")?;

        let mut result = Vec::new();
        for element in &self.elements {
            let keep = predicate.call1((element.as_ref(py),))?;
            if keep.is_true()? {
                result.push(element.as_ref(py));
            }
        }

        let py_list = PyList::new(py, result);
        Ok(kot_list_class.call1((py_list,))?.into_py(py))
    }

    fn fold(&self, py: Python<'_>, initial: &PyAny, operation: &PyAny) -> PyResult<PyObject> {
        let mut result = initial.into_py(py);
        for element in &self.elements {
            result = operation.call1((result.as_ref(py), element.as_ref(py)))?.into_py(py);
        }
        Ok(result)
    }

    fn reduce(&self, py: Python<'_>, operation: &PyAny) -> PyResult<PyObject> {
        if self.elements.is_empty() {
            return Err(PyValueError::new_err("Cannot reduce empty list"));
        }

        let mut result = self.elements[0].clone_ref(py);
        for element in &self.elements[1..] {
            result = operation.call1((result.as_ref(py), element.as_ref(py)))?.into_py(py);
        }
        Ok(result)
    }

    // Conversion methods
    fn to_list(&self, py: Python<'_>) -> PyResult<Py<PyList>> {
        Ok(PyList::new(py, self.elements.iter().map(|e| e.as_ref(py))).into())
    }

    fn to_kot_list(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_list_class = module.getattr("KotList")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        Ok(kot_list_class.call1((py_list,))?.into_py(py))
    }

    fn to_kot_mutable_list(&self, py: Python<'_>) -> KotMutableList {
        KotMutableList::new_with_type(
            self.elements.iter().map(|e| e.clone_ref(py)).collect(),
            self.element_type.clone()
        )
    }

    fn to_kot_set(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let class = module.getattr("KotSet")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        Ok(class.call1((py_list,))?.into_py(py))
    }

    fn to_kot_mutable_set(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let class = module.getattr("KotMutableSet")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        Ok(class.call1((py_list,))?.into_py(py))
    }

    fn sub_list(&self, py: Python<'_>, from_index: usize, to_index: usize) -> PyResult<KotMutableList> {
        if from_index > to_index || to_index > self.elements.len() {
            return Err(PyIndexError::new_err("Invalid sublist range"));
        }

        let elements: Vec<PyObject> = self.elements[from_index..to_index]
            .iter()
            .map(|e| e.clone_ref(py))
            .collect();

        Ok(KotMutableList::new_with_type(elements, self.element_type.clone()))
    }

    fn as_reversed(&self, py: Python<'_>) -> KotMutableList {
        let elements: Vec<PyObject> = self.elements.iter().rev().map(|e| e.clone_ref(py)).collect();
        KotMutableList::new_with_type(elements, self.element_type.clone())
    }

    #[pyo3(signature = (index=0))]
    fn list_iterator(&self, py: Python<'_>, index: usize) -> PyResult<Py<MutableListIterator>> {
        if index > self.elements.len() {
            return Err(PyIndexError::new_err(format!(
                "Index {} out of bounds for list of size {}", index, self.elements.len()
            )));
        }
        Py::new(py, MutableListIterator::new(
            self.elements.clone(),
            self.element_type.clone(),
            index
        ))
    }

    // Additional useful methods
    fn reversed(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_list_class = module.getattr("KotList")?;
        let elements: Vec<&PyObject> = self.elements.iter().rev().collect();
        let py_list = PyList::new(py, elements.iter().map(|e| e.as_ref(py)));
        Ok(kot_list_class.call1((py_list,))?.into_py(py))
    }

    #[pyo3(signature = (key=None, reverse=false))]
    fn sorted(&self, py: Python<'_>, key: Option<&PyAny>, reverse: bool) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_list_class = module.getattr("KotList")?;

        let builtins = py.import("builtins")?;
        let sorted_fn = builtins.getattr("sorted")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));

        let kwargs = PyDict::new(py);
        if let Some(k) = key {
            kwargs.set_item("key", k)?;
        }
        kwargs.set_item("reverse", reverse)?;

        let result = sorted_fn.call((py_list,), Some(kwargs))?;
        Ok(kot_list_class.call1((result,))?.into_py(py))
    }

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

    fn take(&self, py: Python<'_>, n: usize) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_list_class = module.getattr("KotList")?;
        let elements: Vec<&PyObject> = self.elements.iter().take(n).collect();
        let py_list = PyList::new(py, elements.iter().map(|e| e.as_ref(py)));
        Ok(kot_list_class.call1((py_list,))?.into_py(py))
    }

    fn drop(&self, py: Python<'_>, n: usize) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_list_class = module.getattr("KotList")?;
        let elements: Vec<&PyObject> = self.elements.iter().skip(n).collect();
        let py_list = PyList::new(py, elements.iter().map(|e| e.as_ref(py)));
        Ok(kot_list_class.call1((py_list,))?.into_py(py))
    }

    fn distinct(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_list_class = module.getattr("KotList")?;

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
                seen.push(element.clone_ref(py));
                result.push(element.as_ref(py));
            }
        }

        let py_list = PyList::new(py, result);
        Ok(kot_list_class.call1((py_list,))?.into_py(py))
    }

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

// Mutable list iterator
#[pyclass]
pub struct MutableListIterator {
    elements: Vec<PyObject>,
    element_type: Option<PyObject>,
    cursor: usize,
    last_returned: isize,
}

impl MutableListIterator {
    fn new(elements: Vec<PyObject>, element_type: Option<PyObject>, index: usize) -> Self {
        MutableListIterator {
            elements,
            element_type,
            cursor: index,
            last_returned: -1,
        }
    }
}

#[pymethods]
impl MutableListIterator {
    fn has_next(&self) -> bool {
        self.cursor < self.elements.len()
    }

    fn next(&mut self, py: Python<'_>) -> PyResult<PyObject> {
        if !self.has_next() {
            return Err(PyRuntimeError::new_err("No more elements"));
        }
        let element = self.elements[self.cursor].clone_ref(py);
        self.last_returned = self.cursor as isize;
        self.cursor += 1;
        Ok(element)
    }

    fn has_previous(&self) -> bool {
        self.cursor > 0
    }

    fn previous(&mut self, py: Python<'_>) -> PyResult<PyObject> {
        if !self.has_previous() {
            return Err(PyRuntimeError::new_err("No previous elements"));
        }
        self.cursor -= 1;
        let element = self.elements[self.cursor].clone_ref(py);
        self.last_returned = self.cursor as isize;
        Ok(element)
    }

    fn next_index(&self) -> usize {
        self.cursor
    }

    fn previous_index(&self) -> isize {
        self.cursor as isize - 1
    }

    fn add(&mut self, py: Python<'_>, element: &PyAny) -> PyResult<()> {
        let obj = element.into_py(py);
        self.elements.insert(self.cursor, obj);
        self.cursor += 1;
        self.last_returned = -1;
        Ok(())
    }

    fn remove(&mut self) -> PyResult<()> {
        if self.last_returned < 0 {
            return Err(PyRuntimeError::new_err("No element to remove (call next() or previous() first)"));
        }

        self.elements.remove(self.last_returned as usize);

        if (self.last_returned as usize) < self.cursor {
            self.cursor -= 1;
        }

        self.last_returned = -1;
        Ok(())
    }

    fn set(&mut self, py: Python<'_>, element: &PyAny) -> PyResult<()> {
        if self.last_returned < 0 {
            return Err(PyRuntimeError::new_err("No element to set (call next() or previous() first)"));
        }

        self.elements[self.last_returned as usize] = element.into_py(py);
        Ok(())
    }

    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(&mut self, py: Python<'_>) -> Option<PyObject> {
        if self.has_next() {
            self.next(py).ok()
        } else {
            None
        }
    }
}

// Simple iterator for KotMutableList
#[pyclass]
pub struct KotMutableListIterator {
    elements: Vec<PyObject>,
    index: usize,
}

#[pymethods]
impl KotMutableListIterator {
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
