import json
import os
import time
import requests

def forward():
    while True:
        # 从recv中读取短信
        out = os.popen('/root/sms_tool -ju recv').read()
        #从out中解析出json
        json_txt = json.loads(out)        
        #从json中解析出msgs
        msgs = json_txt['msg']
        # print("msgs:\n",msgs)
        if msgs:
            for msg in msgs:
                push_bark(msg)
        time.sleep(3)

def push_bark(msg):
    # print("msg:\n",msg)
    #url为bark的url
    url = 'https://api.day.app/你的秘钥'
    # sender为发件人的手机号
    sender = msg['sender']
    # content为短信内容
    content = msg['content']
    # icon为bark的图标
    icon = '?icon=https://files.getquicker.net/_icons/5F6E945F1FF1C230C006EF44A14C5EE6246509AB.png'#这里是推送信息的图标
    push_msg=f'{url}/来自{sender}的消息/{content}{icon}'
    try:
        # 发送请求
        response = requests.get(push_msg)
        # print("Response:\n", response.text)
        #写入日志
        with open('/root/SMS_Forward/log.txt', 'a') as f:
            f.write(response.text + '\n')
    except Exception as e:
        # print("Error occurred: ", str(e))
        #追加写入日志
        with open('/root/SMS_Forward/log.txt', 'a') as f:
            f.write(str(e)+'\n')        
if __name__ == '__main__':
    forward()
