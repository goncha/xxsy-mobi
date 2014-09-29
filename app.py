# -*- coding: utf-8 -*-

from urllib2 import urlopen, Request

def fetch_html(url):
    req = Request(url)
    req.add_header('user-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0')
    resp = urlopen(req, None, 10)
    if resp.code != 200:
        raise "HTTP " + resp.code
    return resp


if __name__ == '__main__':
    from lxml.html import parse as parse_html
    from lxml.html import tostring as tostring_html
    from urlparse import urlparse
    import sys

    url = sys.argv[1]
    url_obj = urlparse(url)
    base_url = url_obj.scheme + '://' + url_obj.hostname + '/' + ('/'.join(url_obj.path.split('/')[:-1]))
    target_filename = url_obj.path.split('/')[-2] + '.html'

    print 'Base URL:', base_url
    print 'TOC URL:', url

    data = {}

    toc_doc = parse_html(fetch_html(url))

    title_el = toc_doc.xpath('//div[@id="ct_title"]/h1')[0]
    data['title'] = title_el.text
    data['author'] = title_el.getchildren() and title_el.getchildren()[0].text or 'Anonymous'



    chapters = []
    data['chapters'] = chapters
    for el in toc_doc.xpath('//div[@id="catalog_list"]/ul/li/a'):
        ch_url = el.attrib.get('href')
        if ch_url.startswith('http://vip'):
            continue
        print 'Fetching', ch_url
        ch_data = {}
        ch_data['title'] = el.text
        ch_doc = parse_html(fetch_html(base_url + '/' + ch_url))
        ch_data['content'] = ''.join([tostring_html(p) for p in ch_doc.xpath('//div[@id="zjcontentdiv"]/p')])
        chapters.append(ch_data)

    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('novel.html')
    open(target_filename, 'w').write(template.render(data).encode('utf-8'))

# Local Variables: **
# comment-column: 56 **
# indent-tabs-mode: nil **
# python-indent: 4 **
# End: **
