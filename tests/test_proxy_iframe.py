from http.server import BaseHTTPRequestHandler, HTTPServer
import argparse
import os
import random
import sys
import requests


hostname = 'en.wikipedia.org'
# hostname = 'www.lequipe.fr'


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def set_header():
    headers = {
        'Host': hostname
    }

    return headers

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def do_HEAD(self):
        self.do_GET(body=False)

    def do_GET(self, body=True):
        sent = False
        try:

            url = 'https://{}{}'.format(hostname, self.path)
            req_header = self.parse_headers()

            # print(req_header)
            # print(url)
            resp = requests.get(url, headers=merge_two_dicts(req_header, set_header()), verify=False)
            sent = True

            self.send_response(resp.status_code)
            self.send_resp_headers(resp)
            if body:
                # self.wfile.write('BG COLOR'.encode('utf-8'))
                # self.wfile.write(resp.content)
                # if '<body>' in resp.content.decode('utf-8', errors='ignore'):
                #     # print('resp.content = {}'.format(resp.content.decode('utf-8', errors='ignore')))
                    
                #     # html_injected = "<body onload=\"alert(\'toto\');\">"
                #     # html_injected = "<body onload=\"document.body.style.backgroundColor = 'red';\">"
                #     html_injected = """
                #     <body onload=\"var outlineStyle='';
                #     var EltBgColor='';
                #     var isSelected=false;
                #     function getElementIdx(elt)
                #     {
                #         var count = 1;
                #         for (var sib = elt.previousSibling; sib ; sib = sib.previousSibling)
                #         {
                #             if(sib.nodeType == 1 && sib.tagName == elt.tagName) count++
                #         }
                        
                #         return count;
                #     };
                #     function getElementXPath(elt)
                #     {
                #          var path = '';
                #          for (; elt && elt.nodeType == 1; elt = elt.parentNode)
                #          {
                #         idx = getElementIdx(elt);
                #         xname = elt.tagName;
                #         if (idx > 1) xname += '[' + idx + ']';
                #         path = '/' + xname + path;
                #          }
                     
                #          return path;   
                #     };
                #     document.addEventListener('mouseover', function (event) {outlineStyle=event.target.style.outline; event.target.style.outline = '#f00 solid 2px';EltBgColor=event.target.style.backgroundColor;event.target.style.backgroundColor='rgba(12, 242, 143, 0.2)';}, false);
                #     document.addEventListener('mouseout', function (event)
                #     {
                #         event.target.style.outline = outlineStyle;
                #         if(!isSelected)
                #         {
                #             event.target.style.backgroundColor = EltBgColor;
                #         }
                #     }, false);
                #     document.addEventListener('click', function (event) {isSelected=true;console.log(getElementXPath(event.target));event.target.style.backgroundColor='rgba(12, 235, 160, 0.9)';}, false);\">
                #     """
                #     # html_injected = """
                #     # <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
                #     # <script>
                #     # $('body *').bind('mouseover mouseout', function(event) {
                #     #     if (event.type == 'mouseover') {
                #     #         $(this).data('bgcolor', $(this).css('background-color'));
                #     #         $(this).css('background-color','rgba(255,0,0,.5)');
                #     #     } else {
                #     #         $(this).css('background-color', $(this).data('bgcolor'));
                #     #     }
                #     #     return false;
                #     # });
                #     # </script>
                #     # """

                #     gogo = resp.content.decode('utf-8', errors='ignore').replace('<body>', html_injected)#.encode('utf-8')
                #     if isinstance('gogo', str):
                #         gogo = gogo.encode('utf-8')
                #     print('resp.content II = {}'.format(gogo[:500]))
                #     self.wfile.write(gogo)
                if '<body ' in resp.content.decode('utf-8', errors='ignore'):
                    # print('resp.content = {}'.format(resp.content.decode('utf-8', errors='ignore')))
                    
                    # html_injected = "<body onload=\"alert(\'toto\');\" "
                    # html_injected = "<body onload=\"document.body.style.backgroundColor = 'red';\" "
                    html_injected = """
                    <body onload=\"
                    var sXPath = {

                    };
                    var bgColor = '';
                    var osOld = '';
                    function disableLinksOnPage(className)
                    {
                        var linkItems = document.querySelectorAll(className);
                        linkItems.forEach(function(linkItem) {
                          linkItem.setAttribute('href', 'javascript:void(0)');
                          linkItem.setAttribute('disabled', 'disabled');
                        });
                    }
                    disableLinksOnPage('a');
                    disableLinksOnPage('A');
                    function getElementIdx(elt)
                    {
                        var count = 1;
                        for (var sib = elt.previousSibling; sib ; sib = sib.previousSibling)
                        {
                            if(sib.nodeType == 1 && sib.tagName == elt.tagName) count++
                        }
                        
                        return count;
                    };
                    function getElementXPath(elt)
                    {
                         var path = '';
                         for (; elt && elt.nodeType == 1; elt = elt.parentNode)
                         {
                        idx = getElementIdx(elt);
                        xname = elt.tagName;
                        if (idx > 1) xname += '[' + idx + ']';
                        path = '/' + xname + path;
                         }
                     
                         return path;   
                    };
                    document.addEventListener('mouseover', function (event)
                    {

                        


                        if (sXPath[getElementXPath(event.target)] == undefined)
                        {
                            bgColor = event.target.style.backgroundColor;
                            osOld = event.target.style.outline;
                            event.target.style.backgroundColor = 'rgba(12, 242, 143, 0.2)';
                            event.target.style.outline = '#f00 solid 2px';
                        }
                        else if (sXPath[getElementXPath(event.target)] == false)
                        {
                            bgColor = event.target.style.backgroundColor;
                            osOld = event.target.style.outline;
                            event.target.style.backgroundColor = 'rgba(12, 242, 143, 0.2)';
                            event.target.style.outline = '#f00 solid 2px';
                        }
                        else if (sXPath[getElementXPath(event.target)] == true)
                        {

                        }

                    }, false);
                    document.addEventListener('mouseout', function (event)
                    {
                        if (sXPath[getElementXPath(event.target)] != undefined && sXPath[getElementXPath(event.target)] == true)
                        {
                            
                        }
                        else
                        {
                            event.target.style.outline = osOld;
                            event.target.style.backgroundColor = bgColor;
                        }

                    }, false);
                    document.addEventListener('click', function (event) 
                    {

                        if (sXPath[getElementXPath(event.target)] == undefined)
                        {

                            sXPath[getElementXPath(event.target)] = true;
                            sXPath[getElementXPath(event.target) + 'bgOld'] = bgColor;
                            sXPath[getElementXPath(event.target) + 'osOld'] = osOld;
                            event.target.style.backgroundColor = 'rgba(12, 235, 160, 0.9)';

                        }
                        else if (sXPath[getElementXPath(event.target)] == true)
                        {
                            sXPath[getElementXPath(event.target)] = false;
                            event.target.style.backgroundColor = sXPath[getElementXPath(event.target) + 'bgOld'];
                            event.target.style.outline = sXPath[getElementXPath(event.target) + 'osOld'];
                        }
                        else if (sXPath[getElementXPath(event.target)] == false)
                        {
                            sXPath[getElementXPath(event.target)] = true;
                            sXPath[getElementXPath(event.target) + 'bgOld'] = bgColor;
                            sXPath[getElementXPath(event.target) + 'osOld'] = osOld;
                            event.target.style.backgroundColor = 'rgba(12, 235, 160, 0.9)';
                        }
                    }, false);\"  
                    """
                    # html_injected = """
                    # <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
                    # <script>
                    # $('body *').bind('mouseover mouseout', function(event) {
                    #     if (event.type == 'mouseover') {
                    #         $(this).data('bgcolor', $(this).css('background-color'));
                    #         $(this).css('background-color','rgba(255,0,0,.5)');
                    #     } else {
                    #         $(this).css('background-color', $(this).data('bgcolor'));
                    #     }
                    #     return false;
                    # });
                    # </script>
                    # """

                    gogo = resp.content.decode('utf-8', errors='ignore').replace('<body ', html_injected)#.encode('utf-8')
                    if isinstance('gogo', str):
                        gogo = gogo.encode('utf-8')
                    print('resp.content II = {}'.format(gogo[:500]))
                    self.wfile.write(gogo)
                else:
                    self.wfile.write(resp.content)
                # self.wfile.write("<html><body bgcolor='red'></body></html>".encode('utf-8'))
            resp.close()
            return
        finally:
            self.finish()
            if not sent:
                self.send_error(404, 'error trying to proxy')

    def do_POST(self, body=True):
        sent = False
        try:
            url = 'https://{}{}'.format(hostname, self.path)
            content_len = int(self.headers.getheader('content-length', 0))
            post_body = self.rfile.read(content_len)
            req_header = self.parse_headers()

            resp = requests.post(url, data=post_body, headers=merge_two_dicts(req_header, set_header()), verify=False)
            sent = True

            self.send_response(resp.status_code)
            self.send_resp_headers(resp)
            if body:
                self.wfile.write(resp.content)
            return
        finally:
            self.finish()
            if not sent:
                self.send_error(404, 'error trying to proxy')

    def parse_headers(self):
        req_header = {}
        for line in self.headers:
            line_parts = [o.strip() for o in line.split(':', 1)]
            if len(line_parts) == 2:
                req_header[line_parts[0]] = line_parts[1]
        return req_header

    def send_resp_headers(self, resp):
        respheaders = resp.headers
        print('Response Header')
        for key in respheaders:
            if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding', 'content-length', 'Content-Length']:
                # print('{}, {}'.format(key, respheaders[key]))
                self.send_header(key, respheaders[key])
        self.send_header('Content-Length', len(resp.content))
        self.end_headers()



def parse_args(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Proxy HTTP requests')
    parser.add_argument('--port', dest='port', type=int, default=9999,
                        help='serve HTTP requests on specified port (default: random)')
    args = parser.parse_args(argv)
    return args

def main(argv=sys.argv[1:]):
    args = parse_args(argv)
    print('http server is starting on port {}...'.format(args.port))
    server_address = ('127.0.0.1', args.port)
    httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
    print('http server is running as reverse proxy')
    httpd.serve_forever()

if __name__ == '__main__':
    main()