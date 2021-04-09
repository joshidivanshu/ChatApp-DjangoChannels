from django.test import TestCase
from channels.testing import HttpCommunicator
from .consumers import ChatConsumer
import pytest

class MyTests(TestCase):
    @pytest.mark.asyncio
    async def test_my_consumer(self):
        communicator = HttpCommunicator(ChatConsumer, "GET", "/test/")
        response = await communicator.get_response()
        self.assertEqual(response["body"], b"test response")
        self.assertEqual(response["status"], 200)









# from channels.testing import ApplicationCommunicator
# communicator = ApplicationCommunicator(ChatConsumer, {"type": "http"})

# await communicator.send_input({
#     "type": "http.request",
#     "body": b"chunk one \x01 chunk two",
# })