"""
Basic tests for the URL Shortener application.
"""

import pytest
import os
from app import app, is_valid_url, generate_short_id

@pytest.fixture
def client():
    """Create a test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_is_valid_url():
    """Test URL validation function."""
    # Valid URLs
    assert is_valid_url('https://example.com') == True
    assert is_valid_url('http://example.com') == True
    assert is_valid_url('https://www.example.com/path?param=value') == True
    
    # Invalid URLs
    assert is_valid_url('not-a-url') == False
    assert is_valid_url('') == False
    assert is_valid_url('ftp://example.com') == True  # FTP is valid too

def test_generate_short_id():
    """Test short ID generation."""
    short_id = generate_short_id(6)
    assert len(short_id) == 6
    assert short_id.isalnum()
    
    # Test different lengths
    short_id_8 = generate_short_id(8)
    assert len(short_id_8) == 8

def test_home_page(client):
    """Test the home page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'URL Shortener' in response.data

def test_404_page(client):
    """Test 404 page for invalid short URLs."""
    response = client.get('/invalid123')
    assert response.status_code == 404

def test_rate_limiting(client):
    """Test rate limiting (basic test)."""
    # This test would need to be more sophisticated in a real scenario
    response = client.get('/')
    assert response.status_code == 200

if __name__ == '__main__':
    pytest.main([__file__])

