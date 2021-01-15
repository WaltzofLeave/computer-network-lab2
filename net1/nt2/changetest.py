import re

def changeurl(msg,url):
    msg = msg.decode('utf-8')
    print(msg)
    msg = msg.split(' ')
    ans = ''
    msg[1] = url
    for string in msg:
        ans = ans + string + ' '
    ans = ans[:-1]
    msg = ans
    msg = str.encode(msg)
    msg = msg.decode('utf-8')
    msg = msg.split('\r\n')

    dealurl = url
    head_pat = re.compile(r'.*://')
    if head_pat.match(dealurl):
        dealurl = re.split(r'://', dealurl)[-1]
    dealurl = dealurl.split(r'/')[0]

    msg[1] ='Host: '+ dealurl
    ans = ''
    for string in msg:
        ans = ans +string + r'\r\n'
    msg = ans
    print(msg)
connectedmsg = b'POST http://today.hit.edu.cn/boost/replace?callback=Drupal%5CCore%5CRender%5CElement%5CStatusMessages%3A%3ArenderMessages&args%5B0%5D=&token=_AZ3AspTMq078QO9qahwtJ85a5oxfiI8sVz8o_s8szc&_wrapper_format=drupal_ajax HTTP/1.1\r\nHost: today.hit.edu.cn\r\nProxy-Connection: keep-alive'
changeurl(connectedmsg,'http://www.baidu.com')