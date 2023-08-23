import requests
from datetime import datetime

telegram_bot_token = ""


def send_message(chat_id, text):
    token = telegram_bot_token
    tlg_url = "https://api.telegram.org/bot{}/".format(token)
    params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    method = 'sendMessage'
    response = requests.post(tlg_url + method, params)
    return response


def get_updates(offset, timeout=5):
    method = 'getUpdates'
    limit = 100
    token = telegram_bot_token
    tlg_url = "https://api.telegram.org/bot{}/".format(token)
    params = {'timeout': timeout, 'offset': offset, 'limit': limit}
    resp = requests.get(tlg_url + method, params)
    result_json = resp.json()['result']
    return result_json


def get_last_update(offset=None):
    result = get_updates(offset)
    last_update = None
    if len(result) > 0:
        if offset is None:
            last_update = result[-1]
        else:
            for item in result:
                if str(item['update_id']) == str(offset):
                    last_update = item
    return last_update


def main():
    update_id = None
    while True:
        try:
            last_update = get_last_update(update_id)
            update_id = last_update['update_id']
            if last_update is not None and update_id is not None:
                if update_id <= last_update['update_id']:
                    update_id = update_id + 1
                    if 'message' in last_update:
                        chat_id = last_update['message']['chat']['id']
                        text = last_update['message']['text']
                        send_message(chat_id, text)
        except Exception as e:
            str_log = f"{datetime.now().strftime('%d.%m.%Y %H:%M:%S')} - main(): {e}"
            print(str_log)


if __name__ == '__main__':
    main()
