from datetime import datetime
from rest_framework import serializers


class Article:

    def __init__(self, title, link, date, img, a_type):

        self.title = title
        self.ar_link = link
        self.date = self.encode_en_date(date)
        self.img = img
        self.type = a_type

    def encode_en_date(self, datelist):
        dateStr = "{0}-{1}-{2}".format(datelist[3], datelist[2], datelist[1])
        date_time_obj = datetime.strptime(dateStr, '%Y-%B-%d')
        return date_time_obj


class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField()
    ar_link = serializers.CharField()
    date = serializers.DateTimeField()
    img = serializers.CharField()
    type = serializers.CharField()
