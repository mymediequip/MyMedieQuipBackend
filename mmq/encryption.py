from Crypto.Cipher import AES
import base64
import ast
import json

from Crypto import Random
from hashlib import md5
BLOCK_SIZE = 16
KEY = "k]g@d#3[v$s(D4$s{5_=2y5f()#5s3Sc".encode()

def pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + (chr(length)*length).encode()

def unpad(data):
    return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]

def bytes_to_key(data, salt, output=48):
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]

def encrypt(message, passphrase=KEY):
    salt = Random.new().read(8)
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    print("iv",iv)
    aes = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(b"Salted__" + salt + aes.encrypt(pad(message.encode('utf-8'))))

def decrypt(encrypted, passphrase=KEY):
    encrypted = base64.b64decode(encrypted)
    assert encrypted[0:8] == b"Salted__"
    salt = encrypted[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(encrypted[16:]))

def decode_data(data):
    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>decrypt", decrypt(data.get('data', None)).decode('utf-8'))
    try:
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Try")
        if data.get('encoded_data', None)=="yes":
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>IF")
            try:
                output = ast.literal_eval(decrypt(data.get('data', None)).decode('utf-8'))
                print(output, "output---------")
            except Exception as e:
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EEEEEEE", e)
                output = json.loads(decrypt(data.get('data', None)).decode('utf-8'))
            
            # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>HERE")
        else:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ELSE")
            output = data.get('data', None)
        return output
    except Exception as e:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>except", e)
        output = data.get('data', None)
        return output




def internal_decode_data(data):
    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>decrypt", decrypt(data.get('data', None)).decode('utf-8'))
    try:
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Try")
        try:
            output = str(decrypt(data))
            outputdata = output.split("'")
            print(outputdata, "output---------")
            return outputdata[1]
        except Exception as e:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EEEEEEE", e)
            output = decrypt(data)
        return output
    except Exception as e:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>except", e)
        output = data
        return output