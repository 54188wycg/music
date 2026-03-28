#初始化
from DrissionPage import Chromium
from bs4 import BeautifulSoup
import time,json
browser = Chromium()
#访问酷狗+点击热歌榜
tab1 = browser.latest_tab
tab1.get('https://www.kugou.com/')
#登录
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
tab1.ele('css:#secoundContent .homep_d1_d2 .homep_d1_d2_d1 .homep_d1_d2_d1_a1:nth-of-type(2) .homep_cm_item_st1_d1').click()
def wait(x):
    global search1,search2,old,url
    if x=="song":
        while True:
            search2= BeautifulSoup(tab2.html, 'html.parser')
            audio_tag = search2.find(id="myAudio")
            url=audio_tag.get('src')
            time.sleep(0.1)
            if search2.find(class_="ui-dialog playsong")!=None:
                tab2.ele('css:.ui-dialog-close').click()
                tab2.ele('css:#list.icon.list').click()
                url=""
                break
            if url!=old:
                old=url
                break
    elif x=="home":
        while True:
            time.sleep(1)
            search1= BeautifulSoup(tab1.html, 'html.parser')
            state = search1.find(id="before_page").get('style')
            time.sleep(0.5)
            if state=="display: none;":
                break
    else:
        raise ValueError("x不是song或home,请重新输入")
data=[]
time.sleep(3)
#播放页初始化
tab2 = browser.latest_tab
tab2.wait.load_start()
tab2.ele('css:#list.icon.list').click()
old=''
#播放页爬取
for i in range(30):
    tab2.ele(f'css:#musicbox .musiclist li:nth-of-type({i+1})').click()
    wait("song")
    #爬取ing
    if url=="":
        continue
    names = search2.find_all('span', class_='musiclist-songname-txt')
    name=names[i].get('title')
    data.append({"name":name,"addr":url})
with open('hot.json','w+', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
#更新个性歌单
with open('student.json', 'r', encoding='utf-8') as f:
    x = json.load(f)
data=[]
for i in range(100):
    tab1.ele("css:input").clear()
    tab1.ele("css:input").input(x[i]['name'])
    tab1.actions.key_down('ENTER')
    wait("home")
    tab1.ele('css:#search_song .list_content.clearfix li:nth-of-type(1) .search_icon.checkbox').click()
    tab1.ele('css:#search_song .play_all .search_icon').click()
    wait("song")
    #爬取ing
    audio_tag = search2.find(id="myAudio")
    url=audio_tag.get('src')
    data.append({"name":x[i]['name'],"addr":url})
with open('student.json','w+', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
#更新歌手
with open('singers.json', 'r', encoding='utf-8') as f:
    x = json.load(f)
data=[]
for i in x:
    tab2.ele('css:.icon.list-menu-icon-del.clear').click()
    tab1.ele("css:input").clear()
    tab1.ele("css:input").input(i["name"])
    tab1.actions.key_down('ENTER')
    wait('home')
    tab1.ele('css:#search_song .search_icon.checkall').click()
    tab1.ele('css:#search_song .play_all .search_icon').click()
    songs=[]
    time.sleep(3)
    for j in range(30):
        tab2.ele(f'css:#musicbox .musiclist li:nth-of-type({j+1})').click()
        wait("song")
        if url=="":
            continue
        names = search2.find_all('span', class_='musiclist-songname-txt')
        name=names[j].get('title')
        songs.append({"name":name,"addr":url})
    data.append({"name":i["name"],"songs":songs})
with open('singers.json','w+', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
browser.quit()
