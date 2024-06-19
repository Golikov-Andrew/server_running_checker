import json
import os
import socket
import traceback

import requests
from dotenv import load_dotenv

from telegram_notifier.telegram_notifier import TelegramNotifier
from telegram_notifier.tnconf import is_activated, bot_token, telegram_clients

temp_json_file_path = 'temp_file.json'

if __name__ == '__main__':
    load_dotenv()
    CHECK_SERVER_IP = os.getenv('CHECK_SERVER_IP')
    CHECK_SERVER_PORT = os.getenv('CHECK_SERVER_PORT')
    with open(temp_json_file_path, 'r') as f:
        program_object = json.load(f)


    def notify_clients():
        telegram_notifier = TelegramNotifier(
            is_activated, bot_token, 'telegram_notifier_log.txt')
        telegram_notifier.load_clients(telegram_clients)
        ans = telegram_notifier.send_message_to('GAV', message)
        print(ans)
        with open(temp_json_file_path, 'w') as f:
            json.dump(program_object, f)


    message = 'server is running'
    try:
        response = requests.get(
            f'http://{CHECK_SERVER_IP}:{CHECK_SERVER_PORT}')
    except OSError:
        message = 'server is stopped'
        if program_object['server_running']:
            program_object['server_running'] = False
            notify_clients()

    else:
        message = 'server is running'
        if not program_object['server_running']:
            program_object['server_running'] = True
            notify_clients()
