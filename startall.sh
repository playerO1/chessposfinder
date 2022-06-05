#/bin/sh 

# Run chessposfinder.py with many files as different process,
# put output from console to log file's

# input param 1: path with PGN files
# output: proc_log[N]_chess.txt
#start subprocess, TODOwait till all finish

echo scan all: $1 $2 


declare counter=0
#for entry in $(find $1 -maxdepth 1 -type f -name '*.pgn'); do
find "$1" -maxdepth 1 -type f -name '*.pgn' -print0 | 
while IFS= read -r -d '' entry; do
#for entry in "$@"; do
        
   echo "$(( counter += 1 )): '$entry'" 
   python3 ./sunfish/chessposfinder.py "$entry" > proc_log$(( counter ))_chess.txt &
   ROUTINE_PID=$! # Запоминаем PID подоболочки, запущенной в параллель
   echo "Run routine with pid=$ROUTINE_PID"
done

echo Wait all jobs..
jobs
jobs -l
wait
echo All jobs was done
