from werkzeug.security import generate_password_hash

password = "custodian123"
hashed = generate_password_hash(password, method='pbkdf2:sha256')
print("Hashed password:", hashed)
