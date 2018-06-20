#!/usr/env python3
import glob
import io
import re
import os
from settings import team

base_igem = 'http://2018.igem.org/'
base_team = base_igem + 'Team:Aachen/'
base_template = base_igem + 'Template:Aachen/'
base_raw = '?action=raw&ctype=text/'

extensions = ['.png', '.svg', '.gif', '.jpeg', '.jpg', '.bmp', '.ini']


def get_pages():
    pages = []
    for file_name in glob.glob('html/**/*.*', recursive=True):
        if os.name == 'nt':
            file_name = file_name.replace('\\', '/')
        pages.append(file_name[5:])
    return pages


def build():
    links = create_links()
    for page in get_pages():
        print(page)
        if any(x in page.lower() for x in extensions):
            continue
        with io.open('html/' + page, 'r', encoding='utf-8') as f:
            text = f.read()
        for x in re.findall(r'\{\{([^}]+)\}\}', text):
            text = text.replace('{{' + x + '}}', links[x])
        write(page, text)


def create_links():
    links = {}
    for page in get_pages():
        if 'css/' in page:
            tmp = base_template + 'css/' + page[4:-4] + base_raw + 'css'
            links[page[:-4]] = '<link rel="stylesheet" type="text/css" href="' + tmp + '" />'
        elif 'js/' in page:
            tmp = base_template + 'js/' + page[3:-3] + base_raw + 'javascript'
            links[page[:-3]] = '<script type="text/javascript" src="' + tmp + '"></script>'
        elif 'templates/' in page:
            links[page[:-5]] = '{{' + team + page[9:-5] + '}}'
        else:
            if 'index' in page:
                tmp = base_team + page[0:-10]
                links[page[:-5]] = tmp[:-1]
            else:
                links[page[:-5]] = base_team + page[0:-5]

    return links


def write(filename, output):
    filename = 'dist/' + filename
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with io.open(filename, 'w', encoding='utf-8') as f:
        f.write(output)


if __name__ == '__main__':
    build()
