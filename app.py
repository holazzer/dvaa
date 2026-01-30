import os
from flask import Flask, render_template, session, request, redirect, url_for, jsonify

app = Flask(__name__)
app.secret_key = b'17c7d9ce5beb164e1a991453827fa8ea0541e530c7b87a3fbebf01bc1a0567b0'


@app.route('/')
def hello():
    username = session.get('username')
    return render_template("hello.html", username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('task'))
    username = session.get('username')
    if username: return redirect(url_for('hello'))
    return render_template("login.html")


@app.route('/task', methods=['GET', 'POST'])
def task():
    username = session.get('username')
    if not username:
        return redirect(url_for('hello'))
    if not os.path.exists(f'{username}.txt'):
        open(f'{username}.txt', 'w').close()
    entries = {}
    with open(f'{username}.txt', 'r', encoding='utf-8') as f:
        for line in f:
            idx, label = line.split(',')
            entries[idx] = label
    task_ls = os.listdir('static/t100')
    for k in entries: task_ls.remove(k)
    t1 = task_ls[0]
    return render_template("task.html", task_name=t1, username=username)


@app.route('/val')
def val():
    username = session.get('username')
    if not username: return jsonify({'code': -1})
    tid = request.args.get('tid')
    task_ls = os.listdir('static/t100')
    if tid not in task_ls: return jsonify({'code': 404})
    correct = request.args.get('correct')
    if correct == '0' or correct == '1':
        with open(f'{username}.txt', 'a', encoding='utf-8') as f:
            f.write(f'{tid},{correct}\n')
            return jsonify({'code': 200})
    else: return jsonify({'code': -2})


if __name__ == '__main__':
    app.run(debug=True)
