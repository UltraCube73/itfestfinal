from flask import Flask, redirect, url_for
from foobardb import FoobarDB
userdata = FoobarDB('/home/mishail/PycharmProjects/pythonProject1/userdata.db')
app = Flask(__name__)

index_f = open('/home/mishail/PycharmProjects/pythonProject1/index.html', 'r')
index_page = index_f.read()
row = '''<tr style="height: 18px;">
<td style="width: 12.5%; height: 18px;">&nbsp;{}</td>
<td style="width: 37.5%; height: 18px;">&nbsp;{}</td>
<td style="width: 29.5455%; height: 18px;">&nbsp;{}</td>
<td style="width: 20.4545%; height: 18px;">&nbsp;{}</td>
</tr>'''



@app.errorhandler(404)
def not_found(error):
    return 'Error 404', 404

@app.route('/')
def redirect_index():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    f = open('/home/mishail/PycharmProjects/pythonProject1/userlist.list', 'r')
    idlist = f.read().split('\n')
    del idlist[-1]
    f.close()
    del f
    userlist = []
    rowlist = []
    for id in idlist:
        user = dict()
        user['nickname'] = userdata.get(id + '_nickname')
        user['func'] = userdata.get(id)
        user['attempts'] = userdata.get(id + '_attempts')
        userlist.append(user)
    for i in range(len(userlist)):
        user = userlist[i]
        rowlist.append(row.format(i+1, user['nickname'], user['func'], ''))
    table = '\n'.join(rowlist)
    return index_page.format(table)