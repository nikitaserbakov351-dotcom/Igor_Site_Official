import pytest
from igor_site import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage_status(client):
    """Проверка, что главная страница открывается без ошибок"""
    response = client.get('/')
    assert response.status_code == 200

def test_music_section_exists(client):
    """Проверка наличия блока с музыкой в разметке"""
    response = client.get('/')
    assert b'id="music"' in response.data
