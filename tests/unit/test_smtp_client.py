import unittest
from smtp.smtp import SMTPClient

class TestSMTP(unittest.TestCase):
    def test_send(self):
        smtp = SMTPClient()
        result = smtp.send("Subject", "Body", "email@example.com")
        self.assertFalse(result)
