from flask import Flask, jsonify, redirect, render_template, request
import requests
import re

app = Flask(__name__)

@app.route('/')
def site():
    return render_template('index.html');

@app.route('/watch')
def video_player():
    query_param = request.args.get('vid', default=None)
    if query_param is None:
        return redirect('/')
    return render_template('player.html',vid=query_param)

@app.route('/youtube')
def yt():
    datas = []
    url = "https://www.youtube.com"
    query_param = request.args.get('q', default='')
    if query_param:
        url = "https://www.youtube.com/results?search_query="+query_param;
    response = requests.get(url);
    links = re.findall(r'https://i.ytimg.com[^"]*',response.text);
    for link in links:
        start = link.find('/vi/') + 4
        end = link.find('/', start)
        vid = link[start:end]
        if datas and datas[-1]["video"] != vid:
            data = {
                "img": link,
                "video": vid
            }
            #title = re.search(r'{"url":"{data["video"]}.{0,333}{"text":"([^"]*)"',response.text)
            #title = re.findall(r'{"url":"' + re.escape(data["video"]) + r'.*{"text":"([^"]*)"', response.text, re.DOTALL)
            #data["title"] = title;
            datas.append(data)
        elif not datas:
            data = {
                "img": link,
                "video": vid
            }
            datas.append(data)
    return datas;

@app.route('/test')
def test():
    response = requests.get("https://www.youtube.com")
    return response.text

#only for local use
#"""
if __name__ == '__main__':
    app.run(debug=True)
#"""