
## About chessposfinder.py
This is programm for find interesting chess game in PGN file. The *"Chess Position Finder"* can find one fame in list of games in PGN file by any criteria. For example: "who won with less of figures?" or "where is game position with max number of pin".
'chessposfinder.py' help find single game from thousend games with maximum of same criteria.

PGN (Portable Game Notation) - chess game format.

'chessposfinder.py' - this is Python3 console programm: input - from PFN file, output - to console or can be redirect to text file.

## System requirements and envinroment

* *Python3*   (maybe pyton2 will be work too)
* *sunfish* python chess library [look on github.com](https://github.com/thomasahle/sunfish)
* Windows, Linux, etc. - any for run Python's programm.
* RAM: 50 Mb and 20 Mb on disk will be enought.

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

Then see ouutput. Or redirect output to file:

    python3 chessposfinder.py {path_to_file.pgn} > log_best_pgn.txt

then open new file 'log_best_pgn.txt'.

Batch scan of many *.pgn files
---------------------

1. Copy all PGN file into one directory.
2. execute batch script ________
3. wait till all subprocess has finished.
4. See log files .

(linux - sh, windows - cmd) ToDo for CMD script.

## Example output:

    --- PGN file: test.pgn  ---
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

In output using <TAB> for usefull insert into table processor, like OpenOffice Calc or MS Excel (R)(TM).

Perfomance: 2 Mb/10 min. Maybe it slow for large data, but you can run many files in nultiple process.


## About PGN format
Single PGN game parsed by modified from sunfish function ''. Single PGN item parsed by sunfish ''


## Project files:
* chessposfinder.py - main programm for find and analyze result of chess games.
* chessposfinder_test.py - unit-test for chessposfinder.py.
* startall.sh - the Linux bash script for run multiply instances of chessposfinder.py for process many files.
* startall.cmd - the Windows batch script for run multiply instances of chessposfinder.py for process many files.

* chess_coast_tool.py - usefull utilite for convert PGN file into CSV and grab simple game statistic. It is another simple project, not same as chessposfinder.
* chess_coast_tool_test.py - unit-test for chess_coast_tool_test.py.


## Improvement what you search
You can modify this programm for change search criteria.
The program run 'main()' -> for file 'process_file_PGN()' -> for each game 'funct(hist - game sequence, end_is - game result)'.
The 'funct(hist, end_is)' has combined with aggregate and position measure function.

*process_file_PGN(file_name, funct, ignore_withdraw=False)* can ignore withdraw result, use additional option 'ignore_withdraw=True'

The aggregate function:

* def scanAllPosition(hist,end_is, funct):
* def scanMaxLength(hist,end_is):
* def scanFinishPosition(hist,end_is, funct):
* def scanLastNPosition(hist,end_is, funct, n:int=1):

For more combitation you may use it with lambda. Example:

    functGame=lambda hist, end_is: scanFinishPosition(hist, end_is, match_disbalance)

The position measure function:

* def match_koef_razmen_any(pos, end_is): 
* def match_koef_maxstrength(pos, end_is):
* def match_disbalance(pos, end_is):


# Analyze PGN as table data with chess_coast_tool_test.py
Based on *chessposfinder.py* be make *chess_coast_tool.py* - the tool for convert PGN file into CSV file with statistic information. It will be useful for 'table processor' analyze or use external math tool for analyze big data.
Command for start:

    python3 chess_coast_tool.py sample_file_from_lichess_monthly-blitz.pgn data_out.csv
    
## Improvement

See data collection function choose code:

    #The sort of collect data of the game:    
    #functGame=lambda hist: scanFinishPosition(hist, aggregate_count) # get last position, count of figure
    #functGame=scanCoastSumm # scan all positions, average figure by timeline
    functGame=scanMoveCount #Scan count of move

## Research result

"Pre-print" result on 30.11.2022:

1. The wining is not depends of number of moving figure.
2. Classic figure weight is near true. But accuracy of my result is not good.

2022-12-31 finish math on one of lichess.com tournament data. It is 7850 game of blitz tournament; player average Elo is 1854 (min 716, max 2720).
It was strange result of linear regression:

|const|Pawn|kNight|Rook|Bishop|Queen|
|---|---|---|---|---|---|
0.5993|0.2387|0.3410|0.2041|0.1222|0.0363
0.0201|0.0148|0.0155|0.0160|0.0066|0.0098
0.2077|0.8639||||
411.6186|7850.0000||||
1536.0368|5858.7685||||

Table 1 - chess figure coast, linear regression by end 3 move

'const' - the white has less hight win percentage that black figure (on this data is on 0.036 more win).

For this table used Open Ofice function "=LINEAR(C$2:C$7857;O$2:S$7857;1;1)".
The Queen may be have low priority, cause eat other figure (knight, bishop, rock) and it take dependence with each other variable.

Update 2023-01-06. After normalize time on board per figure, in previous dataset (see result of table 1) take next result (table 2):

|const|Pawn|kNight|Rook|Bishop|Queen|
|---|---|---|---|---|---|
2.2069|0.7147|1.0625|0.6593|0.2054|0.0375
0.0746|0.0314|0.0416|0.0322|0.0145|0.0099
0.1921|0.8724||||
373.2754|7850.0000||||
1420.4364|5974.3690||||

Table 2 - chess figure coast, linear regression by average figure time on chess board

The pawn has more weight that many other figure. But this can be result of other figure.


# Usefull links
You can download same PGN from:

* [www.lichess.org](https://www.lichess.org) - free chess, has big open database, easy search by player orchallenge
* [www.pgnmentor.com](https://www.pgnmentor.com) - chess programm and chess start games collection.

### Sunfish library
Sunfish is a simple chess engine, written in Python. See [Sunfish on github](https://github.com/thomasahle/sunfish/).

## License
This software (chessposfinder) distributed under [MIT license](LICENSE.txt). &copy; playerO1 2022
