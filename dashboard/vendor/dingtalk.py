import json
import os
import requests

access_token = os.getenv("DINGTALK_ACCESS_TOKEN")
url = f"https://oapi.dingtalk.com/robot/send?access_token={access_token}"


def notify_alarm(content):
    resp = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {
                "msgtype": "text",
                "text": {"content": content},
                "at": {"isAtAll": True},
            }
        ),
    )
    return resp.json()
