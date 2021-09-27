class News:
    def __init__(self, title = 'default-title', date = 'default-date', text = 'default-text', url = 'default-url', image = 'default-image', id_=''):
        self.__title = title;
        self.__date = date;
        self.__text = text;
        self.__url = url;
        self.__image = image;
        self.__id = id_;
    def setTitle(self, title):
        self.__title = title;
    def getTitle(self):
        return self.__title;

    def setDate(self, date):
        self.__date = date;

    def getDate(self):
        return self.__date;

    def setText(self, text):
        self.__text = text;

    def getText(self):
        return self.__text;

    def setUrl(self, url):
        self.__url = url;

    def getUrl(self):
        return self.__url;

    def setImage(self, image):
        self.__image =image;
    def getImage(self):
        return self.__image;

    def setId(self, id_):
        self.__id = id_;
    def getId(self):
        return self.__id;
