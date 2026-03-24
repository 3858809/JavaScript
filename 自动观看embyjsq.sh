#!/bin/bash

# ===================== 核心配置（固定路径）=====================
SERVER="http://jsq.vban.x/emby"
DEVICE_ID="4148654b-f8f5-40b3-95a1-8360f75c6d22"
ITEM_ID="259603"
MEDIA_SOURCE_ID="mediasource_259603"
LOG_FILE="/home/embyqd/emby_checkin_jsq.log"
TOKEN_FILE="/home/embyqd/emby_token_jsq.dat"

# ===================== 登录配置（与浏览器抓包一致）=====================
EMBY_USERNAME="385"
EMBY_PASSWORD="cEW"
CLIENT_NAME="Emby Web"
DEVICE_NAME="Google Chrome Windows"
CLIENT_VERSION="4.9.0.60"
LANGUAGE="zh-cn"

# ===================== 关键：浏览器真实User-Agent（从你的抓包复制）=====================
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"


# ===================== 其他配置 =====================
LOG_RETENTION_DAYS=10
PUSHDEER_KEY="PDU24090TPIMPF"
PUSHDEER_SERVER="https://api2.pushdeer.com"

# 生成随机32位播放会话ID
PLAY_SESSION_ID=$(openssl rand -hex 16 || date +%s%N | md5sum | cut -c1-32)

# 日志函数
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# ===================== TOKEN文件操作函数 =====================
# 读取本地TOKEN
read_local_token() {
    if [ -f "$TOKEN_FILE" ]; then
        # 读取TOKEN并去除换行符/空格
        TOKEN=$(cat "$TOKEN_FILE" | tr -d '\n' | tr -d '\r' | tr -d ' ')
        if [ -n "$TOKEN" ] && [ "${#TOKEN}" -eq 32 ]; then  # 验证TOKEN长度（32位）
            log "从本地文件读取到TOKEN：${TOKEN:0:8}****"
            echo "已从本地读取TOKEN：${TOKEN:0:8}****"
            return 0
        else
            log "本地TOKEN文件内容无效（长度不符），将重新登录"
            echo "本地TOKEN无效，准备登录获取新TOKEN..."
            return 1
        fi
    else
        log "本地TOKEN文件不存在，将使用登录方式获取"
        echo "本地TOKEN文件不存在，准备登录获取新TOKEN..."
        return 1
    fi
}

# 保存TOKEN到本地
save_local_token() {
    local new_token="$1"
    if [ -n "$new_token" ] && [ "${#new_token}" -eq 32 ]; then
        # 写入TOKEN并设置文件权限为仅当前用户可读
        echo "$new_token" > "$TOKEN_FILE"
        chmod 600 "$TOKEN_FILE"
        log "已将新TOKEN保存到本地文件：$TOKEN_FILE"
        echo "新TOKEN已保存到本地文件：$TOKEN_FILE"
    else
        log "TOKEN无效（长度不符），保存失败"
        echo "错误：TOKEN无效，保存失败"
    fi
}

# ===================== 登录获取TOKEN函数 =====================
login_and_get_token() {
    log "开始尝试登录Emby账号（用户名：$EMBY_USERNAME）"
    echo "--- 开始登录Emby账号 ---"
    
    # 登录请求：添加真实User-Agent
    login_response=$(curl -s -w "HTTP_CODE:%{http_code}" \
        -A "$USER_AGENT" \
        -X POST "${SERVER}/Users/authenticatebyname" \
        -H "X-Emby-Client: $CLIENT_NAME" \
        -H "X-Emby-Device-Name: $DEVICE_NAME" \
        -H "X-Emby-Device-Id: $DEVICE_ID" \
        -H "X-Emby-Client-Version: $CLIENT_VERSION" \
        -H "X-Emby-Language: $LANGUAGE" \
        -H "Content-Type: application/x-www-form-urlencoded; charset=UTF-8" \
        -d "Username=$EMBY_USERNAME&Pw=$EMBY_PASSWORD")
    
    http_code=$(echo "$login_response" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
    response_body=$(echo "$login_response" | sed "s/HTTP_CODE:[0-9]*//g")
    
    log "登录响应状态码：$http_code"
    log "登录响应体：$response_body"
    echo "登录响应体：$response_body"
    
    if [ "$http_code" -ne 200 ]; then
        error_msg="登录失败：状态码$http_code，响应=$response_body"
        log "$error_msg"
        echo "错误：$error_msg"
        send_notification "Emby登录失败" "$error_msg"
        exit 1
    fi
    
    NEW_TOKEN=$(echo "$response_body" | grep -oE '"AccessToken":"[^"]+"' | cut -d'"' -f4)
    if [ -z "$NEW_TOKEN" ] || [ "$NEW_TOKEN" = "null" ]; then
        error_msg="登录成功但未获取到有效TOKEN，响应：$response_body"
        log "$error_msg"
        echo "错误：$error_msg"
        send_notification "EmbyTOKEN获取失败" "$error_msg"
        exit 1
    fi
    
    TOKEN="$NEW_TOKEN"
    save_local_token "$NEW_TOKEN"
    
    success_msg="登录成功！新TOKEN：${NEW_TOKEN:0:8}****（已保存到$TOKEN_FILE）"
    log "$success_msg"
    echo "成功：$success_msg"
    send_notification "Emby登录成功" "已获取新访问令牌并保存到本地：${NEW_TOKEN:0:8}****"
    
    AUTH="MediaBrowser Client=\"$CLIENT_NAME\", Device=\"$DEVICE_ID\", Version=\"$CLIENT_VERSION\", Token=\"$TOKEN\""
}


# ===================== 修复：TOKEN有效性检测函数 =====================
check_token_validity() {
    log "开始检测TOKEN有效性"
    echo "--- 检测TOKEN有效性 ---"
    
    # 如果TOKEN为空/无效，直接登录
    if [ -z "$TOKEN" ] || [ "${#TOKEN}" -ne 32 ]; then
        log "TOKEN为空或长度不符，直接进行登录"
        echo "TOKEN无效，准备登录..."
        login_and_get_token
        return 1
    fi
    
    # 改用更稳定的公共接口检测TOKEN（/System/Info/Public）
    # 该接口无需GUID，仅验证TOKEN是否有效
    check_response=$(curl -s -w "HTTP_CODE:%{http_code}" \
        -X GET "${SERVER}/System/Info/Public" \
        -H "X-Emby-Client: $CLIENT_NAME" \
        -H "X-Emby-Device-Name: $DEVICE_NAME" \
        -H "X-Emby-Device-Id: $DEVICE_ID" \
        -H "X-Emby-Client-Version: $CLIENT_VERSION" \
        -H "X-Emby-Language: $LANGUAGE" \
        -H "X-Emby-Authorization: MediaBrowser Client=\"$CLIENT_NAME\", Device=\"$DEVICE_ID\", Version=\"$CLIENT_VERSION\", Token=\"$TOKEN\"")
    
    # 分离状态码和响应体
    http_code=$(echo "$check_response" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
    check_body=$(echo "$check_response" | sed "s/HTTP_CODE:[0-9]*//g")
    
    log "TOKEN检测状态码：$http_code"
    log "TOKEN检测响应：$check_body"
    
    # 优化检测逻辑：仅在明确401时重新登录
    case "$http_code" in
        200)
            # TOKEN有效
            log "TOKEN有效，无需重新登录"
            echo "TOKEN有效，继续执行签到流程"
            return 0
            ;;
        401)
            # TOKEN过期/无效，重新登录
            log "TOKEN已过期（401未授权），需要重新登录"
            echo "TOKEN已过期，准备自动登录..."
            login_and_get_token
            return 1
            ;;
        *)
            # 其他错误（500/404等），不重新登录，直接尝试使用本地TOKEN签到
            log "TOKEN检测失败（状态码$http_code），跳过登录，直接使用本地TOKEN尝试签到"
            echo "TOKEN检测失败（$http_code），将直接使用本地TOKEN尝试签到..."
            # 构建认证头（使用本地TOKEN）
            AUTH="MediaBrowser Client=\"$CLIENT_NAME\", Device=\"$DEVICE_ID\", Version=\"$CLIENT_VERSION\", Token=\"$TOKEN\""
            return 0
            ;;
    esac
}

# 清理过期日志函数
cleanup_log() {
    if [ -f "$LOG_FILE" ]; then
        awk -v days="$LOG_RETENTION_DAYS" '
            BEGIN {
                cutoff = systime() - days * 86400
            }
            {
                if (match($0, /^\[([0-9]{4}-[0-9]{2}-[0-9]{2})/, arr)) {
                    cmd = "date -d \"" arr[1] "\" +%s"
                    cmd | getline ts
                    close(cmd)
                    if (ts >= cutoff) print $0
                } else {
                    print $0
                }
            }
        ' "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
        log "已清理$LOG_RETENTION_DAYS天前的日志"
    fi
}

# PushDeer通知函数
send_notification() {
    local title="$1"
    local message="$2"
    
    # 如果PushDeer Key未配置，跳过发送
    if [ -z "$PUSHDEER_KEY" ] || [ "$PUSHDEER_KEY" = "你的真实PushDeer密钥" ]; then
        log "PushDeer密钥未配置，跳过通知发送"
        echo "--- PushDeer密钥未配置，跳过通知发送 ---"
        return
    fi
    
    # URL编码
    encoded_title=$(echo "$title" | curl -Gso /dev/null -w %{url_effective} --data-urlencode @- "" | cut -c 3-)
    encoded_message=$(echo "$message" | curl -Gso /dev/null -w %{url_effective} --data-urlencode @- "" | cut -c 3-)
    
    # 发送通知
    echo "--- 发送PushDeer通知 ---"
    log "发送通知：标题=$title，内容=$message"
    response=$(curl -s -w "HTTP状态码: %{http_code}\n" \
        -X POST "${PUSHDEER_SERVER}/message/push" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "pushkey=${PUSHDEER_KEY}&text=${encoded_title}&desp=${encoded_message}")
    
    echo "通知响应：$response"
    log "通知响应：$response"
}

# ===================== 脚本主执行流程 =====================
log "===== 见手青播放开始 ====="
echo "=== 启动见手青播放 === $(date +'%Y-%m-%d %H:%M:%S')"

# 清理过期日志
cleanup_log

# 发送启动通知
send_notification "见手青播放启动" "今日自动签到流程已开始"

# 第一步：读取本地TOKEN
read_local_token

# 第二步：检测TOKEN有效性（修复后的逻辑）
check_token_validity

# 确保认证头使用最新TOKEN
if [ -z "$AUTH" ]; then
    AUTH="MediaBrowser Client=\"$CLIENT_NAME\", Device=\"$DEVICE_ID\", Version=\"$CLIENT_VERSION\", Token=\"$TOKEN\""
fi
log "当前使用的认证头：$AUTH"
echo "当前使用的TOKEN：${TOKEN:0:8}****"

# 第三步：模拟播放进度
log "发送播放进度请求（会话ID=$PLAY_SESSION_ID）"
echo "--- 模拟播放进度 ---"
response=$(curl -s -w "%{http_code}" -X POST "$SERVER/Sessions/Playing/Progress" \
  -H "X-Emby-Authorization: $AUTH" \
  -H "X-Emby-Client: $CLIENT_NAME" \
  -H "X-Emby-Device-Name: $DEVICE_NAME" \
  -H "X-Emby-Device-Id: $DEVICE_ID" \
  -H "X-Emby-Client-Version: $CLIENT_VERSION" \
  -H "Content-Type: application/json" \
  -d "{
        \"ItemId\": \"$ITEM_ID\",
        \"MediaSourceId\": \"$MEDIA_SOURCE_ID\",
        \"PlaySessionId\": \"$PLAY_SESSION_ID\",
        \"PositionTicks\": 600000000,
        \"IsPaused\": false,
        \"PlayMethod\": \"DirectStream\"
      }")

http_code=${response: -3}
response_body=${response%???}

log "播放进度请求状态码：$http_code"
log "播放进度请求响应：$response_body"

# 检查播放进度请求是否失败（如果失败，尝试登录后重试）
if [ "$http_code" -eq 401 ]; then
    log "播放进度请求401，TOKEN确实过期，重新登录"
    echo "当前TOKEN已过期，重新登录..."
    login_and_get_token
    # 重新构建认证头
    AUTH="MediaBrowser Client=\"$CLIENT_NAME\", Device=\"$DEVICE_ID\", Version=\"$CLIENT_VERSION\", Token=\"$TOKEN\""
    # 重新发送播放进度请求
    response=$(curl -s -w "%{http_code}" -X POST "$SERVER/Sessions/Playing/Progress" \
      -H "X-Emby-Authorization: $AUTH" \
      -H "Content-Type: application/json" \
      -d "{
            \"ItemId\": \"$ITEM_ID\",
            \"MediaSourceId\": \"$MEDIA_SOURCE_ID\",
            \"PlaySessionId\": \"$PLAY_SESSION_ID\",
            \"PositionTicks\": 600000000,
            \"IsPaused\": false,
            \"PlayMethod\": \"DirectStream\"
          }")
    http_code=${response: -3}
    response_body=${response%???}
    log "重试播放进度请求状态码：$http_code"
fi

# 最终检查播放进度请求
if [ "$http_code" -ne 200 ] && [ "$http_code" -ne 204 ]; then
    error_msg="播放进度请求失败：状态码$http_code，响应=$response_body"
    log "$error_msg"
    echo "错误：$error_msg"
    send_notification "见手青播放失败" "$error_msg"
    exit 1
elif echo "$response_body" | grep -qi "error"; then
    error_msg="播放进度请求返回错误：$response_body"
    log "$error_msg"
    echo "错误：$error_msg"
    send_notification "见手青播放失败" "$error_msg"
    exit 1
fi

# 模拟真实播放延迟
sleep 10

# 第四步：模拟停止播放
log "发送停止播放请求"
echo "--- 模拟停止播放 ---"
response=$(curl -s -w "%{http_code}" -X POST "$SERVER/Sessions/Playing/Stopped" \
  -H "X-Emby-Authorization: $AUTH" \
  -H "X-Emby-Client: $CLIENT_NAME" \
  -H "X-Emby-Device-Name: $DEVICE_NAME" \
  -H "X-Emby-Device-Id: $DEVICE_ID" \
  -H "X-Emby-Client-Version: $CLIENT_VERSION" \
  -H "Content-Type: application/json" \
  -d "{
        \"ItemId\": \"$ITEM_ID\",
        \"MediaSourceId\": \"$MEDIA_SOURCE_ID\",
        \"PlaySessionId\": \"$PLAY_SESSION_ID\",
        \"PositionTicks\": 650000000
      }")

http_code=${response: -3}
response_body=${response%???}

log "停止播放请求状态码：$http_code"
log "停止播放请求响应：$response_body"

# 检查停止播放请求是否失败
if [ "$http_code" -ne 200 ] && [ "$http_code" -ne 204 ]; then
    error_msg="停止播放请求失败：状态码$http_code，响应=$response_body"
    log "$error_msg"
    echo "错误：$error_msg"
    send_notification "见手青播放失败" "$error_msg"
    exit 1
elif echo "$response_body" | grep -qi "error"; then
    error_msg="停止播放请求返回错误：$response_body"
    log "$error_msg"
    echo "错误：$error_msg"
    send_notification "见手青播放失败" "$error_msg"
    exit 1
fi

# 签到成功收尾
log "===== 今日签到成功 ====="
echo "=== 签到成功！可在Emby查看观看记录 ==="
send_notification "见手青播放成功" "今日自动播放已完成，使用TOKEN：${TOKEN:0:8}****"