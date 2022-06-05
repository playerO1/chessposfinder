#
# Chess find interesting games.
# (C) A.K. 2022 
# 24.04.2022
#

#import sys
#import time
#from datetime import datetime
#import importlib

import tools
from tools import WHITE, BLACK
import sunfish

#from sunfish import sunfish
#from sunfish import tools
#from sunfish.tools import WHITE, BLACK
#TODO как по другому сделать импорт из другой папки? AttributeError: module 'sunfish' has no attribute 'pst'
#import importlib
#sunfish = importlib.import_module('unsfish.sunfish','sunfish')
#tools = importlib.import_module('sunfish.tools','sunfish')


#PRINT_DEBUG = False

# ---------- my logic ------------
#расчитывает максимальное возможное число ударов на 1 клетку "напряжённость пустой клетки"  (TODO test me)
def match_koef_maxstrength(pos, end_is):
    cellN=dict() #
    for newM,newP in tools.gen_legal_moves(pos):
       #print(newM, newP)
       #sunfish.print_pos(newP)
       p=newM[1]
       if p in cellN: 
           cellN[p]=cellN[p]+1 
       else:
           cellN[p]=1
       #pos.board[newM[1]]
       for newM2,newP2 in tools.gen_legal_moves(newP): # за другого игрока. todo лучше pos.clone pos.nullmove()?
           #print(newM2, newP2)
           #sunfish.print_pos(newP2)
           p=newM[1]
           if p in cellN: 
               cellN[p]=cellN[p]+1 
           else:
               cellN[p]=1
    val=max([cellN[k] for k in cellN])
    return val

# подсчитывает количество "битых" позиций с фигурами. Не учитывает значимость фигур! Это ещё не размен.
def match_koef_razmen_any(pos, end_is): 
    cellN=set() #
    firstP=None
    for newM,newP in tools.gen_legal_moves(pos):
       #print(newM, newP)
       #sunfish.print_pos(newP)
       firstP = newP
       p=newM[1]
       f=pos.board[newM[1]]
       if f!='.' and f!='p' and f!='P' : 
           #print("razmen A ",newM," figure ", pos.board[newM[0]], " eat ", f)
           cellN.add(p)
    for newM,newP in tools.gen_legal_moves(firstP): #немного нечестный расчёт - надо учитывать все варианты, но примерно так сойдёт для ускорения
       #print(newM, newP)
       #sunfish.print_pos(newP)
       firstM = newP
       p=newM[1]
       f=firstP.board[newM[1]]
       if f!='.' and f!='p' and f!='P' : 
           #print("razmen B ",newM," figure ", firstP.board[newM[0]], " eat ", f)
           cellN.add(p)
    return len(cellN)

#todo : максимальное колебание "оценок"
#todo : победа с большим перевесом фигур (победил с меньшим числом фигур)

# find position with max value of funct()
def scanAllPosition(hist,end_is, funct): # hist=_parse_single_pgn(gameFEN), funct=match_koef_razmen_any(pos)
    i=0
    maxV=0
    maxI=0
    for p,m in hist:
        i=i+1
        val=funct(p,end_is)
        #print(i, ". ", m, " value=", val)
        if val>maxV:  #maxV=max(maxV,val)
            maxV=val
            maxI=i
    #print("max=",maxV," at ", maxI)
    return maxV, maxI

def scanMaxLength(hist,end_is): # самая длинная игра
    i=0
    for p,m in hist:
        i=i+1
    return i,i

def match_disbalance(pos, end_is):
    #def scoreDiff(pos): #наибольшая разница по фигурам. Чем больше тем невероятнее победа. ПРОВЕРИТЬ зависимость от цвета!
    price={'p':1,'r':4,'n':3,'b':3,'q':5,'k':0,   'P':-1,'R':-4,'N':-3,'B':-3,'Q':-5,'K':0, }
    # tools.get_color(pos)
    # sunfish.piece
    v=0
    for i, p in enumerate(pos.board):
        #if not p.isupper(): continue
        if p in price:
            v = v + price[p]
    enp_move_by = tools.get_color(pos)
    if enp_move_by != end_is: #todo withdraw 1/2-1/2
        v=-v
    if end_is == 3: # withdraw - no win 1/2 - it is not easy with low of figures
        v = abs(v)/2
    #print("debug v=",v," color=",tools.get_color(pos)," pos=", pos)
    return v
    
def scanFinishPosition(hist,end_is, funct): # самая последняя позиция
    lastI=0
    lastP=None
    for p,m in hist:
        lastI=lastI+1
        lastP = p
    #return lastP,lastI
    if lastP==None: return 0, 0
    v = funct(lastP, end_is)
    return v, lastI

#todo def scanFinishPosition(hist,end_is, funct, n=4): #def scanAllPosition(hist,end_is, funct): 

# --------------------------


#-------- improvement sunfish tool ---------

# на основе tools.py:readPGN (sunfish)
# Хорошо парсит однострочный формат PGN с lichess.com ,
# может парсить несколько строк (с переносами) только нужно тчобы последняя строка была пустая.
def _parse_single_pgn(lines):
    parts = lines.split() #re.sub('{.*?}', '', ' '.join(lines)).split()
    # some PGN file (no lichess.com) has not space between 1.e4e5
    for i in range(len(parts)):
        # replace hardik with shardul
        s=parts[i]
        if s[0].isdigit() and '.' in s:
            dotP=s.index('.')
            if dotP+1<len(s):
                parts[i] = s[dotP+1:]
    msans = [part for part in parts if len(part)>0 and not part[0].isdigit()]
    pos0 = tools.parseFEN(tools.FEN_INITIAL)
    for msan in msans:
        #print("msan is \"", msan,"\"")
        try:
            move = tools.parseSAN(pos0, msan)
            #print("move is ", move)
        except AssertionError:
            print('PGN was:', ' '.join(lines))
            raise
        yield pos0, move
        #print(msan,">>>", move)
        pos0 = pos0.move(move)
         
def _parse_single_pgn_result(line):
    if ' 1-0' in line:
        return WHITE
    if ' 0-1' in line:
        return BLACK
    if ' 1/2-1/2' in line:
        return 3 # withdraw...none
    raise AssertionError('Unknown result game for PGN: '+line)


# funct: val, moveI = scanAll(hist, funct)
def process_file_PGN(file_name, funct):
    lI=0
    current_game_meta = ""
    current_game_line = ""
    prev_meta=False
    print("line\tmove\tvalue")
    maxI=-1
    maxIM=None
    maxV=-1
    maxL=None
    total_games_success=0
    total_games_errors=0
    with open(file_name, newline='') as lines:
        is_game=False
        for line in lines:
            lI=lI+1
            #print(lI)#,'="',line,'"', len(line))
            is_game_change=is_game
            if line.startswith('['):
                current_game_meta = current_game_meta + line
                prev_meta=True
                is_game = False
            elif len(line)<3 or not line[0].isdigit():
                is_game=False
                #pass
            else:
                is_game=True
                current_game_line = current_game_line + line
                
            if (not is_game and is_game_change):
                line = current_game_line
                current_game_line = ""
                line=line.replace('\r\n', " ") #\\r", "").replace("\\n", "")
                #print(lI,">>>",line)
                #continue
                if len(line)<6: continue # сразу сдались
                if not('1-0' in line or '0-1' in line): continue # без ничьих
                try:
                    hist=_parse_single_pgn(line)
                    end_is = _parse_single_pgn_result(line)
                    #todo parse result: WHITE 1-0 , BLACK  0-1 NONE 1/2-1/2
                    val, moveI = funct(hist, end_is) #scanAll(hist, funct)
                    print(lI,"\t",moveI,"\t",val,'\t', line) # todo Do print current_game_meta?
                    if maxV<val:
                        maxI=lI
                        maxIM=moveI
                        maxV=val
                        maxL=line
                    if prev_meta:
                        current_game_meta=""
                        prev_meta=False
                    total_games_success=total_games_success+1
                except AssertionError as err:
                    print("Error parse line {0} cause {1}".format(lI, err))
                    total_games_errors=total_games_errors+1
    print("--- End of file, processed {0} games + error parsing {1} games ---".format(total_games_success, total_games_errors))
    return maxI,maxIM,maxV, maxL


#-----------------


def main():
    import sys
    import os
    if len(sys.argv)!=2:
        print("Required PGN file. Use python chessposfinder.py path/to_file.pgn")
        return
    file_name=sys.argv[1]
    if not os.path.isfile(file_name):
        print("Required PGN file. File not found: ", file_name)
        return
    print("--- PGN file:",file_name," ---")
    #functPos = match_koef_razmen_any # funct(pos); match_koef_maxstrength, match_koef_razmen_any
    #functGame = lambda hist: scanAllPosition(hist, functPos)
    # functGame = lambda hist: scanAllPosition(hist,, lambda pos: pos.score)
    # functGame = scanMaxLength # lambda hist, end_is: len(hist)  #самая долгая игра
    
    functGame=lambda hist, end_is: scanFinishPosition(hist, end_is, match_disbalance)
    
    maxI,maxIM,maxV,maxL = process_file_PGN(file_name, functGame)
    if maxI<=0:
        print('--- no games ---')
        return
    print("--- best: ---")
    print(maxI,"\t",maxIM,"\t",maxV,'\t', maxL)
    hist=_parse_single_pgn(maxL)
    i=0
    for pos,move in hist:
        i=i+1
        if i==maxIM:
            sunfish.print_pos(pos)
            break

if __name__ == '__main__':
    main()

"""
maxI,maxIM,maxV,maxL = process_file_PGN('/home/user2/Programming/Python project/chess analyzer/lichess_The-Alexey_2022-04-22.pgn' )
print("--- best: ---")
print(maxI,"\t",maxIM,"\t",maxV,'\t', maxL)
hist=_parse_single_pgn(maxL)
i=0
for pos,move in hist:
   i=i+1
   if i==maxIM:
       sunfish.print_pos(pos)
       break


----------------------
1258     44      8      1. b3 e5 2. Ba3 Bxa3 3. Nxa3 d6 4. e4 f6 5. d3 Nc6 6. f3 Nd4 7. Qd2 Nh6 8. O-O-O O-O 9. h4 Nf7 10. c3 Ne6 11. d4 exd4 12. cxd4 d5 13. e5 fxe5 14. dxe5 Nxe5 15. h5 h6 16. Re1 Nc6 17. g3 d4 18. Bh3 Qd5 19. Nc4 Ng5 20. Bxc8 Raxc8 21. Rh4 Nxf3 22. Rf4 Nxd2 23. Kxd2 Rxf4 24. gxf4 Nb4 25. Nf3 Qxf3 26. Re7 Qxf4+ 27. Ke2 Nxa2 28. Ne5 Nc3+ 29. Ke1 1-0

_parse_single_pgn('1. b3 e5 2. Ba3 Bxa3 3. Nxa3 d6 4. e4 f6 5. d3 Nc6')
_parse_single_pgn('1. e4 e5 2. f4 exf4 3. Nf3 g5 4. Bc4 Bg7 5. h4 h6 6. hxg5 hxg5 7. Rxh8 Bxh8 8. d4 g4')
1.e4 e5 2.f4 exf4 3.Nf3 g5 4.Bc4 Bg7 5.h4 h6 6.hxg5 hxg5 7.Rxh8 Bxh8 8.d4 g4
9.Bxf4 gxf3 10.Qxf3 Qe7 11.c3 Nf6 12.Nd2 d5 13.Bd3 dxe4 14.Nxe4 Nxe4 15.Qxe4 Qxe4+
16.Bxe4 c6 17.Kd2 Be6 18.b3 Nd7 19.Rh1 Bf6 20.Kc2 O-O-O 21.Bd6 Nb6 22.Bc5 Kc7
23.Rh7 Rh8 24.c4 Rxh7 25.Bxh7 Nd7 26.Kd3 Nxc5+ 27.dxc5 Be7 28.b4 a6 29.a3 f5
30.Bg6 Kd7 31.Bh5 Bg5 32.Bd1 Bc1 33.Ba4 Bxa3 34.Kc3 Bc1 35.Bd1 Bf4 36.Kd4 Ke7
37.b5 Kf6 38.Bf3 Bd7 39.b6 Bg3 40.Bd1 Bh4 41.Ke3 Ke5 42.Bf3 Bf2+ 43.Kd3 Bxc5
44.Kc3 Bxb6  0-1


1.e4 e5 2.f4 exf4 3.Nf3 g5 4.Bc4 Bg7 5.h4 h6 6.hxg5 hxg5 7.Rxh8 Bxh8 8.d4 g4
msans = [part for part in ('1.e4 e5 2.f4 exf4 3.Nf3 g5 4.Bc4 Bg7 5.h4 h6 6.hxg5 hxg5 7.Rxh8 Bxh8 8.d4 g4'.split()) if not part[0].isdigit()]
re.sub('{.*?}', '', ' '.join('1.e4 e5 2.f4 exf4 3.Nf3 g5 4.Bc4 Bg7 5.h4 h6 6.hxg5 hxg5 7.Rxh8 Bxh8 8.d4 g4')).split()
import re
def _parse_single_pgnX(lines):
    parts = lines.split() #re.sub('{.*?}', '', ' '.join(lines)).split()

    l = list(map(lambda x: x.replace('Pant', 'Ishan'), l)) # некоторые форматы без пробелов "1.e4"
    msans = [part for part in parts if not part[0].isdigit()]
    for i in range(len(parts)):
       # replace hardik with shardul
       s=parts[i]
       dotP=s.index('.')
        if s.[0].isdigit() and ('.' in s and s.index('.')<len(s)):
            parts[i] = 'Shardul'
  https://www.pythontutorial.net/python-regex/python-regex-split/
  import re
s = 'A! B. C D'
pattern = r'\W+'
l = re.split(pattern, s, 2)
print(l)
re.split(r'[0-9]', '1.a4 b2', 2)
re.split(r'^[0-9].| ', '1.a4 b2', 2)
  
    msans = [part for part in parts if not part[0].isdigit() and len(part)>0]
    pos0 = tools.parseFEN(tools.FEN_INITIAL)
    for msan in msans:
        #print("msan is \"", msan,"\"")
        try:
            move = tools.parseSAN(pos0, msan)
            #print("move is ", move)
        except AssertionError:
            print('PGN was:', ' '.join(lines))
            raise
        #yield pos0, move
        pos0 = pos0.move(move)
        print("move:",move)

maxI,maxIM,maxV,maxL = process_file_PGN('/home/user2/Programming/Python project/chess analyzer/lichess_The-Alexey_2022-04-17 (1).pgn' )

scanAll(_parse_single_pgn('1. e3 e5 2. g3 d5 3. c3 f5 4. a4 Nc6 5. b3 Be6 6. Ba3 Bxa3 7. Nxa3 d4 8. Bd3 dxe3 9. dxe3 e4 10. Bc4 Qxd1+ 11. Rxd1 Rd8 12. Bxe6 Rxd1+ 13. Kxd1 Nd8 14. Ne2 Nxe6 15. h4 Nc5 16. Kc2 Nd3 17. Rd1 Nf6 18. f4 Ng4 19. h5 Ngf2 20. Kd2 Ke7 21. Rf1 Rd8 22. Kc2 g6 23. Nb5 gxh5 24. Nxc7 Rc8 25. Nb5 a6 26. Na7 Rc7 27. b4 b6 28. Nd4 Rxa7 29. Nc6+ Kd7 30. Nxa7 Kc7 31. c4 Kb7 32. Nb5 axb5 33. axb5 Nxb4+ 34. Kb3 Nfd3 35. Ra1 h4 36. gxh4 Kc7 37. Rg1 Kd7 38. Rg7+ Kd6 39. Rxh7 Kc5 40. Rc7+ Nc6 41. bxc6 Kd6 42. Rc8 Nc5+ 43. Kb4 Nd3+ 44. Kb5 Nc5 45. Kxb6 Na4+ 46. Kb5 Nc5 47. c7 Nb7 48. Rd8+ Kxc7 49. Rf8 Nd6+ 50. Kb4 Kc6 51. h5 Kd7 52. h6 Ke7 53. Ra8 Nf7 54. h7 Kf6 55. Ra7 Kg6 56. Rxf7 Kxf7 57. h8=Q Kg6 58. Qe8+ Kh6 59. Qe5 Kh5 60. Qxf5+ Kh4 61. Qxe4 Kg3 62. c5 Kf2 63. c6 Ke2 64. c7 Kd2 65. c8=R Ke2 66. f5 Kf2 67. f6 Ke2 68. f7 Ke1 69. f8=Q Kd1 70. Qd4+ Ke2 71. e4 Ke1 72. Qf3 1/2-1/2'))

scanAll(_parse_single_pgn('1. e3 e5 2. g3 d5 3. c3 f5 4. a4 Nc6 5. b3 Be6 6. Ba3 Bxa3 7. Nxa3 d4 8. Bd3 dxe3 9. dxe3 e4 10. Bc4 Qxd1+ 11. Rxd1 Rd8 12. Bxe6 Rxd1+ 13. Kxd1 Nd8 14. Ne2 Nxe6 15. h4 Nc5 16. Kc2 Nd3 17. Rd1 Nf6 18. f4 Ng4 19. h5 Ngf2 20. Kd2 Ke7 21. Rf1 Rd8 22. Kc2 g6 23. Nb5 gxh5 24. Nxc7 Rc8 25. Nb5 a6 26. Na7 Rc7 27. b4 b6 28. Nd4 Rxa7 29. Nc6+ Kd7 30. Nxa7 Kc7 31. c4 Kb7 32. Nb5 axb5 33. axb5 Nxb4+ 34. Kb3 Nfd3 35. Ra1 h4 36. gxh4 Kc7 37. Rg1 Kd7 38. Rg7+ Kd6 39. Rxh7 Kc5 40. Rc7+ Nc6 41. bxc6 Kd6 42. Rc8 Nc5+ 43. Kb4 Nd3+ 44. Kb5 Nc5 45. Kxb6 Na4+ 46. Kb5 Nc5 47. c7 Nb7 48. Rd8+ Kxc7 49. Rf8 Nd6+ 50. Kb4 Kc6 51. h5 Kd7 52. h6 Ke7 53. Ra8 Nf7 54. h7 Kf6 55. Ra7 Kg6 56. Rxf7 Kxf7 57. h8=Q Kg6 58. Qe8+ Kh6 59. Qe5 Kh5 60. Qxf5+ Kh4 61. Qxe4 Kg3 62. c5 Kf2 63. c6 Ke2 64. c7 Kd2 65. c8=R Ke2 66. f5 Kf2 67. f6 Ke2 68. f7 Ke1 69. f8=Q Kd1 70. Qd4+ Ke2 71. e4 Ke1 72. Qf3 1/2-1/2')) #todo не работает парсинг из-за c8=R "AssertionError: Sunfish only supports queen promotion in c8=R"

scanAll(_parse_single_pgn('1. e4 a5 2. d4 b6 3. d5 Ba6 4. Bxa6 Rxa6 5. c4 e6 6. Nf3 exd5 7. exd5 d6 8. Ng5 Be7 9. h4 Nh6 10. Qf3 O-O 11. O-O Qd7 12. Qd3 f6 13. Qxh7# 1-0'))

1. e3 e5 2. g3 d5 3. c3 f5 4. a4 Nc6 5. b3 Be6 6. Ba3 Bxa3 7. Nxa3 d4 8. Bd3 dxe3 9. dxe3 e4 10. Bc4 Qxd1+ 11. Rxd1 Rd8 12. Bxe6 Rxd1+ 13. Kxd1 Nd8 14. Ne2 Nxe6 15. h4 Nc5 16. Kc2 Nd3 17. Rd1 Nf6 18. f4 Ng4 19. h5 Ngf2 20. Kd2 Ke7 21. Rf1 Rd8 22. Kc2 g6 23. Nb5 gxh5 24. Nxc7 Rc8 25. Nb5 a6 26. Na7 Rc7 27. b4 b6 28. Nd4 Rxa7 29. Nc6+ Kd7 30. Nxa7 Kc7 31. c4 Kb7 32. Nb5 axb5 33. axb5 Nxb4+ 34. Kb3 Nfd3 35. Ra1 h4 36. gxh4 Kc7 37. Rg1 Kd7 38. Rg7+ Kd6 39. Rxh7 Kc5 40. Rc7+ Nc6 41. bxc6 Kd6 42. Rc8 Nc5+ 43. Kb4 Nd3+ 44. Kb5 Nc5 45. Kxb6 Na4+ 46. Kb5 Nc5 47. c7 Nb7 48. Rd8+ Kxc7 49. Rf8 Nd6+ 50. Kb4 Kc6 51. h5 Kd7 52. h6 Ke7 53. Ra8 Nf7 54. h7 Kf6 55. Ra7 Kg6 56. Rxf7 Kxf7 57. h8=Q Kg6 58. Qe8+ Kh6 59. Qe5 Kh5 60. Qxf5+ Kh4 61. Qxe4 Kg3 62. c5 Kf2 63. c6 Ke2 64. c7 Kd2 65. c8=R Ke2 66. f5 Kf2 67. f6 Ke2 68. f7 Ke1 69. f8=Q Kd1 70. Qd4+ Ke2 71. e4 Ke1 72. Qf3 1/2-1/2

-------------------------

"""
