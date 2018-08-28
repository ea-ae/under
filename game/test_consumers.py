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

    # Make sure the 'Home' tab returns no extra data, since a cult has not been created yet
    await communicator.send_json_to({
        'type': 'page_data', 
        'page': 'home'
    })
    response = await communicator.receive_json_from()
    assert response == {'type': 'page_data', 'page': 'home'}, 'Empty home page data was not returned.'

    # Create a cult and check if redirection message is received
    await communicator.send_json_to({
        'type': 'create_cult',
        'cult_data': {'cult_name': 'cultname',
                      'cult_type': 'chi'}
    })

    response = await communicator.receive_json_from()
    assert response == {'type': 'page_redirect', 'page': 'contacts'}, 'Incorrect page redirect response.'

    # Contacts page mission completion

    await communicator.send_json_to({
        'type': 'page_data',
        'page': 'contacts'
    })

    response = await communicator.receive_json_from()
    assert response['contacts']['anonymous']['options'][0]['enabled'] is False,\
        'Objective not completed, yet it is enabled.'

    # Buy an HQ upgrade

    await communicator.send_json_to({
        'type': 'hq_upgrade',
        'command': 'buy',
        'item': 'windowbars'
    })

    # Check if mission requirement complete and select it

    await communicator.send_json_to({
        'type': 'page_data',
        'page': 'contacts'
    })

    response = await communicator.receive_json_from()
    assert response['contacts']['anonymous']['options'][0]['enabled'] is True, \
        'Objective is completed, yet it is disabled.'

    await communicator.send_json_to({
        'type': 'card_choice',
        'contact': 'anonymous',
        'choice': 0
    })

    response = await communicator.receive_json_from()
