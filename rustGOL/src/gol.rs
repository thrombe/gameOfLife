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

// run game of life
pub fn gol() {
    const WIDTH: usize = 151;
    const HEIGHT: usize = 160;
    const LEN: usize = WIDTH*HEIGHT;
    let mut cells = [0 as u8; WIDTH*HEIGHT];
    let mut board = [b' '; (WIDTH+1)*HEIGHT];
    init_board(&mut board, HEIGHT, WIDTH); // sets the b'\n'
    let mut indices = [-1 as i32; WIDTH*HEIGHT];

    randomise_cells(&mut cells, &mut indices);
    ncurses::initscr();
    print_reset(&mut cells, &mut indices, &mut board, LEN);
    for _ in 0..200 {
        cells_set(&mut cells, &indices, WIDTH, LEN);
        print_reset(&mut cells, &mut indices, &mut board, LEN);
    }
    ncurses::endwin();
}

// cell++ for every neighbor or alive cells
#[inline(always)]
fn cells_set(cells: &mut [u8], indices: &[i32], width: usize, len: usize) {
    let around: [(i32, i32); 8] = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)];
    for &i in indices.iter() {
        if i == -1 {break} // end of live cells
        for (j, k) in around.iter() { // go around i and do ++ (torus)
            let index = ((i as i32)+j + (width as i32)*k) as usize;
            if index >= len {continue} // broken slightly
            cells[index] += 0b0000_0001;
        }
    }
}

// sets board and resets cells for next generation
#[inline(always)]
fn print_reset(cells: &mut [u8], indices: &mut [i32], board: &mut [u8], len: usize) {
    let mut i_indices: usize = 0;
    let mut i_board: usize = 0;
    for i_cells in 0..len {
        match cells[i_cells] & 0b0000_1111 { // set cell
            3 => cells[i_cells] = 0b0001_0000,
            2 => cells[i_cells] = cells[i_cells] & 0b0001_0000,
            _ => cells[i_cells] = 0b0000_0000,
        }
        
        if cells[i_cells] > 0b0000_1111 { // if alive
            indices[i_indices] = i_cells as i32;
            i_indices += 1;
            board_set(&mut i_board, board, b'x');
        } else { // if dead
            board_set(&mut i_board, board, b' ');
        }
        i_board += 1;
    }
    indices[i_indices] = -1; // will crash if every cell is alive but whatever
    
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
fn randomise_cells(cells: &mut [u8], indices: &mut [i32]) {
    // init with 2 neigh count (cuz if 2 neighs alive, then stay same), just so that print_reset works nicely
    // let ant: [usize; 5] = [2, 2+50*1, 50, 1+50*2, 2+50*2];
    let mut i_indices: usize = 0;
    // for i in ant.iter() {
    for i in 0..cells.len() {
        if i % 151 != 75 {continue}
        cells[i] = 0b0001_0010;
        indices[i_indices] = i as i32;
        i_indices += 1;
    }
    indices[i_indices] = -1;
}