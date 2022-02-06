
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializers
import os


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from datetime import date, datetime

# Create your views here.


@api_view(['GET'])
def get_routes(request):
    routes = [
        {
            'Endpoint': '/articles/',
            'method': 'GET',
            'body': None,
            'description': "return array of all news articles"
        },
        {
            'Endpoint': '/articles/category',
            'method': 'GET',
            'body': None,
            'description': "return array of specific type articles"
        }
    ]
    return Response(routes)


@api_view(['GET'])
def get_articles(request):
    articles = return_all_articles()
    serializer = serializers.ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_articles_by_cat(request, cat):
    articles = return_specific_articles(cat)
    serializer = serializers.ArticleSerializer(articles, many=True)
    return Response(serializer.data)


def return_all_articles():
    

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    topicsList = ['politics', 'society', 'culture', 'sports', 'international']

    articles_list = []
    for topic in topicsList:

        topiclink = 'https://en.hespress.com/' + topic
        driver.get(topiclink)
        driver.execute_script("window.scrollTo(0,180000);")

        # articles = driver.find_elements_by_class_name("stretched-link")
        articles = driver.find_elements_by_class_name("cover")

        for article in articles:
            p = get_article_object(topic, article)

            articles_list.append(p)

    return articles_list


def get_article_object(topic, article):
    ar = article.find_element_by_class_name("stretched-link")
    ard = article.find_element_by_class_name("text-muted")
    ardImg = article.find_element_by_class_name("wp-post-image")

    p = serializers.Article(
        title=ar.get_attribute('title'),
        link=ar.get_attribute('href'),
        date=ard.get_attribute("innerHTML").split(' '),
        img=ardImg.get_attribute("src"),
        a_type=topic
    )

    return p


def return_specific_articles(topic):
    articles_list = []
    driver = webdriver.Chrome(".\chromedriver")
    topiclink = 'https://en.hespress.com/' + topic
    driver.get(topiclink)
    driver.execute_script("window.scrollTo(0,180000);")
    articles = driver.find_elements_by_class_name("cover")
    for article in articles:
        p = get_article_object(topic, article)
        articles_list.append(p)

    return articles_list


def encode_en_date(datelist):
    dateStr = "{0}-{1}-{2}".format(datelist[3], datelist[2], datelist[1])
    date_time_obj = datetime.strptime(dateStr, '%Y-%B-%d')
    return date_time_obj
