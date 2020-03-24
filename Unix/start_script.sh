FILE=save_pid.txt
if [ -f "$FILE" ] ; then
    echo "$FILE exists, kill older bot first!"
    exit 0
fi
nohup python3 repeat.py > logs.out 2>&1 &
echo $! > save_pid.txt