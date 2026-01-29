import pytest
from datetime import datetime
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
from src.account import Account

class TestEmailSending:

    @pytest.fixture(autouse=True)
    def mock_gov_api(self, mocker):
        mock = mocker.patch("src.company_account.requests.get")
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            "result": {"subject": {"statusVat": "Czynny"}}
        }

    def test_send_email_personal_success(self, mocker):
        account = PersonalAccount("Alice", "Cooper", "12345678901")
        account.incoming_transfer(100)
        account.outcoming_transfer(50)
        
        to_email = "alice@example.com"
        today = datetime.now().strftime("%Y-%m-%d")
        expected_subject = f"Account Transfer History {today}"
        expected_body = f"Personal account history: [100, -50]"

        mock_smtp_send = mocker.patch('smtp.smtp.SMTPClient.send', return_value=True)
        result = account.send_history_via_email(to_email)
        assert result is True
        mock_smtp_send.assert_called_once_with(expected_subject, expected_body, to_email)


    def test_send_email_company_failure(self, mocker):
        account = CompanyAccount("TechCorp", "1234567890")
        account.incoming_transfer(5000)
        
        to_email = "ceo@techcorp.com"
        today = datetime.now().strftime("%Y-%m-%d")
        expected_subject = f"Account Transfer History {today}"
        expected_body = f"Company account history: [5000]"
        mock_smtp_send = mocker.patch('smtp.smtp.SMTPClient.send', return_value=False)
        result = account.send_history_via_email(to_email)

        assert result is False
        mock_smtp_send.assert_called_once_with(expected_subject, expected_body, to_email)


    def test_smtp_client_is_instantiated(self, mocker):
        account = PersonalAccount("Bob", "Marley", "12345678901")
        
        mock_smtp_class = mocker.patch('src.account.SMTPClient')
        account.send_history_via_email("test@test.com")
        mock_smtp_class.assert_called_once()

    def test_send_email_base_account_prefix(self, mocker):
        account = Account()
        account.history = [10]

        to_email = "base@example.com"
        today = datetime.now().strftime("%Y-%m-%d")
        expected_subject = f"Account Transfer History {today}"
        expected_body = "Account history: [10]"

        mock_smtp_send = mocker.patch('smtp.smtp.SMTPClient.send', return_value=True)
        result = account.send_history_via_email(to_email)

        assert result is True
        mock_smtp_send.assert_called_once_with(expected_subject, expected_body, to_email)