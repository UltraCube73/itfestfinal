import discord
from foobardb import FoobarDB
from dialogflow_request import request
import gamedata as gd

userdata = FoobarDB('./userdata.db')

token_f = open('token.token', 'r')
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
    await client.change_presence(activity=discord.Game('!help'))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = str(message.author.id)
    user_id_s = str(message.author.id) + '_was-shown'

    msg = cut_notif(message.content)

    if userdata.get(user_id) == False:
        userdata.set(user_id, 'start')
        userdata.set(user_id_s, False)


    if msg.startswith('!игнат'):
        await message.channel.send('```{}```'.format(request(user_id, cut_cmd(msg))))

    else:
        game = gd.GameData()
        func = getattr(game, userdata.get(user_id))
        wasShown = userdata.get(user_id_s)

        if wasShown and gd.selection_list == []:
            wasShown = False
            print(2)

        if wasShown:
            print(2)
            try:
                choice = int(msg)
                if 1 <= choice <= len(gd.selection_list):
                    gd.embed_send_list, gd.send_list = [], []
                    func(choice)
                    for i in gd.embed_send_list:
                        await message.channel.send(embed=i)
                    for i in gd.send_list:
                        await message.channel.send(i)
                    userdata.set(user_id, gd.next_func)
                    userdata.set(user_id_s, False)
                    gd.selection_list = []
                    func = getattr(game, gd.next_func)
                    func(None)

                    for i in gd.embed_send_list:
                        await message.channel.send(embed=i)
                    for i in gd.selection_list:
                        await message.channel.send(i)
                    for i in gd.send_list:
                        await message.channel.send(i)

                    userdata.set(user_id_s, True)
                else:
                    await message.channel.send('Ввод должен являться числом от 1 до {}!'.format(len(gd.selection_list)))
            except Exception as e:
                await message.channel.send('Ввод должен являться целым числом!')

        if not wasShown:
            func(None)

            for i in gd.embed_send_list:
                await message.channel.send(embed=i)
            for i in gd.selection_list:
                await message.channel.send(i)
            for i in gd.send_list:
                await message.channel.send(i)

            userdata.set(user_id_s, True)

client.run(token)
