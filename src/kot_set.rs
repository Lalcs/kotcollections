use pyo3::prelude::*;
use pyo3::types::{PyList, PySet, PyDict, PyTuple, PyType};
use pyo3::exceptions::{PyIndexError, PyValueError, PyTypeError};

/// A read-only set implementation that reproduces Kotlin's Set interface.
#[pyclass(subclass)]
#[derive(Clone)]
pub struct KotSet {
    elements: Vec<PyObject>,  // We use Vec to maintain insertion order
    element_type: Option<PyObject>,
}

impl KotSet {
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
                    "KotSet expected element of type {}, got {}",
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
        KotSet { elements, element_type }
    }

    pub fn get_elements(&self) -> &Vec<PyObject> {
        &self.elements
    }
}

#[pymethods]
impl KotSet {
    #[new]
    #[pyo3(signature = (elements=None))]
    fn new(py: Python<'_>, elements: Option<&PyAny>) -> PyResult<Self> {
        let mut set = KotSet {
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
        let mut set = KotSet {
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
        Ok(format!("KotSet({{{}}})", items.join(", ")))
    }

    fn __str__(&self, py: Python<'_>) -> PyResult<String> {
        let items: Vec<String> = self.elements.iter()
            .map(|e| e.as_ref(py).str().map(|s| s.to_string()).unwrap_or_else(|_| "?".to_string()))
            .collect();
        Ok(format!("{{{}}}", items.join(", ")))
    }

    fn __eq__(&self, py: Python<'_>, other: &PyAny) -> PyResult<bool> {
        if let Ok(other_set) = other.extract::<PyRef<KotSet>>() {
            if self.elements.len() != other_set.elements.len() {
                return Ok(false);
            }
            for elem in &self.elements {
                let mut found = false;
                for other_elem in &other_set.elements {
                    if elem.as_ref(py).eq(other_elem.as_ref(py))? {
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

    fn __hash__(&self, py: Python<'_>) -> PyResult<isize> {
        let mut hash: isize = 0;
        for elem in &self.elements {
            hash = hash.wrapping_add(elem.as_ref(py).hash()? as isize);
        }
        Ok(hash)
    }

    fn __iter__(&self, py: Python<'_>) -> PyResult<Py<KotSetIterator>> {
        Py::new(py, KotSetIterator {
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

    // Basic methods
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
            if !self.contains_element(py, item)? {
                return Ok(false);
            }
        }
        Ok(true)
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

    fn first_predicate(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<PyObject> {
        for element in &self.elements {
            let result = predicate.call1((element.as_ref(py),))?;
            if result.is_true()? {
                return Ok(element.clone_ref(py));
            }
        }
        Err(PyValueError::new_err("No element matching predicate found"))
    }

    fn first_or_null_predicate(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<Option<PyObject>> {
        for element in &self.elements {
            let result = predicate.call1((element.as_ref(py),))?;
            if result.is_true()? {
                return Ok(Some(element.clone_ref(py)));
            }
        }
        Ok(None)
    }

    fn first_or_none_predicate(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<Option<PyObject>> {
        self.first_or_null_predicate(py, predicate)
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

    fn single(&self, py: Python<'_>) -> PyResult<PyObject> {
        if self.elements.is_empty() {
            return Err(PyValueError::new_err("Set is empty"));
        }
        if self.elements.len() > 1 {
            return Err(PyValueError::new_err("Set has more than one element"));
        }
        Ok(self.elements[0].clone_ref(py))
    }

    fn single_or_null(&self, py: Python<'_>) -> Option<PyObject> {
        if self.elements.len() == 1 {
            Some(self.elements[0].clone_ref(py))
        } else {
            None
        }
    }

    fn single_or_none(&self, py: Python<'_>) -> Option<PyObject> {
        self.single_or_null(py)
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

    fn map_not_null(&self, py: Python<'_>, transform: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_list_class = module.getattr("KotList")?;

        let mut result = Vec::new();
        for element in &self.elements {
            let transformed = transform.call1((element.as_ref(py),))?;
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
        for element in &self.elements {
            let transformed = transform.call1((element.as_ref(py),))?;
            let iter = transformed.iter()?;
            for item in iter {
                result.push(item?);
            }
        }

        let py_list = PyList::new(py, result);
        Ok(kot_list_class.call1((py_list,))?.into_py(py))
    }

    // Filter methods
    fn filter(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<KotSet> {
        let mut result = Vec::new();
        for element in &self.elements {
            let keep = predicate.call1((element.as_ref(py),))?;
            if keep.is_true()? {
                result.push(element.clone_ref(py));
            }
        }
        Ok(KotSet::new_with_type(result, self.element_type.clone()))
    }

    fn filter_not(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<KotSet> {
        let mut result = Vec::new();
        for element in &self.elements {
            let keep = predicate.call1((element.as_ref(py),))?;
            if !keep.is_true()? {
                result.push(element.clone_ref(py));
            }
        }
        Ok(KotSet::new_with_type(result, self.element_type.clone()))
    }

    fn filter_not_null(&self, py: Python<'_>) -> KotSet {
        let result: Vec<PyObject> = self.elements.iter()
            .filter(|e| !e.as_ref(py).is_none())
            .map(|e| e.clone_ref(py))
            .collect();
        KotSet::new_with_type(result, self.element_type.clone())
    }

    fn filter_not_none(&self, py: Python<'_>) -> KotSet {
        self.filter_not_null(py)
    }

    fn filter_is_instance(&self, py: Python<'_>, klass: &PyType) -> PyResult<KotSet> {
        let mut result = Vec::new();
        for element in &self.elements {
            if element.as_ref(py).is_instance(klass)? {
                result.push(element.clone_ref(py));
            }
        }
        Ok(KotSet::new_with_type(result, None))
    }

    fn partition(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<(KotSet, KotSet)> {
        let mut matching = Vec::new();
        let mut non_matching = Vec::new();

        for element in &self.elements {
            let result = predicate.call1((element.as_ref(py),))?;
            if result.is_true()? {
                matching.push(element.clone_ref(py));
            } else {
                non_matching.push(element.clone_ref(py));
            }
        }

        Ok((
            KotSet::new_with_type(matching, self.element_type.clone()),
            KotSet::new_with_type(non_matching, self.element_type.clone())
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
            return Err(PyValueError::new_err("Set is empty"));
        }

        let builtins = py.import("builtins")?;
        let max_fn = builtins.getattr("max")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        Ok(max_fn.call1((py_list,))?.into_py(py))
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
            return Err(PyValueError::new_err("Set is empty"));
        }

        let builtins = py.import("builtins")?;
        let min_fn = builtins.getattr("min")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        Ok(min_fn.call1((py_list,))?.into_py(py))
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
            return Err(PyValueError::new_err("Cannot find max of empty set"));
        }

        let builtins = py.import("builtins")?;
        let max_fn = builtins.getattr("max")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        let kwargs = PyDict::new(py);
        kwargs.set_item("key", selector)?;
        Ok(max_fn.call((py_list,), Some(kwargs))?.into_py(py))
    }

    fn min_by(&self, py: Python<'_>, selector: &PyAny) -> PyResult<PyObject> {
        if self.elements.is_empty() {
            return Err(PyValueError::new_err("Cannot find min of empty set"));
        }

        let builtins = py.import("builtins")?;
        let min_fn = builtins.getattr("min")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        let kwargs = PyDict::new(py);
        kwargs.set_item("key", selector)?;
        Ok(min_fn.call((py_list,), Some(kwargs))?.into_py(py))
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

    // Set operations
    fn intersect(&self, py: Python<'_>, other: &PyAny) -> PyResult<KotSet> {
        let mut other_elements = Vec::new();
        for item in other.iter()? {
            other_elements.push(item?.into_py(py));
        }

        let mut result = Vec::new();
        for element in &self.elements {
            for other_elem in &other_elements {
                if element.as_ref(py).eq(other_elem.as_ref(py))? {
                    result.push(element.clone_ref(py));
                    break;
                }
            }
        }

        Ok(KotSet::new_with_type(result, self.element_type.clone()))
    }

    fn union(&self, py: Python<'_>, other: &PyAny) -> PyResult<KotSet> {
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

        Ok(KotSet::new_with_type(result, self.element_type.clone()))
    }

    fn subtract(&self, py: Python<'_>, other: &PyAny) -> PyResult<KotSet> {
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
                result.push(element.clone_ref(py));
            }
        }

        Ok(KotSet::new_with_type(result, self.element_type.clone()))
    }

    fn plus(&self, py: Python<'_>, element: &PyAny) -> PyResult<KotSet> {
        let mut result: Vec<PyObject> = self.elements.iter().map(|e| e.clone_ref(py)).collect();

        // Check if element is iterable (but not string or bytes)
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

        Ok(KotSet::new_with_type(result, self.element_type.clone()))
    }

    fn minus(&self, py: Python<'_>, element: &PyAny) -> PyResult<KotSet> {
        let mut to_remove = Vec::new();

        // Check if element is iterable (but not string or bytes)
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
                result.push(elem.clone_ref(py));
            }
        }

        Ok(KotSet::new_with_type(result, self.element_type.clone()))
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

    fn reduce_or_null(&self, py: Python<'_>, operation: &PyAny) -> PyResult<Option<PyObject>> {
        if self.elements.is_empty() {
            return Ok(None);
        }
        Ok(Some(self.reduce(py, operation)?))
    }

    fn reduce_or_none(&self, py: Python<'_>, operation: &PyAny) -> PyResult<Option<PyObject>> {
        self.reduce_or_null(py, operation)
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

    fn on_each(&self, py: Python<'_>, action: &PyAny) -> PyResult<KotSet> {
        for element in &self.elements {
            action.call1((element.as_ref(py),))?;
        }
        Ok(self.clone())
    }

    // Sorting methods
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

    fn sorted_descending(&self, py: Python<'_>) -> PyResult<PyObject> {
        self.sorted(py, None, true)
    }

    fn sorted_by(&self, py: Python<'_>, selector: &PyAny) -> PyResult<PyObject> {
        self.sorted(py, Some(selector), false)
    }

    fn sorted_by_descending(&self, py: Python<'_>, selector: &PyAny) -> PyResult<PyObject> {
        self.sorted(py, Some(selector), true)
    }

    // Grouping methods
    fn group_by(&self, py: Python<'_>, key_selector: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_map_class = module.getattr("KotMap")?;
        let kot_list_class = module.getattr("KotList")?;

        let dict = PyDict::new(py);
        for element in &self.elements {
            let elem = element.as_ref(py);
            let key = key_selector.call1((elem,))?;

            if let Ok(Some(list)) = dict.get_item(key) {
                let list = list.downcast::<PyList>()?;
                list.append(elem)?;
            } else {
                let list = PyList::new(py, &[elem]);
                dict.set_item(key, list)?;
            }
        }

        // Convert lists to KotLists
        let result_dict = PyDict::new(py);
        for (key, value) in dict.iter() {
            let kot_list = kot_list_class.call1((value,))?;
            result_dict.set_item(key, kot_list)?;
        }

        Ok(kot_map_class.call1((result_dict,))?.into_py(py))
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

    fn to_kot_set(&self, py: Python<'_>) -> KotSet {
        KotSet::new_with_type(
            self.elements.iter().map(|e| e.clone_ref(py)).collect(),
            self.element_type.clone()
        )
    }

    fn to_kot_mutable_set(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let class = module.getattr("KotMutableSet")?;
        let py_list = PyList::new(py, self.elements.iter().map(|e| e.as_ref(py)));
        Ok(class.call1((py_list,))?.into_py(py))
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

        Ok(kot_map_class.call1((dict,))?.into_py(py))
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

        Ok(kot_map_class.call1((dict,))?.into_py(py))
    }

    // Zip methods
    fn zip(&self, py: Python<'_>, other: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_list_class = module.getattr("KotList")?;

        let mut result = Vec::new();
        let other_iter = other.iter()?;

        for (a, b) in self.elements.iter().zip(other_iter) {
            let b = b?;
            let tuple = PyTuple::new(py, &[a.as_ref(py), b]);
            result.push(tuple);
        }

        let py_list = PyList::new(py, result);
        Ok(kot_list_class.call1((py_list,))?.into_py(py))
    }

    // Take/Drop methods
    fn take(&self, py: Python<'_>, n: usize) -> PyResult<KotSet> {
        let elements: Vec<PyObject> = self.elements.iter()
            .take(n)
            .map(|e| e.clone_ref(py))
            .collect();
        Ok(KotSet::new_with_type(elements, self.element_type.clone()))
    }

    fn drop(&self, py: Python<'_>, n: usize) -> PyResult<KotSet> {
        let elements: Vec<PyObject> = self.elements.iter()
            .skip(n)
            .map(|e| e.clone_ref(py))
            .collect();
        Ok(KotSet::new_with_type(elements, self.element_type.clone()))
    }

    // Random methods
    #[pyo3(signature = (random_instance=None))]
    fn random(&self, py: Python<'_>, random_instance: Option<&PyAny>) -> PyResult<PyObject> {
        if self.elements.is_empty() {
            return Err(PyIndexError::new_err("Set is empty"));
        }

        let random_module = py.import("random")?;
        let index: usize = if let Some(rng) = random_instance {
            rng.call_method1("randint", (0, self.elements.len() - 1))?.extract()?
        } else {
            random_module.call_method1("randint", (0, self.elements.len() - 1))?.extract()?
        };

        Ok(self.elements[index].clone_ref(py))
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

    // Find methods
    fn find(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<Option<PyObject>> {
        self.first_or_null_predicate(py, predicate)
    }

    // Utility methods
    fn if_empty(&self, py: Python<'_>, default_value: &PyAny) -> PyResult<PyObject> {
        if self.elements.is_empty() {
            Ok(default_value.call0()?.into_py(py))
        } else {
            Ok(self.clone().into_py(py))
        }
    }
}

// Iterator for KotSet
#[pyclass]
pub struct KotSetIterator {
    elements: Vec<PyObject>,
    index: usize,
}

#[pymethods]
impl KotSetIterator {
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
