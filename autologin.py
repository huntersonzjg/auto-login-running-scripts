
# -*- coding: utf-8 -*-
import time
import requests
account = "006205"
password = "20060608"
# ������ַ
url = "http://172.21.3.1/ac_portal/login.php"
# ����ͷ
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",     # ����ָ��������404
}
# ʱ�������ȡms��λ��
tag = int(time.time()*1000)
# RC4�����㷨
def do_encrypt_rc4(src:str, passwd:str)->str:
    i, j, a, b, c = 0, 0, 0, 0, 0
    key, sbox = [], []
    plen = len(passwd)
    size = len(src)
    output = ""

    # ��ʼ����Կkey��״̬����sbox
    for i in range(256):
        key.append(ord(passwd[i % plen]))
        sbox.append(i)
    # ״̬��������
    for i in range(256):
        j = (j + sbox[i] + key[i]) % 256
        temp = sbox[i]
        sbox[i] = sbox[j]
        sbox[j] = temp
    # ��Կ�������������
    for i in range(size):
        # ����Կ����
        a = (a + 1) % 256
        b = (b + sbox[a]) % 256
        temp = sbox[a]
        sbox[a] = sbox[b]
        sbox[b] = temp
        c = (sbox[a] + sbox[b]) % 256
        # �����ֽ�������Կ������
        temp = ord(src[i]) ^ sbox[c]
        # �����ֽ�ת����hex����ʽ����������ȡ�����λ����Ϊһλ��[0x0��0xF]������ĳ�[00, 0F]��
        temp = str(hex(temp))[-2:]
        temp = temp.replace('x', '0')
        # ���
        output += temp
    return output
# ����RC4�����㷨��ȡ����ʱ���������
pwd = do_encrypt_rc4(password, str(tag))
# �˺š����롢ʱ���д��payload����
payload = f"opr=pwdLogin&userName={account}&pwd={pwd}&auth_tag={tag}&rememberPwd=1"

# �ύ��¼
res = requests.post(url, data=payload, headers=headers)