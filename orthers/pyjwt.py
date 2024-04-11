import base64
import os
from datetime import datetime, timedelta

import jwt


def generator_jwt():
    """生成token"""
    # 1.生成载荷字典信息
    # 过期时常
    expire_2h = datetime.utcnow() + timedelta(hours=2)
    playload_dict = {
        'user_id': 66,
        'exp': expire_2h,
    }

    # 2.生成密钥
    key = base64.b64encode(os.urandom(32)).decode()

    # 生成token
    token = jwt.encode(payload=playload_dict, key=key, algorithm='HS256')
    print(token)
    return token,key


def decode_jwt(token,key):

    payload=jwt.decode(token,key=key,algorithms='HS256')
    print(payload)
if __name__ == '__main__':
    token,key = generator_jwt()


    decode_jwt(token,key)
