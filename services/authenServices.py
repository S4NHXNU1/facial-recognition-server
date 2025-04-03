from repository.userRepository import InsertUser, AuthorizeUser

def AddUser(username, password):

    res = InsertUser(username, password)

    if res == 0:
        return False

    return True

def Auth(username, password):

    res = AuthorizeUser(username, password)

    if res == 0:
        return False

    return True