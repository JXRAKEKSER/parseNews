from flask import Flask, render_template, url_for;
from bson import ObjectId
import index as index_mod;
app = Flask(__name__);

@app.route('/')
def index():
    index_mod.refreshNews();
    item = index_mod.getAllDataList();
    return render_template('index.html', item=item);

@app.route('/news/')
def getNews(url):
    data = index_mod.findNews('/gubernator/tekush/367863/');
    return render_template('news.html', data=data);

if __name__ == '__main__':
    app.run(debug=True);