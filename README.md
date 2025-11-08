# 概览
## 本系统默认接口地址为127.0.0.1:25613，可通过反向代理或公网ip将接口开放出去，建议使用反向代理，如果要使用公网ip，请将Main.py最后一行host里的127.0.0.1修改为0.0.0.0，修改后 公网ip:25613就是接口地址，端口号可自行修改
## 添加移除key，第一次添加不需要验证，直接生成key，并设置权限为管理员，后边添加权限为代理，管理员拥有所有权限，代理可给用户添加授权，添加余额9999e9999或直接添加余额inf为无限余额(inf设置为字符串即可)
## 授权86400秒消费1余额，不足1余额的按1余额计算，永久扣450余额
## 请不要将授权对象设置为list

# 接口地址
## home目录为GET请求，其余为POST请求
```
POST/GET 127.0.0.1:25613
```

# 认证
## 所有以修改数据为目的的API请求都需要在Authorization头部中包含您的API密钥
```
Authorization: Bearer YOUR_KEY
```
### 请妥善保管您的API密钥，不要在前端代码中硬编码或公开分享。建议使用环境变量或安全的配置管理方式存储密钥。
### API只有管理员和代理拥有，普通用户只有查询权限，不需要密钥

# API格式
## /admin/key
```json
{
    "type": "类型(append/remove/search)(搜索key需要key跟名称对应)",
    "name": "key的名称(可为用户id)"
}
```
## /admin/account_balance
```json
{
    "type": "类型(append/remove)",
    "name": "key的名称(可为用户id)",
    "num": "需要操作的数量"
}
```
## /admin/authorize
```json
{
    "type": "类型(append/remove)",
    "name": "操作对象",
    "num": "修改时长(秒)(仅append使用)"
}
```
## /home
```json
{
    "name": "查询对象(list为查询代理列表)"
}
```

# 返回参数
## error 错误信息
## code 状态码(200为有授权， 401为未授权或过期)
## content 内容
## time 当前时间
## authorize_time 授权到期时间
## key 生成的key
## name 名字
## account_balance 账户余额
## group 用户组
## data 数据