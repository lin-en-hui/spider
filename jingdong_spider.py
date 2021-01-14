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
url = 'https://www.jd.com/'
driver.get(url)
driver.find_element_by_id('key').send_keys(search)
# 输入回车进行搜索
driver.find_element_by_id('key').send_keys(Keys.ENTER)
time.sleep(2)

book_final_list = []
while True:
    # 执行脚本,进度条拉到最底部
    driver.execute_script('window.scrollTo(0,document.body.\
    scrollHeight)')
    # 获取所有商品信息
    book_list = driver.find_elements_by_class_name('gl-item')
    #     print(book_list)
    for book in book_list:
        judge = 0
        # 根据属性选择器查找
        # 图书链接
        book_url = book.find_element_by_css_selector('.p-img a').get_attribute('href')
        # 图书名称
        book_name = book.find_element_by_css_selector('.p-name em').text.replace("\n", "--")
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

        # 图书ISBN
        str = driver.find_element_by_xpath('//*[@id="parameter2"]').text
        pattern = re.compile('ISBN：(.+)\n')  # 正则匹配  ISBM: 与\n之间的内容
        isbn = pattern.findall(str)
        book_isbn = isbn[0]

        # 判断ISBN是否重复，用continue实现去重
        res = [item["图书ISBN"] for item in book_final_list]  # 所有的ISBN
        #         print(res)
        for i in res:
            if book_isbn == i:
                judge = 1
        if judge == 1:
            driver.close()
            driver.switch_to.window(handle_main)
            continue

        # 图书出版社
        pattern = re.compile('出版社： (.+)\n')  # 正则匹配  出版社:  与\n之间的内容
        pub = pattern.findall(str)
        book_pub = pub[0]
        # 图书作者
        str = driver.find_element_by_xpath('//*[@id="p-author"]').text
        pattern = re.compile('(.+)著')  # 正则匹配  获取'著'之前的内容
        a = pattern.findall(str)

        if a == []:
            time.sleep(3)
            driver.close()
            driver.switch_to.window(handle_main)
            continue
        else:
            author = a[0]
            time.sleep(3)
            driver.close()
            driver.switch_to.window(handle_main)

        book_content = f'''
                         图书名称: {book_name}
                         图书作者: {author}
                         图书出版社: {book_pub}
                         图书ISBN: {book_isbn}
                         图书链接: {book_url}
                         \n
                         '''
        print(book_content)
        # 将数据保存到字典里
        book_dic = {
            "图书名称": book_name,
            "图书作者": author,
            "图书出版社": book_pub,
            "图书ISBN": book_isbn,
            "图书链接": book_url,
        }
        # 将当前图书信息存入总列表中
        book_final_list.append(book_dic)
    #         print(book_final_list)
    # 点击下一页,-1表示没找到
    if driver.page_source.find(
            'pn-next disabled') == -1:
        driver.find_element_by_class_name \
            ('pn-next').click()
        time.sleep(2)
    else:
        print("爬取结束")
        break
# 关闭退出浏览器
driver.quit()