import discord
from db import db, User
from dialogflow_request import request
import gamedata as gd

gdlist = {}

token_f = open('token', 'r')
token = token_f.read()

client = discord.Client()

def cut_notif(word):
    word = word.split()
    if word[0].find('<@') != -1:
        word.pop(0)
    return ' '.join(word)

def cut_cmd(word):
    word = word.split()
    if word[0].find('!') != -1:
        word.pop(0)
    return ' '.join(word)

@client.event
async def on_ready():
    print('username: {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!help"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = cut_notif(message.content)

    user = User.query.filter_by(user_id=message.author.id).first()
    if user == None:
        print('\n---\nNew user detected: {}\nAdding to db...'.format(str(message.author.id)))
        new_user = User(user_id=message.author.id, user_func='start', username=message.author.display_name, user_was_shown=False, user_attempts=1)
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(user_id=message.author.id).first()
        print('Done!\n---\n')

    if msg.startswith('!help'):
        embed = discord.Embed(title='Основные команды')
        embed.add_field(name='!игнат <сообщение>', value='Обращение к умному ассистенту')
        embed.add_field(name='!help', value='Просмотр списка команд')
        await message.channel.send(embed=embed)

    elif msg.startswith('!игнат'):
        print('\n---\nNew df request\nUser: {}\nMessage: {}'.format(str(message.author.id), cut_cmd(msg)))
        response = request(message.author.id, cut_cmd(msg))
        await message.channel.send('`{}`'.format(response))
        print('Response: {}\n---\n'.format(response))

    elif msg.startswith('!'):
        await message.channel.send('Неизвестная команда!')

    else:
        try:
            game = gdlist[str(message.author.id)]
        except Exception as e:
            print('\n---\nNew user connected: {}\n---\n'.format(str(message.author.id)))
            gdlist[str(message.author.id)] = gd.UserObject
            game = gdlist[str(message.author.id)]
        game.id = message.author.id
        func = getattr(game.GameData(), user.user_func)

        wasShown = user.user_was_shown
        if wasShown and game.selection_list == []:
            wasShown = False

        if wasShown:
            try:
                if game.selection_list != ['next']:
                    choice = int(msg)
                else:
                    choice = 0
                if 1 <= choice <= len(game.selection_list) or game.selection_list == ['next']:
                    game.embed_send_list, game.send_list = [], []

                    func(choice)

                    for i in game.embed_send_list:
                        if type(i) is str:
                            await message.channel.send(i)
                        else:
                            await message.channel.send(embed=i)
                    for i in game.send_list:
                        await message.channel.send(i)
                    user.user_func = game.next_func
                    user.user_was_shown = False
                    db.session.commit()

                    func = getattr(game.GameData(), game().next_func)
                    game.embed_send_list, game.send_list, game.selection_list = [], [], []

                    func(None)

                    for i in game.embed_send_list:
                        if type(i) is str:
                            await message.channel.send(i)
                        else:
                            await message.channel.send(embed=i)
                    if game.selection_list != ['next']:
                        for i in game.selection_list:
                            await message.channel.send(i)
                    else:
                        await message.channel.send('Отправьте любое сообщение, чтобы продолжить.')
                    for i in game.send_list:
                        await message.channel.send(i)

                    user.user_was_shown = True
                    db.session.commit()
                else:
                    await message.channel.send('Ввод должен являться числом от 1 до {}!'.format(len(game.selection_list)))
            except Exception as e:
                await message.channel.send('Ввод должен являться целым числом!')

        if not wasShown:

            game.embed_send_list, game.send_list, game.selection_list = [], [], []

            func(None)

            for i in game.embed_send_list:
                if type(i) is str:
                    await message.channel.send(i)
                else:
                    await message.channel.send(embed=i)
            if game.selection_list != ['next']:
                for i in game.selection_list:
                    await message.channel.send(i)
            else:
                await message.channel.send('Отправьте любое сообщение, чтобы продолжить.')
            for i in game.send_list:
                await message.channel.send(i)

            user.user_was_shown = True
            db.session.commit()

client.run(token)
