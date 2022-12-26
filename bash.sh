#! /bin/bash
cd /home/TGMusic
screen -S TGMusic -X multiuser on
screen -S TGMusic -X acladd support
source venvBOT/bin/activate
# shellcheck disable=SC2160
while [ true ]
do
python3 main.py
done
echo "Shit case happened"