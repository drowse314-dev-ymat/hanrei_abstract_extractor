# encoding: utf-8

import sys
import re
import argparse
try:
    from html import parser as htmlparser
except:
    import HTMLParser as htmlparser
from lxml import etree


def format_text_of(element):
    as_string = etree.tostring(element)
    text = _clean(as_string)
    text = _get_text_from(element, text)
    text = text.replace(u'<br/>', u'\n')
    text = _single_breaks(text)
    text = _clean_around_breaks(text)
    return text.strip()

def _clean(htmltext):
    cleaned = htmlparser.HTMLParser().unescape(htmltext)
    if cleaned == htmltext:
        cleaned = cleaned.decode('utf-8')
    return cleaned

def _get_text_from(element, as_string):
    headtext = element.text
    if headtext is None:
        headtext = u'</{}>'.format(element.tag)
    as_string = as_string[as_string.find(headtext):] 
    as_string = as_string[:as_string.find(u'</{}>'.format(element.tag)):] 
    return as_string

def _single_breaks(text):
    length = len(text)
    while True:
        text = text.replace('\n\n', '\n')
        shortened = len(text)
        if length - shortened == 0:
            break
        length = shortened
    return text

def _clean_around_breaks(text):
    lines = [
        line.strip()
        for line in text.split(u'\n')
    ]
    return u'\n'.join(lines)

re_datestr = re.compile(
    u'(?P<nengou>(?:明治)|(?:大正)|(?:昭和)|(?:平成))(?P<year>\d+)年'
    u'(?P<month>\d{2})月'
    u'(?P<day>\d{2})日'
)
nengou_alphabet = {
    u'明治': u'm', u'大正': u't',
    u'昭和': u's', u'平成': u'h',
}

def expanddate(datestr):
    matched = re_datestr.match(datestr)
    assert matched
    as_dict = matched.groupdict()
    gou = nengou_alphabet[as_dict['nengou']]
    year = as_dict['year']
    month = unicode(int(as_dict['month']))
    day = unicode(int(as_dict['day']))
    return gou + year, month, day

def abstracts_from_xml(filepath, dateheader=True, encoding='utf-8'):
    xml_text = _read_as_text(filepath, encoding=encoding)
    root = etree.fromstring(xml_text.encode(encoding))
    for abstract in _abstracts_from(root, dateheader=dateheader):
        yield abstract

def _read_as_text(filepath, encoding='utf-8'):
    return open(filepath, 'rb').read().decode(encoding)

def _abstracts_from(hanreirecords, dateheader=True):
    for hanrei in hanreirecords.findall(u'.//Hanrei'):
        date_header = expanddate(hanrei.find('.//Date').text)
        abstract = format_text_of(hanrei.find('.//Abstract'))
        data = []
        if dateheader:
            data.append(date_header)
        data.append(abstract)
        yield tuple(data)

def runtest(args):

    # format one
    orig_xml = (
        u'<Abstract>一　雇用者の安全配慮義務違反によりじん肺にかかったことを'
        u'理由とする損害賠償請求権の消滅時効は、じん肺法所定の管理区分についての'
        u'最終の行政上の決定を受けた時から進行する。\n<br/><br/>  二　炭鉱労務に従事して'
        u'じん肺にかかった者又はその相続人が、雇用者に対し、財産上の損害の賠償を'
        u'別途請求する意思のない旨を訴訟上明らかにして慰謝料の支払を求めた場合に、'
        u'じん肺が重篤な進行性の疾患であって、現在の医学では治療が不可能とされ、'
        u'その症状も深刻であるなど判示の事情の下において、その慰謝料額を、じん肺法'
        u'所定の管理区分に従い、死者を含む管理四該当者につき一二〇〇万円又は'
        u'一〇〇〇万円、管理三該当者につき六〇〇万円、管理二該当者につき三〇〇万円'
        u'とした原審の認定には、その額が低きに失し、著しく不相当なものとして、'
        u'経験則又は条理に反する違法がある。\n<br/>ダミー<br/></Abstract>'
    )
    orig_elem = etree.fromstring(orig_xml)
    processed = format_text_of(orig_elem)

    expected = ( 
        u'一　雇用者の安全配慮義務違反によりじん肺にかかったことを'
        u'理由とする損害賠償請求権の消滅時効は、じん肺法所定の管理区分についての'
        u'最終の行政上の決定を受けた時から進行する。\n二　炭鉱労務に従事して'
        u'じん肺にかかった者又はその相続人が、雇用者に対し、財産上の損害の賠償を'
        u'別途請求する意思のない旨を訴訟上明らかにして慰謝料の支払を求めた場合に、'
        u'じん肺が重篤な進行性の疾患であって、現在の医学では治療が不可能とされ、'
        u'その症状も深刻であるなど判示の事情の下において、その慰謝料額を、じん肺法'
        u'所定の管理区分に従い、死者を含む管理四該当者につき一二〇〇万円又は'
        u'一〇〇〇万円、管理三該当者につき六〇〇万円、管理二該当者につき三〇〇万円'
        u'とした原審の認定には、その額が低きに失し、著しく不相当なものとして、'
        u'経験則又は条理に反する違法がある。\nダミー'
    )

    assert format_text_of(orig_elem) == expected

    empty_xmltext = u'<Abstract><br/></Abstract>'
    empty_abstelem =  etree.fromstring(empty_xmltext)
    assert format_text_of(empty_abstelem) == u''

    # date conversion
    expected = {
        u'平成7年03月07日': (u'h7', u'3', u'7'),
        u'平成17年03月27日': (u'h17', u'3', u'27'),
        u'昭和43年03月01日': (u's43', u'3', u'1'),
        u'明治30年01月02日': (u'm30', u'1', u'2'),
        u'大正12年12月02日': (u't12', u'12', u'2'),
    }

    for datestr in expected:
        assert expanddate(datestr) == expected[datestr]

    # format an xml
    abstracts = list(abstracts_from_xml('test/hanrei.xml', dateheader=True))
    expected = list(_iter_testcase('test/abstracts.txt'))
    for got, exp in zip(abstracts, expected):
        assert len(got) == len(exp)
        assert got[0] == exp[0]
        assert got[1] == exp[1]
        assert got == exp
    abstracts = list(abstracts_from_xml('test/hanrei2.xml', dateheader=True))

    expected = list(_iter_testcase('test/abstracts2.txt'))
    for got, exp in zip(abstracts, expected):
        assert len(got) == len(exp)
        assert got[0] == exp[0], \
                (unicode(repr(got[0])) + got[1]).encode('utf-8') + \
                (unicode(repr(exp[0])) + exp[1]).encode('utf-8') 
        assert got[1] == exp[1], \
                (unicode(repr(got[0])) + got[1]).encode('utf-8') + \
                (unicode(repr(exp[0])) + exp[1]).encode('utf-8') 
        assert got == exp


def _iter_testcase(path):
    txtcontent = open(path, 'rb').read().decode('utf-8')
    lines = txtcontent.split(u'\n')
    header = None
    stack = []
    for line in lines:
        if line.startswith(u'#'):
            if header is not None:
                yield header, u'\n'.join(stack)
            header = tuple(line[2:].split(u','))
            stack = []
        elif line != u'':
            stack.append(line)
    yield header, u'\n'.join(stack)


def ex_abstracts(args):
    for dateheader, abstract in abstracts_from_xml(args.xmlfile, encoding=args.enc):
        abstract = abstract.replace(u'\n', args.linesep)
        if abstract == u'':
            continue

        date = u'.'.join(dateheader)
        sys.stdout.write(
            ((u'{}' + args.fieldsep + u'{}\n').format(date, abstract)).encode(args.enc)
        )


if __name__ == '__main__':

    argX = argparse.ArgumentParser()
    subparsers = argX.add_subparsers()

    test = subparsers.add_parser('test')
    test.set_defaults(func=runtest)

    abstract_extractor = subparsers.add_parser('abstract')
    abstract_extractor.set_defaults(func=ex_abstracts)
    abstract_extractor.add_argument('xmlfile')
    abstract_extractor.add_argument('--linesep', default=u'|')
    abstract_extractor.add_argument('--fieldsep', default=u',')
    abstract_extractor.add_argument('-e', '--enc', default='utf-8')

    args = argX.parse_args()
    args.func(args)