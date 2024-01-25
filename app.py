from flask import Flask, request
import requests
import re

app = Flask(__name__)

@app.route('/')
def site():
    query_param = request.args.get('q', default='bpn333')
    source = """
    <script>
    fetch("/youtube?q="""+query_param+'''").then(r => r.json()).then(data =>{
    console.log(data);
    data.forEach(src => {
    var img = document.createElement("img");
    img.src = src.img;
    var container = document.createElement("div");
    container.addEventListener('click',()=>{
    container.innerHTML = "";
    var tmp = document.createElement("iframe");
    tmp.width = 1046;
    tmp.height = 523;
    tmp.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
    tmp.src = "https://www.youtube.com/embed/" + src.video;
    container.appendChild(tmp);
    })
    container.appendChild(img);
    document.body.appendChild(container);
    //var an = document.createElement("a");
    //an.href = "https://www.youtube.com/watch?v="+src.video;
    //an.appendChild(img);
    //document.body.appendChild(an);
    });
    });
    </script>
    '''
    return source

@app.route('/youtube')
def yt():
    datas = []
    query_param = request.args.get('q', default='')
    url = "https://www.youtube.com/results?search_query="
    response = requests.get(url+query_param);
    links = re.findall(r'https://i.ytimg.com[^"]*',response.text);
    for link in links:
        start = link.find('/vi/') + 4
        end = link.find('/', start)
        vid = link[start:end]
        data = {
            "img": link,
            "video": vid
        }
        datas.append(data);
    return datas;

if __name__ == '__main__':
    app.run(debug=True)