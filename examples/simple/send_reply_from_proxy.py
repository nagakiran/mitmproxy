"""
This example shows how to send a reply from the proxy immediately
without sending any data to the remote server.
"""
from mitmproxy import http
import re

# with open('/opt/aruba/central/apps/monitoring_ui/src/client_connectivity/controller.js', 'r') as myfile:
#   data = myfile.read().encode('UTF-8')
redirectMap = {
    'https://.*.cloudfront.net/.*/monitoring/client_connectivity/controller.js' : '/opt/aruba/central/apps/monitoring_ui/src/client_connectivity/controller.js',
    'https://.*.cloudfront.net/.*/monitoring/client_connectivity/template.html' : '/opt/aruba/central/apps/monitoring_ui/src/client_connectivity/template.html'
}

def request(flow: http.HTTPFlow) -> None:
    # pretty_url takes the "Host" header of the request into account, which
    # is useful in transparent mode where we usually only have the IP otherwise.

    for route in redirectMap:
        if re.match(route,flow.request.pretty_url):
            with open(redirectMap[route], 'r') as myfile:
                data = myfile.read().encode('UTF-8')
    # if flow.request.pretty_url == "http://example.com/path":
            flow.response = http.HTTPResponse.make(
                200,  # (optional) status code
                b"Hello World",  # (optional) content
                # data,
                # {"Content-Type": "text/html"}  # (optional) headers
                {}  # (optional) headers
            )
            flow.response.content = data
