from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db= SQLAlchemy()
DB_NAME="databse.db"

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs' #SECRER KEY - encrypt session data and cookies
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    ################ Controllers
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/') # el / es un prefix al lo que estat en su controller
    
    ################ Creacion de Database
    from .models import User, Chat

    create_database(app)
    
    ################ Login
    login_manager= LoginManager()
    login_manager.login_view = 'auth.login' # donde nos va a redirigir si el usuario no esta logueado
    login_manager.init_app(app)
    
    @login_manager.user_loader # esto le dice a flask como cargar un usuario, es como un filter by pero por id que es la PK
    def load_user(id):
        return User.query.get(int(id))
    
    
    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')
