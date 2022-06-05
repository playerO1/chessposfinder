
## About chessposfinder.py
This is programm for find interesting chess game in PGN file. The *"Chess Position Finder"* can find one fame in list of games in PGN file by any criteria. For example: "who won with less of figures?" or "where is game position with max number of pin".
'chessposfinder.py' help find single game from thousend games with maximum of same criteria.

PGN (Portable Game Notation) - chess game format.
'chessposfinder.py' - this is Python3 console programm: input - from PFN file, output - to console or can be redirect to text file.

## System requirements and envinroment

Python3   (maybe pyton2 will be work too)
sunfish python chess library [look on github.com](https://github.com/thomasahle/sunfish)

## How to run it

prepare
--------
1. ensure you have Python3, or install Python3.
2. download this project files (chessposfinder.py, etc.), or gust do 'git clone ...github.com/playero1/chessposfinder.git' (todo url)
3. install 'sunfish' - try 'pip3 install sunfish', or download files from git (see other project https://github.com/thomasahle/sunfish)
4. may be you should copy chessposfinder.py to same folder with sunfish library (not sure, ToDo check import for run with separate folder)
5. download or save same chess games into PGN format file.
6. run python3 chessposfinder.py path/to/chess-data-file.pgn

run
--------
Open terminal
    python3 chessposfinder.py {path_to_file.pgn}
see ouutput.
Or redirect output to file:
    python3 chessposfinder.py {path_to_file.pgn} > log_best_pgn.txt
then open new file log_best_pgn.txt

Batch scan many files
---------------------

1. Copy all PGN file into one directory.
2. execute batch script ________
3. wait till all subprocess has finished.
4. See log files .

(linux - sh, windows - cmd) ToDo for CMD script.

## Example output:

    --- PGN file: /home/user2/Programming/Python project/chess analyzer/git/test.pgn  ---
    line    move    value
    10       18      -9      1. e4 b6 2. d4 d6 3. Nc3 Nc6 4. d5 Qd7 5. dxc6 Qxc6 6. Bb5 Qxb5 7. Nxb5 Bb7 8. Nxc7+ Kd8 9. Nxa8 e5 1-0 
    21       30      -1      1.c4 g6 2.d4 Bg7 3.e4 d6 4.Nc3 c5 5.dxc5 Bxc3+ 6.bxc3 dxc5 7.Bd3 Nc6 8.f4 Qa5 9.Ne2 Be6 10.f5 O-O-O 11.fxe6 Ne5 12.exf7 Nf6 13.O-O Nxd3 14.Bh6 Ne5 15.Qb3 Nxf7  1-0 
    35       23      -21     1.d4 Nf6 2.Nf3 Ne4 3.e3 e6 4.Nbd2 Bb4 5.c3 Nc6 6.Nxe4 Qh4 7.Nxh4 b6 8.cxb4 Ba6 9.Bxa6 Ne5 10.dxe5 Rc8 11.Bxc8 h5 12.Qxd7+ 1-0 
    39       22      -21     1.d4 Nf6 2.Nf3 Ne4 3.e3 e6 4.Nbd2 Bb4 5.c3 Nc6 6.Nxe4 Qh4 7.Nxh4 b6 8.cxb4 Ba6 9.Bxa6 Ne5 10.dxe5 Rc8 11.Bxc8 h5 1-0 
    41       23      21      1.d4 Nf6 2.Nf3 Ne4 3.e3 e6 4.Nbd2 Bb4 5.c3 Nc6 6.Nxe4 Qh4 7.Nxh4 b6 8.cxb4 Ba6 9.Bxa6 Ne5 10.dxe5 Rc8 11.Bxc8 h5 12.Qxd7+ 0-1 
    43       22      21      1.d4 Nf6 2.Nf3 Ne4 3.e3 e6 4.Nbd2 Bb4 5.c3 Nc6 6.Nxe4 Qh4 7.Nxh4 b6 8.cxb4 Ba6 9.Bxa6 Ne5 10.dxe5 Rc8 11.Bxc8 h5 0-1 
    --- End of file, processed 6 games + error parsing 0 games ---
    --- best: ---
    41       23      21      1.d4 Nf6 2.Nf3 Ne4 3.e3 e6 4.Nbd2 Bb4 5.c3 Nc6 6.Nxe4 Qh4 7.Nxh4 b6 8.cxb4 Ba6 9.Bxa6 Ne5 10.dxe5 Rc8 11.Bxc8 h5 12.Qxd7+ 0-1 
    
      8 · · ♝ · ♔ · · ♖
      7 ♙ · ♙ ♙ · ♙ ♙ ·
      6 · ♙ · · ♙ · · ·
      5 · · · · ♟ · · ♙
      4 · ♟ · · ♞ · · ♞
      3 · · · · ♟ · · ·
      2 ♟ ♟ · · · ♟ ♟ ♟
      1 ♜ · ♝ ♛ ♚ · · ♜
        a b c d e f g h 

In output usint <TAB> for usefull insert into table processor, like OpenOffice Calc or MS Excel (R)(TM).

Perfomance: 2 Mb/10 min. Maybe it slow for large data, but you can run many files in nultiple process.


## About PGN format
Single PGN game parsed by modified from sunfish function ''. Single PGN item parsed by sunfish ''


## File:
* chessposfinder.py - main programm for find and analyze result of chess games.
* chessposfinder_test.py - unit-test for chessposfinder.py.
* startall.sh - script for run multiply instances of chessposfinder.py for process many files.

## Improvement what you search
You can modify this programm for change search criteria.
...

## Usefull links
You can download same PGN from:
* www.lichess.org - easy search by player
* www.pgnmentor.com


## Introduction
Sunfish is a simple, but strong chess engine, written in Python, mostly for teaching purposes. Without tables and its simple interface, it takes up just 111 lines of code! (see [`compressed.py`](https://github.com/thomasahle/sunfish/blob/master/compressed.py)) Yet [it plays at ratings above 2000 at Lichess](https://lichess.org/@/sunfish-engine).

