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

const WIDTH: usize = 151;
const HEIGHT: usize = 160;
const TORUS: bool = true;

const ISHTOP: usize = !1 + 1; // -1

// run game of life
pub fn gol() {
    // let mut cells = [0u8; WIDTH*HEIGHT];
    let mut cells = [[0u8; WIDTH]; HEIGHT];
    let mut board = [b' '; (WIDTH+1)*HEIGHT];
    init_board(&mut board, HEIGHT, WIDTH); // sets the b'\n'
    let mut indices = [(ISHTOP, ISHTOP); WIDTH*HEIGHT];

    draw_structure(2, 15, 15, &mut cells, &mut indices);
    ncurses::initscr();
    print_reset(&mut cells, &mut indices, &mut board);
    for _ in 0..200 {
        cells_set(&mut cells, &indices);
        print_reset(&mut cells, &mut indices, &mut board);
    }
    ncurses::endwin();
}

// cell++ for every neighbor or alive cells
#[inline(always)]
fn cells_set(cells: &mut [[u8; WIDTH]; HEIGHT], indices: &[(usize, usize)]) {
    let m1: usize = ISHTOP;
    let around: [(usize, usize); 8] = [(m1, m1), (0, m1), (1, m1), (1, 0), (1, 1), (0, 1), (m1, 1), (m1, 0)];
    for &i in indices.iter() {
        if i.0 == ISHTOP {break} // end of live cells
        for (ai, aj) in around.iter() { // go around i and do ++ (torus)
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
            match cells[i_cells_y][i_cells_x] & 0b0000_1111 { // set cell
                3 => cells[i_cells_y][i_cells_x] = 0b0001_0000,
                2 => cells[i_cells_y][i_cells_x] = cells[i_cells_y][i_cells_x] & 0b0001_0000,
                _ => cells[i_cells_y][i_cells_x] = 0b0000_0000,
            }
            
            if cells[i_cells_y][i_cells_x] > 0b0000_1111 { // if alive
                indices[i_indices] = (i_cells_x, i_cells_y);
                i_indices += 1;
                board_set(&mut i_board, board, b'x');
            } else { // if dead
                board_set(&mut i_board, board, b' ');
            }
            i_board += 1;
        }
    }
    indices[i_indices] = (ISHTOP, 0); // will crash if every cell is alive but whatever
    
    // println!("{}", std::str::from_utf8(&board).unwrap());
    ncurses::erase(); // seems like this is the slowest part of the code
    ncurses::addstr(std::str::from_utf8(&board).unwrap());
    ncurses::refresh();
}

// sets value to board cells
#[inline(always)]
fn board_set(i: &mut usize, board: &mut [u8], val: u8) {
    if board[*i] == b'\n' {*i += 1}
    board[*i] = val;
}

// sets b'\n' at correct places
fn init_board(board: &mut [u8], height: usize, width: usize) {
    let mut offset = 0;
    for i in 1..=height {
        board[i*width + offset] = b'\n';
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
fn draw_structure(num:usize, xoff: usize, yoff: usize,  cells: &mut [[u8; WIDTH]; HEIGHT], indices: &mut [(usize, usize)]) {
    if num == 0 {draw_line(cells, indices)}

    let mut i_indices: usize = 0;
    for (x, y) in import_structure::from_py_structure(num).iter() { // will crash other parts if it goes outside bordrs
        cells[*y+yoff][*x+xoff] = 0b0001_0010;
        indices[i_indices] = (*x+xoff, *y+yoff);
        i_indices += 1;
    }
    indices[i_indices] = (ISHTOP, 0);
}