// this file is for importing structures from files and converting to whatever format required

use serde_json::{from_str};
use std::fs::read_to_string;

// imports from file but does so with sorting. so its alphabetic order
#[allow(unused_assignments)]
pub fn from_py_structure(num: usize) -> Vec<(usize, usize)> {
    let path = "../structures.txt";
    let file_data: serde_json::Value = from_str(&read_to_string(path).unwrap()).unwrap();

    let mut i = 0; // finding key for num
    let mut kee = &String::new();
    for (key, _) in file_data.as_object().unwrap().iter() {
        if i == num {
            kee = key;
            break
        }
        i += 1;
    }

    let mut indices: Vec<(usize, usize)> = Vec::new();
    let mut x: usize = 0;
    let mut y: usize = 0;
    for val in file_data[kee].as_array().unwrap().iter() {
        let coords: Vec<&str> = val.as_str().unwrap().split(";").collect();
        x = coords[0].parse().unwrap();
        y = coords[1].parse().unwrap();
        indices.append(&mut vec!((x, y)));
    }

    indices
}
