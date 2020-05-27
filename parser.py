import requests

from bs4 import BeautifulSoup


URL = 'https://www.zakon.kz/news'
HOST = 'https://www.zakon.kz'

#Заголовки нужны для того чтоб не блокали ip
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'accept': '*/*',
}


def get_HTML(url, params=None):
    '''Функция которая возвращает Html страницу'''
    req = requests.get(url, headers=HEADERS, params=params)
    return req


def get_Content(html):
    '''Функция для вохврата Контента с основновного URL'''
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='cat_news_item')

    articles_content = []
    for item in items:
        try:
            com = item.find('span', class_='comm_num').get_text(strip=True)
        except:
            com = 'No comments'
        try:
            articles_content.append({
                'title': item.find('a', class_='tahoma font12').get_text(strip=True),
                'href': HOST + item.find('a', class_='tahoma font12').get('href'),
                'date': date + " " +item.find('span', class_="tahoma font12 date n3").get_text(strip=True),
                'com': com,
                'text': None
            })
        except:
            date = item.find('span', class_='tahoma font12 date n2').get_text(strip=True)
    return articles_content


def add_Text(article_html):
    '''Функция для получения текста статьи для первого вида страниц'''
    soup = BeautifulSoup(article_html, 'html.parser')

    text = soup.find('div', class_='full_text').get_text(strip=True)
    return text


def add_Text_For_Two_Page(article_html):
    '''Функция для получения текста статьи для второго вида страниц'''
    soup = BeautifulSoup(article_html, 'html.parser')

    text = soup.find('div', class_='full_story').get_text(strip=True)
    return text


def parse():
    """Основная функция"""
    html = get_HTML(URL)
    if html.status_code == 200:
        #Создание экземпляра Словаря с данными
        articles = get_Content(html.text)
        for i in range(len(articles)):
            try:
                print(f"Парсинг статьи {i} из {len(articles)}")
                #Получения ссылки на страничку
                article_url = articles[i]['href']
                #Получени HTML страницы
                article_html = get_HTML(article_url)
                #Добавление в словать текста ститьи
                articles[i]['text'] = add_Text(article_html.text)
            except:
                # Если будет второй вид странички выполняется второй метод
                articles[i]['text'] = add_Text_For_Two_Page(article_html.text)
        print(articles)
    else:
        print("WTF man?")


parse()