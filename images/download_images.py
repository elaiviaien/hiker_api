from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import urllib.request
options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
browser.get('https://www.google.com/search?q=%D1%84%D0%BE%D0%BD&tbm=isch&ved=2ahUKEwisg5uwi6nzAhXCzyoKHYD-AVoQ2-cCegQIABAA&oq=%D1%84%D0%BE%D0%BD&gs_lcp=CgNpbWcQAzIHCCMQ7wMQJzIHCAAQsQMQQzIHCAAQsQMQQzIECAAQQzIECAAQQzIHCAAQsQMQQzIECAAQQzIECAAQQzIHCAAQsQMQQzIHCAAQsQMQQ1DjuwVY47sFYLq9BWgAcAB4AIABUYgBUZIBATGYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=Uu5WYaySMMKfqwGA_YfQBQ&bih=952&biw=1853&rlz=1C1SQJL_ruUA877UA877')
time.sleep(10)  # Allow 2 seconds for the web page to open
scroll_pause_time = 0.5 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = browser.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    browser.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = browser.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break
generated_html = browser.page_source
soup = BeautifulSoup(generated_html, 'html.parser')

avas = soup.find('body').find('div',class_='islrc').find_all(
        'div', class_='isv-r PNCib MSM1fd BUooTd')
links=[]
file = open("page.html",'w',encoding='utf-8')
file.write(str(avas))
file.close()
for ava in avas:
    img = ava.find('img',class_='rg_i Q4LuWd')
    if img.get('data-src') :
        links.append(img.get('data-src'))
    if img.get('src') :
        links.append(img.get('src'))
i=0
for link in links:
    i+=1
    urllib.request.urlretrieve(link, str(i)+'.jpg')


