import re

def escape(data):
    return data.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;'," ")

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def replaceWithLink(data):
    regex = r"<a href=\"(.*?\")>|<(?:img|video).*?(src=\"(.*?\"))>"
    match = re.finditer(regex, data, re.MULTILINE|re.IGNORECASE)
    d = data
    for i in match:
        if i.group(1) is not None:
            d = d.replace(i.group(0), i.group(1))
        if i.group(3) is not None:
            d = d.replace(i.group(0), i.group(3))
    return d

f = open("CodeLearnRaw.txt", "r", encoding='utf-8')
data = replaceWithLink(f.read())
data = striphtml(data)
data = escape(data)
print(data)
f.close()
f = open("CodeLearn.txt", "w", encoding='utf-8')
f.write(data)
f.close()


