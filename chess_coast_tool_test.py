#
# Chess collect game stats.
# (C) A.K. 2022 
# 27.11.2022
#

# test for chess_coast_tool.py


import chess_coast_tool
import tools
#from tools import WHITE, BLACK
#import sunfish




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

print("--- Unit test for chess_coast_tool.py ---")

# === parsing test (see also chessposfinder.py) ===


print("Test _parse_single_pgn() 1")
hist=chess_coast_tool._parse_single_pgn('')
check_equals('(0 move)', moves_to_str(hist), 'PGN parse test 1')

print("Test _parse_single_pgn() 2 www.lichess.com format")
hist=chess_coast_tool._parse_single_pgn("1. e4 b6 2. d4 d6 3. Nc3 Nc6 4. d5 Qd7 5. dxc6 Qxc6 6. Bb5 Qxb5 7. Nxb5 Bb7 8. Nxc7+ Kd8 9. Nxa8 e5 1-0")
check_equals('e2e4 b7b6 d2d4 d7d6 b1c3 b8c6 d4d5 d8d7 d5c6 d7c6 f1b5 c6b5 c3b5 c8b7 b5c7 e8d8 c7a8 e7e5 (18 move)', moves_to_str(hist), 'PGN parse test 2')

#print("Test _parse_single_pgn() 3 www.pgnmentor.com format")
#hist=chess_coast_tool._parse_single_pgn("""1.c4 g6 2.d4 Bg7 3.e4 d6 4.Nc3 c5 5.dxc5 Bxc3+ 6.bxc3 dxc5 7.Bd3 Nc6 8.f4 Qa5
#9.Ne2 Be6 10.f5 O-O-O 11.fxe6 Ne5 12.exf7 Nf6 13.O-O Nxd3 14.Bh6 Ne5 15.Qb3 Nxf7  1-0""")
#check_equals('c2c4 g7g6 d2d4 f8g7 e2e4 d7d6 b1c3 c7c5 d4c5 g7c3 b2c3 d6c5 f1d3 b8c6 f2f4 d8a5 g1e2 c8e6 f4f5 e8c8 f5e6 c6e5 e6f7 g8f6 e1g1 e5d3 c1h6 #d3e5 d1b3 e5f7 (30 move)', moves_to_str(hist), 'PGN parse test 3')

print("Test _parse_single_pgn() 4.1 мат в 5 ходов начало чёрными")
hist=chess_coast_tool._parse_single_pgn("e4 f6 Qe2 g5 Qh5# 1-0")
check_equals('e2e4 f7f6 d1e2 g7g5 e2h5 (5 move)', moves_to_str(hist), 'PGN parse test 4.1')

print("Test _parse_single_pgn() 4.2 мат в 4 хода начало белыми")
hist=chess_coast_tool._parse_single_pgn("f3 e6 g4 Qh4# 0-1")
check_equals('f2f3 e7e6 g2g4 d8h4 (4 move)', moves_to_str(hist), 'PGN parse test 4.2')

#print("Test _parse_single_pgn() 4.3 чёрные отдаютвсе фигуры и проигрывают сдаются")
#hist=chess_coast_tool._parse_single_pgn("1.d4 Nf6 2.Nf3 Ne4 3.e3 e6 4.Nbd2 Bb4 5.c3 Nc6 6.Nxe4 Qh4 7.Nxh4 b6 8.cxb4 Ba6 9.Bxa6 Ne5 10.dxe5 Rc8 11.Bxc8 h5 12.Qxd7+ 1-0")
#check_equals('d2d4 g8f6 g1f3 f6e4 e2e3 e7e6 b1d2 f8b4 c2c3 b8c6 d2e4 d8h4 f3h4 b7b6 c3b4 c8a6 f1a6 c6e5 d4e5 a8c8 a6c8 h7h5 d1d7 (23 move)', moves_to_str(hist), 'PGN parse test 4.3')

print("Test _parse_single_pgn() 4.4 игра и ничья по согласию")
hist=chess_coast_tool._parse_single_pgn("1. b3 d5 2. a4 Nf6 3. Ba3 e5 4. f3 Bxa3 5. Nxa3 Nc6 6. g4 Be6 7. Nh3 Qd6 8. Bg2 O-O-O 9. d3 d4 10. O-O h6 11. Qd2 g5 12. Nb5 Qb4 13. Qxb4 Nxb4 14. c4 Nc2 15. Rac1 Ne3 16. Rfe1 Rd6 17. c5 1/2-1/2")
check_equals('b2b3 d7d5 a2a4 g8f6 c1a3 e7e5 f2f3 f8a3 b1a3 b8c6 g2g4 c8e6 g1h3 d8d6 f1g2 e8c8 d2d3 d5d4 e1g1 h7h6 d1d2 g7g5 a3b5 d6b4 d2b4 c6b4 c2c4 b4c2 a1c1 c2e3 f1e1 d8d6 c4c5 (33 move)', moves_to_str(hist), 'PGN parse test 4.4')


#print("Test _parse_single_pgn() 4.5 gambit.pgn")
#hist=chess_coast_tool._parse_single_pgn("1. e4 e5 2. f4 Bc5 3.Nf3 d6 4.c3 f5 5.fxe5 dxe5 6.exf5 Qe7 7.d4 exd4+ 8.Be2 dxc3  9.Nxc3 Nf6 10.Bg5 Bxf5 11.Nd5 Qf7 12.Bxf6 gxf6 13.Nh4 Bg6 14.Rc1 Bb6 15.Rf1 Nd7  16.Rxc7 Bxc7 17.Nxc7+ Ke7 18.Qa4 Rac8 19.Bc4 Nc5 20.Qb4 Kd8 21.Qxc5 Rxc7  22.Qd6+ Qd7 23.Qxf6+ Qe7+ 24.Qxe7+ Kxe7 25.b3 a6 26.a4 Rf8 27.Rg1 Rc5 28.Nf3 b5  29.axb5 axb5 30.Be2 Rc1+ 31.Kd2 Rxg1 32.Nxg1 b4 33.Nh3 Kd6 34.Ng5 h6 35.Nf3 Kd5  36.Ke3  0-1")
#check_equals('...', moves_to_str(hist), 'PGN parse test 4.5 gambit.pgn')


print("Test parse_game_data() 5.1")
test_str_meta="""[Event "Monthly Blitz Arena"]
[Site "https://lichess.org/VDbaLr56"]
[Date "2022.04.27"]
[White "ajaykthakur22pm"]
[Black "Qutrippen"]
[Result "1-0"]
[UTCDate "2022.04.27"]
[UTCTime "20:58:43"]
[WhiteElo "1576"]
[BlackElo "1216"]
[WhiteRatingDiff "+2"]
[BlackRatingDiff "-2"]
[Variant "Standard"]
[TimeControl "300+0"]
[ECO "B00"]
[Termination "Normal"]
"""
test_str_pgn="1. e4 e5 2. d4 Nc6 3. d5 Nd4 4. Nf3 Nxf3+ 5. Qxf3 d6 6. Nc3 Nf6 7. Bb5+ Bd7 8. Bd3 g6 9. h3 Bg7 10. Bg5 Qe7 11. Nb5 Bxb5 12. Bxb5+ Kf8 13. h4 a6 14. Bd3 Nh5 15. Bxe7+ Kxe7 1-0"
gdata=chess_coast_tool.parse_game_data(test_str_meta, 100, test_str_pgn)  # type GData
check_equals(100, gdata.line, 'PGN parse result test 5.1')
check_equals(test_str_pgn, gdata.pgn, 'PGN parse result test 5.1')
check_equals("ajaykthakur22pm", gdata.name_W, 'PGN parse result test 5.1')
check_equals("Qutrippen", gdata.name_B, 'PGN parse result test 5.1')
check_equals(1576, gdata.elo_W, 'PGN parse result test 5.1')
check_equals(1216, gdata.elo_B, 'PGN parse result test 5.1')
check_equals(1, gdata.result, 'PGN parse result test 5.1') # 1=WHITE

print("Test game_filter() 5.2")
check_equals(False, chess_coast_tool.game_filter(gdata), 'PGN parse result test 5.2') # not allow this game - elo difference too much
#TODO more test for game_filter




# === math result test ===

# TODO unittest:!

print("Test scanFinishPosition aggregate_count() 20.1")
pgn="e4 f6 Qe2 g5 Qh5# 1-0"
hist=chess_coast_tool._parse_single_pgn(pgn)
functGame=lambda hist: chess_coast_tool.scanFinishPosition(hist, chess_coast_tool.aggregate_count)
check_equals(({'p': 8, 'r': 2, 'n': 2, 'b': 2, 'q': 1, 'k': 1, 'P': 8, 'R': 2, 'N': 2, 'B': 2, 'Q': 1, 'K': 1}, 5), functGame(hist), 'Math of game, 20.1')

#TODO test functGame with difference values


print("Test scanCoastSumm() 20.3")
pgn="f3 e6 g4 Qh4# 0-1"
hist = chess_coast_tool._parse_single_pgn(pgn)
check_equals(({'p': 32, 'N': 8, 'P': 32, 'k': 4, 'n': 8, 'b': 8, 'r': 8, 'q': 4, 'R': 8, 'K': 4, 'Q': 4, 'B': 8}, 4), chess_coast_tool.scanCoastSumm(hist), 'Math of game, 20.3')
#TODO test scanCoastSumm with difference values


print("Test scanMoveCount() 20.5")
pgn="f3 e6 g4 Qh4# 0-1"
hist = chess_coast_tool._parse_single_pgn(pgn)
check_equals(({'p': 1, 'r': 0, 'n': 0, 'b': 0, 'q': 1, 'k': 0, 'P': 2, 'R': 0, 'N': 0, 'B': 0, 'Q': 0, 'K': 0}, 4), chess_coast_tool.scanMoveCount(hist), 'Math of game, 20.5')
#TODO test scanMoveCount with difference values


print("Test scanLastPosition,aggregate_count 21.1")
pgn="f3 e6 g4 Qh4# 0-1"
hist = chess_coast_tool._parse_single_pgn(pgn)
functGame=lambda hist: chess_coast_tool.scanLastPosition(hist, chess_coast_tool.aggregate_count, n=3)
check_equals(({'p': 8, 'r': 2, 'n': 2, 'b': 2, 'q': 1, 'k': 1, 'P': 8, 'R': 2, 'N': 2, 'B': 2, 'Q': 1, 'K': 1}, 1), functGame(hist), 'Math of game, 21.1')

print("Test scanLastPosition,aggregate_count 21.2")
pgn="f3 e6 g4 Qh4# 0-1"
hist = chess_coast_tool._parse_single_pgn(pgn)
functGame=lambda hist: chess_coast_tool.scanLastPosition(hist, chess_coast_tool.aggregate_count, n=1)
check_equals(({'p': 8, 'r': 2, 'n': 2, 'b': 2, 'q': 1, 'k': 1, 'P': 8, 'R': 2, 'N': 2, 'B': 2, 'Q': 1, 'K': 1}, 3), functGame(hist), 'test, 21.2')

print("Test scanLastPosition,aggregate_count 21.3")
pgn="1. e4 e5 2. d4 Nc6 3. d5 Nd4 4. Nf3 Nxf3+ 5. Qxf3 d6 6. Nc3 Nf6 7. Bb5+ Bd7 8. Bd3 g6 9. h3 Bg7 10. Bg5 Qe7 11. Nb5 Bxb5 12. Bxb5+ Kf8 13. h4 a6 14. Bd3 Nh5 15. Bxe7+ Kxe7 1-0"
hist = chess_coast_tool._parse_single_pgn(pgn)
functGame=lambda hist: chess_coast_tool.scanLastPosition(hist, chess_coast_tool.aggregate_count, n=1)
check_equals(({'p': 8, 'r': 2, 'n': 1, 'b': 1, 'q': 0, 'k': 1, 'P': 8, 'R': 2, 'N': 0, 'B': 2, 'Q': 1, 'K': 1}, 29), functGame(hist), 'test, 21.3')

print("Test scanLastPosition,aggregate_count 21.4")
pgn="1. e4 e5 2. d4 Nc6 3. d5 Nd4 4. Nf3 Nxf3+ 5. Qxf3 d6 6. Nc3 Nf6 7. Bb5+ Bd7 8. Bd3 g6 9. h3 Bg7 10. Bg5 Qe7 11. Nb5 Bxb5 12. Bxb5+ Kf8 13. h4 a6 14. Bd3 Nh5 15. Bxe7+ Kxe7 1-0"
hist = chess_coast_tool._parse_single_pgn(pgn)
functGame=lambda hist: chess_coast_tool.scanLastPosition(hist, chess_coast_tool.aggregate_count, n=2)
check_equals(({'p': 8, 'r': 2, 'n': 1, 'b': 1, 'q': 1, 'k': 1, 'P': 8, 'R': 2, 'N': 0, 'B': 2, 'Q': 1, 'K': 1}, 28), functGame(hist), 'test, 21.4')



print("--- All unit-test done success ---")



print("--- Perfomance test ---")
# debugging, profilling and memory dump:
import cProfile
def test_perfomance_scanAllPosition_1():
    #pgn="1.d4 Nf6 2.Nf3 Ne4 3.e3 e6 4.Nbd2 Bb4 5.c3 Nc6 6.Nxe4 Qh4 7.Nxh4 b6 8.cxb4 Ba6 9.Bxa6 Ne5 10.dxe5 Rc8 11.Bxc8 h5 1-0"
    pgn="1. d4 Nf6 2. Nf3 Ne4 3. e3 e6 4. Nbd2 Bb4 5. c3 Nc6 6. Nxe4 Qh4 7. Nxh4 b6 8. cxb4 Ba6 9. Bxa6 Ne5 10. dxe5 Rc8 11. Bxc8 h5 1-0"
    hist = chess_coast_tool._parse_single_pgn(pgn)
    result_value, result_i = chess_coast_tool.scanCoastSumm(hist)
    check_equals(({'q': 13, 'R': 44, 'K': 22, 'n': 30, 'b': 32, 'r': 43, 'P': 176, 'N': 44, 'p': 176, 'B': 44, 'k': 22, 'Q': 22}, 22), (result_value, result_i), 'Validate perfomance test')
    result_value, result_i = chess_coast_tool.scanMoveCount(hist)
    check_equals(({'p': 0, 'r': 0, 'n': 0, 'b': 0, 'q': 0, 'k': 0, 'P': 0, 'R': 0, 'N': 0, 'B': 0, 'Q': 0, 'K': 0}, 0), (result_value, result_i), 'Validate perfomance test')
    
print("Test perfomance scanAllPosition() and match_koef_razmen_any()")
cProfile.run('test_perfomance_scanAllPosition_1()')
#from guppy import hpy; h=hpy()  #pip3 install guppy3
#h.heap()

