import bcrypt
pwd = 'pass1234'

hash_pw = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())

print(hash_pw)


print(bcrypt.checkpw("pass12342".encode("utf-8"), hash_pw))

