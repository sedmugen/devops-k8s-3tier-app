import json
from unittest.mock import patch, MagicMock

def test_health_endpoint(client):
    """Test /health endpoint returns 200 OK and healthy status."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['service'] == 'flask-api'

@patch('app.get_db_connection')
def test_get_items_endpoint(mock_get_db, client):
    """Test GET /api/items returns item list."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        {
            'id': 1,
            'name': 'Test Item',
            'description': 'Test Description',
            'created_at': '2026-08-04 18:00:00'
        }
    ]

    response = client.get('/api/items')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['name'] == 'Test Item'

def test_create_item_missing_name(client):
    """Test POST /api/items without name returns 400 Bad Request."""
    response = client.post(
        '/api/items',
        data=json.dumps({'description': 'No name provided'}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

@patch('app.get_db_connection')
def test_create_item_success(mock_get_db, client):
    """Test POST /api/items creates item successfully."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.lastrowid = 10

    response = client.post(
        '/api/items',
        data=json.dumps({'name': 'New Item', 'description': 'Valid Item'}),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['id'] == 10
    assert data['name'] == 'New Item'

@patch('app.get_db_connection')
def test_delete_item_not_found(mock_get_db, client):
    """Test DELETE /api/items/<id> returns 404 when item does not exist."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0

    response = client.delete('/api/items/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'Item not found'

@patch('app.get_db_connection')
def test_delete_item_success(mock_get_db, client):
    """Test DELETE /api/items/<id> succeeds for existing item."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    response = client.delete('/api/items/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Item deleted'
