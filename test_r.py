# test_reminders.py

import pytest
from app import create_app
from pymongo import MongoClient
from datetime import datetime

@pytest.fixture
def client():
    app = create_app(testing=True)
    client = app.test_client()
    
    with app.app_context():
        yield client

def test_create_reminder_success(client):
    response = client.post('/reminders', json={
        'userId': '60c72b2f4f1a2566b4fdf5b1',
        'type': 'exame',
        'dateTime': datetime.now().isoformat(),
        'description': 'Exame de sangue'
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Lembrete criado com sucesso!'
    assert data['reminder']['type'] == 'exame'
    assert data['reminder']['description'] == 'Exame de sangue'

def test_create_reminder_missing_fields(client):
    response = client.post('/reminders', json={
        'userId': '60c72b2f4f1a2566b4fdf5b1',
        'type': 'medicamento'
        # Falta a data/hora e a descrição
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == 'Todos os campos são obrigatórios.'

def test_list_reminders(client):
    userId = '60c72b2f4f1a2566b4fdf5b1'
    
    # Cria um lembrete para o teste
    client.post('/reminders', json={
        'userId': userId,
        'type': 'medicamento',
        'dateTime': datetime.now().isoformat(),
        'description': 'Tomar remédio para pressão'
    })
    
    response = client.get(f'/reminders/{userId}')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]['description'] == 'Tomar remédio para pressão'
