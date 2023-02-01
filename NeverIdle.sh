#!/bin/bash

#启动NeverIdle
function startNeverIdle(){
    #变量screen名称
	screen_name1="oracleZY"
	#变量命令 cmd1="browsh"
	killall -9 NeverIdle
	#创建screen但不进入
	killall screen
	screen -dmS $screen_name1
	#执行指令、输入回车分割。
	screen -x -S $screen_name1 -p 0 -X stuff "/home/NeverIdle -c 2h -m 2 -n 4h"
	screen -x -S $screen_name1 -p 0 -X stuff '\n' 
}

#ps -ef |grep NeverIdle 这个就是看NeverIdle的启动情况
#grep -v "grep" 是为了去掉查询 grep的那一条
#wc -l 是计数的

if ! screen -list | grep -q "oracleZY"; then
        echo "-----NeverIdle没运行-----"
	startNeverIdle
else
        echo "-----NeverIdle已经运行-----"
fi




