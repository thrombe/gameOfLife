// this file is for importing structures from files and converting to whatever format required

use serde_json::{from_str};
use std::fs::read_to_string;

// imports from file but does so with sorting. so its alphabetic order
pub fn from_py_structure(args: Vec<String>, mut num: usize) -> Vec<(usize, usize)> {
    let path = "../structures.txt";
    let file_data: serde_json::Value = from_str(&read_to_string(path).unwrap()).unwrap();


    // this stuff is a hot mess. ew
    let mut kee = String::new(); // trying to find key in args
    if args.len() > 3 {
        kee = match args[3].parse() {
            Ok(val) => {
                num = val;
                String::new()
            },    
            Err(_) => String::from(&args[3]),
        }        
    }
    let mut keys: Vec<&String> = Vec::new();
    let mut i = 0; // finding key for num
    for (key, _) in file_data.as_object().unwrap().iter() {
        if i == num && kee == String::new() {
            kee = String::from(key);
            break
        }
        keys.append(&mut vec!(key));
        i += 1;
    }
    if kee == String::new() {panic!("wrong structure index {:?}", keys)}



    let mut indices: Vec<(usize, usize)> = Vec::new();
    let mut x: usize;
    let mut y: usize;
    for val in file_data[kee].as_array().expect(&format!("wrong structure key {:?}", keys)).iter() {
        let coords: Vec<&str> = val.as_str().unwrap().split(";").collect();
        x = coords[0].parse().unwrap();
        y = coords[1].parse().unwrap();
        indices.append(&mut vec!((x, y)));
    }

    indices
}
