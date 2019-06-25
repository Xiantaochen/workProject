import time
from lxml import etree
import aiohttp
import asyncio
urls = [
    'https://aaai.org/ocs/index.php/AAAI/AAAI18/paper/viewPaper/16488',
    'https://aaai.org/ocs/index.php/AAAI/AAAI18/paper/viewPaper/16583',
    # 省略后面8个url...
]
titles = []
sem = asyncio.Semaphore(10) # 信号量，控制协程数，防止爬的过快
'''
提交请求获取AAAI网页,并解析HTML获取title
'''
async def get_title(url):
    async with sem:
        # async with是异步上下文管理器
        async with aiohttp.ClientSession() as session:  # 获取session
            async with session.request('GET', url) as resp:  # 提出请求
                # html_unicode = await resp.text()
                # html = bytes(bytearray(html_unicode, encoding='utf-8'))
                html = await resp.read() # 可直接获取bytes
                title = etree.HTML(html).xpath('//*[@id="title"]/text()')
                print(''.join(title))
'''
调用方
'''
def main():
    loop = asyncio.get_event_loop()           # 获取事件循环
    tasks = [get_title(url) for url in urls]  # 把所有任务放到一个列表中
    loop.run_until_complete(asyncio.wait(tasks)) # 激活协程
    loop.close()  # 关闭事件循环

if __name__ == '__main__':
    start = time.time()
    main()  # 调用方
    print('总耗时：%.5f秒' % float(time.time()-start))

from pymitmproxy import (url for url in urls if url)