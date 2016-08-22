from __future__ import print_function
import httplib2
import os
import urllib.request as urllib2
from io import BytesIO

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient.http import MediaUpload
from apiclient.http import MediaIoBaseUpload
from oauth2client import util 
DEFAULT_CHUNK_SIZE = 512 * 1024 
MAX_URI_LENGTH = 2048 
TOO_MANY_REQUESTS = 429 


class MediaUrlUpload(MediaUpload): 
    
     @util.positional(3) 
     def __init__(self, url, mimetype, chunksize=DEFAULT_CHUNK_SIZE, resumable=False): 
       super(MediaUrlUpload, self).__init__() 
       self._response = urllib2.urlopen(url)
       self._mimetype = mimetype 
       if not (chunksize == -1 or chunksize > 0): 
         raise InvalidChunkSizeError() 
       self._chunksize = chunksize 
       self._resumable = resumable 
       self._size = self._response.length
     def chunksize(self): 
       return self._chunksize 
    
     def mimetype(self): 
       return self._mimetype 
    
     def size(self): 
       return self._size
    
     def resumable(self): 
       return self._resumable 
    
     def getbytes(self, begin, length): 
       data = self._response.read(length)
       return data
    
     def has_stream(self): 
       return False 
    
     def stream(self): 
       return None
    
     def to_json(self): 
       """This upload type is not serializable.""" 
       raise NotImplementedError('MediaIoBaseUpload is not serializable.') 



try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    flags.noauth_local_webserver = True
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'upload'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'drive-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    Url = "http://vignette3.wikia.nocookie.net/walkingdead/images/a/a6/SFH_Pre_Release_5.png/revision/latest?cb=20140209223959"
    media_body = MediaUrlUpload(Url, mimetype='image/png', chunksize=512 * 1024  , resumable=True)
    body = {
        'title': 'pic.png'
    }
    r = service.files().create(body=body, media_body=media_body).execute()
main()
