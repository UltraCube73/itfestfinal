from flask import Flask, redirect, url_for, render_template
from foobardb import FoobarDB
userdata = FoobarDB('./userdata.db')
app = Flask(__name__)

index_f = open('index.html', 'r')
index = index_f.read()
row = '''<tr style="height: 18px;">
<td style="width: 12.5%; height: 18px;">&nbsp;{}</td>
<td style="width: 37.5%; height: 18px;">&nbsp;{}</td>
<td style="width: 29.5455%; height: 18px;">&nbsp;{}</td>
<td style="width: 20.4545%; height: 18px;">&nbsp;{}</td>
</tr>'''

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

@app.route('/')
def redirect():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    f = open('userlist.list', 'r')
    idlist = f.read().split('\n')
    f.close()
    del f
    userlist = []
    for id in idlist:
        user = dict()
        user['nickname'] = userdata.get(id + '_nickname')
        user['func'] = userdata.get(id)
        user['attempts'] = userdata.get(id + '_attempts')
        userlist.append(user)
    print(userlist)
    return userlist