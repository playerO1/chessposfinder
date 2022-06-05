#
# Chess find interesting games.
# (C) A.K. 2022 
# 22.05.2022
#

# test for chessposfinder.py


import chessposfinder
import tools
#from tools import WHITE, BLACK
#import sunfish


# funct: val, moveI = scanAll(hist, funct)
#def process_file_PGN(file_name, funct):
#    return maxI,maxIM,maxV, maxL


#-----------------


#if __name__ == '__main__':
#    main()

def check_equals(exp,val, test_name=''):
    if (exp!=val): raise AssertionError('Expected \"'+str(exp)+'\" <> value \"'+str(val)+'\" test error found! '+test_name)

def moves_to_str(parsed_pgn):
    s=""
    n=0
    for pos,move in parsed_pgn:
        s=s+tools.mrender(pos,move)+' ' # str(move) or tools.mrender(pos,move)
        n=n+1
    return s+'('+str(n)+' move)'

print("--- Unit test for chessposfinder.py ---")

# === parsing test ===

print("Test _parse_single_pgn() 1")
hist=chessposfinder._parse_single_pgn('')
check_equals('(0 move)', moves_to_str(hist), 'PGN parse test 1')

print("Test _parse_single_pgn() 2 www.lichess.com format")
hist=chessposfinder._parse_single_pgn("1. e4 b6 2. d4 d6 3. Nc3 Nc6 4. d5 Qd7 5. dxc6 Qxc6 6. Bb5 Qxb5 7. Nxb5 Bb7 8. Nxc7+ Kd8 9. Nxa8 e5 1-0")
check_equals('e2e4 b7b6 d2d4 d7d6 b1c3 b8c6 d4d5 d8d7 d5c6 d7c6 f1b5 c6b5 c3b5 c8b7 b5c7 e8d8 c7a8 e7e5 (18 move)', moves_to_str(hist), 'PGN parse test 2')

print("Test _parse_single_pgn() 3 www.pgnmentor.com format")
hist=chessposfinder._parse_single_pgn("""1.c4 g6 2.d4 Bg7 3.e4 d6 4.Nc3 c5 5.dxc5 Bxc3+ 6.bxc3 dxc5 7.Bd3 Nc6 8.f4 Qa5
9.Ne2 Be6 10.f5 O-O-O 11.fxe6 Ne5 12.exf7 Nf6 13.O-O Nxd3 14.Bh6 Ne5 15.Qb3 Nxf7  1-0""")
check_equals('c2c4 g7g6 d2d4 f8g7 e2e4 d7d6 b1c3 c7c5 d4c5 g7c3 b2c3 d6c5 f1d3 b8c6 f2f4 d8a5 g1e2 c8e6 f4f5 e8c8 f5e6 c6e5 e6f7 g8f6 e1g1 e5d3 c1h6 d3e5 d1b3 e5f7 (30 move)', moves_to_str(hist), 'PGN parse test 3')

print("Test _parse_single_pgn() 4.1 мат в 5 ходов начало чёрными")
hist=chessposfinder._parse_single_pgn("e4 f6 Qe2 g5 Qh5# 1-0")
check_equals('e2e4 f7f6 d1e2 g7g5 e2h5 (5 move)', moves_to_str(hist), 'PGN parse test 4.1')

print("Test _parse_single_pgn() 4.2 мат в 4 хода начало белыми")
hist=chessposfinder._parse_single_pgn("f3 e6 g4 Qh4# 0-1")
check_equals('f2f3 e7e6 g2g4 d8h4 (4 move)', moves_to_str(hist), 'PGN parse test 4.2')

print("Test _parse_single_pgn() 4.3 чёрные отдаютвсе фигуры и проигрывают сдаются")
hist=chessposfinder._parse_single_pgn("1.d4 Nf6 2.Nf3 Ne4 3.e3 e6 4.Nbd2 Bb4 5.c3 Nc6 6.Nxe4 Qh4 7.Nxh4 b6 8.cxb4 Ba6 9.Bxa6 Ne5 10.dxe5 Rc8 11.Bxc8 h5 12.Qxd7+ 1-0")
check_equals('d2d4 g8f6 g1f3 f6e4 e2e3 e7e6 b1d2 f8b4 c2c3 b8c6 d2e4 d8h4 f3h4 b7b6 c3b4 c8a6 f1a6 c6e5 d4e5 a8c8 a6c8 h7h5 d1d7 (23 move)', moves_to_str(hist), 'PGN parse test 4.3')

print("Test _parse_single_pgn() 4.4 игра и ничья по согласию")
hist=chessposfinder._parse_single_pgn("1. b3 d5 2. a4 Nf6 3. Ba3 e5 4. f3 Bxa3 5. Nxa3 Nc6 6. g4 Be6 7. Nh3 Qd6 8. Bg2 O-O-O 9. d3 d4 10. O-O h6 11. Qd2 g5 12. Nb5 Qb4 13. Qxb4 Nxb4 14. c4 Nc2 15. Rac1 Ne3 16. Rfe1 Rd6 17. c5 1/2-1/2")
check_equals('b2b3 d7d5 a2a4 g8f6 c1a3 e7e5 f2f3 f8a3 b1a3 b8c6 g2g4 c8e6 g1h3 d8d6 f1g2 e8c8 d2d3 d5d4 e1g1 h7h6 d1d2 g7g5 a3b5 d6b4 d2b4 c6b4 c2c4 b4c2 a1c1 c2e3 f1e1 d8d6 c4c5 (33 move)', moves_to_str(hist), 'PGN parse test 4.4')

print("Test _parse_single_pgn_result() 5.1")
end_of_game=chessposfinder._parse_single_pgn_result("e4 f6 Qe2 g5 Qh5# 1-0")
check_equals(0, end_of_game, 'PGN parse result test 5.1')
print("Test _parse_single_pgn_result() 5.2")
end_of_game=chessposfinder._parse_single_pgn_result("f3 e6 g4 Qh4# 0-1")
check_equals(1, end_of_game, 'PGN parse result test 5.2')
print("Test _parse_single_pgn_result() 5.3")
end_of_game=chessposfinder._parse_single_pgn_result("1. b3 d5 2. a4 Nf6 3. Ba3 e5 4. f3 Bxa3 5. Nxa3 Nc6 6. g4 Be6 7. Nh3 Qd6 8. Bg2 O-O-O 9. d3 d4 10. O-O h6 11. Qd2 g5 12. Nb5 Qb4 13. Qxb4 Nxb4 14. c4 Nc2 15. Rac1 Ne3 16. Rfe1 Rd6 17. c5 1/2-1/2")
check_equals(3, end_of_game, 'PGN parse result test 5.3')


# === math result test ===

print("Test scanMaxLength() 6.1")
pgn="e4 f6 Qe2 g5 Qh5# 1-0"
hist=chessposfinder._parse_single_pgn(pgn)
end_of_game=chessposfinder._parse_single_pgn_result(pgn)
check_equals((5,5), chessposfinder.scanMaxLength(hist, end_of_game), 'Math of game, 6.1')

print("Test scanMaxLength() 6.2")
pgn="f3 e6 g4 Qh4# 0-1"
hist,end_of_game = chessposfinder._parse_single_pgn(pgn),chessposfinder._parse_single_pgn_result(pgn)
check_equals((4,4), chessposfinder.scanMaxLength(hist, end_of_game), 'Math of game, 6.2')


print("Test scanFinishPosition() and match_disbalance() 7.1")
pgn="e4 f6 Qe2 g5 Qh5# 1-0"
hist,end_of_game = chessposfinder._parse_single_pgn(pgn),chessposfinder._parse_single_pgn_result(pgn)
check_equals((0,5), chessposfinder.scanFinishPosition(hist, end_of_game, chessposfinder.match_disbalance), 'Math of game, 7.1')

print("Test scanFinishPosition() and match_disbalance() 7.2")
pgn="f3 e6 g4 Qh4# 0-1"
hist,end_of_game = chessposfinder._parse_single_pgn(pgn),chessposfinder._parse_single_pgn_result(pgn)
check_equals((0,4), chessposfinder.scanFinishPosition(hist, end_of_game, chessposfinder.match_disbalance), 'Math of game, 7.2')

print("Test scanFinishPosition() and match_disbalance() 7.3 чёрные отдают все фигуры и проигрывают - сдаются, ход чёрных")
pgn="1.d4 Nf6 2.Nf3 Ne4 3.e3 e6 4.Nbd2 Bb4 5.c3 Nc6 6.Nxe4 Qh4 7.Nxh4 b6 8.cxb4 Ba6 9.Bxa6 Ne5 10.dxe5 Rc8 11.Bxc8 h5 12.Qxd7+ 1-0"
hist,end_of_game = chessposfinder._parse_single_pgn(pgn),chessposfinder._parse_single_pgn_result(pgn)
check_equals((-21,23), chessposfinder.scanFinishPosition(hist, end_of_game, chessposfinder.match_disbalance), 'Math of game, 7.3')

print("Test scanFinishPosition() and match_disbalance() 7.4 чёрные отдают все фигуры и проигрывают - сдаются на ход раньше, ходбелых")
pgn="1.d4 Nf6 2.Nf3 Ne4 3.e3 e6 4.Nbd2 Bb4 5.c3 Nc6 6.Nxe4 Qh4 7.Nxh4 b6 8.cxb4 Ba6 9.Bxa6 Ne5 10.dxe5 Rc8 11.Bxc8 h5 1-0"
hist,end_of_game = chessposfinder._parse_single_pgn(pgn),chessposfinder._parse_single_pgn_result(pgn)
check_equals((-21,22), chessposfinder.scanFinishPosition(hist, end_of_game, chessposfinder.match_disbalance), 'Math of game, 7.4')

print("Test scanFinishPosition() and match_disbalance() 7.5 чёрные отдают все фигуры и проигрывают - но сдаются белые, ход чёрных")
pgn="1.d4 Nf6 2.Nf3 Ne4 3.e3 e6 4.Nbd2 Bb4 5.c3 Nc6 6.Nxe4 Qh4 7.Nxh4 b6 8.cxb4 Ba6 9.Bxa6 Ne5 10.dxe5 Rc8 11.Bxc8 h5 12.Qxd7+ 0-1"
hist,end_of_game = chessposfinder._parse_single_pgn(pgn),chessposfinder._parse_single_pgn_result(pgn)
check_equals((21,23), chessposfinder.scanFinishPosition(hist, end_of_game, chessposfinder.match_disbalance), 'Math of game, 7.5')

print("Test scanFinishPosition() and match_disbalance() 7.6 чёрные отдают все фигуры и проигрывают -  но сдаются белые на ход раньше, ходбелых")
pgn="1.d4 Nf6 2.Nf3 Ne4 3.e3 e6 4.Nbd2 Bb4 5.c3 Nc6 6.Nxe4 Qh4 7.Nxh4 b6 8.cxb4 Ba6 9.Bxa6 Ne5 10.dxe5 Rc8 11.Bxc8 h5 0-1"
hist,end_of_game = chessposfinder._parse_single_pgn(pgn),chessposfinder._parse_single_pgn_result(pgn)
check_equals((21,22), chessposfinder.scanFinishPosition(hist, end_of_game, chessposfinder.match_disbalance), 'Math of game, 7.6')

print("Test scanFinishPosition() and match_disbalance() 7.7 чёрные отдают все фигуры и проигрывают - но объявляется ничья, ход чёрных")
pgn="1.d4 Nf6 2.Nf3 Ne4 3.e3 e6 4.Nbd2 Bb4 5.c3 Nc6 6.Nxe4 Qh4 7.Nxh4 b6 8.cxb4 Ba6 9.Bxa6 Ne5 10.dxe5 Rc8 11.Bxc8 h5 12.Qxd7+ 1/2-1/2"
hist,end_of_game = chessposfinder._parse_single_pgn(pgn),chessposfinder._parse_single_pgn_result(pgn)
check_equals((10.5,23), chessposfinder.scanFinishPosition(hist, end_of_game, chessposfinder.match_disbalance), 'Math of game, 7.7')

print("Test scanFinishPosition() and match_disbalance() 7.8 чёрные отдают все фигуры и проигрывают - но объявляется ничья, белые на ход раньше, ходбелых")
pgn="1.d4 Nf6 2.Nf3 Ne4 3.e3 e6 4.Nbd2 Bb4 5.c3 Nc6 6.Nxe4 Qh4 7.Nxh4 b6 8.cxb4 Ba6 9.Bxa6 Ne5 10.dxe5 Rc8 11.Bxc8 h5 1/2-1/2"
hist,end_of_game = chessposfinder._parse_single_pgn(pgn),chessposfinder._parse_single_pgn_result(pgn)
check_equals((10.5,22), chessposfinder.scanFinishPosition(hist, end_of_game, chessposfinder.match_disbalance), 'Math of game, 7.8')


print("Test scanAllPosition() and match_koef_razmen_any() 8.1 нет рзмена - сразумат")
pgn="f3 e6 g4 Qh4# 0-1"
hist,end_of_game = chessposfinder._parse_single_pgn(pgn),chessposfinder._parse_single_pgn_result(pgn)
check_equals((0,0), chessposfinder.scanAllPosition(hist, end_of_game, chessposfinder.match_koef_razmen_any), 'Math of game, 8.1')

print("Test scanAllPosition() and match_koef_razmen_any() 8.2 ...")
pgn="1.d4 Nf6 2.Nf3 Ne4 3.e3 e6 4.Nbd2 Bb4 5.c3 Nc6 6.Nxe4 Qh4 7.Nxh4 b6 8.cxb4 Ba6 9.Bxa6 Ne5 10.dxe5 Rc8 11.Bxc8 h5 1-0"
hist,end_of_game = chessposfinder._parse_single_pgn(pgn),chessposfinder._parse_single_pgn_result(pgn)
check_equals((3,10), chessposfinder.scanAllPosition(hist, end_of_game, chessposfinder.match_koef_razmen_any), 'Math of game, 8.2')


print("Test match_koef_razmen_any() 9.1")
pos = tools.parseFEN(tools.FEN_INITIAL)
val = chessposfinder.match_koef_razmen_any(pos, end_is=0)
check_equals(0, val, 'Math of game, 9.1')

print("Test match_disbalance() 10.1")
pos = tools.parseFEN(tools.FEN_INITIAL)
val = chessposfinder.match_disbalance(pos, end_is=0)
check_equals(0, val, 'Math of game, 10.1')

print("Test match_koef_maxstrength() 11.1")
pos = tools.parseFEN(tools.FEN_INITIAL)
val = chessposfinder.match_koef_maxstrength(pos, end_is=0)
check_equals(42, val, 'Math of game, 11.1')
#todo test: why 42??? should be 8*2=16.





print("--- All unit-test done success ---")



print("--- Perfomance test ---")
# отладка, профайл и дамп памяти:
import cProfile
def test_perfomance_scanAllPosition_1():
    pgn="1.d4 Nf6 2.Nf3 Ne4 3.e3 e6 4.Nbd2 Bb4 5.c3 Nc6 6.Nxe4 Qh4 7.Nxh4 b6 8.cxb4 Ba6 9.Bxa6 Ne5 10.dxe5 Rc8 11.Bxc8 h5 1-0"
    hist,end_of_game = chessposfinder._parse_single_pgn(pgn),chessposfinder._parse_single_pgn_result(pgn)
    result_value, result_i = chessposfinder.scanAllPosition(hist, end_of_game, chessposfinder.match_koef_razmen_any)
    check_equals((3,10), (result_value, result_i), 'Validate perfomance test')
print("Test perfomance scanAllPosition() and match_koef_razmen_any()")
cProfile.run('test_perfomance_scanAllPosition_1()')
#from guppy import hpy; h=hpy()  #pip3 install guppy3
#h.heap()

