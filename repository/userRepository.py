from models.model import db, User
import bcrypt

def InsertUser(username, password):
    new_user = User(username=username, password=password, face_embedding=None)
    db.session.add(new_user)
    
    try:
        db.session.commit()
        return 1
    except Exception as e:
        db.session.rollback()
        return 0
    
def AuthorizeUser(username, password):
    user = User.query.where((User.username == username)).first()

    if user is None:
        return 0
    
    storedPassword = user.password
    validPassword = bcrypt.checkpw(password.encode('utf-8'), storedPassword .encode('utf-8'))

    if not validPassword:
        return 0
    
    return 1

def UpdateEmbedding(username, face_embedding):
    user = User.query.where(User.username == username).first()

    if user is None:
        return 0
    
    user.face_embedding = face_embedding
    
    try:
        db.session.commit()
        return 1
    except Exception as e:
        db.session.rollback()
        return 0

def GetEmbedding(username):
    user = User.query.where(User.username == username).first()

    if user is None:
        return 0
    
    return user.face_embedding