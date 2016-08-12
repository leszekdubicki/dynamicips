#client to connect to dynamicip-s web api
import requests
import json
import ConfigParser


class DynIPsClient:
    def __init__(self):
        self._url = None
        self._headers = {'content-type': 'application/json'}
        self._configFile = "./dynip_client_config.ini"
    def setConfigFile(self, configFile = None):
        #check if config file was altered and alter it if necessry
        if not configFile == None:
            self._configFile = configFile
    def readConfig(self):
        #create configuration object
        config = ConfigParser.ConfigParser()
        config.read(self._configFile)
        if config.has_option("app","url"):
            self._url = config.get('app','url')
        if config.has_option("app","url"):
            self._url = config.get('app','url')
        if config.has_option("host","address"):
            self._address = config.get('host','address')
        if config.has_option("host","name"):
            self._name = config.get('host','name')
        if config.has_option("host","ssh_port"):
            self._ssh_port = config.get('host','ssh_port')

    def set_url(self, url):
        self._url = url
    def setUrl(self, url):
        #copy of set_url method
        self.set_url(url)
    def getUrl(self):
        return self._url
    def addHost(self):
        #adds host 
        uri = '/hosts/add'
        r = requests.post(self._url + uri, headers = self._headers ,data=json.dumps({'host':{"address":self._address}}))
        print r.json()
        #check for url (turned off for now)
        """
        if self.checkUrl() == True:
        else:
            #return custom status code
            return {'status_code':1404, 'projects': []}
        """
        if r.status_code == 200:
            return r.json()
        else:
            return {'status_code':r.status_code, 'projects': []}
            #I'd rather not store all the projects not to consume too much memory (see below)
    def get_hosts(self):
        #gets list of projects
        uri = '/hosts'
        #check for url (turned off for now)
        """
        r = requests.get(self._url + uri, headers = self._headers)
        if self.checkUrl() == True:
        else:
            #return custom status code
            return {'status_code':1404, 'projects': []}
        """
        if r.status_code == 200:
            return r.json()
        else:
            return {'status_code':r.status_code, 'projects': []}
            #I'd rather not store all the projects not to consume too much memory (see below)
