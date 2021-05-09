from flask import Flask, redirect, url_for
from foobardb import FoobarDB
import function_table as ft

app = Flask(__name__)

index_f = open('index.html', 'r')
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
    userdata = FoobarDB('./userdata.db')
    f = open('userlist.list', 'r')
    idlist = f.read().split('\n')
    del idlist[-1]
    f.close()
    del f
    userlist = []
    rowlist = []
    for id in idlist:
        user = dict()
        user['nickname'] = userdata.get(id + '_nickname')
        user['func'] = ft.function_table[userdata.get(id)]
        user['attempts'] = userdata.get(id + '_attempts')
        user['score'] = ft.score_table[userdata.get(id)] - user['attempts']
        userlist.append(user)
    userlist = sorted(userlist, key=lambda user: user['score'], reverse=True)
    for i in range(len(userlist)):
        user = userlist[i]
        rowlist.append(row.format(i+1, user['nickname'], user['func'], user['attempts']))
    del userdata
    table = '\n'.join(rowlist)
    return index_page.format(table)
if __name__ == '__main__':
    app.run()