from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from pymouse import PyMouse
import random
import time
import re

# 获取输入框的id，并输入关键字python爬虫
search = input("请输入关键字：")
# 打开浏览器并赋予url
driver = webdriver.Chrome()
url = 'http://www.cmpedu.com/index.htm'
driver.get(url)
driver.find_element_by_id('__KEY2').send_keys(search)
# 输入回车进行搜索
driver.find_element_by_id('__KEY2').send_keys(Keys.ENTER)
time.sleep(2)

book_final_list = []
while True:
    # 执行脚本,进度条拉到最底部
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    # 获取所有商品信息
    book_list = driver.find_elements_by_class_name('ts_solgcontlist')
    #     print(book_list)
    for book in book_list:
        judge = 0
        # 根据属性选择器查找
        # 图书链接
        book_url = book.find_element_by_css_selector('a').get_attribute('href')
        #         print(book_url)

        # 窗口切换
        handle_main = driver.current_window_handle
        js = "window.open('" + book_url + "');"
        driver.execute_script(js)
        handle_all = driver.window_handles  # 仅限于只有2个窗口时
        for h in handle_all:
            # 判断语句来看是否有新窗口，有的话就保存新窗口句柄为handle_new
            if h != handle_main:
                handle_new = h
        driver.switch_to.window(handle_new)

        # 图书ISBN  出版社的网站比较干净，所以没有重复的ISBN，无需去重
        str = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/div[2]/div[1]').text
        pattern = re.compile('ISBN：(.+)\n')  # 正则匹配  ISBM: 与\n之间的内容
        isbn = pattern.findall(str)
        book_isbn = isbn[0]
        book_isbn = book_isbn.replace("-", "")

        # 图书名称
        book_name = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/div[2]/div[1]/div[1]/div[1]').text
        #         pattern = re.compile('书　　名：(.+)\n')
        #         name = pattern.findall(str)
        #         book_name = name[0]

        # 图书作者
        str = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/div[2]/div[1]/div[1]/div[3]').text
        pattern = re.compile('作者：(.+)')
        author = pattern.findall(str)
        if author == []:
            book_author = "劳拉格雷泽 龚辉伦"
        else:
            book_author = author[0]

        time.sleep(3)
        driver.close()
        driver.switch_to.window(handle_main)

        book_content = f'''
                             图书名称: {book_name}
                             图书作者: {book_author}
                             图书出版社:机械工业出版社
                             图书ISBN: {book_isbn}
                             图书链接: {book_url}
                             \n
                             '''
        print(book_content)
        book_dic = {
            "图书名称": book_name,
            "图书作者": book_author,
            "图书出版社": "机械工业出版社",
            "图书ISBN": book_isbn,
            "图书链接": book_url,
        }
        # 将当前图书信息存入总列表中
        book_final_list.append(book_dic)
    #         print(book_final_list)
    # 点击下一页,以judge2为辅助，取出class值，若有值即disable，判断已经是最后一页，否则继续爬！
    judge2 = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[2]/div/div/ul/li[8]').get_attribute('class')
    if judge2:
        print("爬取结束")
        break
    else:
        driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[2]/div/div/ul/li[8]/a').click()
        time.sleep(2)
# 关闭退出浏览器
driver.quit()