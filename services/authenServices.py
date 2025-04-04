from repository.userRepository import InsertUser, AuthorizeUser
import bcrypt

def AddUser(username, password):

    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    res = InsertUser(username, password.decode('utf-8'))

    if res == 0:
        return False

    return True

def Auth(username, password):

    res = AuthorizeUser(username, password)

    if res == 0:
        return False

    return True