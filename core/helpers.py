from core.modules import *
from core import models


class DBHelpers(object):
    @staticmethod
    def is_in_read_content(user_id, article_url):
        hit_count = models.ReadContent.objects(userId__exact=user_id, articleUrl__exact=article_url)
        if len(hit_count) > 0:
            return True
        else:
            return False

    @staticmethod
    def mongo_connector(db_name):
        mongo_uri = 'mongodb://{user}:{password}@{host}:{port},{host}:{port}/{db_name}?authSource={user}'. \
            format(user=config.DB_USER_NAME, password=config.DB_PASSWORD, host=config.DB_HOST, port=config.DB_PORT,
                   db_name=db_name)
        return mongo_uri


class Calculators(object):
    @staticmethod
    def predict_read_time(content):
        read_time = str(datetime.timedelta(seconds=len(content.split())) / 3.5)
        return read_time

    @staticmethod
    def detect_likely_score(score):
        if score >= 0.75:
            return 2
        if score >= 0.5:
            return 1
        if score <= 0.5:
            return 0

    @staticmethod
    def likely_alias_to_text(alias):
        likely_alias_dict = {
            0: 'Unlikely',
            1: 'Likely',
            2: 'Very Likely',
            3: 'Unknown'

        }
        alias_match = likely_alias_dict.get(alias, 3)
        return alias_match


class PartnerHelpers(object):
    @staticmethod
    def partner_url_stripper(__url):
        return urlparse(__url).hostname

    @staticmethod
    def check_partner_in_db(__url):
        partner_host_name = PartnerHelpers.partner_url_stripper(__url)
        partner_url_check = models.PartnerList.objects(partnerHostName__contains=partner_host_name)
        if len(partner_url_check) > 0:
            return True
        else:
            return False


class Preprocessors(object):
    @staticmethod
    def text_divider(source_text):
        sentences_array = str(source_text).split('.')
        return sentences_array

    @staticmethod
    def specify_punctuation(target_string):
        formatted_string = re.sub("([.,!?()'])", r' \1 ', target_string)
        formatted_string = re.sub('\s{2,}', ' ', formatted_string)
        return formatted_string


class ArticleHelpers(object):
    @staticmethod
    def check_article_exists(__url):
        article_url = models.Article.objects(articleUrl__exact=__url)
        if len(article_url) > 0:
            return True
        else:
            return False
