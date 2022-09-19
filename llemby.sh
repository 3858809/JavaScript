#!/bin/bash
echo -e `date '+%Y-%m-%d %H:%M:%S %A'` "\n后台进程杀死firefox" >> /home/llemby_log.txt
pkill firefox 
echo -e `date '+%Y-%m-%d %H:%M:%S %A'` "\n后台进程杀死browsh" >> /home/llemby_log.txt
pkill browsh
echo -e `date '+%Y-%m-%d %H:%M:%S %A'` "\n开始浏览网页pornemby.club/web/index.html#!/home" >> /home/llemby_log.txt
browsh https://pornemby.club/web/index.html#!/home
