# Project
#   Small CHAP logic example
#
# Date
#   09.03.2019
#
# Author
# - Malik Fleury
# - Bastien Wermeille

# Quel hachage cryptographique utilisez-vous et pourquoi ?
# SHAKE_256 (SHA3) : MD5, SHA1 ont des collisions et SHA2 se base sur le même principe que SHA1
#
# Quelles précautions pour le générateur aléatoire ?
# Grande entropie, tous les nombres doivent avoir la même probabilité d'être généré
#
# Quelles précautions pour la construction garantissant l'unicité du nonce ?
# Ajout d'un timestamp au nonce afin d'assurer l'unicité
#
# Quelles précautions pour la durée de validité du nonce ?
# 
#

import secrets
import hashlib
import datetime
from datetime import timedelta

def hash_function(password):
    # Use hexdigest to facilitate display
    return hashlib.sha3_256(password.encode('utf-8')).hexdigest()

def nonce_generation_function():
    return secrets.token_hex(16)

class Client:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def connect(self, server):
        print(self.username + " connect to " + server.username)

        print(self.username + " request nonce")
        nonce = server.get_nonce(self.username)

        print(self.username + " generate cnonce")
        cnonce = nonce_generation_function()

        hashed_pass = hash_function(nonce + cnonce + self.password)

        print(self.username + " request authentication")
        status = server.auth(self.username, cnonce, hashed_pass)

        print(self.username + " authentication " + ("sucessful" if status else "failed"))
        

class Server:
    def __init__(self, username, password_database, time_validity):
        self.username = username
        self.password_database = password_database
        self.time_validity = time_validity
        self.nonce_database = {}

    def get_nonce(self, username):
        print(self.username + " nonce requested")
        nonce = nonce_generation_function()
        self.nonce_database[username] = {
            'validity':datetime.datetime.now() + self.time_validity,
            'value': nonce
        }
        return nonce

    def auth(self, username, cnonce, hashed_pass):
        print(self.username + " authentication requested by " + username)
        try:
            # Check validity
            validity = self.nonce_database[username]['validity']
            if validity < datetime.datetime.now():
                print(self.username + " auth requested by " + username + "nonce invalid")
                return False
            nonce = self.nonce_database[username]['value']

            hashed_pass_server = hash_function(nonce+cnonce+self.password_database[username])
            return secrets.compare_digest(hashed_pass_server, hashed_pass)
        except Exception as e:
            print(e)
            print(self.username + " auth requested by " + username + "nonce invalid")
            return False



if __name__ == '__main__':
    password_database = {
        'Alice': '8xHm5EbL6S%M%QHD^UN327Y8dzJq7B*_Zk@bdJ=39A97^3%rsr',
        'Jon': 'atpy+hQB4uc4b!+xs?fBY%_?+ASf_*r@fFD3GKVc8-63?vku6F',
        'Emilia': 'z!@W3yKFPdV*-@-Qwu&VX*JHTjFR2q42MnKMYV8a6mPmtMFhy$'
    }

    # Nonce duration validity
    server_nonce_validity = timedelta(seconds=15)

    alice = Client('Alice', password_database['Alice'])
    bob = Server('Bob', password_database, server_nonce_validity)

    alice.connect(bob)
