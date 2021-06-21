#![allow(dead_code)]
#![allow(non_snake_case)]
// #![allow(unused_assignments)]

mod gol;
mod bbrain;
mod import_structure;
use std::time;

fn main() {
    let now = time::Instant::now();
    // gol::gol();
    bbrain::bbrain();
    println!("{:?}", now.elapsed());
}

// fn main() {
//     println!("{:?}", import_structure::from_py_structure(4))
// }