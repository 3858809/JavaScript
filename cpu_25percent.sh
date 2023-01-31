cpuq=$(lscpu | awk '/^CPU\(/{print $NF*100/4}');
[ -d "/opt/oracle25cpu" ] || mkdir -p /opt/oracle25cpu;
cat << eof > /opt/oracle25cpu/cpu.sh;
cpuc=$(lscpu | awk '/^CPU\(/{print $NF}');
for ((i=0;i<cpuc;i++))
do
    {
        dd if=/dev/zero of=/dev/null
    } &
done
wait
eof

cat << eof > /lib/systemd/system/cpur.service
[Unit]
Description=cpu stress 25 percents
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash /opt/oracle25cpu/cpu.sh
CPUQuota=${cpuq}%

[Install]
WantedBy=multi-user.target
eof

systemctl daemon-reload;
systemctl enable cpur --now;
systemctl restart cpur;
