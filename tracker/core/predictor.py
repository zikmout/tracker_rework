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
        http_client.close()
        return response.body
    except Exception as e:
        error_str = 'Error making SBB prediction ({})'.format(e)
        # print('Error -> {}'.format(error_str))
        http_client.close()
        return json.dumps({ 'error': '{}'.format(error_str)})