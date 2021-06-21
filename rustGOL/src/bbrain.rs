/*
0b0001_0000 is alive
0b0011_0000 is dying
0b0000_0000 is dead
*/

use ncurses;

use crate::gol::{init_board, draw_structure, cells_set, board_set, ISHTOP, WIDTH, HEIGHT, NCURSED, LOOPS};

// run brian's brain
pub fn bbrain() {
    let mut cells = [[0u8; WIDTH]; HEIGHT];
    let mut board = [b' '; (WIDTH+1)*HEIGHT];
    init_board(&mut board); // sets the b'\n'
    let mut indices = [(ISHTOP, ISHTOP); WIDTH*HEIGHT];

    draw_structure(5, 15, 15, &mut cells, &mut indices);
    if NCURSED {
        ncurses::initscr();
        ncurses::curs_set(ncurses::CURSOR_VISIBILITY::CURSOR_INVISIBLE);
    }
    for _ in 0..LOOPS {
        cells_set(&mut cells, &indices);
        print_reset(&mut cells, &mut indices, &mut board);
    }
    if NCURSED {ncurses::endwin();}
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
                2 => { // if count == 2 and state is dead, come alive
                    cells[i_cells_y][i_cells_x] = 0b0001_0000;
                    indices[i_indices] = (i_cells_x, i_cells_y);
                    i_indices += 1;
                    board_set(&mut i_board, board, b'x');
                }
                0b0001_0000..=0b0001_1111 => { // go dying if alive
                    cells[i_cells_y][i_cells_x] = 0b0011_0000;
                    board_set(&mut i_board, board, b'o');
                }
                _ => { // else dead
                    cells[i_cells_y][i_cells_x] = 0b0000_0000;
                    board_set(&mut i_board, board, b' ')
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