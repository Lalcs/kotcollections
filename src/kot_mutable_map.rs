use pyo3::prelude::*;
use pyo3::types::{PyList, PyDict, PyTuple, PyType};
use pyo3::exceptions::PyKeyError;

/// A mutable map implementation that reproduces Kotlin's MutableMap interface.
#[pyclass(subclass)]
#[derive(Clone)]
pub struct KotMutableMap {
    keys: Vec<PyObject>,
    values: Vec<PyObject>,
    key_type: Option<PyObject>,
    value_type: Option<PyObject>,
}

impl KotMutableMap {
    fn find_key_index(&self, py: Python<'_>, key: &PyAny) -> PyResult<Option<usize>> {
        for (i, k) in self.keys.iter().enumerate() {
            if k.as_ref(py).eq(key)? {
                return Ok(Some(i));
            }
        }
        Ok(None)
    }

    pub fn new_with_types(
        keys: Vec<PyObject>,
        values: Vec<PyObject>,
        key_type: Option<PyObject>,
        value_type: Option<PyObject>,
    ) -> Self {
        KotMutableMap { keys, values, key_type, value_type }
    }
}

#[pymethods]
impl KotMutableMap {
    #[new]
    #[pyo3(signature = (elements=None))]
    fn new(py: Python<'_>, elements: Option<&PyAny>) -> PyResult<Self> {
        let mut map = KotMutableMap {
            keys: Vec::new(),
            values: Vec::new(),
            key_type: None,
            value_type: None,
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

    #[classmethod]
    fn of_types(
        _cls: &PyType,
        py: Python<'_>,
        key_type: &PyType,
        value_type: &PyType,
        elements: Option<&PyAny>,
    ) -> PyResult<Self> {
        let mut map = KotMutableMap {
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
        Ok(format!("KotMutableMap({{{}}})", items.join(", ")))
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

    fn __iter__(&self, py: Python<'_>) -> PyResult<Py<KotMutableMapKeyIterator>> {
        Py::new(py, KotMutableMapKeyIterator {
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

    fn __setitem__(&mut self, py: Python<'_>, key: &PyAny, value: &PyAny) -> PyResult<()> {
        self.put(py, key, value)?;
        Ok(())
    }

    fn __delitem__(&mut self, py: Python<'_>, key: &PyAny) -> PyResult<()> {
        match self.find_key_index(py, key)? {
            Some(idx) => {
                self.keys.remove(idx);
                self.values.remove(idx);
                Ok(())
            }
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
        let kot_set_class = module.getattr("KotMutableSet")?;
        let py_list = PyList::new(py, self.keys.iter().map(|k| k.as_ref(py)));
        Ok(kot_set_class.call1((py_list,))?.into_py(py))
    }

    #[getter]
    fn values(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_list_class = module.getattr("KotMutableList")?;
        let py_list = PyList::new(py, self.values.iter().map(|v| v.as_ref(py)));
        Ok(kot_list_class.call1((py_list,))?.into_py(py))
    }

    #[getter]
    fn entries(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_set_class = module.getattr("KotMutableSet")?;

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

    // Mutable methods
    fn put(&mut self, py: Python<'_>, key: &PyAny, value: &PyAny) -> PyResult<Option<PyObject>> {
        let key_obj = key.into_py(py);
        let value_obj = value.into_py(py);

        match self.find_key_index(py, key)? {
            Some(idx) => {
                let old_value = self.values[idx].clone_ref(py);
                self.values[idx] = value_obj;
                Ok(Some(old_value))
            }
            None => {
                self.keys.push(key_obj);
                self.values.push(value_obj);
                Ok(None)
            }
        }
    }

    fn put_all(&mut self, py: Python<'_>, from: &PyAny) -> PyResult<()> {
        if let Ok(dict) = from.downcast::<PyDict>() {
            for (k, v) in dict.iter() {
                self.put(py, &k, &v)?;
            }
        } else if let Ok(map) = from.extract::<PyRef<KotMutableMap>>() {
            for (k, v) in map.keys.iter().zip(map.values.iter()) {
                let key = k.as_ref(py);
                let value = v.as_ref(py);
                match self.find_key_index(py, key)? {
                    Some(idx) => {
                        self.values[idx] = v.clone_ref(py);
                    }
                    None => {
                        self.keys.push(k.clone_ref(py));
                        self.values.push(v.clone_ref(py));
                    }
                }
            }
        } else {
            // Assume it's an iterable of (key, value) pairs
            let iter = from.iter()?;
            for item in iter {
                let item = item?;
                let key = item.get_item(0)?;
                let value = item.get_item(1)?;
                self.put(py, &key, &value)?;
            }
        }
        Ok(())
    }

    fn put_if_absent(&mut self, py: Python<'_>, key: &PyAny, value: &PyAny) -> PyResult<Option<PyObject>> {
        match self.find_key_index(py, key)? {
            Some(idx) => Ok(Some(self.values[idx].clone_ref(py))),
            None => {
                self.keys.push(key.into_py(py));
                self.values.push(value.into_py(py));
                Ok(None)
            }
        }
    }

    fn get_or_put(&mut self, py: Python<'_>, key: &PyAny, default_value: &PyAny) -> PyResult<PyObject> {
        match self.find_key_index(py, key)? {
            Some(idx) => Ok(self.values[idx].clone_ref(py)),
            None => {
                let value = default_value.call0()?.into_py(py);
                self.keys.push(key.into_py(py));
                self.values.push(value.clone_ref(py));
                Ok(value)
            }
        }
    }

    fn remove(&mut self, py: Python<'_>, key: &PyAny) -> PyResult<Option<PyObject>> {
        match self.find_key_index(py, key)? {
            Some(idx) => {
                self.keys.remove(idx);
                Ok(Some(self.values.remove(idx)))
            }
            None => Ok(None)
        }
    }

    fn remove_entry(&mut self, py: Python<'_>, key: &PyAny, value: &PyAny) -> PyResult<bool> {
        match self.find_key_index(py, key)? {
            Some(idx) => {
                if self.values[idx].as_ref(py).eq(value)? {
                    self.keys.remove(idx);
                    self.values.remove(idx);
                    Ok(true)
                } else {
                    Ok(false)
                }
            }
            None => Ok(false)
        }
    }

    fn clear(&mut self) {
        self.keys.clear();
        self.values.clear();
    }

    fn compute(&mut self, py: Python<'_>, key: &PyAny, remapping_function: &PyAny) -> PyResult<Option<PyObject>> {
        let current_value = match self.find_key_index(py, key)? {
            Some(idx) => Some(self.values[idx].clone_ref(py)),
            None => None
        };

        let new_value = remapping_function.call1((key, current_value.as_ref().map(|v| v.as_ref(py))))?;

        if new_value.is_none() {
            // Remove the entry if the new value is None
            if let Some(idx) = self.find_key_index(py, key)? {
                self.keys.remove(idx);
                self.values.remove(idx);
            }
            Ok(None)
        } else {
            // Update or insert
            match self.find_key_index(py, key)? {
                Some(idx) => {
                    self.values[idx] = new_value.into_py(py);
                    Ok(Some(self.values[idx].clone_ref(py)))
                }
                None => {
                    self.keys.push(key.into_py(py));
                    self.values.push(new_value.into_py(py));
                    Ok(Some(self.values.last().unwrap().clone_ref(py)))
                }
            }
        }
    }

    fn compute_if_absent(&mut self, py: Python<'_>, key: &PyAny, mapping_function: &PyAny) -> PyResult<PyObject> {
        match self.find_key_index(py, key)? {
            Some(idx) => Ok(self.values[idx].clone_ref(py)),
            None => {
                let value = mapping_function.call1((key,))?.into_py(py);
                self.keys.push(key.into_py(py));
                self.values.push(value.clone_ref(py));
                Ok(value)
            }
        }
    }

    fn compute_if_present(&mut self, py: Python<'_>, key: &PyAny, remapping_function: &PyAny) -> PyResult<Option<PyObject>> {
        match self.find_key_index(py, key)? {
            Some(idx) => {
                let current_value = self.values[idx].as_ref(py);
                let new_value = remapping_function.call1((key, current_value))?;

                if new_value.is_none() {
                    self.keys.remove(idx);
                    self.values.remove(idx);
                    Ok(None)
                } else {
                    self.values[idx] = new_value.into_py(py);
                    Ok(Some(self.values[idx].clone_ref(py)))
                }
            }
            None => Ok(None)
        }
    }

    fn merge(&mut self, py: Python<'_>, key: &PyAny, value: &PyAny, remapping_function: &PyAny) -> PyResult<Option<PyObject>> {
        match self.find_key_index(py, key)? {
            Some(idx) => {
                let current_value = self.values[idx].as_ref(py);
                let new_value = remapping_function.call1((current_value, value))?;

                if new_value.is_none() {
                    self.keys.remove(idx);
                    self.values.remove(idx);
                    Ok(None)
                } else {
                    self.values[idx] = new_value.into_py(py);
                    Ok(Some(self.values[idx].clone_ref(py)))
                }
            }
            None => {
                self.keys.push(key.into_py(py));
                self.values.push(value.into_py(py));
                Ok(Some(self.values.last().unwrap().clone_ref(py)))
            }
        }
    }

    fn replace(&mut self, py: Python<'_>, key: &PyAny, value: &PyAny) -> PyResult<Option<PyObject>> {
        match self.find_key_index(py, key)? {
            Some(idx) => {
                let old_value = self.values[idx].clone_ref(py);
                self.values[idx] = value.into_py(py);
                Ok(Some(old_value))
            }
            None => Ok(None)
        }
    }

    fn replace_entry(&mut self, py: Python<'_>, key: &PyAny, old_value: &PyAny, new_value: &PyAny) -> PyResult<bool> {
        match self.find_key_index(py, key)? {
            Some(idx) => {
                if self.values[idx].as_ref(py).eq(old_value)? {
                    self.values[idx] = new_value.into_py(py);
                    Ok(true)
                } else {
                    Ok(false)
                }
            }
            None => Ok(false)
        }
    }

    fn replace_all(&mut self, py: Python<'_>, function: &PyAny) -> PyResult<()> {
        for i in 0..self.keys.len() {
            let key = self.keys[i].as_ref(py);
            let value = self.values[i].as_ref(py);
            let new_value = function.call1((key, value))?;
            self.values[i] = new_value.into_py(py);
        }
        Ok(())
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

    fn map_keys(&self, py: Python<'_>, transform: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_map_class = module.getattr("KotMap")?;

        let dict = PyDict::new(py);
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            let new_key = transform.call1((entry,))?;
            dict.set_item(new_key, v.as_ref(py))?;
        }

        Ok(kot_map_class.call1((dict,))?.into_py(py))
    }

    fn map_values(&self, py: Python<'_>, transform: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_map_class = module.getattr("KotMap")?;

        let dict = PyDict::new(py);
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            let new_value = transform.call1((entry,))?;
            dict.set_item(k.as_ref(py), new_value)?;
        }

        Ok(kot_map_class.call1((dict,))?.into_py(py))
    }

    // Filter methods
    fn filter(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_map_class = module.getattr("KotMap")?;

        let dict = PyDict::new(py);
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            let keep = predicate.call1((entry,))?;
            if keep.is_true()? {
                dict.set_item(k.as_ref(py), v.as_ref(py))?;
            }
        }

        Ok(kot_map_class.call1((dict,))?.into_py(py))
    }

    fn filter_keys(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_map_class = module.getattr("KotMap")?;

        let dict = PyDict::new(py);
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let keep = predicate.call1((k.as_ref(py),))?;
            if keep.is_true()? {
                dict.set_item(k.as_ref(py), v.as_ref(py))?;
            }
        }

        Ok(kot_map_class.call1((dict,))?.into_py(py))
    }

    fn filter_values(&self, py: Python<'_>, predicate: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_map_class = module.getattr("KotMap")?;

        let dict = PyDict::new(py);
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let keep = predicate.call1((v.as_ref(py),))?;
            if keep.is_true()? {
                dict.set_item(k.as_ref(py), v.as_ref(py))?;
            }
        }

        Ok(kot_map_class.call1((dict,))?.into_py(py))
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

    // ForEach methods
    fn for_each(&self, py: Python<'_>, action: &PyAny) -> PyResult<()> {
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let entry = PyTuple::new(py, &[k.as_ref(py), v.as_ref(py)]);
            action.call1((entry,))?;
        }
        Ok(())
    }

    // Plus/Minus operations (return new maps like KotMap)
    fn plus(&self, py: Python<'_>, other: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_map_class = module.getattr("KotMap")?;

        let dict = PyDict::new(py);
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            dict.set_item(k.as_ref(py), v.as_ref(py))?;
        }

        if let Ok(other_dict) = other.downcast::<PyDict>() {
            for (k, v) in other_dict.iter() {
                dict.set_item(k, v)?;
            }
        } else {
            // Assume it's a tuple (key, value)
            let key = other.get_item(0)?;
            let value = other.get_item(1)?;
            dict.set_item(key, value)?;
        }

        Ok(kot_map_class.call1((dict,))?.into_py(py))
    }

    fn minus(&self, py: Python<'_>, keys_to_remove: &PyAny) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let kot_map_class = module.getattr("KotMap")?;

        let mut remove_keys = Vec::new();

        if keys_to_remove.is_instance_of::<pyo3::types::PyString>() {
            remove_keys.push(keys_to_remove.into_py(py));
        } else if let Ok(iter) = keys_to_remove.iter() {
            for item in iter {
                remove_keys.push(item?.into_py(py));
            }
        } else {
            remove_keys.push(keys_to_remove.into_py(py));
        }

        let dict = PyDict::new(py);
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            let mut should_remove = false;
            for rk in &remove_keys {
                if k.as_ref(py).eq(rk.as_ref(py))? {
                    should_remove = true;
                    break;
                }
            }
            if !should_remove {
                dict.set_item(k.as_ref(py), v.as_ref(py))?;
            }
        }

        Ok(kot_map_class.call1((dict,))?.into_py(py))
    }

    // Conversion methods
    fn to_dict(&self, py: Python<'_>) -> PyResult<Py<PyDict>> {
        let dict = PyDict::new(py);
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            dict.set_item(k.as_ref(py), v.as_ref(py))?;
        }
        Ok(dict.into())
    }

    fn to_kot_map(&self, py: Python<'_>) -> PyResult<PyObject> {
        let module = py.import("kotcollections")?;
        let class = module.getattr("KotMap")?;
        let dict = PyDict::new(py);
        for (k, v) in self.keys.iter().zip(self.values.iter()) {
            dict.set_item(k.as_ref(py), v.as_ref(py))?;
        }
        Ok(class.call1((dict,))?.into_py(py))
    }

    fn to_kot_mutable_map(&self, py: Python<'_>) -> KotMutableMap {
        KotMutableMap::new_with_types(
            self.keys.iter().map(|k| k.clone_ref(py)).collect(),
            self.values.iter().map(|v| v.clone_ref(py)).collect(),
            self.key_type.clone(),
            self.value_type.clone()
        )
    }
}

// Key iterator for KotMutableMap
#[pyclass]
pub struct KotMutableMapKeyIterator {
    keys: Vec<PyObject>,
    index: usize,
}

#[pymethods]
impl KotMutableMapKeyIterator {
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
