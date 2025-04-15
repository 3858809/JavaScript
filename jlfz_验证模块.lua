

function 流程开始()
	
	--setLogOff(true) --关闭日志
	
	使用ip = ""
	
	ljsjk()
	
	
	--更新壳子程序("/mnt/sdcard/nnfz.apk")
	
	--sleep(10000)
	
	打印设备相关信息()
	
	if checkIsDebug() == false then
		
		--检查和更新壳子()
		
		检查和更新脚本()
		
	end
	
	print("开启脚本")
	
	local arr = getUIConfig("main.config")
	arr =jsonLib.decode(arr)
	local 开启前往界面 = arr["page0"]["开启前往界面"]
	
	if 开启前往界面 == 1 or 开启前往界面 == "1" then
		local ret = showUIEx("续期页面.ui",10,10,-1,-1,onUIXUQIEvent)
	end
	
	setControlBarPosNew(0,0)--设置悬浮窗位置
	
	-- 自定义配置文件路径
	cfgFilePath = "/mnt/sdcard/jl_nnfz_cfg.json"
	
	分辨率适配 = 0
	
	垃圾回收记时器 = 0
	
	显示hud("正在读取信息..")
	
	
	hudid = createHUD()
	
	显示hud("正在校验登录信息...")
	
	::登录验证::
	--验证登录
	if 检查用户密码是否有效() ~=true then
		sleep(3000)
		goto 登录验证
	end
	
	检查并适配分辨率()
	
	显示hud("")
	
	--api获取ip()
	
	--开启心跳包 线程
	local 心跳包线程 = Thread.newThread(更新ip心跳包)
	
	运行模式 = -1
	
	前往boss倒计时最低 = "0"
	前往boss倒计时最高 = "0"
	脚本延迟开启 = 0
	
	--其他配置
	
	卡屏间隔 = 20
	
	
	坐标1=""
	坐标2=""
	坐标3=""
	坐标4=""
	坐标5=""
	坐标6=""
	坐标7=""
	坐标8=""
	卡屏次数=0
	
	
	--定义UI事件
	function onUIEvent(handle,event,arg1,arg2,arg3)
		local 页数 = arg1
		local 控件id = arg2
		local 控件值 = arg3
		
		--print("账号:"..账号)
		--print("密码:"..密码)
		
		setUIText(handle,0,"剩余时间",到期时间)
		setUIText(handle,0,"展示用户名",卡号)
		
		if event == "onload" then
			--print("窗口被加载了")
			--print("用户ID:"..用户ID)
		elseif event == "onclick" then
			--print("按钮点击事件:",arg1,arg2,arg3)
		elseif event == "onchecked" then
			--print("多选框选中或反选事件:",arg1,arg2,arg3)
		elseif event == "onselected" then
			--print("单选框或者下拉框事件:",arg1,arg2,arg3)
		elseif event == "onclose" then
			--print("关闭窗口",arg1)
			if arg1 then
				--print("继续")
				--更新通知key("PushDeer",getUIText(handle,5,"PushDeer通知key"))
				--更新通知key("Gotify",getUIText(handle,5,"Gotify通知key"))
				closeWindow(handle,arg1)
				
				--主流程()
			else
				--print("退出")
				exitScript()
			end
			
		elseif event == "onwebviewjsevent" then
			--print("webview事件",arg1,arg2,arg3)
		end
	end
	
	print("读取自定义配置")
	local 启动状态 = 读取自定义配置("启动状态")
	
	print("启动状态:")
	print(启动状态)
	if 启动状态 == nil or 启动状态 == "" or 启动状态 == "停止" or 启动状态 == "读取配置" then
		print("开启前往界面"..开启前往界面)
		if 开启前往界面 == 0 or 开启前往界面 == "0" then
			local ret = showUIEx("主要配置.ui",10,10,-1,-1,onUIEvent)
		end
		
	end
	
	更新自定义配置("启动状态","正常")
	
	
	setStopCallBack(function(error,exitcode)
		--error 为true表示代码错误导致的结束
		--exitcode 为1表示用户触发的结束 2是调用exitScript 0是主线程结束退出
		
		print("设置脚本结束回调函数",error,exitcode)
		
		if error then
			print("脚本异常结束了!!!5秒后尝试重启脚本!")
			sleep(5000)
			restartScript()--重启脚本
		else
			print("脚本正常结束了!!!")
			更新自定义配置("启动状态","停止")
		end
		
		mysql.closeSQL(con)
		
		
	end)
	
    主流程()
    
end



function 主流程()
	
	
	::开始主流程::
	
	local status, err = pcall(读取配置参数)
	if status == false then
		--读取报错
		更新自定义配置("启动状态","读取配置")
		restartScript()
	end
	
	
	print(运行模式)
	if 运行模式==0 or 运行模式 == "0" then
		local th = Thread.newThread(开启卡屏检测)
		
		等待并提示信息(脚本延迟开启,"挂机模式")
		
		if 挂机模式 == "0" or 挂机模式 == 0 then
			显示hud("挂机模式->【野外boss】")
			野外刷boss()
		elseif 挂机模式 == "1" or 挂机模式 == 1 then
			显示hud("挂机模式->【原地挂机】")
			原地挂机()
		end
	elseif 运行模式==1 or 运行模式 == "1" then --自动日常
		等待并提示信息(脚本延迟开启,"自动日常")
		显示hud("自动日常")
		自动日常()
	end
	print("主流程结束")
end



--遍历怪物确定要打的boss()
--野外刷boss()


