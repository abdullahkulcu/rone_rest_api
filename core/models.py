from mongoengine import *
from datetime import *
from core import config, helpers
import os

rone_connector = helpers.DBHelpers.mongo_connector('storiame')
ssl_config = {
    'ssl': config.DB_SSL,
    'ssl_ca_certs': os.path.join(os.path.dirname(os.path.abspath(__file__)) + '/' + config.DB_CERT_FILE)
}
connect(host=rone_connector, **ssl_config)


class Article(Document):
    articleUrl = StringField(required=True, unique=True)
    articleTitle = StringField(required=True)
    articleContent = StringField(required=True)
    articleAuthor = StringField(required=False)
    articleImage = StringField(required=True)
    anger = FloatField(required=True)
    disgust = FloatField(required=True)
    fear = FloatField(required=True)
    joy = FloatField(required=True)
    sadness = FloatField(required=True)
    analytical = FloatField(required=True)
    confident = FloatField(required=True)
    tentative = FloatField(required=True)
    openness_big5 = FloatField(required=True)
    conscientiousness_big5 = FloatField(required=True)
    extraversion_big5 = FloatField(required=True)
    agreeableness_big5 = FloatField(required=True)
    neuroticism_big5 = FloatField(required=True)
    nlu = DynamicField(required=True)
    articleDate = DateTimeField(required=True)
    articleLanguage = StringField(required=True)


class HitData(Document):
    userId = StringField(required=True)
    userIp = StringField(required=True)
    currentUrl = StringField(required=True)
    referralUrl = StringField(required=True)
    clickDate = DateTimeField(datetime.now())
    userAgent = StringField(required=True)
    resolution = StringField(required=True)
    contentCategory = StringField(required=True)
    countryCode = StringField(required=True, default="None")
    countryName = StringField(required=True, default="None")
    regionCode = StringField(required=False, default="None")
    regionName = StringField(required=False, default="None")
    city = StringField(required=True, default="None")
    zipCode = StringField(required=False, default="None")
    timeZone = StringField(required=True, default="None")
    latitude = StringField(required=True, default="None")
    longitude = StringField(required=True, default="None")
    metroCode = StringField(required=True, default="None")


class ReadContent(Document):
    userId = StringField(required=True)
    articleUrl = StringField(required=True)
    convertStatus = IntField(required=True, default=0)


class PartnerList(Document):
    partnerId = StringField(required=True, unique=True)
    partnerName = StringField(required=True, unique=True)
    partnerHostName = StringField(required=True, unique=True)
    jsFileName = StringField(required=False, unique=True)
    partnerType = IntField(required=True)
    partnerPackage = StringField(required=True)
    status = IntField(required=True, default=1)
