#!/usr/env python3

import http.server as server
import re
import socketserver
import time
import urllib
import urllib.parse as parse
import urllib.request as request

from template import get_page

team_pages = {}
host = "igem.org"
served_at = "igem.localhost:8000"

port = served_at.split(':')
if len(port) == 1:
    port = "80"
else:
    port = port[1]


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        pass


noredir_opener = request.build_opener(NoRedirect())


def request_igem_file(path, sub_domain):
    print(sub_domain, host)
    resp = request.urlopen("http://" + sub_domain + host + "/" + path)
    data = resp.read()
    data = data.replace(host.encode("utf-8"), served_at.encode("utf-8"))
    return data, resp


def get_wiki_template(team, sub_domain):
    if team not in team_pages:
        try:
            data = re.split(r"<p>\W*IDE\W*</p>", request_igem_file(
                "Team:" + team + "/IDE",
                sub_domain
            )[0].decode('utf-8'))
            if len(data) != 2:
                return None
            team_pages[team] = data
        except request.HTTPError:
            return None
    return team_pages[team]


class IGEMHTTPRequestHandler(server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path.startswith("/Team:"):
            sub_domain = self.headers["host"].replace(served_at, "").strip()
            team = self.path[6:].split('/')[0]
            template = get_wiki_template(team, sub_domain)
            if template is None:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(
                    "Please create an IDE template".encode('utf-8'))
                return
            self.send_response(200)
            self.end_headers()
            page = self.path[1:].split('/', 1)
            if len(page) == 1:
                page = ''
            else:
                page = '/' + page[1]
            template_head = template[0].replace('/IDE', page)
            template_foot = template[1].replace('/IDE', page)
            if page == "":
                page = "/"
            if page.endswith('/'):
                page += "index"
            self.wfile.write(template_head.encode('utf-8'))
            try:
                self.wfile.write(get_page(page).encode('utf-8'))
            except Exception as e:
                self.wfile.write(("Error:<br />" + str(e)).encode('utf-8'))
            self.wfile.write(template_foot.encode('utf-8'))
            return
        return self.proxy_upstream()
        # return super().do_GET()

    def do_POST(self):
        self.proxy_upstream()

    def proxy_upstream(self):
        head = {
            k: v.replace(served_at, host)
            for k, v in self.headers.items()
            if k not in ("Content-Length", "Content-Type")
        }
        nhost = head["Host"].replace(served_at, host).strip()
        head["Host"] = nhost
        if "Cookie" in head:
            head["Cookie"] = head["Cookie"].replace(served_at.split(":")[0], host)
        url = "http://" + nhost + self.path
        data = None
        if self.command == "POST":
            data = self.rfile.read(int(self.headers['Content-Length']))
            a = [b.encode('utf-8') for b in [served_at, host]]
            for _ in range(3):
                data = data.replace(*a)
                a = [parse.quote(b).encode('utf-8') for b in a]
            # head["Content-Length"] = str(len(data))
            head["Referer"] = head["Referer"].replace("http:", "https:")
            url = url.replace("http:", "https:")
        req = request.Request(url,
                              data=data,
                              headers=head,
                              method=self.command)
        opener = noredir_opener
        try:
            resp = opener.open(req)
        except urllib.error.HTTPError as e:
            resp = e
        self.send_response(resp.status)
        for k, v in resp.info().items():
            if k not in ["Transfer-Encoding"]:
                v = v.replace(host, served_at).replace("https", "http")
                if k == "Set-Cookie":
                    v = v.replace(":" + port, "")
                self.send_header(k, v)
        body = b''
        next_body = resp.read()
        while len(next_body) > 0:
            body += next_body
            next_body = resp.read()
        body = body.replace(
            host.encode('utf-8'),
            served_at.encode('utf-8')
        ).replace(b"https", b"http")
        self.end_headers()
        while len(body) > 0:
            count = self.wfile.write(body)
            body = body[count:]

class ThreadSocketServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    Handler = IGEMHTTPRequestHandler
    stop = False
    while not stop:
        try:
            server = ThreadSocketServer(("0.0.0.0", int(port)), Handler)
        except OSError as e:
            if e.errno != 98:
                raise
            print("Failed to listen, waiting 10 seconds")
            time.sleep(10)
        else:
            print("Now listening")
            stop = True
            server.allow_reuse_address = True
            server.serve_forever()
