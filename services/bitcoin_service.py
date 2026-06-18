import os
import requests

class BitcoinService:
    def __init__(self):
        # ดึง Key จากไฟล์ .env ที่บอสทำไว้
        self.api_key = os.getenv("UNISAT_API_KEY")
        self.base_url = "https://open-api.unisat.io/v1"

    def get_balance(self, address):
        # คำสั่งดึงยอดเงิน
        url = f"{self.base_url}/indexer/address/{address}/balance"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)
        return response.json()
