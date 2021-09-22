import requests
import hashlib
import random
import os

database_passwords = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt"

def get_hash(text):
	return hashlib.sha256(text.strip("\n").encode('utf-8')).hexdigest()

password = str(input(": "))
sha256_password = get_hash(password)

characters = []
fails = []
guess = ""
found = False

data = requests.get(url = database_passwords).text

print(f"\nFind Password (Database mode...)\n")
for l in data.split("\n"):
	guess_hash = get_hash(l)
	if(guess_hash == sha256_password):
		print("Encontrado")
		found == True
		break


for c_n in range(32,126):
	characters.append(chr(c_n))

print(found)
input()
while(found == False):
	guess = ""
	for i in range(len(password)):
		guess += random.choice(characters)

	if(len(fails) == 0):
		fails.append(guess)
		
	if(guess not in fails and len(fails) != 0):
		guess_hash = get_hash(guess)
		os.system("clear")
		print(f"\nFind Password (Random mode)...\n{sha256_password}\ng{guess_hash}")

		if(guess_hash == sha256_password):
			found = True
			print(guess)
		else:
			fails.append(guess)
		
