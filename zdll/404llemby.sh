#!/bin/bash
#变量screen名称
screen_name1="zdll"
#变量命令 cmd1="browsh" 
pkill firefox 
pkill browsh 
#screen -S zdll -X quit 
#创建screen但不进入
echo -e `date '+%Y-%m-%d %H:%M:%S %A'` "\n执行脚本开始" >> /home/404llemby.txt 
killall screen
screen -dmS $screen_name1
#执行指令、输入回车分割。
screen -x -S $screen_name1 -p 0 -X stuff "browsh https://404.sb/web/index.html" 
screen -x -S $screen_name1 -p 0 -X stuff '\n' 
sleep 10
#screen -x -S $screen_name1 -p 0 -X stuff '\003' #\003代表 ctrl+c
#screen -S zdll -X quit 
killall screen
echo -e `date '+%Y-%m-%d %H:%M:%S %A'` "\n执行脚本结束" >> /home/404llemby.txt
