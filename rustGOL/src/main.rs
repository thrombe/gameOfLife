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

use std::env;

fn main() {
    let now = time::Instant::now();

    // check and do stuff with command line arguments
    let args: Vec<String> = env::args().collect();
    if args.len() > 1 {
        match &args[1][..] {
            "gol" => gol::gol(args),
            "bbrain" => bbrain::bbrain(args),
            _ => println!("[what to run(gol, bbrain), how many loops, what structure to import(name/num), xoffset, yoffset]"),
        }
    } else {gol::gol(args)}

    println!("{:?}", now.elapsed());
}
