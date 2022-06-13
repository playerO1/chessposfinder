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

# find position with max value of funct()
def scanAllPosition(hist,end_is, funct): # hist=_parse_single_pgn(gameFEN), funct=match_koef_razmen_any(pos)
    i=0
    maxV=float('-inf')
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
    price={ 'p':1,'r':4,'n':3,'b':3,'q':5,'k':0,   'P':-1,'R':-4,'N':-3,'B':-3,'Q':-5,'K':0 }
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

def scanLastNPosition(hist,end_is, funct, n:int=1): # hist=_parse_single_pgn(gameFEN), funct=match_koef_razmen_any(pos)
    maxV=float('-inf')
    maxI=0
    lastNP=[]
    size=0
    for p,m in hist:
        size=size+1
        lastNP.append(p)
        if len(lastNP)>n: lastNP.pop(0)
    i=size-len(lastNP)
    #print(i, " ", size, len(lastNP))
    for p in lastNP:
        i=i+1
        val=funct(p,end_is)
        if val>maxV:
            maxV=val
            maxI=i
    #print("max=",maxV," at ", maxI)
    return maxV, maxI

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


# funct(hist, end_is): val, moveI = scanAll(hist, funct)
def process_file_PGN(file_name, funct, ignore_withdraw=False):
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
    with open(file_name, newline='') as lines: #fixme UnicodeDecodeError: 'utf-8' codec can't decode byte 0xed in position 1055: invalid continuation    byte    open(filename, encoding="latin-1") ?
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
                try:
                    end_is = _parse_single_pgn_result(line)
                    if ignore_withdraw and end_is==3: continue # без ничьих
                    hist=_parse_single_pgn(line)
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
    
    #functGame=lambda hist, end_is: scanFinishPosition(hist, end_is, match_disbalance)
    functGame=lambda hist, end_is: scanLastNPosition(hist, end_is, match_disbalance, 8)
    
    
    maxI,maxIM,maxV,maxL = process_file_PGN(file_name, functGame) #, ignore_withdraw=True
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
