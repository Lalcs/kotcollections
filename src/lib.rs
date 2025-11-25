use pyo3::prelude::*;

mod kot_list;
mod kot_mutable_list;
mod kot_set;
mod kot_mutable_set;
mod kot_map;
mod kot_mutable_map;
mod kot_grouping;

use kot_list::KotList;
use kot_mutable_list::KotMutableList;
use kot_set::KotSet;
use kot_mutable_set::KotMutableSet;
use kot_map::KotMap;
use kot_mutable_map::KotMutableMap;
use kot_grouping::KotGrouping;

/// A Python module implemented in Rust.
#[pymodule]
fn _kotcollections(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<KotList>()?;
    m.add_class::<KotMutableList>()?;
    m.add_class::<KotSet>()?;
    m.add_class::<KotMutableSet>()?;
    m.add_class::<KotMap>()?;
    m.add_class::<KotMutableMap>()?;
    m.add_class::<KotGrouping>()?;
    Ok(())
}
