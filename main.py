import sys
from pyrogram import Client
from configparser import ConfigParser

config_object = ConfigParser()

anim = ['|', '/', '-', '\\']

def save_ini(config_object):
    with open('config.ini', 'w') as conf:
        config_object.write(conf)

def backup(app, posts):
    with app:
        count = 0
        for message in app.iter_history(posts['channel']):
            sys.stdout.write('\rloading ' + anim[count % len(anim)])
            if message.author_signature == posts['signature']:
                count += 1
                app.copy_message(posts['backup'], posts['channel'], message.message_id)
    sys.stdout.write('\r')
    print(f'Backuped {count} messages\n')

def clear(app, posts):
    with app:
        count = 0
        for message in app.iter_history(posts['channel']):
            sys.stdout.write('\rloading ' + anim[count % len(anim)])
            if message.author_signature == posts['signature']:
                count += 1
                app.delete_messages(posts['channel'], message.message_id)
    sys.stdout.write('\r')
    print(f'Deleted {count} messages')

def main():
    config_object.read("config.ini")

    try:
        userinfo = config_object["USERINFO"]
        posts = config_object["POSTS"]
    except KeyError:
        config_object["USERINFO"] = {
            "api_id": 'None',
            "api_hash": 'None'
        }

        config_object["POSTS"] = {
            "channel": 'None',
            "backup": 'None',
            "signature": 'None'
        }

        save_ini(config_object)

        userinfo = config_object["USERINFO"]
        posts = config_object["POSTS"]


    if userinfo['api_id'] == 'None' or userinfo['api_hash'] == 'None':
        print('Insert the following data by taking them from https://my.telegram.org/')
        ai = input('api_id: ')
        ah = input('api_hash: ')
        
        userinfo['api_id'] = ai
        userinfo['api_hash'] = ah

        save_ini(config_object)

    if (posts['channel'] == 'None' or posts['signature'] == 'None') or input('do you want to change channel ids for deletion and backup? y/n ') == 'y':
        print('Get channel id from https://t.me/JsonDumpBot \n(forward_from_chat.id)')
        channel = input('channel id: ')
        signature = input('posts with whose signature you need to process: ')

        if input('is it necessary to backup messages? y/n ') == 'y':
            bckp = input('backup channel id: ')
            posts['backup'] = bckp

        posts['channel'] = channel
        posts['signature'] = signature

        save_ini(config_object)

    app = Client('tg_clear_posts', api_id=userinfo['api_id'], api_hash=userinfo['api_hash'])

    while True:
        ans = input('what do you want to do? backup/clear/exit: ')
        print(' ')
        if ans == 'backup':
            backup(app, posts)
        elif ans == 'clear':
            clear(app, posts)
        elif ans == 'exit':
            exit()
        else:
            print('command not found')

if __name__ == '__main__':
    main()

            