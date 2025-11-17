#!/bin/bash

# 核心配置参数（无需修改，保持原有效配置）
SERVER="https://emby.na.org/emby"
TOKEN="097f93fb9b0b4e6"
DEVICE_ID="4148654b-f8f5-40b3-95a1-8360115c6d44"
ITEM_ID="190687"
MEDIA_SOURCE_ID="mediasource_190687"
LOG_FILE="./emby_checkin.log"

# 新增：日志清理配置（保留最近30天的日志）
LOG_RETENTION_DAYS=10  # 可根据需要修改天数

# PushDeer 配置（已改为可用的服务器）
PUSHDEER_KEY="PDU24090TPIMPFah7knPo1xPDN1"  # 务必替换为你的实际密钥
PUSHDEER_SERVER="https://api2.pushdeer.com"  # 测试可用的服务器

# 生成随机32位播放会话ID（兼容无openssl的环境）
PLAY_SESSION_ID=$(openssl rand -hex 16 || date +%s%N | md5sum | cut -c1-32)

# 构建Emby认证头
AUTH="MediaBrowser Client=\"Emby Web\", Device=\"$DEVICE_ID\", Version=\"4.9.1.80\", Token=\"$TOKEN\""

# 日志函数（记录执行过程）
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 新增：清理过期日志（仅保留最近指定天数的内容）
cleanup_log() {
    if [ -f "$LOG_FILE" ]; then
        # 备份并保留最近30天的日志（利用awk按日期筛选）
        awk -v days="$LOG_RETENTION_DAYS" '
            BEGIN {
                # 计算30天前的时间戳（秒）
                cutoff = systime() - days * 86400
            }
            {
                # 提取日志中的日期（格式：[YYYY-MM-DD ...]）
                if (match($0, /^\[([0-9]{4}-[0-9]{2}-[0-9]{2})/, arr)) {
                    # 将日期转换为时间戳
                    cmd = "date -d \"" arr[1] "\" +%s"
                    cmd | getline ts
                    close(cmd)
                    # 保留30天内的日志
                    if (ts >= cutoff) print $0
                } else {
                    # 保留无日期的行（极少情况）
                    print $0
                }
            }
        ' "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
        log "已清理$LOG_RETENTION_DAYS天前的日志"
    fi
}


# PushDeer通知函数（URL编码+调试输出，确保送达）
send_notification() {
    local title="$1"
    local message="$2"
    
    # 对标题和内容进行URL编码，避免特殊字符导致失败
    encoded_title=$(echo "$title" | curl -Gso /dev/null -w %{url_effective} --data-urlencode @- "" | cut -c 3-)
    encoded_message=$(echo "$message" | curl -Gso /dev/null -w %{url_effective} --data-urlencode @- "" | cut -c 3-)
    
    # 发送通知并记录调试信息
    echo "--- 发送PushDeer通知 ---"
    log "发送通知：标题=$title，内容=$message"
    response=$(curl -s -w "HTTP状态码: %{http_code}\n" \
        -X POST "${PUSHDEER_SERVER}/message/push" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "pushkey=${PUSHDEER_KEY}&text=${encoded_title}&desp=${encoded_message}")
    
    # 输出响应结果（方便排查问题）
    echo "通知响应：$response"
    log "通知响应：$response"
}

# 脚本主执行流程
log "===== Emby自动签到开始 ====="
echo "=== 启动Emby自动签到 === $(date +'%Y-%m-%d %H:%M:%S')"

# 新增：执行日志清理
cleanup_log

# 发送启动通知（可选，怕打扰可注释）
send_notification "Emby签到启动" "今日自动签到流程已开始"

# 第一步：模拟播放进度
log "发送播放进度请求（会话ID=$PLAY_SESSION_ID）"
echo "--- 模拟播放进度 ---"
response=$(curl -s -w "%{http_code}" -X POST "$SERVER/Sessions/Playing/Progress" \
  -H "X-Emby-Authorization: $AUTH" \
  -H "Content-Type: application/json" \
  -d "{
        \"ItemId\": \"$ITEM_ID\",
        \"MediaSourceId\": \"$MEDIA_SOURCE_ID\",
        \"PlaySessionId\": \"$PLAY_SESSION_ID\",
        \"PositionTicks\": 20000000,
        \"IsPaused\": false,
        \"PlayMethod\": \"DirectStream\"
      }")

http_code=${response: -3}
response_body=${response%???}

# 检查播放进度请求是否失败
if [ "$http_code" -ne 200 ] && [ "$http_code" -ne 204 ]; then
    error_msg="播放进度请求失败：状态码$http_code，响应=$response_body"
    log "$error_msg"
    echo "错误：$error_msg"
    send_notification "Emby签到失败" "$error_msg"
    exit 1
elif echo "$response_body" | grep -qi "error"; then
    error_msg="播放进度请求返回错误：$response_body"
    log "$error_msg"
    echo "错误：$error_msg"
    send_notification "Emby签到失败" "$error_msg"
    exit 1
fi

# 模拟真实播放延迟（1.5秒更自然）
sleep 1.5

# 第二步：模拟停止播放
log "发送停止播放请求"
echo "--- 模拟停止播放 ---"
response=$(curl -s -w "%{http_code}" -X POST "$SERVER/Sessions/Playing/Stopped" \
  -H "X-Emby-Authorization: $AUTH" \
  -H "Content-Type: application/json" \
  -d "{
        \"ItemId\": \"$ITEM_ID\",
        \"MediaSourceId\": \"$MEDIA_SOURCE_ID\",
        \"PlaySessionId\": \"$PLAY_SESSION_ID\",
        \"PositionTicks\": 25000000
      }")

http_code=${response: -3}
response_body=${response%???}

# 检查停止播放请求是否失败
if [ "$http_code" -ne 200 ] && [ "$http_code" -ne 204 ]; then
    error_msg="停止播放请求失败：状态码$http_code，响应=$response_body"
    log "$error_msg"
    echo "错误：$error_msg"
    send_notification "Emby签到失败" "$error_msg"
    exit 1
elif echo "$response_body" | grep -qi "error"; then
    error_msg="停止播放请求返回错误：$response_body"
    log "$error_msg"
    echo "错误：$error_msg"
    send_notification "Emby签到失败" "$error_msg"
    exit 1
fi

log "===== 今日签到成功 ====="
echo "=== 签到成功！可在Emby查看观看记录 ==="
# 可选：发送成功通知（建议保留，确认脚本正常运行）
send_notification "Emby签到成功" "今日自动签到已完成，记录已生成"
