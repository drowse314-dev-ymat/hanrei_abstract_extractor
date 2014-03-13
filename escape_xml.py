# encoding: utf-8

import sys
import re
import argparse


re_nonentity_ampersand = re.compile(u'&(?!(?:\#?)\w+;)')

def escape_xml(xml_text):
    escaped = re_nonentity_ampersand.sub(
        u'&amp;',
        xml_text,
    )
    return escaped

def read_as_text(filename, fileenc='utf-8'):
    with open(filename, 'rb') as f:
        txt = f.read().decode(fileenc)
    return txt


def run(args):
    xmlfile = args.xmlfile
    shellenc = args.shell_encoding
    xml_text = read_as_text(xmlfile)
    escaped_xml_text = escape_xml(xml_text)
    sys.stdout.write(escaped_xml_text.encode('utf-8'))

def simpletest(args):
    orig = u'M&A &nbsp; &#1224;'
    expected = u'M&amp;A &nbsp; &#1224;'
    escaped = escape_xml(orig)
    assert escaped == expected


if __name__ == '__main__':
    argX = argparse.ArgumentParser()
    subparsers = argX.add_subparsers()

    test = subparsers.add_parser('test')
    test.set_defaults(func=simpletest)

    escape = subparsers.add_parser('escape')
    escape.add_argument('xmlfile')
    escape.add_argument('-e', '--shell_encoding', default='utf-8')
    escape.set_defaults(func=run)

    args = argX.parse_args()

    args.func(args)
