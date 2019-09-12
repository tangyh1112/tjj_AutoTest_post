from atexit import register
from random import randrange
from threading import Thread, currentThread
from time import ctime, sleep
import requests


# 自定义一个集合对象，重写__str__方法
class CleanOutputSet(set):
    def __str__(self):
        return ', '.join(x for x in self)


# 列表生成式   randrange()用于生成一个随机数，range()返回一个列表
loops = (randrange(2, 5) for x in range(randrange(10, 20)))
remaining = CleanOutputSet()

def mobile():
    url_xs = "http://6.duotucms.com/index.php/index/order"  # 下沙
    url_yp = "http://1.duotucms.com/index.php/index/order"  # 河庄
    url_by = "http://3.duotucms.com/index.php/index/order"  # 白杨
    urls = [url_xs, url_yp,url_by]  #
    cookie = "cp_language=zh,PHPSESSID=trv69789qg0pn10ut5s49rmois"
    data1 = "name=%E6%B1%A4%E9%93%B6%E5%8D%8E&tel=18989848397&sn=331023199511125124"  # tyh
    data2 = "name=%E4%B8%87%E5%A4%8F%E5%A9%B7&tel=15267429753&sn=330127199405094029"  # WXT
    data3 = "name=%E5%90%B4%E7%8E%B2%E9%92%B0&tel=15268351131&sn=330483199506206226"  # wly
    dataS = [data1, data2, data3]
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        'Content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'Cookie': cookie}
    for url in urls:
        for data in dataS:
            response_passed = requests.request("post", url, data=data, headers=headers)
            response_passed.encoding = 'utf-8'
            a = response_passed.text
            print(data + "    " + url)
            print(a.encode('utf-8').decode("unicode_escape"))


def loop(nsec):
    myname = currentThread().name
    remaining.add(myname)
    print('[%s] 开始了 %s' % (ctime(), myname))
    sleep(nsec)
    mobile()
    remaining.remove(myname)
    print('[%s] 结束了 %s (%s second)' % (ctime(), myname, nsec))
    print('  (还存在：%s)' % (remaining or 'NONE'))


def _main():
    # 创建3~6个线程，每个线程睡眠2~4秒
    for pause in loops:
        Thread(target=loop, args=(pause,)).start()


# 装饰器，在脚本的最后执行
@register
def _atexit():
    print('所有的完成于：', ctime())


if __name__ == '__main__':
    _main()