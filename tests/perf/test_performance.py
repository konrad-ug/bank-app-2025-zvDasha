import pytest
import requests
import random

class TestPerformance:
    BASE_URL = "http://127.0.0.1:5000/api/accounts"
    TIMEOUT = 0.5  

    @pytest.fixture(scope="function")
    def session(self):
        with requests.Session() as s:
            yield s

    def _generate_pesel(self):
        return ''.join(str(random.randint(0, 9)) for _ in range(11))

    def test_perf_create_delete_loop(self, session):
        for i in range(100):
            pesel = self._generate_pesel()
            payload = {
                "name": "Perf",
                "surname": "Tester",
                "pesel": pesel
            }

            resp_create = session.post(self.BASE_URL, json=payload, timeout=self.TIMEOUT)
            assert resp_create.status_code == 201, f"Iteration {i}: Failed to create"

            resp_delete = session.delete(f"{self.BASE_URL}/{pesel}", timeout=self.TIMEOUT)
            assert resp_delete.status_code == 200, f"Iteration {i}: Failed to delete"

    def test_perf_create_transfer_loop(self, session):
        pesel = self._generate_pesel()
        setup_payload = {
            "name": "Transfer",
            "surname": "Master",
            "pesel": pesel
        }
        
        resp_setup = session.post(self.BASE_URL, json=setup_payload, timeout=self.TIMEOUT)
        assert resp_setup.status_code == 201, "Setup failed"

        transfer_amount = 10
        transfer_payload = {"amount": transfer_amount, "type": "incoming"}

        try:
            for i in range(100):
                resp = session.post(
                    f"{self.BASE_URL}/{pesel}/transfer", 
                    json=transfer_payload, 
                    timeout=self.TIMEOUT
                )
                assert resp.status_code == 200

            resp_get = session.get(f"{self.BASE_URL}/{pesel}", timeout=self.TIMEOUT)
            assert resp_get.status_code == 200
            
            actual_balance = resp_get.json()["balance"]
            expected_balance = 100 * transfer_amount
            assert actual_balance == expected_balance, f"Balance mismatch! Got {actual_balance}, expected {expected_balance}"

        finally:
            session.delete(f"{self.BASE_URL}/{pesel}", timeout=self.TIMEOUT)