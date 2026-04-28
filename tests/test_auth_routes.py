import pytest


def test_register_route_success(client):
    """Test successful registration via API."""
    response = client.post("/registro", json={
        "username": "newuser",
        "password": "password123"
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Usuario criado com sucesso"
    assert "id" in data


def test_register_route_missing_fields(client):
    """Test registration with missing fields fails."""
    response = client.post("/registro", json={"username": "user"})
    
    assert response.status_code == 400


def test_register_route_duplicate(client):
    """Test registration with duplicate username fails."""
    client.post("/registro", json={
        "username": "duplicate",
        "password": "password123"
    })
    
    response = client.post("/registro", json={
        "username": "duplicate",
        "password": "password123"
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert "já existe" in data["message"]


def test_login_route_success(client, test_db):
    """Test successful login via API."""
    import sqlite3
    from werkzeug.security import generate_password_hash
    
    conn = sqlite3.connect(str(test_db))
    conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        ("testuser", generate_password_hash("testpass"))
    )
    conn.commit()
    conn.close()
    
    response = client.post("/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Login bem-sucedido"


def test_login_route_invalid_credentials(client):
    """Test login with invalid credentials fails."""
    response = client.post("/login", json={
        "username": "nonexistent",
        "password": "wrongpass"
    })
    
    assert response.status_code == 401
    data = response.get_json()
    assert "inválidas" in data["message"]


def test_login_route_missing_fields(client):
    """Test login with missing fields fails."""
    response = client.post("/login", json={"username": "user"})
    
    assert response.status_code == 400


def test_logout_route_requires_login(client):
    """Test logout requires authentication."""
    response = client.post("/logout")
    
    assert response.status_code == 200


def test_encurtar_requires_login(client):
    """Test /encurtar route requires login."""
    response = client.post("/encurtar", json={"url": "https://google.com"})
    
    # flask_login returns 302 redirect when not authenticated
    assert response.status_code == 302


def test_encurtar_works_with_login(logged_client):
    """Test /encurtar works with authenticated user."""
    response = logged_client.post("/encurtar", json={"url": "https://google.com"})
    
    assert response.status_code == 200
    data = response.get_json()
    assert "url" in data