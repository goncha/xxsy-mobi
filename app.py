# -*- coding: utf-8 -*-


if __name__ == '__main__':

    from lxml.html import parse as parse_html
    from urlparse import urlparse
    import sys

    url = sys.argv[1]
    url_obj = urlparse(url)
    base_url = url_obj.scheme + '://' + url_obj.hostname + '/' + ('/'.join(url_obj.path.split('/')[:-1]))

    print 'Base URL:', base_url
    print 'TOC URL:', url

    tocDoc = parse_html(url)
    print tocDoc.xpath('//div[@id="ct_title"]/h1')[0].text

    for e in tocDoc.xpath('//div[@id="catalog_list"]/ul/li/a'):
        print e.text, e.attrib.get('href')


# Local Variables: **
# comment-column: 56 **
# indent-tabs-mode: nil **
# python-indent: 4 **
# End: **
