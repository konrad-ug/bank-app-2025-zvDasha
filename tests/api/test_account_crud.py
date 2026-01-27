import pytest
import requests

URL = "http://127.0.0.1:5000/api/accounts"

def test_create_and_get_all_accounts():
    unique_pesel = "06923847512"
    payload = {"name": "Joe", "surname": "Tone", "pesel": unique_pesel}
    
    requests.post(URL, json=payload)
    
    response = requests.get(URL)
    assert response.status_code == 200
    accounts = response.json()
    assert any(acc["pesel"] == unique_pesel for acc in accounts)

def test_get_account_by_pesel():
    unique_pesel = "01929487674"
    payload = {"name": "Joe", "surname": "Tone", "pesel": unique_pesel}
    requests.post(URL, json=payload)

    response = requests.get(f"{URL}/{unique_pesel}")
    assert response.status_code == 200
    assert response.json()["pesel"] == unique_pesel
    assert response.json()["name"] == "Joe"

def test_get_non_existent_account():
    response = requests.get(f"{URL}/00000000000")
    assert response.status_code == 404
    assert response.json()["message"] == "Account not found"

def test_update_account():
    unique_pesel = "02848837465"
    requests.post(URL, json={"name": "Joe", "surname": "Tone", "pesel": unique_pesel})

    update_data = {"name": "Den"}
    patch_response = requests.patch(f"{URL}/{unique_pesel}", json=update_data)
    assert patch_response.status_code == 200

    get_response = requests.get(f"{URL}/{unique_pesel}")
    assert get_response.json()["name"] == "Den"
    assert get_response.json()["surname"] == "Tone"

def test_delete_account():
    unique_pesel = "03193847561"
    requests.post(URL, json={"name": "Mira", "surname": "Tor", "pesel": unique_pesel})

    del_response = requests.delete(f"{URL}/{unique_pesel}")
    assert del_response.status_code == 200
    get_response = requests.get(f"{URL}/{unique_pesel}")
    assert get_response.status_code == 404