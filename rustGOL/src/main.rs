
mod gol;
use std::time;

fn main() {
    let now = time::Instant::now();
    gol::gol();
    println!("{:?}", now.elapsed());
}
