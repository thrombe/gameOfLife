/*
byte = 0000_0000 -> right 4 save neigh count, 5th stores cell state
for each generation:
  . read the 4 bits, set cell state, set cell in board, 
    reset cell (set state and AND with 0b0001_0000)
  . save live indices and then -1 to stop
    . try eliminating this and directly use the cells for this. ie, if dead, continue
  . 
*/

use ncurses;

use super::{WIDTH, HEIGHT, TORUS, NCURSED, LOOPS};

pub const ISHTOP: usize = !1 + 1; // -1

// run game of life
pub fn gol() {
    let mut cells = [[0u8; WIDTH]; HEIGHT];
    let mut board = [b' '; (WIDTH+1)*HEIGHT];
    init_board(&mut board); // sets the b'\n'
    let mut indices = [(ISHTOP, ISHTOP); WIDTH*HEIGHT];

    draw_structure(2, 15, 15, &mut cells, &mut indices);
    if NCURSED {
        ncurses::initscr();
        ncurses::curs_set(ncurses::CURSOR_VISIBILITY::CURSOR_INVISIBLE);
    }
    print_reset(&mut cells, &mut indices, &mut board);
    for _ in 0..LOOPS {
        cells_set(&mut cells, &indices);
        print_reset(&mut cells, &mut indices, &mut board);
    }
    if NCURSED {ncurses::endwin();}
}

// ishtop is equivalent to -1 when added with another no (with wrapping)
const AROUND: [(usize, usize); 8] = [(ISHTOP, ISHTOP), (0, ISHTOP), (1, ISHTOP), (1, 0), (1, 1), (0, 1), (ISHTOP, 1), (ISHTOP, 0)];

// cell++ for every neighbor or alive cells
#[inline(always)]
pub fn cells_set(cells: &mut [[u8; WIDTH]; HEIGHT], indices: &[(usize, usize)]) {
    for &i in indices.iter() {
        if i.0 == ISHTOP {break} // end of live cells
        for (ai, aj) in AROUND.iter() { // go around i and do ++ (torus)
            set_cell(cells, i.0.wrapping_add(*ai), i.1.wrapping_add(*aj));
        }
    }
}

#[inline(always)]
fn set_cell(cells: &mut [[u8; WIDTH]; HEIGHT], mut x: usize, mut y: usize) {
    if !TORUS & ((x > WIDTH) | (y > HEIGHT)) {return} // hard borders

    // torus
    if x == WIDTH {x = 0; // wrap from right
    } else if x == ISHTOP {x = WIDTH-1} // wrap from left
    if y == HEIGHT {y = 0; // wrap from below
    } else if y == ISHTOP {y = HEIGHT-1} // wrap from top    }
    cells[y][x] += 0b0000_0001;
}

// sets board and resets cells for next generation
#[inline(always)]
fn print_reset(cells: &mut [[u8; WIDTH]; HEIGHT], indices: &mut [(usize, usize)], board: &mut [u8]) {
    let mut i_indices: usize = 0;
    let mut i_board: usize = 0;
    for i_cells_y in 0..HEIGHT {
        for i_cells_x in 0..WIDTH {
            match cells[i_cells_y][i_cells_x] { // set cell
                // checking alivecount
                3 | 18 | 19 => { // come alive if 3 (stay alive if 2 or 3)
                    cells[i_cells_y][i_cells_x] = 0b0001_0000;
                    indices[i_indices] = (i_cells_x, i_cells_y);
                    i_indices += 1;
                    board_set(&mut i_board, board, b'x');
                }
                _ => { // else dead
                    cells[i_cells_y][i_cells_x] = 0b0000_0000;
                    board_set(&mut i_board, board, b' ');
                }
            }
            i_board += 1;
        }
    }
    indices[i_indices] = (ISHTOP, 0); // will crash if every cell is alive but whatever
    
    if NCURSED {
        ncurses::erase(); // seems like this is the slowest part of the code
        ncurses::addstr(std::str::from_utf8(&board).unwrap());
        ncurses::refresh();
    } else {
        println!("{}", std::str::from_utf8(&board).unwrap());
    }
}

// sets value to board cells
#[inline(always)]
pub fn board_set(i: &mut usize, board: &mut [u8], val: u8) {
    if board[*i] == b'\n' {*i += 1}
    board[*i] = val;
}

// sets b'\n' at correct places
pub fn init_board(board: &mut [u8]) {
    let mut offset = 0;
    for i in 1..=HEIGHT {
        board[i*WIDTH + offset] = b'\n';
        offset += 1;
    }
}

// randomise initial stste of board
fn draw_line(cells: &mut [[u8; WIDTH]; HEIGHT], indices: &mut [(usize, usize)]) {
    let mut i_indices: usize = 0;
    for j in 0..HEIGHT {
        for i in 0..WIDTH {
            if i != 50 {continue}
            cells[j][i] = 0b0001_0010;
            indices[i_indices] = (i, j);
            i_indices += 1;
        }
    }
    indices[i_indices] = (ISHTOP, 0);
}

use crate::import_structure;
pub fn draw_structure(num:usize, xoff: usize, yoff: usize,  cells: &mut [[u8; WIDTH]; HEIGHT], indices: &mut [(usize, usize)]) {
    if num == 0 {draw_line(cells, indices)}

    let mut i_indices: usize = 0;
    for (x, y) in import_structure::from_py_structure(num).iter() { // will crash other parts if it goes outside bordrs
        cells[*y+yoff][*x+xoff] = 0b0001_0010;
        indices[i_indices] = (*x+xoff, *y+yoff);
        i_indices += 1;
    }
    indices[i_indices] = (ISHTOP, 0);
}