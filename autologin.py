
# -*- coding: utf-8 -*-
import time
import requests
account = "006205"
password = "20060608"
# 请求网址
url = "http://172.21.3.1/ac_portal/login.php"
# 请求头
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",     # 必须指定，否则报404
}
# 时间戳（提取ms单位）
tag = int(time.time()*1000)
# RC4加密算法
def do_encrypt_rc4(src:str, passwd:str)->str:
    i, j, a, b, c = 0, 0, 0, 0, 0
    key, sbox = [], []
    plen = len(passwd)
    size = len(src)
    output = ""

    # 初始化密钥key和状态向量sbox
    for i in range(256):
        key.append(ord(passwd[i % plen]))
        sbox.append(i)
    # 状态向量打乱
    for i in range(256):
        j = (j + sbox[i] + key[i]) % 256
        temp = sbox[i]
        sbox[i] = sbox[j]
        sbox[j] = temp
    # 秘钥流的生成与加密
    for i in range(size):
        # 子密钥生成
        a = (a + 1) % 256
        b = (b + sbox[a]) % 256
        temp = sbox[a]
        sbox[a] = sbox[b]
        sbox[b] = temp
        c = (sbox[a] + sbox[b]) % 256
        # 明文字节由子密钥异或加密
        temp = ord(src[i]) ^ sbox[c]
        # 密文字节转换成hex，格式对齐修正（取最后两位，若为一位（[0x0，0xF]），则改成[00, 0F]）
        temp = str(hex(temp))[-2:]
        temp = temp.replace('x', '0')
        # 输出
        output += temp
    return output
# 利用RC4加密算法获取基于时间戳的密码
pwd = do_encrypt_rc4(password, str(tag))
# 账号、密码、时间戳写入payload报文
payload = f"opr=pwdLogin&userName={account}&pwd={pwd}&auth_tag={tag}&rememberPwd=1"

# 提交登录
res = requests.post(url, data=payload, headers=headers)