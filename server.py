from game_logic.game import Game
from game_logic.dictionnary import Dictionnary
from game_logic.utils import server_print
from server_utils import MessageType
import asyncio
import logging
import json

logging.basicConfig(level=logging.DEBUG)
game_ids = 0
my_games = {}

async def handle_requests(reader, writer):
    """
        Handle requests
    """
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    message_json = json.loads(message)
    
    #TODO: Check validity of message here.
    request_type = message_json["type"]

    if request_type == MessageType.START:
        start_game(message_json, writer)

    elif request_type == MessageType.PLAY:
        handle_next_player_move(message_json, writer)

    elif request_type == MessageType.FINISH:
        finish_game(message_json, writer)
    
    await writer.drain()
    
    logging.debug("Close the client socket")
    writer.close()

def start_game(message_json, writer):
    """
        Handles new game crations with id equal to game_ids
    """
    global my_games
    global game_ids
    
    my_games[game_ids] = Game("game_logic/words.txt")
    
    writer.write(str(game_ids).encode())
    game_ids += 1
    

def handle_next_player_move(message, writer):
    """
        handles the wordchain logic here
    """
    global my_games

    my_game = my_games[message["gameid"]]
    
    score_factor = my_game.check_timing(message["time"])

    out = my_game.next(message["word"], score_factor)
    
    if not out[1]:
        logging.debug("Send: %r" % out[0])
        writer.write(out[0].encode())
    else:
        logging.debug("Send error: %r" % out[1])
        writer.write(str(out[1]).encode())

def finish_game(message, writer):
    """
        Handles game finishing
    """
    global my_games

    my_games[message["gameid"]].end()
    del my_games[message["gameid"]]
    
    logging.debug(f"Bye Bye {message['userid']} !")
    writer.write(f"Bye Bye {message['userid']} !".encode())


def main():
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_requests, '127.0.0.1', 8888, loop=loop)
    server = loop.run_until_complete(coro)


    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == "__main__":
    main()