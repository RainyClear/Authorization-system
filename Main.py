import os
import time
import json
import uuid
import random
from flask import Flask, jsonify, request

# 绝对路径
file_path = os.path.dirname(__file__).replace("\\", "/")

app = Flask(__name__)

@app.route("/admin/key", methods = ["POST"])
def admin_key():
    # 获取参数
    type = request.form.get("type")
    name = request.form.get("name")
    Authorization = request.headers.get("Authorization")
    
    if type is None:
        return jsonify({"error": "type is None"}), 400
    if name is None:
        return jsonify({"error": "name is None"}), 400
    
    # 读取key数据
    with open(f"{file_path}/config/key.json", "r", encoding = "utf_8") as key_json:
        key_data = key_json.read()
        key_data = json.loads(key_data)
    with open(f"{file_path}/config/account.json", "r") as account_file:
        account_data = account_file.read()
        account_json = json.loads(account_data)

    # 第一个key添加不需要验证key
    if type != "append" or key_data != {}:
        if Authorization is None:
            return jsonify({"error": "Authorization is None"}), 400
        if Authorization[:7] != "Bearer ":
            return jsonify({"error": "Authorization error"}), 400
        if Authorization[7:] not in key_data:
            return jsonify({"error": "key do not exist"}), 400
        if type == "search":
            if name != key_data[Authorization[7:]]["name"]:
                return jsonify({"error": "name error or key error"}), 200
            return jsonify({"name": name, "group": key_data[Authorization[7:]]["group"], "account_balance": key_data[Authorization[7:]]["account_balance"]})
        if key_data[Authorization[7:]]["group"] != "administrator":
            return jsonify({"error": "You don't have permission"}), 400
    # 添加key
    if type == "append":
        if name in account_json:
            return jsonify({"error": "The name already exists"}), 400
        # 生成key
        uid = str(uuid.uuid4()).replace('-', '')
        num = random.randint(1000, 9999)
        key = f"rc-{uid}{num}"

        group = "agent"
        # 第一个key为管理员权限，其他为代理
        if key_data == {}:
            group = "administrator"

        data_json = {"name": name, "group": group, "account_balance": 0}
        key_data[key] = data_json
        with open(f"{file_path}/config/key.json", "w", encoding = "utf-8") as file:
            json.dump(key_data, file, ensure_ascii = False, indent = 4)
        account_json[name] = key
        with open(f"{file_path}/config/account.json", "w") as file:
            json.dump(account_json, file, ensure_ascii = False, indent = 4)
        return jsonify({"key": key, "name": name, "group": group}), 200
    
    elif type == "remove":
        if name not in account_json:
            return jsonify({"error": "name do not exist"}), 400
        if key_data[account_json[name]]["group"] == "administrator":
            return jsonify({"error": "The administrator account cannot be deleted"}), 400
        del key_data[account_json[name]]
        del account_json[name]
        with open(f"{file_path}/config/key.json", "w", encoding = "utf-8") as file:
            json.dump(key_data, file, ensure_ascii = False, indent = 4)
        with open(f"{file_path}/config/account.json", "w", encoding = "utf_8") as file:
            json.dump(account_json, file, ensure_ascii = False, indent = 4)
        return jsonify({"content": "ok"}), 200
    else:
        return jsonify({"error": "type error"}), 400
    
@app.route("/admin/account_balance", methods = ["POST"])
def admin_account_balance():
    # 获取参数
    type = request.form.get("type")
    name = request.form.get("name")
    num = request.form.get("num")
    Authorization = request.headers.get("Authorization")
    
    if num is None:
        return jsonify({"error": "num is None"}), 400
    try:
        num = float(num)
    except Exception:
        return jsonify({"error": "num is not a number"}), 400
    if type is None:
        return jsonify({"error": "type is None"}), 400
    if name is None:
        return jsonify({"error": "name is None"}), 400
    
    # 读取key数据
    with open(f"{file_path}/config/key.json", "r", encoding = "utf_8") as key_json:
        key_data = key_json.read()
        key_data = json.loads(key_data)
    with open(f"{file_path}/config/account.json", "r") as account_file:
        account_data = account_file.read()
        account_json = json.loads(account_data)

    if Authorization is None:
        return jsonify({"error": "Authorization is None"}), 400
    if Authorization[:7] != "Bearer ":
        return jsonify({"error": "Authorization error"}), 400
    try:
        if key_data[Authorization[7:]]["group"] != "administrator":
            return jsonify({"error": "You don't have permission"}), 400
    except Exception:
        return jsonify({"error": "key do not exist"}), 400
    
    if type == "append":
        # 读取账户余额
        account_balance = float(key_data[account_json[name]]["account_balance"])

        account_balance += num

        key_data[account_json[name]]["account_balance"] = str(account_balance)

        with open(f"{file_path}/config/key.json", "w", encoding = "utf-8") as file:
            json.dump(key_data, file, ensure_ascii = False, indent = 4)
        return jsonify({"content": "ok"}), 200
    
    elif type == "remove":
        # 读取账户余额
        account_balance = float(key_data[account_json[name]]["account_balance"])

        account_balance -= num
        
        if account_balance < 0:
            return jsonify({"error": "Insufficient balance"}), 400
        if str(account_balance) == "nan":
            account_balance = 0

        key_data[account_json[name]]["account_balance"] = str(account_balance)

        with open(f"{file_path}/config/key.json", "w", encoding = "utf-8") as file:
            json.dump(key_data, file, ensure_ascii = False, indent = 4)
        return jsonify({"content": "ok"}), 200
    else:
        return jsonify({"error": "type error"}), 400
    
@app.route("/admin/authorize", methods = ["POST"])
def admin_authorize():
    # 获取参数
    type = request.form.get("type")
    name = request.form.get("name")
    num = request.form.get("num")
    Authorization = request.headers.get("Authorization")
    
    if type is None:
        return jsonify({"error": "type is None"}), 400
    if name is None:
        return jsonify({"error": "name is None"}), 400
    
    # 读取key数据
    with open(f"{file_path}/config/key.json", "r", encoding = "utf_8") as key_json:
        key_data = key_json.read()
        key_data = json.loads(key_data)
    with open(f"{file_path}/config/account.json", "r") as account_file:
        account_data = account_file.read()
        account_json = json.loads(account_data)

    if Authorization is None:
        return jsonify({"error": "Authorization is None"}), 400
    if Authorization[:7] != "Bearer ":
        return jsonify({"error": "Authorization error"}), 400
    try:
        test = key_data[Authorization[7:]]
    except Exception:
        return jsonify({"error": "key do not exist"}), 400
    
    with open(f"{file_path}/config/authorize.json", "r") as file_authorize:
        authorize_data = file_authorize.read()
        authorize_data = json.loads(authorize_data)

    if name not in authorize_data:
        authorize_data[name] = 0
    
    # 当前时间戳
    now_timestamp = time.time()
    
    if type == "append":
        if num is None:
            return jsonify({"error": "num is None"}), 400
        try:
            num = float(num)
        except Exception:
            return jsonify({"error": "num is not a number"}), 400
        
        key_data[Authorization[7:]]["account_balance"] = float(key_data[Authorization[7:]]["account_balance"])
        
        # 计算余额
        use_balance = round(num / 86400, 2) if round(num / 86400, 2) >= 1 else 1

        if use_balance > key_data[Authorization[7:]]["account_balance"]:
            return jsonify({"error": "balance is shortage"})
        
        balance_now = key_data[Authorization[7:]]["account_balance"]

        key_data[Authorization[7:]]["account_balance"] -= use_balance

        if str(key_data[Authorization[7:]]["account_balance"]) == "nan":
            key_data[Authorization[7:]]["account_balance"] = balance_now - 450

        key_data[Authorization[7:]]["account_balance"] = str(key_data[Authorization[7:]]["account_balance"])

        with open(f"{file_path}/config/key.json", "w", encoding = "utf-8") as file:
            json.dump(key_data, file, ensure_ascii = False, indent = 4)
            
        # 日志写入
        with open(f"{file_path}/log/authorize.log", "r", encoding = "utf-8") as log_file:
            log_data = log_file.read()
        with open(f"{file_path}/log/authorize.log", "w", encoding = "utf-8") as file:
            file.write(f"{log_data}\n[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_timestamp))}](余额 {balance_now} / {key_data[Authorization[7:]]["account_balance"]}) {key_data[Authorization[7:]]["name"]} 为 {name} 授权 {num} 秒".replace("\n", ""))
            
        # 判断授权是否到期
        if now_timestamp > authorize_data[name]:
            authorize_data[name] = time.time()
        authorize_data[name] += num
    elif type == "remove":
        try:
            authorize_data[name] = 0
        except Exception:
            return jsonify({"error": "key do not exist"}), 400
        
    # 最大时间
    if str(authorize_data[name]) == "inf" or authorize_data[name] > 32536799999:
        authorize_data[name] = 32536799999

    # 授权到期时间
    authorize_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(authorize_data[name]))
    with open(f"{file_path}/config/authorize.json", "w", encoding = "utf-8") as file:
        json.dump(authorize_data, file, ensure_ascii = False, indent = 4)
    return jsonify({"content": "ok", "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_timestamp)), "authorize_time": authorize_time}), 200

@app.route("/home", methods = ["GET"])
def home():
    name = request.args.get("name")
    if name is None:
        return jsonify({"error": "name is None"}), 400
    if name == "list":
        # 读取数据
        with open(f"{file_path}/config/account.json", "r", encoding = "utf-8") as account_file:
            account_data = account_file.read()
            account_json = json.loads(account_data)
        account_list = list(account_json.keys())
        return jsonify({"data": account_list})

    # 读取数据
    with open(f"{file_path}/config/authorize.json", "r") as authorize_file:
        authorize_data = authorize_file.read()
        authorize_json = json.loads(authorize_data)
    code = 401
    if name not in authorize_json:
        authorize_timestamp = 0
    else:
        # 获取当前时间戳
        now_timestamp = time.time()
        authorize_timestamp = authorize_json[name]
        if now_timestamp < authorize_timestamp:
            code = 200
    # 授权截至时间
    authorize_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(authorize_timestamp))
    return jsonify({"code": code, "authorize_time": authorize_time, "name": name})
        
    
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 25613)