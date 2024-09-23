from flask import Flask, request, render_template, redirect, url_for, flash, session
import pandas as pd
import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
from PureCloudPlatformClientV2 import ApiClient, Configuration
import requests
import os
import json

app = Flask(__name__)
app.secret_key = 'key'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

credentials = {
    'organizacion_1': {
        'client_id': 'tu_cliente_id_aqui',
        'client_secret': 'tu_cliente_secreto_aqui',
        'host': 'tu_host_de_region_genesys_aqui'
    },
    'organizacion_2': {
        'client_id': 'tu_cliente_id_aqui',
        'client_secret': 'tu_cliente_secreto_aqui',
        'host': 'tu_host_de_region_genesys_aqui'
    },
    'organizacion_3': {
        'client_id': 'tu_cliente_id_aqui',
        'client_secret': 'tu_cliente_secreto_aqui',
        'host': 'tu_host_de_region_genesys_aqui',
        'token_url': 'tu_host_de_region_genesys_token_aqui'
    }
}

def get_access_token(client_id, client_secret, token_url='tu_host_de_region_genesys_token_aqui'):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(token_url, headers=headers, data=data)
    response_data = response.json()
    return response_data.get('access_token')

def configure_client_for_organization(organization):
    creds = credentials.get(organization)
    if not creds:
        raise ValueError("Invalid organization selected.")
    
    client_id = creds['client_id']
    client_secret = creds['client_secret']
    host = creds['host']
    token_url = creds.get('token_url', 'tu_host_de_region_genesys_token_aqui')
    
    access_token = get_access_token(client_id, client_secret, token_url)
    if not access_token:
        raise ValueError("Failed to obtain access token.")
    
    config = Configuration()
    config.host = host
    config.access_token = access_token
    
    return config

def get_users(config):
    api_client = ApiClient()
    api_client.configuration = config
    user_api = PureCloudPlatformClientV2.UsersApi(api_client)
    
    try:
        page_number = 1
        page_size = 25
        users = []

        while True:
            api_response = user_api.get_users(page_number=page_number, page_size=page_size)
            users.extend(api_response.entities)

            if api_response.page_count > page_number:
                page_number += 1
            else:
                break
        return users
    except ApiException as e:
        return []

def send_autoanswer_requests(user_ids, config):
    api_client = ApiClient()
    api_client.configuration = config
    user_api = PureCloudPlatformClientV2.UsersApi(api_client)
    
    batch_size = 40
    messages = []

    for i in range(0, len(user_ids), batch_size):
        batch = user_ids[i:i + batch_size]
        body = [{'id': user_id, 'acdAutoAnswer': True} for user_id in batch]
        try:
            api_response = user_api.patch_users_bulk(body)
            messages.extend([f"AutoAnswer activated for {user.name} (ID: {user.id})" for user in api_response.entities])
        except ApiException as e:
            messages.append(f'Exception when calling UsersApi->patch_users_bulk: {e}')
    
    return messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'organization' not in request.form:
        return redirect(url_for('index'))
    
    organization = request.form['organization']
    
    if organization == 'null':
        flash('Please select an organization.')
        return redirect(url_for('index'))

    try:
        config = configure_client_for_organization(organization)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    
 
    data = pd.read_excel(file)
    user_names = data['name'].tolist()
    
    user_names = list(set(user_names))
    
    users = get_users(config)
    results = []

    for name in user_names:
        found = False
        for user in users:
            if user.name == name:
                results.append({'name': user.name, 'id': user.id})
                found = True
                break
        if not found:
            results.append({'name': name, 'id': 'ID not found'})
    
    return render_template('results.html', results=results)

@app.route('/activate_autoanswer', methods=['POST'])
def activate_autoanswer():
    user_ids = request.form.getlist('user_ids')
    organization = request.form.get('organization')
    
    if not user_ids:
        flash('Please select at least one user.')
        return redirect(url_for('index'))
    
    if not organization:
        flash('Organization not specified.')
        return redirect(url_for('index'))

    try:
        config = configure_client_for_organization(organization)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for('index'))

    messages = send_autoanswer_requests(user_ids, config)
    
    return render_template('results.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
