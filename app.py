# Project
#   Small CHAP logic example
# 
# Date
#   09.03.2019
# 
# Author 
# - Malik Fleury
# - Bastien Wermeille


class Client:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def connect(self, server):
        print(self.name + " connect to " + server.name)
        nonce = server.get_nonce(self.name)

        # Hash password
        hashed_pass = "TODO hash current password"
        server.auth(self.name, hashed_pass)

        server.send_message()

class Server:
    def __init__(self, name, password_database):
        self.name = name
        self.password_database = password_database
        self.nonce_database = {}

    def get_nonce(self, username):
        nonce = "TODO Random nonce"
        self.nonce_database[username] = {
            'validity':12,
            'value': nonce
        }
        return nonce


    def auth(self, username, hashed_pass):
        try:
            return password_database[username] == hashed_pass
        except Exception:
            return False
    
    def send_message(self):
        pass

if __name__ == '__main__':
    #TODO

    password_database = {
        'Alice': 'a9d9gV!@P8L)<=a?[kMGV]\>AGe-~dFbuTE]u<qv/`F5Tcf7m/',
        'Jon': '9-a/3s\~UQ@R-tq3=qJDAy)MFbAg68Psf\f59g,F*hQ`*R6#+c',
        'Emilia': '9-a/3s\~UQ@R-tq3=qJDAy)MFbAg68Psf\f59g,F*hQ`*R6#+c'
    }

    alice = Client('Alice', password_database['Alice'])
    bob = Server('Bob', password_database)

    alice.connect(bob)