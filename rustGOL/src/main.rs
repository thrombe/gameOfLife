#![allow(dead_code)]
#![allow(non_snake_case)]
// #![allow(unused_assignments)]

mod gol;
mod bbrain;
mod import_structure;
use std::time;

const WIDTH: usize = 151;
const HEIGHT: usize = 160;
const TORUS: bool = true;
const NCURSED: bool = true;
const LOOPS: usize = 200;

fn main() {
    let now = time::Instant::now();
    gol::gol();
    // bbrain::bbrain();
    println!("{:?}", now.elapsed());
}
