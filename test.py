import json
import requests

# 请填写此参数（第一次访问/admin/key无需填写）
key = "YOUR_KEY"

url = "http://127.0.0.1:25613"

headers = {
    "Authorization": f"Bearer {key}"
}

def key(type, name):
    data = {
        "type": type,
        "name": name
    }
    print(requests.post(url + "/admin/key", data = data, headers = headers).text)

def account_balance(type, name, num):
    data = {
        "type": type,
        "name": name,
        "num": num
    }
    print(requests.post(url + "/admin/account_balance", data = data, headers = headers).text)

def authorize(type, name, num):
    data = {
        "type": type,
        "name": name,
        "num": num
    }
    print(requests.post(url + "/admin/authorize", data = data, headers = headers).text)

def home(name):
    params = {
        "name": name
    }
    print(requests.get(url + "/home", params = params).text)
    
if __name__ == "__main__":
    print("1.添加/删除/查询key\n2.添加/减少余额\n3.添加/移除授权\n4.查询授权\n5.代理列表")
    number = int(input("请选择： "))
    if number != 5:
        name = input("请输入操作对象： ")
        if number != 4:
            type = input("请输入操作类型：")
        if number == 2 or number == 3:
            num = input("请输入数量：")
    match number:
        case 1:
            key(type, name)
        case 2:
            account_balance(type, name, num)
        case 3:
            authorize(type, name, num)
        case 4:
            home(name)
        case 5:
            home("list")