from app.main import app
import pytest
import json


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_list(client):
    rv = client.get('/tasks')
    json_data = rv.get_json()

    assert rv.status_code == 200
    assert json_data['result'] == [{'id': 1, 'name': 'first task', 'status': 0}]


def test_create_success(client):
    payload = {'name': 'eat breakfast'}
    rv = client.post('/task',
                     data=json.dumps(payload),
                     headers={'content-type': 'application/json'})
    json_data = rv.get_json()
    result = json_data['result']
    assert rv.status_code == 201
    assert result['name'] == 'eat breakfast'
    assert result['status'] == 0


def test_create_with_empty_payload(client):
    payload = {}
    rv = client.post('task',
                     data=json.dumps(payload),
                     headers={'content-type': 'application/json'})
    assert rv.status_code == 400


def test_create_with_invalid_status(client):
    payload = {'name': 'play the piano', 'status': 'a'}
    rv = client.post('task',
                     data=json.dumps(payload),
                     headers={'content-type': 'application/json'})
    assert rv.status_code == 400


def test_put_create_success(client):
    payload = {'id': 99, 'name': 'coding', 'status': 1}
    rv = client.put('/task/99',
                    data=json.dumps(payload),
                    headers={'content-type': 'application/json'})
    json_data = rv.get_json()
    assert rv.status_code == 201
    assert json_data['name'] == 'coding'


def test_put_update_success(client):
    payload = {'id': 1, 'name': 'testing', 'status': 0}
    rv = client.put('/task/1',
                    data=json.dumps(payload),
                    headers={'content-type': 'application/json'})

    json_data = rv.get_json()
    assert rv.status_code == 200
    assert json_data['name'] == 'testing'
    assert json_data['status'] == 0


def test_delete_success(client):
    rv = client.delete('/task/1', headers={'content-type': 'application/json'})
    assert rv.status_code == 200


def test_delete_no_content(client):
    rv = client.delete('/task/123', headers={'content-type': 'application/json'})
    assert rv.status_code == 204
