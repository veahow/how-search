from flask import Flask
from flask import render_template
from flask import request
import requests

app = Flask(__name__)

def getHTML(wd, pn):
    '''
    爬虫函数 获取百度搜索字
    '''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    url = 'https://www.baidu.com/s?wd=%s&pn=%s' % (wd, pn)

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('网页获取失败')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/s')
def search():
    '''
    搜索关键字传送函数
    '''
    if request.method == 'GET':
        wd = request.args.get('wd')
        pn = request.args.get('pn')
        print(getHTML(wd, pn)) 
    else:
        return '失败 Failed'

if __name__ == '__main__':
    app.run(debug=True, port=8000)