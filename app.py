from flask import Flask, render_template, redirect, url_for, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


LOGIN_PAGE_URL = 'https://autenticacao.info.ufrn.br/sso-server/login'
LOGIN_URL = 'https://autenticacao.info.ufrn.br/sso-server/login'
CLIENT_ID = ''
CLIENT_SECRET = ''

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login_form():
    return redirect(LOGIN_PAGE_URL) 

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form.get('username')
    password = request.form.get('password')

    try:

        login_page_response = requests.get(LOGIN_PAGE_URL)
        login_page_soup = BeautifulSoup(login_page_response.text, 'html.parser')
        lt = login_page_soup.find('input', {'name': 'lt'})['value']
        execution = login_page_soup.find('input', {'name': 'execution'})['value']
        _eventId = login_page_soup.find('input', {'name': '_eventId'})['value']

        login_payload = {
            'username': username,
            'password': password,
            'lt': lt,
            'execution': execution,
            '_eventId': _eventId
        }


        login_response = requests.post(LOGIN_URL, data=login_payload)
        
        if login_response.status_code == 200:

            if "Autentica\u00e7\u00e3o Integrada" not in login_response.text:
                return redirect(url_for('custom_success'))
            else:
                return jsonify({'message': 'Authentication failed', 'error': 'Invalid credentials'}), 401
        else:
            return jsonify({'message': 'Authentication failed', 'error': login_response.text}), login_response.status_code
    
    except requests.exceptions.RequestException as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

@app.route('/custom_success')
def custom_success():
    return render_template('custom_success.html')

if __name__ == '__main__':
    app.run(debug=True)