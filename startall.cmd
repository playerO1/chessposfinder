rem Warning: ToDo this script was not tested. Bee carefull.
@echo off

:lbl_start_new
if %1.==. goto lbl_end
echo scan: %1
rem todo: counter vis set command for log name
start python3 .\sunfish\chessposfinder.py %1 > proc_log_%1_chess.txt

shift
goto lbl_start_new

:lbl_end
echo all subprocess started.
