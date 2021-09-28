import re;
import requests
from bs4 import BeautifulSoup


from News import News;
import crud;
import json;
url = 'http://www.volgograd.ru';

def parseNote(newsUrl):
    newsPageReq = requests.get(newsUrl);
    soupObj = BeautifulSoup(newsPageReq.text, 'lxml');
    newsObj = News();
    newsObj.setTitle(re.sub('\s+', ' ', soupObj.find('h1').text));
    newsObj.setUrl(newsUrl);
    newsObj.setText(re.sub('\s+', ' ', soupObj.find('div', class_ = 'news-detail').find('p').text));
    newsObj.setDate(re.sub('\s+',' ',soupObj.find('div', class_ = 'date').text));
    newsObj.setImage(url+str(soupObj.find('img', class_ = 'detail_picture')['src']));
    return newsObj;
def parseNewsUrlList(url):

    indexPage =  requests.get(url);
    soup = BeautifulSoup(indexPage.text, 'lxml');
    newsUrlList = soup.find('div', class_='news-feed').find_all('a');
    return newsUrlList;


def refreshNews():
    crud.collection.delete_many({});
    print(crud.collection.count_documents({}));
    for newsListItem in parseNewsUrlList(url):
        news = parseNote(url+newsListItem.get('href'));
        crud.insertData(crud.collection, {'title': news.getTitle(), 'date': news.getDate(), 'text': news.getText(), 'url': news.getUrl(), 'image': news.getImage()});

##print(crud.findData(crud.collection, {'title': 'В Волгоградской области с начала года удвоилось число самозанятых '}));

def findNews(urlWithoutDomain):
     list = [];
     dbObj = crud.collection.find_one({'url': 'http://www.volgograd.ru/'+urlWithoutDomain});
     list.append({'title': dbObj['title'], 'date' : dbObj['date'],'text' : dbObj['text'],'url' : dbObj['url'], 'image' : dbObj['image']});
     return list;

def getAllDataList():
    list = [];
    for item in crud.collection.find():
        list.append({ 'id':str(item['_id']), 'title':item['title'], 'date' : item['date'],'text' : item['text'],'url' : item['url'], 'image' : item['image']});
    return list;
if __name__ == '__main__':
    print(getAllDataList());





