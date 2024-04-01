from werkzeug.security import generate_password_hash, check_password_hash

string = "hahah12345"
hash = generate_password_hash(string, method='pbkdf2:md5',salt_length=8)
print(check_password_hash(hash, "hahah12345"))
print(hash)
print(len(hash))
