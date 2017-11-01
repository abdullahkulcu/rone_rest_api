from core.geoip_finder import *

app = Flask(__name__)
app.ENV = config.ENV
port = getattr(config, str(app.ENV) + "_PORT")
debug = getattr(config, str(app.ENV) + "_DEBUG")
host = getattr(config, str(app.ENV) + "_HOST")
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/hit', methods=['POST'])
def send_hit_data():
    try:
        user_ip = str(request.headers.get("X-Forwarded-For", request.remote_addr))
        geoip_info = GeoIPFinder.find_details(user_ip)
        hit_data = models.HitData(userId=request.json['userId'])
        hit_data.userIp = user_ip
        hit_data.currentUrl = request.json['currentUrl']
        hit_data.referralUrl = request.json['referralUrl']
        hit_data.userAgent = request.json['userAgent']
        hit_data.resolution = request.json['resolution']
        hit_data.contentCategory = request.json['contentCategory']
        hit_data.countryCode = geoip_info['country_code']
        hit_data.countryName = geoip_info['country_name']
        hit_data.regionCode = geoip_info['region_code']
        hit_data.regionName = geoip_info['region_name']
        hit_data.city = geoip_info['city']
        hit_data.zipCode = geoip_info['zip_code']
        hit_data.timeZone = geoip_info['time_zone']
        hit_data.longitude = str(geoip_info['longitude'])
        hit_data.latitude = str(geoip_info['latitude'])
        hit_data.metroCode = str(geoip_info['metro_code'])
        hit_data.save(validate=True)

        read_content = models.ReadContent(userId=request.json['userId'])
        read_content.articleUrl = request.json['articleUrl']
        read_content.save(validate=True)
        return jsonify(result="OK")
    except:
        raise Exception("Error while processing the request.")


@app.route('/add/article', methods=['POST'])
def add_article():
    try:
        article_url = request.json['articleUrl']
        check_url_exists = helpers.ArticleHelpers.check_article_exists(article_url)
        if check_url_exists is False:
            article = models.Article(articleUrl=article_url)
            processed_data = text_processor.DataHandler.process_data(request.json['articleContent'])
            tone_dictionary = text_processor.ArticleDataExtractor.extract_tone_data(processed_data['tone_data'])
            article.articleContent = request.json['articleContent']
            article.articleTitle = request.json['articleTitle']
            article.articleAuthor = request.json['articleAuthor']
            article.articleImage = request.json['articleImage']
            article.articleDate = datetime.datetime.now()
            article.articleLanguage = text_processor.DataTranslator.detect_content_language(
                request.json['articleContent'])
            for tone_type, score in tone_dictionary.items():
                article[tone_type] = score
            article.nlu = processed_data['nlu_data']
            article.save(validate=True)
            return jsonify(result="Article added. 201")
        else:
            return jsonify(result="Article added. 203")
    except:
        raise


@app.route('/user/recommendations', methods=['POST'])
def find_tone():
    recommended_articles = text_processor.UserDataCalculator.user_recommendations(request.json['userId'])
    return jsonify(result=recommended_articles)



@app.route('/auth/partner', methods=['POST'])
def check_partner():
    try:
        partner_url = request.json['partnerUrl']
        result_ = helpers.PartnerHelpers.check_partner_in_db(__url=partner_url)
        if result_:
            return 200
        else:
            abort(404, "Partner not found in DB")
    except:
        raise Exception("Something went wrong during validate partner.")


@app.route('/get/article', methods=['GET'])
def get_all_articles():
    output = list()
    try:
        for article in models.Article.objects:
            output.append(
                {
                    'articleUrl': article.articleUrl,
                    'articleTitle': article.articleTitle,
                    'articleContent': article.articleContent,
                    'articleAuthor': article.articleAuthor,
                    'anger': article.anger,
                    'disgust': article.disgust,
                    'fear': article.fear,
                    'joy': article.joy,
                    'sadness': article.sadness,
                    'analytical': article.analytical,
                    'confident': article.confident,
                    'tentanive': article.tentative,
                    'opennes_big5': article.openness_big5,
                    'conscientiousness_big5': article.conscientiousness_big5,
                    'extraversion_big5': article.extraversion_big5,
                    'agreeableness_big5': article.agreeableness_big5,
                    'neuroticism_big5': article.neuroticism_big5,
                    'nlu': article.nlu,
                    'articleDate': article.articleDate
                }
            )
    except:
        raise Exception("Something went wrong during get articles.")
    return jsonify(result=output)


if __name__ == '__main__':
    app.run(host=config.DEV_HOST, port=config.DEV_PORT, debug=config.DEV_DEBUG)
