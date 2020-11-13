from game_logic.utils import info, server_print, warning, print_server_response
from server_utils import MessageType
import asyncio
import logging
import json
import time
import uuid

logging.basicConfig(level=logging.INFO)

#Random user id
user_id = str(uuid.uuid4())

game_id = None

async def play_with_server_request(message, loop):
    """
        The client ask the server to create a new game 
        and send the game id
        @input: json_string message  
        @input: event_loop loop
    """
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888,
                                                   loop=loop)

    logging.debug('Send: %r' % message)
    writer.write(message.encode())

    data = await reader.read(100)
    logging.debug('Received: %r' % data.decode())
    
    message = data.decode()

    print_server_response(message)
    
    logging.debug('Close the socket')
    writer.close()

async def send_launch_game_request(message, loop):
    """
        The client ask the server to create a new game 
        and send the game id

        @input: json_string message  
        @input: event_loop loop
    """
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888,
                                                   loop=loop)

    logging.debug('Send: %r' % message)
    writer.write(message.encode())

    data = await reader.read(100)
    logging.debug('Received: %r' % data.decode())
    
    message = data.decode()
    
    # Store the game id
    global game_id 
    game_id = int(message)

    logging.debug('Close the socket')
    writer.close()


loop = asyncio.get_event_loop()

# Start game request
while game_id is None:
    try:
        info("Starting a new game....")

        payload = {"type": MessageType.START, 
                   "userid": user_id}

        loop.run_until_complete(send_launch_game_request(json.dumps(payload), loop))

    except KeyboardInterrupt:
        info("Stopped game starting ...")
        break

info(f"Connected on game id : {game_id} \n")

# Start game loop
while True:
    try:
        info("\nPlease provide an animal name")
        
        start = time.time()
        word = input()

        payload = {"type": MessageType.PLAY, 
                   "word": word, 
                   "time": int(time.time() - start), 
                   "gameid": game_id}

        loop.run_until_complete(play_with_server_request(json.dumps(payload), loop))

    except KeyboardInterrupt:
        info("Game_finished ...")
        payload = {"type": MessageType.FINISH, 
                   "gameid": game_id, 
                   "userid": user_id}
        loop.run_until_complete(play_with_server_request(json.dumps(payload), loop))
        break

loop.close()