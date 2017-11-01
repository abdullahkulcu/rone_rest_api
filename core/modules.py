import json
import requests
import datetime
import random
import re
from urllib.parse import urlparse

from flask import Flask
from flask import abort
from flask import jsonify
from flask import request
from guess_language import guess_language
from collections import OrderedDict
from operator import itemgetter
from flask_cors import CORS, cross_origin
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features

import core.config as config
import core.models as models
import core.helpers as helpers
import core.content_analyzer as text_processor