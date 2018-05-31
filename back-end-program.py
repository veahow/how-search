from flask import Flask
from flask import render_template
from flask import request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_html(content, page=0, engine='baidu'):
    '''
    爬虫函数 爬取搜索页面内容
    '''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    if engine == 'baidu':
        url = 'https://www.baidu.com/s?wd=%s&pn=%s' % (content, page)
    elif engine == 'bing':
        url = 'https://cn.bing.com/search?q=%s&first=%s' % (content, page)
    elif engine == 'sogou':
        url = 'https://www.sogou.com/web?query=%s&page=%s' % (content, page)
    
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('网页获取失败')

def get_result(html, content, engine='baidu'):
    soup = BeautifulSoup(html, 'html.parser')
    if engine == 'baidu':
        vars = soup.find_all('div', 'result c-container ')
    elif engine == 'bing':
        vars = soup.find_all('li', 'b_algo')
    elif engine == 'sogou':
        vars = soup.find_all('div', 'vrwrap')

    titles = []
    hrefs = []
    for var in vars:
        if var == None:
            continue

        if engine == 'baidu':
            if var.h3 == None:
                continue
            a_tag = var.h3.a
        elif engine == 'bing':
            if var.h2 == None:
                continue
            a_tag = var.h2.a
        elif engine == 'sogou':
            if var.h3 == None:
                continue
            a_tag = var.h3.a
        title = ''

        hrefs.append(a_tag['href'])

        for i in range(0, len(a_tag.contents)):
            title += str(a_tag.contents[i])
        titles.append(title)   
    
    length = len(hrefs)
    return render_template('result.html', content=content, titles=titles, hrefs=hrefs, length=length)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/s')
def search():
    '''
    搜索关键字传送函数
    '''
    if request.method == 'GET':
        content = request.args.get('content')
        page = request.args.get('page')
        engine = request.args.get('engine')

        html = get_html(content, page, engine)

        return get_result(html, content, engine)
    else:
        return '失败 Failed'

if __name__ == '__main__':
    app.run(debug=True, port=8000)