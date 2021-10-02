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
    textAccum = '';
    for paragraph in soupObj.find('div', class_ = 'news-detail').find_all('p'):
        if(len(paragraph.text)>0):
            textAccum = textAccum + re.sub('\s+', ' ', paragraph.text);
    newsObj.setText(textAccum);
    newsObj.setDate(re.sub('\s+',' ',soupObj.find('div', class_ = 'date').text));
    newsObj.setImage(url+str(soupObj.find('img', class_ = 'detail_picture')['src']));
    return newsObj;

def parseNewsUrlList(url):

    indexPage =  requests.get(url);
    soup = BeautifulSoup(indexPage.text, 'lxml');
    newsUrlList = soup.find('div', class_='news-feed').find_all('a');
    return newsUrlList;


def refreshNews():

    for newsListItem in parseNewsUrlList(url):
        news = parseNote(url + newsListItem.get('href'));
        if (crud.collection.find_one({'title': news.getTitle()}) is None):
            crud.insertData(crud.collection,
                            {'title': news.getTitle(), 'date': news.getDate(),
                             'text': news.getText(),
                             'url': news.getUrl(), 'image': news.getImage()});
        else:
            pass



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
    refreshNews();








