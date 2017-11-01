from core.modules import *

url = getattr(config, str(config.ENV) + "_GEOIP_URL")
port = getattr(config, str(config.ENV) + "_GEOIP_PORT")
full_url = url + ":" + port


class GeoIPFinder(object):
    @staticmethod
    def find_details(_target):
        geoip_url = full_url + "/json/{_target}".format(_target=_target)
        response = requests.get(geoip_url)
        _data = json.loads(response.text)
        if _data is None:
            _data = "127.0.0.1"
        for key, value in _data.items():
            if value == u'' or value is None or value == '':
                _data[key] = 'n/a'
        return _data
