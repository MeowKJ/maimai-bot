from cryptography.fernet import Fernet

# 生成一个密钥
SECRET_KEY = Fernet.generate_key()

# 将密钥保存到文件
with open("secret_key.txt", "wb") as key_file:
    key_file.write(SECRET_KEY)
