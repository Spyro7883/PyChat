from flask import Blueprint, request, jsonify

auth = Blueprint('auth', __name__)

@auth.route('/notify', methods=['POST'])
def notify():
    print("A user has connected to the web page")
    return jsonify({ 'message': 'User connection logged' })

@auth.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message')
    
    print(f"Message from client: {message}")
    return jsonify({ 'message': 'Message sent' })
