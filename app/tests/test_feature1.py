import logging
import json
import unittest
import asyncio
from app import create_app, socketio  # Use the correct import for SocketIO

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Feature1TestCase(unittest.TestCase):
    def setUp(self):
        # Create a test instance of the app
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def run_async(self, coro):
        return asyncio.run(coro)

    async def async_test_detect(self):
        payload = {'messages': ['message1', 'message2']}
        response = await self.client.post('/detect', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_detect(self):
        self.run_async(self.async_test_detect())

if __name__ == "__main__":
    unittest.main()
