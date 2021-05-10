import discord
from db import db, User
from dialogflow_request import request
import gamedata as gd

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
    try:
        user = User.query.filter_by(user_id=message.author.id).first()
        user.user_id
    except Exception as e:
        print(1)
        db.create_all()
        new_user = User(user_id=message.author.id, user_func='start', username=message.author.display_name, user_was_shown=False, user_attempts=1)
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(user_id=message.author.id).first()

    if msg.startswith('!help'):
        embed = discord.Embed(title='Основные команды')
        embed.add_field(name='!start', value='Сброс прогресса игры и возврат в начало')
        embed.add_field(name='!игнат <сообщение>', value='Обращение к умному ассистенту')
        embed.add_field(name='!help', value='Просмотр списка команд')
        await message.channel.send(embed=embed)

    elif msg.startswith('!игнат'):
        await message.channel.send('`{}`'.format(request(message.author.id, cut_cmd(msg))))

    elif msg.startswith('!start'):
        user.user_func = 'start'
        db.session.commit()
        await message.channel.send('Прогресс был сброшен!')

    else:
        game = gd.GameData()
        func = getattr(game, user.user_func)
        wasShown = user.user_was_shown

        if wasShown and gd.selection_list == []:
            wasShown = False

        if wasShown:
            try:
                if gd.selection_list != ['next']:
                    choice = int(msg)
                else:
                    choice = 0
                if 1 <= choice <= len(gd.selection_list) or gd.selection_list == ['next']:
                    gd.embed_send_list, gd.send_list = [], []
                    func(choice)
                    for i in gd.embed_send_list:
                        await message.channel.send(embed=i)
                    for i in gd.send_list:
                        await message.channel.send(i)
                    user.user_func = gd.next_func
                    user.user_was_shown = False
                    db.session.commit()

                    func = getattr(game, gd.next_func)
                    gd.embed_send_list, gd.send_list, gd.selection_list = [], [], []
                    func(None)
                    for i in gd.embed_send_list:
                        await message.channel.send(embed=i)
                    if gd.selection_list != ['next']:
                        for i in gd.selection_list:
                            await message.channel.send(i)
                    else:
                        await message.channel.send('Отправьте любое сообщение, чтобы продолжить.')
                    for i in gd.send_list:
                        await message.channel.send(i)

                    user.user_was_shown = True
                    db.session.commit()
                else:
                    await message.channel.send('Ввод должен являться числом от 1 до {}!'.format(len(gd.selection_list)))
            except Exception as e:
                await message.channel.send('Ввод должен являться целым числом!')

        if not wasShown:
            func(None)

            for i in gd.embed_send_list:
                await message.channel.send(embed=i)
            if gd.selection_list != ['next']:
                for i in gd.selection_list:
                    await message.channel.send(i)
            else:
                await message.channel.send('Отправьте любое сообщение, чтобы продолжить.')
            for i in gd.send_list:
                await message.channel.send(i)

            user.user_was_shown = True
            db.session.commit()

client.run(token)
