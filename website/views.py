#### Vista

from flask import Blueprint,render_template,request, flash, jsonify
from .models import Chat
from . import db
from flask_login import login_required, current_user # para manejar que el usuario este logueado para acceder
import json


views = Blueprint('views',__name__)



@views.route('/messages', methods=['GET'])
@login_required
def get_messages():
    messages = Chat.query.all()
    messages_data = [{'user': chat.user.first_name, 'data': chat.data,'color': chat.user.color,} for chat in messages]
    return jsonify(chats=messages_data)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        chat = request.form.get('chat') # Obtenemos la nota del HTML
        
        if len(chat) < 1:
            flash('Chat is too short!', category='error') 
        else:
            new_chat = Chat(data=chat, user_id=current_user.id)  # Damos el esquema de nuestra nota según nuestro models
            db.session.add(new_chat) # Añadimos la nota a la DB
            db.session.commit() # Guardamos cambios en la DB
            flash('Chat added!', category='success')
            
    user_name = current_user.first_name 
    return render_template('home.html', user=current_user, user_name=user_name)



@views.route('/delete-chat', methods=['POST'])
def delete_chat():  
    chat = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    chatId = chat['chatId'] # accedemos al id de la nota que nos da la solicitud
    chat = Chat.query.get(chatId) # obtenemos nota con el id obtenido
    if chat: # si encuentra la nota
        if chat.user_id == current_user.id: # si el id del usuario que la creo es igual al id del usuario actual
            db.session.delete(chat) # la eliminamos
            db.session.commit() # la guardamos

    return jsonify({}) # sino la encuentra, devuelve vacio