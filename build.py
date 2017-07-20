#!/usr/env python3
import glob
import io
import re
import os

base_igem = 'http://2017.igem.org/'
base_team = base_igem + 'Team:Bristol/'
base_template = base_igem + 'Template:Bristol/'
base_raw = '?action=raw&ctype=text/'

extensions = ['.png', '.svg', '.gif', '.jpeg', '.jpg', '.bmp']


def get_pages():
    pages = []
    for file in glob.glob('html/**/*.*', recursive=True):
        pages.append(file[5:])
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
            pass
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
