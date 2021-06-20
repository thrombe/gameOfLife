
mod gol;
mod import_structure;
use std::time;

fn main() {
    let now = time::Instant::now();
    gol::gol();
    println!("{:?}", now.elapsed());
}

// fn main() {
//     println!("{:?}", import_structure::from_py_structure(4))
// }