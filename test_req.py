import os
import time
import random
import celery
import urllib

import json

from tornado import httpclient


def make_request_for_predictions(content, min_acc=0.75):
    # Making synchronous HTTP Request (because workers are aynchronous already)
    post_data = { 'content': content, 'min_acc': min_acc }
    body = urllib.parse.urlencode(post_data)

    http_client = httpclient.HTTPClient()
    try:
        response = http_client.fetch('http://localhost:5567/api/v1/predict/is_sbb', method='POST', body=body)
        print('RESPONSE => {}'.format(response.body))
        return response.body
    except httpclient.HTTPError as e:
        print('HTTPError -> {}'.format(e))
    except Exception as e:
        print('Error -> {}'.format(e))
    http_client.close()
    return None

print(json.loads(make_request_for_predictions('Simon is not there', min_acc=0.75)))

'''async def make_request_for_predictions(content, min_acc=0.75):
    # Making synchronous HTTP Request (because workers are aynchronous already)
    print('func')
    post_data = { 'content': content, 'min_acc': min_acc }
    body = urllib.parse.urlencode(post_data)

    http_client = httpclient.AsyncHTTPClient()
    try:
        response = yield http_client.fetch('http://localhost:5567/api/v1/predict/is_sbb', method='POST', body=body)
        print('RESPONSE => {}'.format(response.body))
        http_client.close()
        raise gen.Return(response)
    except Exception as e:
        print('Error -> {}'.format(e))
        http_client.close()
        raise gen.Return([])


def test():
    print('OK')
    
    print('LL')
    resp = make_request_for_predictions('Simon is not there', min_acc=0.75)
    print('AFTER')
    print(resp)


test()
    #return json.loads(response.body)
        #return False#json.dumps({'response':'NOT'})
    #return True
'''