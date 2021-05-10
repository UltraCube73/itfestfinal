from flask import redirect, url_for
from db import db, User
import function_table as ft
from application import app

index_f = open('index.html', 'r')
index_page = index_f.read()
row = '''<tr style="height: 18px;">
<td style="width: 12.5%; height: 18px;">&nbsp;{}</td>
<td style="width: 37.5%; height: 18px;">&nbsp;{}</td>
<td style="width: 29.5455%; height: 18px;">&nbsp;{}</td>
<td style="width: 20.4545%; height: 18px;">&nbsp;{}</td>
</tr>'''

db.init_app(app)

@app.errorhandler(404)
def not_found(error):
    return 'Error 404', 404

@app.route('/')
def redirect_index():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    users = User.query.all()
    userlist = []
    rowlist = []
    for userdata in users:
        user = dict()
        user['nickname'] = userdata.username
        user['func'] = ft.function_table[userdata.user_func]
        user['attempts'] = userdata.user_attempts
        user['score'] = ft.score_table[userdata.user_func] - user['attempts']
        userlist.append(user)
    userlist = sorted(userlist, key=lambda user: user['score'], reverse=True)
    for i in range(len(userlist)):
        user = userlist[i]
        rowlist.append(row.format(i+1, user['nickname'], user['func'], user['attempts']))
    table = '\n'.join(rowlist)
    return index_page.format(table)