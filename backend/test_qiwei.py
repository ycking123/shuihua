import requests
import json
import time

# 配置你的 Token 和 AgentID
# MY_ACCESS_TOKEN = "fBWeXDtZP3uwetRC3_z7dPrVmEWjpvPpIlA_aKhDicWIbTazVb6LKKdGXPUzeyvEWvp4-Vy0JdUBe8RGKIzzu1kSshJcDckxEX4ylh7zVwPpqETKLNFA3rKePuX_N1eRuv-6NdCLPLC8hVdyos6OaLlgF-bmvO67rEBzVN-cEWFymx8zJ5WVNfJDvSaugj_Oz6dDiq7H4AdFXMjdkzZXbw"
MY_AGENT_ID = 1000003
CORP_ID = "wwcd40432aceae49af"      # 你的企业ID
CORP_SECRET = "6OBPpFJwL2C0Y5Lni4PdJGZrV_7JXZ7HdkFWB9_PWTo"    # 你的应用Secret


def get_access_token(corp_id, corp_secret):
    """
    获取企业微信 access_token
    :param corp_id: 企业ID
    :param corp_secret: 应用的Secret
    :return: access_token (字符串)，失败返回 None
    """
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    
    params = {
        "corpid": corp_id,
        "corpsecret": corp_secret
    }
    
    try:
        response = requests.get(url, params=params)
        result = response.json()
        
        if result.get("errcode") == 0:
            print(f"✅ 成功获取 access_token")
            return result.get("access_token")
        else:
            print(f"❌ 获取失败: {result.get('errmsg')}")
            return None
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        return None


# 使用示例：
# access_token = get_access_token("你的企业ID", "你的应用Secret")
# print(access_token)


def create_wecom_private_calendar(access_token, agent_id):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/oa/calendar/add?access_token={access_token}"

    payload = {
        "calendar": {
            "summary": "研发部项目日历",
            "color": "#0000FF",
            "description": "用于记录研发部重要里程碑",
            "is_public": 0,
            # 至少共享给一个测试成员，确保你用这个成员登录时能看到
            "shares": [
                {"userid": "LanJing", "permission": 1},
                {"userid": "ZhangXiaoYan", "permission": 1},
            ]
        },
        # 自建应用一般不需要 agentid，但你可以保留，不影响
        "agentid": agent_id
    }

    headers = {"Content-Type": "application/json;charset=utf-8"}

    print(f"正在尝试创建私有日历，使用的 AgentID: {agent_id}...")
    try:
        valid_json = json.dumps(payload, ensure_ascii=False, indent=2)
        print(f"发送的请求体:\n{valid_json}")
    except Exception as e:
        print(f"JSON格式错误: {e}")
        return None

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.encoding = "utf-8"
        result = response.json()

        print(f"服务器返回:\n{json.dumps(result, ensure_ascii=False, indent=2)}")

        if result.get("errcode") == 0:
            cal_id = result.get("cal_id")
            print(f"✅ 私有日历创建成功！cal_id: {cal_id}")
            # 可以顺手调用一下 get_calendar_info(MY_ACCESS_TOKEN, cal_id) 核验
            return cal_id
        else:
            print(f"❌ 创建失败: {result.get('errmsg')}")
            return None
    except Exception as e:
        print(f"❌ 请求发生错误: {str(e)}")
        return None



def create_wecom_public_calendar(access_token, agent_id):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/oa/calendar/add?access_token={access_token}"

    payload = {
        "calendar": {
            "admins":[
				"LanJing",
				"ZhangXiaoYan"
		],
            "summary": "研发部项目公共日历1",
            "color": "#0000FF",
            "description": "用于记录研发部重要里程碑（公共日历）",
            "is_public": 1,
            "public_range": {
                "userids": ["LanJing", "ZhangXiaoYan"],          # 改成你实际的 userid
                # "partyids": [1232, 34353]            # 可选：部门 id
            },
            # 如果需要指定管理员或通知范围，再加 admins / shares
            #查看权限
            "shares": [
                {"userid": "LanJing", "permission": 1},
                {"userid": "ZhangXiaoYan", "permission": 1},
            ]


        },
        "agentid": agent_id
    }

    headers = {"Content-Type": "application/json;charset=utf-8"}

    print(f"正在尝试创建公共日历，使用的 AgentID: {agent_id}...")
    print(f"发送的请求体:\n{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = requests.post(url, headers=headers, json=payload)
    response.encoding = "utf-8"
    result = response.json()
    print(f"服务器返回:\n{json.dumps(result, ensure_ascii=False, indent=2)}")

    if result.get("errcode") == 0:
        cal_id = result.get("cal_id")
        print(f"✅ 公共日历创建成功！cal_id: {cal_id}")
        return cal_id
    else:
        print(f"❌ 创建失败: {result.get('errmsg')}")
        return None

def create_wecom_meeting(access_token, admin_userid):
    """创建预约会议（精简版，配置直接写在函数内）"""
    url = f"https://qyapi.weixin.qq.com/cgi-bin/meeting/create?access_token={access_token}"

    # --- 直接在这里修改参数 ---
    payload = {
        "admin_userid": admin_userid,     # 【必填】会议管理员的 userid
        "title": "周一产品周会",           # 【必填】会议标题
        "meeting_start": int(time.time()) + 600, # 【必填】开始时间（这里演示的是当前时间+10分钟）
        "meeting_duration": 3600,         # 【必填】持续时长（秒），3600=1小时

        # --- 下面是选填字段，不需要就把那行删掉 ---
        "description": "请大家准备好PPT", # 【选填】会议描述
        "location": "第一会议室",          # 【选填】会议地点
        # "agentid": 1000003,             # 【选填】应用ID（一般不需要）

        # 邀请参会人
        "invitees": {
            # "userid": ["lisi", "wangwu"]  # 【选填】参会成员 userid 列表
            "userid": ["LanJing", "ZhangXiaoYan"]
        },

        # 会议设置
        "settings": {
            "password": "8888",           # 【选填】会议密码（4-6位数字）
            "allow_enter_before_host": True, # 【选填】允许主持人前入会
            "enable_enter_mute": 0        # 【选填】入会是否静音：0-否，1-是
        }
    }
    # --------------------------

    headers = {'Content-Type': 'application/json;charset=utf-8'}

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        
        print(f"【创建会议】返回结果:\n{json.dumps(result, ensure_ascii=False, indent=2)}")

        if result.get("errcode") == 0:
            print(f"✅ 会议创建成功！meetingid: {result.get('meetingid')}")
            return result.get('meetingid')
        else:
            print(f"❌ 会议创建失败: {result.get('errmsg')}")
            return None
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        return None

# 执行创建
if __name__ == "__main__":
    MY_ACCESS_TOKEN = get_access_token(CORP_ID, CORP_SECRET)
    if MY_ACCESS_TOKEN:
        print(f"获取到的 access_token: {MY_ACCESS_TOKEN}")
    # create_wecom_private_calendar(MY_ACCESS_TOKEN, MY_AGENT_ID)
    # create_wecom_public_calendar(MY_ACCESS_TOKEN, MY_AGENT_ID)
    create_wecom_meeting(MY_ACCESS_TOKEN, admin_userid="LanJing")