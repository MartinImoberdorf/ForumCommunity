from . import db  # importamos el db de init
from flask_login import UserMixin
from sqlalchemy.sql import func

# solo para user add el UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) # 150 es el max length, que es unico no irrepetible en los demas usuarios
    password=db.Column(db.String(150))
    first_name=db.Column(db.String(150))
    color = db.Column(db.String(7)) 
    chats = db.relationship('Chat', backref='user', lazy=True) # Esto seria como si fuera la tabla notasXUsuarios - Esto es la clave de como guardar las notas de cada usuario

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Definimos la FK del usuario a referenciar
    