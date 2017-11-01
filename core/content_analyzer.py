from core.modules import *


class DataProcessor(object):
    @staticmethod
    def nlu_data_processor(content_to_process):
        nlp_processor = NaturalLanguageUnderstandingV1(
            version="2017-02-27",
            username=config.NLU_USER,
            password=config.NLU_PASS
        )
        processed_data = nlp_processor.analyze(
            text=content_to_process,
            features=[features.Entities(), features.Keywords(), features.Categories(), features.Emotion(),
                      features.Sentiment()]
        )
        return processed_data

    @staticmethod
    def data_tone_processor(content_to_process):
        tone_processor = ToneAnalyzerV3(
            version="2016-02-11",
            username=config.TONE_USER,
            password=config.TONE_PASS
        )
        processed_data = tone_processor.tone(content_to_process)
        return processed_data


class DataTranslator(object):
    @staticmethod
    def translate_text(text_to_translate, source_lang_code):
        google_translate_url = "https://translation.googleapis.com/language/translate/v2?key={}". \
            format(config.GOOGLE_TRANSLATE)
        request_data = {
            "q": text_to_translate,
            "source": source_lang_code,
            "target": "en",
            "format": "text"
        }
        response_data = requests.post(google_translate_url, data=request_data)
        test = json.loads(response_data.text)
        return test['data']['translations'][0]['translatedText']

    @staticmethod
    def detect_content_language(source_text):
        sentence_array = helpers.Preprocessors.text_divider(source_text)
        detected_lang = guess_language(sentence_array[0])
        if detected_lang is None or detected_lang <= 0:
            detected_lang = "NaN"
        return detected_lang

    @staticmethod
    def check_content_language_is_english(source_text):
        sentence_array = helpers.Preprocessors.text_divider(source_text)
        punctuation_fixed_article = helpers.Preprocessors.specify_punctuation(source_text)
        detected_lang = guess_language(sentence_array[0])
        if detected_lang != 'en':
            result = DataTranslator.translate_text(punctuation_fixed_article, detected_lang)
            return result
        else:
            return source_text


class DataHandler(object):
    @staticmethod
    def process_data(data_to_process):
        translated_content = DataTranslator.check_content_language_is_english(data_to_process)
        tone_analysis = DataProcessor.data_tone_processor(translated_content)
        nlu_analysis = DataProcessor.nlu_data_processor(translated_content)
        response = dict()
        response['tone_data'] = dict()
        response['tone_data']['document_tone'] = tone_analysis['document_tone']
        for key in nlu_analysis:
            if 'nlu_data' not in response:
                response['nlu_data'] = dict()
            response['nlu_data'][key] = nlu_analysis[key]
        return response


class ArticleDataExtractor(object):
    @staticmethod
    def extract_tone_data(tone_object):
        extracted_dict = dict()
        tone_categories = tone_object['document_tone']['tone_categories']
        for tone_category in tone_categories:
            for tone in tone_category['tones']:
                extracted_dict[tone['tone_id']] = tone['score']
        return extracted_dict


class UserDataCalculator(object):
    @staticmethod
    def user_recommendations(user_id):
        article_list = list()
        recommendation_list = list()
        user_average = dict()
        result_object = dict()
        selected_emotions = OrderedDict()
        processed_tone_count = 0
        recommendation_count = 0
        tone_list = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'analytical', 'confident', 'tentative',
                     'openness_big5', 'conscientiousness_big5', 'extraversion_big5', 'agreeableness_big5',
                     'neuroticism_big5']
        for read_article in models.ReadContent.objects(userId__exact=user_id):
            article_list.append(read_article.articleUrl)
        lang_list = models.Article.objects(articleUrl__in=article_list).distinct('articleLanguage')
        for tone in tone_list:
            current_tone_average = models.Article.objects(articleUrl__in=article_list).average(tone)
            likelihood_value = helpers.Calculators.detect_likely_score(current_tone_average)
            if likelihood_value > 0:
                user_average[current_tone_average] = tone
                selected_emotions = OrderedDict(sorted(user_average.items(), reverse=True))
        for user_score, user_tone in selected_emotions.items():
            processed_tone_count += 1
            if processed_tone_count < 4:
                for article in models.Article.objects(articleUrl__not__in=article_list):
                    article_score = helpers.Calculators.detect_likely_score(article[user_tone])
                    if helpers.Calculators.detect_likely_score(user_score) == article_score and article_score > 0:
                        if article['articleUrl'] not in recommendation_list and article['articleLanguage'] in lang_list:
                            recommendation_list.append(article['articleUrl'])
        for recommendation in recommendation_list:
            article_details = models.Article.objects(articleUrl__exact=recommendation)\
                .only('articleUrl', 'articleImage', 'articleTitle').first()
            result_object[str(recommendation_count)] = {
                'articleUrl' : article_details.articleUrl,
                'articleImage' : article_details.articleImage,
                'articleTitle' : article_details.articleTitle
            }
            recommendation_count += 1
        result_object['recommendation_count'] = recommendation_count
        return result_object

