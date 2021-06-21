#![allow(dead_code)]
#![allow(non_snake_case)]
// #![allow(unused_assignments)]

mod gol;
mod bbrain;
mod import_structure;
use std::time;

pub const WIDTH: usize = 151;
pub const HEIGHT: usize = 160;
pub const TORUS: bool = true;
pub const NCURSED: bool = true;
pub const LOOPS: usize = 200;

fn main() {
    let now = time::Instant::now();
    gol::gol();
    // bbrain::bbrain();
    println!("{:?}", now.elapsed());
}
