import pytest
import requests

URL = "http://127.0.0.1:5000/api/accounts"

@pytest.fixture
def create_account():
    def _create(pesel, balance=0):
        requests.delete(f"{URL}/{pesel}")
        payload = {
            "name": "John", 
            "surname": "Dor", 
            "pesel": pesel
        }
        resp = requests.post(URL, json=payload)
        assert resp.status_code == 201, f"Failed to create account: {resp.text}"
        
        if balance > 0:
            resp_transfer = requests.post(f"{URL}/{pesel}/transfer", json={
                "amount": balance, 
                "type": "incoming"
            })
            assert resp_transfer.status_code == 200
            
        return pesel
    return _create


def test_incoming_transfer(create_account):
    pesel = create_account("90000000001", balance=0)
    response = requests.post(f"{URL}/{pesel}/transfer", json={
        "amount": 100,
        "type": "incoming"
    })
    
    assert response.status_code == 200
    assert response.json()["message"] == "Order accepted for processing"
    acc = requests.get(f"{URL}/{pesel}").json()
    assert acc["balance"] == 100

def test_outgoing_transfer(create_account):
    pesel = create_account("90000000002", balance=500)
    response = requests.post(f"{URL}/{pesel}/transfer", json={
        "amount": 200,
        "type": "outgoing"
    })
    
    assert response.status_code == 200
    acc = requests.get(f"{URL}/{pesel}").json()
    assert acc["balance"] == 300

def test_outgoing_transfer_not_enough_money(create_account):
    pesel = create_account("90000000003", balance=50)
    response = requests.post(f"{URL}/{pesel}/transfer", json={
        "amount": 100,
        "type": "outgoing"
    })
    
    assert response.status_code == 422
    assert response.json()["message"] == "Not enough money"

def test_express_transfer(create_account):
    pesel = create_account("90000000004", balance=100)
    response = requests.post(f"{URL}/{pesel}/transfer", json={
        "amount": 10,
        "type": "express"
    })
    
    assert response.status_code == 200
    acc = requests.get(f"{URL}/{pesel}").json()
    assert acc["balance"] == 89

def test_transfer_invalid_type(create_account):
    pesel = create_account("90000000005")

    response = requests.post(f"{URL}/{pesel}/transfer", json={
        "amount": 100,
        "type": "scam_method"
    })
    
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid transfer type"

def test_transfer_account_not_found():
    response = requests.post(f"{URL}/00000000000/transfer", json={
        "amount": 100,
        "type": "incoming"
    })
    
    assert response.status_code == 404
    assert response.json()["message"] == "Account not found"