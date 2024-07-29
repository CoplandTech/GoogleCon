from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import re
import json
from files_operations import get_contacts_by_phone, normalize_phone_number

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "USER": generate_password_hash("PASSWORD")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username
    return None

@app.route('/')
def index():
    return "Ну и шо ты тут забыл!?"

@app.route('/get_name', methods=['GET'])
@auth.login_required
def get_full_name_by_phone():
    phone_number = request.args.get('phone')
    if not phone_number:
        return jsonify({'error': 'Phone number parameter is missing'}), 400, {'Content-Type': 'application/json; charset=utf-8'}

    phone_number = normalize_phone_number(phone_number)
    
    contacts_list = get_contacts_by_phone()

    for contact in contacts_list:
        for stored_number in contact['PhoneNumbers']:
            if phone_number == normalize_phone_number(stored_number):
                return contact['Name'], 200, {'Content-Type': 'text/plain; charset=utf-8'}

    return phone_number, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run()