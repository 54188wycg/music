from DrissionPage import Chromium
from bs4 import BeautifulSoup
import time,json
browser = Chromium()
tab1 = browser.latest_tab
tab1.get('https://www.kugou.com/')
search1= BeautifulSoup(tab1.html, 'html.parser')
if search1.find(class_="cmhead1_d5 _login").get('style')==None:
    tab1.ele('css:.cmhead1_d5._login').click()
    while True:
        search1= BeautifulSoup(tab1.html, 'html.parser')
        try:
            if search1.find(class_="cmhead1_d5 _login").get('style')!=None:
                break
        except:
            pass
        time.sleep(0.1)
        print(search1.find(class_="cmhead1_d5 _login"))
exit()
tab1.ele('css:#secoundContent .homep_d1_d2 .homep_d1_d2_d1 .homep_d1_d2_d1_a1:nth-of-type(2) .homep_cm_item_st1_d1').click()
data=[]
time.sleep(3)
tab2 = browser.latest_tab
tab2.wait.load_start()
tab2.ele('css:#list.icon.list').click()
old='54188'
for i in range(3):
    tab2.ele(f'css:#musicbox .musiclist li:nth-of-type({i+1})').click()
    while True:
        search= BeautifulSoup(tab2.html, 'html.parser')
        audio_tag = search.find(id="myAudio")
        url=audio_tag.get('src')
        time.sleep(0.1)
        if url!=old:
            old=url
            break
    names = search.find_all('span', class_='musiclist-songname-txt')
    name=names[i].get('title')
    data.append({"name":name,"addr":url})
print(data)