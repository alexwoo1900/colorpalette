import configparser


class ColorConfiguration(object):
    def __init__(self):
        self.conf = configparser.ConfigParser()

        self.colorboard_cache_on = True
        self.colorboard_rtcp_on = False

        self.colorstrip_width = 4
        self.colorstrip_height = 10

        self.load_config()

    def load_config(self):
        self.conf.read('config.ini')

        if int(self.conf['colorboard']['use_colorboard_cache']):
            self.colorboard_cache_on = True
        elif int(self.conf['colorboard']['use_colorboard_rtcp']):
            self.colorboard_rtcp_on = True
        else:
            self.colorboard_cache_on = False
            self.colorboard_rtcp_on = False

        self.colorstrip_width = int(self.conf['colorstrip']['width'])
        self.colorstrip_height = int(self.conf['colorstrip']['height'])

