# -*- coding: utf-8 -*- 
# @Author : Leo

import base64


def rc4_decrypt(msg: str, key: str) -> str:
    """rc4解密程序"""

    def rc4_init():
        # 没管秘钥小于256的情况，小于256不断重复填充即可
        box_array = list(range(256))
        j = 0
        for i in range(256):
            j = (j + box_array[i] + ord(key[i % len(key)])) % 256
            box_array[i], box_array[j] = box_array[j], box_array[i]
        return box_array

    temp = base64.urlsafe_b64decode(msg.encode('utf-8'))
    temp_deco = bytes.decode(temp, encoding='ISO-8859-1', errors='ignore')
    result = []
    box = rc4_init()
    x = y = 0
    for s in temp_deco:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        t = (box[x] + box[y]) % 256
        k = box[t]
        result.append(chr(ord(s) ^ k))
    return ''.join(result)


"""
参考链接：
- https://www.jianshu.com/p/d9ad5fc524ec
- https://www.cnblogs.com/wswang/p/7717997.html
- https://stackoverflow.com/questions/22216076/unicodedecodeerror-utf8-codec-cant-decode-byte-0xa5-in-position-0-invalid-s

"""

t_key = 'ae834a300a90837fe37a70942e7e161ad37145de0d331ae1f80a8b7b963775b7'
t_dec_msg = 'sNpF0wXlU2200DjjZSsE94Ds7MaN4Fjl3O4LJclC7K2dHN9VNeeMUukOuHBNpZbTfcRxWPOXcwYlq05eQugJmURKkCLFGsoY0lM3maxZX/6Y7aM9EORFupIDUW5PZq6nPQ=='
plain_text = rc4_decrypt(t_dec_msg, t_key)
print(plain_text)
