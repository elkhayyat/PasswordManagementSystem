import json


class TestRegister:
    def setup(self):
        with open('test_data/register.json') as f:
            self.data = json.load(f)
            self.personal_account_data = self.data.get('personal_account')
            self.business_account_data = self.data.get('business_account')

    def test_register_business_account(self):
        pass

    def test_register_personal_account(self):
        pass
