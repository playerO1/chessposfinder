#
# Chess find interesting games, collect game stats. Database tool for : import andexport local database, for fast find games.
# (C) A.K. 2022 
# 22.05.2022, 27.11.2022
#


import tools
from tools import WHITE, BLACK
import sunfish




# ---------- my logic ------------

# find position with max value of funct()

def scanMaxLength(hist): # wery long game
    i=0
    for p,m in hist:
        i=i+1
    return i,i

def match_disbalance(pos):
    price={'p':1,'r':4,'n':3,'b':3,'q':5,'k':0,   'P':-1,'R':-4,'N':-3,'B':-3,'Q':-5,'K':0, }
    # tools.get_color(pos)
    # sunfish.piece
    v=0
    for i, p in enumerate(pos.board):
        #if not p.isupper(): continue
        if p in price:
            v = v + price[p]
    #print("debug v=",v," color=",tools.get_color(pos)," pos=", pos)
    return v

def aggregate_count(pos, swapColor):
    count={'p':0,'r':0,'n':0,'b':0,'q':0,'k':0,   'P':0,'R':0,'N':0,'B':0,'Q':0,'K':0 }
    for i, p in enumerate(pos.board):
        #if not p.isupper(): continue
        if not p in count: continue # OR count[p]=0
        if swapColor:
            p = p.swapcase() #if p.isupper(): p = p.casefold() else: p = p.capitalize()
        count[p]=count[p]+1
    #print("debug v=",v," color=",tools.get_color(pos)," pos=", pos)
    return count
    
def scanFinishPosition(hist, funct): # the last game position
    lastI=0
    lastP=None
    for p,m in hist:
        lastI=lastI+1
        lastP = p
    #return lastP,lastI
    if lastP==None: return 0, 0
    v = funct(lastP, lastI%2==1)
    return v, lastI

def plasMapByKey(a,b):
    #import collections, functools, operator
    #s = dict(functools.reduce(operator.add,map(collections.Counter, [a, b])))
    s = {}
    for k in (a.keys() | b.keys()):
        s[k] = a.get(k, 0) + b.get(k, 0)
    return s

def scanCoastSumm(hist): # aggregate_count summ of all
    lastI=0
    lastMS=None
    for p,m in hist:
        ms=aggregate_count(p, lastI%2==1)
        if lastI==0: #lastMS==None:
            lastMS = ms
        else:
            lastMS = plasMapByKey(lastMS, ms)
        lastP = p
        lastI=lastI+1
    return lastMS, lastI

def scanMoveCount(hist):
    count={'p':0,'r':0,'n':0,'b':0,'q':0,'k':0,   'P':0,'R':0,'N':0,'B':0,'Q':0,'K':0 }
    lastI=0
    for p,m in hist:
        f=p.board[m[0]]
        #print("test",p,m,f)
        if not f in count: raise Error("Wring figure "+f+" at "+m) #continue # OR count[p]=0
        swapColor = lastI%2==1
        if swapColor:
            f = f.swapcase()
        count[f]=count[f]+1
        lastI=lastI+1
    return count, lastI

# --------------------------


#-------- improvement sunfish tool ---------

# maked by rewrite tools.py (sunfish)
#import re
def _parse_single_pgn(lines):
    #TODO lichessformat: "1. e4 b6 2. d4 d6 3. Nc3" but can be another format: "1.e4 b6 2.d4 d6 3.Nc3" - to do work with him.
    #if (parts.substring(1,3)!="1. "...parts
    parts = lines.split() #re.sub('{.*?}', '', ' '.join(lines)).split()
    msans = [part for part in parts if not part[0].isdigit()]
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
        pos0 = pos0.move(move)


# struct: gdata (line:int,name_W,name_B,elo_W:int,elo_B:int,result:int(-1/0/+1),pgn:String, value_?...)
class GData:
    line:int=None
    name_W=None
    name_B=None
    elo_W:int=0
    elo_B:int=0
    result=None
    pgn=None # 0,-1 black, +1 white
    length:int=0
    data=None # map{}
    def toMap(self):
        m={'line':self.line,'name_W':self.name_W,'name_B':self.name_B,'elo_W':self.elo_W,'elo_B':self.elo_B,'result':self.result,'length':self.length,'pgn':self.pgn}
        if self.data!=None:
            m = dict(m.items() | self.data.items()) #  + same as |  . TODO add 'var_' prefix
        return m


def game_filter(gdata:GData):
    if (abs( gdata.elo_W-gdata.elo_B)>200): return False
    if ((gdata.elo_W+gdata.elo_B)/2<600): return False
    if (len(gdata.pgn)<10): return False
    #if (time_control > 30)
    #if (gdata.result==0): return False
    return True

import re #reg expression
def parse_game_data(meta_str, lineN:int, pgn_str):
    gdata=GData()
    gdata.line=lineN
    gdata.pgn=pgn_str.replace('\r\n', ' ').replace('\n\r', ' ') #TODO space or empty for new line? It may be trouble when parsed next
    #print("debug PGN:", gdata.pgn)
    #s='[White "hadwao"]'
    if match := re.search('\[White "(.*)"\]', meta_str, re.IGNORECASE):
        gdata.name_W = match.group(1)
    if match := re.search('\[Black "(.*)"\]', meta_str, re.IGNORECASE):
        gdata.name_B = match.group(1)
    if match := re.search('\[WhiteElo "(.*)"\]', meta_str, re.IGNORECASE):
        eloS = match.group(1)
        if '?' == eloS or ''== eloS:
            gdata.elo_W = -1
        else:
            gdata.elo_W = int(eloS)
    if match := re.search('\[BlackElo "(.*)"\]', meta_str, re.IGNORECASE):
        eloS = match.group(1)
        if '?' == eloS or ''== eloS:
            gdata.elo_B = -1
        else:
            gdata.elo_B = int(eloS)
    #[Termination "Normal"] [Termination "Time forfeit"]
    #[Result "1-0"] - in comment or PGN.
    if match := re.search('\[Result "(.*)"\]', meta_str, re.IGNORECASE):
        gres=match.group(1)
        if (gres=="1-0"): gdata.result = 1#WHITE
        elif (gres=="0-1"): gdata.result = -1#BLACK
        elif (gres=="1/2-1/2"): gdata.result = 0
        else:
            print("Warn undefined result:", gres)
            gdata.result = gres
    #print("META LIKE:", meta_str)
    #print("line ", gdata.line," white:" ,gdata.name_W," ",gdata.elo_W," black:" ,gdata.name_B," ",gdata.elo_B," result=",gdata.result )
    return gdata

# funct: val, moveI = scanAll(hist, funct)
# return yield gdata
def process_file_PGN(file_name, funct):
    lI=0
    current_game_meta = ""
    current_pgn_multiline = ""
    prev_meta=False
    #print("line\tmove\tvalue")
    #maxL=None
    total_games_success=0
    total_games_errors=0
    
    with open(file_name, newline='') as lines:
        for line in lines:
            lI=lI+1
            #print(lI)#,'="',line,'"', len(line))
            has_empty=False
            if line.startswith('['):
                current_game_meta = current_game_meta + line
                prev_meta=True
                if (len(current_pgn_multiline)>1):
                    raise# new Error("Wrong line pgn format. Not finish parsed: "+current_pgn_multiline)
            elif len(line)<3 or not line[0].isdigit():
                has_empty=True;
                #pass
            else:
                if len(current_pgn_multiline)>0:
                    current_pgn_multiline=current_pgn_multiline+" "
                current_pgn_multiline = current_pgn_multiline + line #for multiline

            if (has_empty and len(current_pgn_multiline)>1): #TODO if end line is not empty?
                #if len(line)<6: continue # сразу сдались
                #if not('1-0' in line or '0-1' in line): continue # без ничьих
                gdata = parse_game_data(current_game_meta, lI, current_pgn_multiline);
                #print("debug PGN game:", gdata.pgn)
                current_pgn_multiline=""
                has_empty=False
                if prev_meta:
                    current_game_meta=""
                    prev_meta=False
                if not game_filter(gdata): #TODO add filter function form param
                    continue
                try:
                    hist=_parse_single_pgn(gdata.pgn)
                    val, moveI = funct(hist) #scanAll(hist, funct)
                    #gdata.data=funct(hist) #scanAll(hist, funct)
                    gdata.data=val
                    gdata.length=moveI
                    print("success line {0}".format(lI-1))
                    yield gdata

#                    if prev_meta:
#                        current_game_meta=""
#                        prev_meta=False
                    total_games_success=total_games_success+1
                    #maxL=line
                except AssertionError as err:
                    print("Error parse line {0} cause {1}".format(lI-1, err))
                    total_games_errors=total_games_errors+1
                if prev_meta:
                    current_game_meta=""
                    prev_meta=False
    print("--- End of file, processed {0} games + error parsing {1} games ---".format(total_games_success, total_games_errors))


# parser, filter, file-maker


#-----------------

import csv
def main():
    import sys
    import os
    if len(sys.argv)!=3:
        print("Required PGN file. Use python myposfinder.py path/to_file.pgn")
        return
    file_name_pgn=sys.argv[1]
    if not os.path.isfile(file_name_pgn):
        print("Required PGN file. File not found: ", file_name_pgn)
        return
    file_name_out=sys.argv[2]
    print("--- PGN file:",file_name_pgn,"  out:",file_name_out," ---")

    #The sort of collect data of the game:    
    #functGame=lambda hist: scanFinishPosition(hist, aggregate_count) # get last position, count of figure
    functGame=scanCoastSumm # scan all positions, average figure by timeline
    #functGame=scanMoveCount

    resultIter = process_file_PGN(file_name_pgn, functGame)
    
    firstRow=True
    with open(file_name_out, 'w', newline='') as csvfile:
        #out_writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        c_writer = None # csv.DictWriter(csvfile, fieldnames=fieldnames)
        for gdata in resultIter:
            #print("line ", gdata.line," white:" ,gdata.name_W," ",gdata.elo_W," black:" ,gdata.name_B," ",gdata.elo_B, "result=",gdata.result, " PGN=",gdata.pgn, " data=",gdata.data )
            #print("line: ", gdata.toMap() )
            row=gdata.toMap()
            if firstRow:
                # header
                c_writer = csv.DictWriter(csvfile, fieldnames=row.keys())
                c_writer.writeheader()
                firstRow = False
            c_writer.writerow(row)
            #spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])


        
    print("--- finish ---")

if __name__ == '__main__':
    main()



#Excel/OpenOffice: https://wiki.openoffice.org/wiki/Documentation/How_Tos/Calc:_LINEST_function
#LINEST(yvalues; xvalues; allow_const; stats) =ЛИНЕЙН(C$2:C$5;A$2:B$5;1;1)  Ctrl+Shift+Enter
#ЛИНЕИН()...
#Legend: P-пешка, R-ладья, N-конь, B - офицер, Q - ферзь, K - король , большие буквы - белые, 
#in sunfish.py: piece = { 'P': 100, 'N': 280, 'B': 320, 'R': 479, 'Q': 929, 'K': 60000 }
# PPPPPPPP\n'  #  80 - 89
# RNBQKBNR
