import requests
import json

from flask import Flask
from flask import request, render_template
from logging import FileHandler
import logging

app = Flask(__name__)

@app.route('/')
def home():
    return 'active'

@app.route('/add_task')
def add_task():
    if request.method == 'GET':
        spider = request.args.get('spider', 'walmart')
        sku = request.args.get('sku', '')
        url = request.args.get('url', '')

        url = 'http://54.183.59.58/schedule.json'

        if not sku or not url:
            return "You should provide one of either sku or url"

        params = {'project': 'spiders',
                  'spider': spider,
                  'sku': sku,
                  'url':url}

        res = requests.post(url, params=params)
        if res.status_code == 200:
            data = json.loads(res.content)
            if data['status'] == 'ok':
                task_id = data['jobid']

                link = 'http://54.183.59.58/items/spiders/' + spider + '/' \
                       + task_id + '.jl'
                return render_template('main.html', link=link)
            else:
                return data['message']
        else:
            return res.content

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

