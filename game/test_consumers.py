import pytest
from channels.testing import WebsocketCommunicator
from django.test import Client

from .routing import application
from main.models import User
from game.models import WarfareGame


@pytest.fixture
async def communicator():
    user = User.objects.create_user(username='ws-testuser', password='password')
    client = Client()
    client.force_login(user)
    cookies = (b'cookie', '{}={}'.format('ssid', client.cookies['ssid'].value).encode())
    ws_communicator = WebsocketCommunicator(application, 'ws/warfare', headers=[cookies])
    yield ws_communicator
    await ws_communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_game(communicator):
    game = WarfareGame(name='alpha')
    game.save()

    connected = await communicator.connect()
    assert connected, 'Authenticated user was unable to connect.'


