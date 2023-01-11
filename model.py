import os
import requests
import os
import random
import aiohttp
from utils.image_utils import BuildImage
from services.log import logger
import urllib.parse
import requests
from bs4 import BeautifulSoup
from configs.path_config import TEMP_PATH

# async def b23_extract(text):
#     b23 = re.compile(r"b23.tv/(\w+)|(bili(22|23|33|2233).cn)/(\w+)", re.I).search(
#         text.replace("\\", "")
#     )
#     url = f"https://{b23[0]}"
#     async with aiohttp.request(
#         "GET", url, timeout=aiohttp.client.ClientTimeout(10)
#     ) as resp:
#         return str(resp.url)

async def search_bili_by_title(title: str):
    search_url = f"https://api.bilibili.com/x/web-interface/search/all/v2?keyword={urllib.parse.quote(title)}"

    async with aiohttp.request(
        "GET", search_url, timeout=aiohttp.client.ClientTimeout(10)
    ) as resp:
        result = (await resp.json())["data"]["result"]

    for i in result:
        if i.get("result_type") != "video":
            continue
        # 只返回第一个结果
        return i["data"][0].get("arcurl")


def getHeaders():
    '''
    访问header头（可以抄去爬虫用）
    '''
    # 各种PC端
    user_agent_list_2 = [
    # Opera
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    # Firefox
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    # Safari
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    # chrome
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    # 360
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    # 淘宝浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    # 猎豹浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    # QQ浏览器
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    # sogou浏览器
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    # maxthon浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
    # UC浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
    ]
    #各种移动端
    user_agent_list_3 = [
    # IPhone
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # IPod
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # IPAD
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # Android
    "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    # QQ浏览器 Android版本
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    # Android Opera Mobile
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    # Android Pad Moto Xoom
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    # BlackBerry
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    # WebOS HP Touchpad
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    # Nokia N97
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    # Windows Phone Mango
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    # UC浏览器
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    # UCOpenwave
    "Openwave/ UCWEB7.0.2.37/28/999",
    # UC Opera
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999"
    ]
    # 一部分 PC端的
    user_agent_list_1 = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    user_agent_list = user_agent_list_1 + user_agent_list_2 + user_agent_list_3
    UserAgent = random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}
    return headers



async def al_video(orurl,laiyuan:str,url=None) -> str:
    '''
    orurl:视频源链接（用于获取视频详细信息）
    laiyuan:视频平台
    url:调用api获取信息的合成链接
    '''
    #创建视频信息卡片

    #抖音平台使用api获取标题、作者、封面、作者头像
    if laiyuan == 'douyin':
        try:
            res = requests.get(url,timeout= 15)
            res = res.json()
            name = res['data']['title']
            if name == None:
                return None
            if '"' in name:
                name = str(name).replace('"',' ')
            if ':' in name:
                name = str(name).replace(':','——')
            #name_size = getsize(name)
            author = res['data']['author']
            cover = res['data']['cover']
            r = requests.get(cover,headers=getHeaders())
            with open(f'{TEMP_PATH}/douyin_cover.png','wb') as f:
                f.write(r.content)
            cover_ = BuildImage(0,0,background=f'{TEMP_PATH}/douyin_cover.png')
            cover_w = cover_.w
            cover_h = cover_.h
            author_cover = res['data']['avatar']
            r = requests.get(author_cover,headers=getHeaders())
            with open(f'{TEMP_PATH}/douyin_author_cover.png','wb') as f:
                f.write(r.content)
            author_cover_ = BuildImage(0,0,background=f'{TEMP_PATH}/douyin_author_cover.png')
            await author_cover_.acircle()
            await author_cover_.aresize(w=40,h=40)
            author_cover_w = author_cover_.w
            author_cover_h = author_cover_.h

            #获取视频点赞、评论、收藏数、发布时间，以及作者获赞和粉丝数
            res = requests.get(orurl)
            orurl = res.url
            s =requests.Session()
            r = s.post(orurl,headers=getHeaders())
            html = r.text
            # Note=open('x.txt',mode='w',encoding='utf-8')
            # Note.write(f'{r.text}') #\n 换行符
            # Note.close()
            soup = BeautifulSoup(html,'html.parser')
            data_list =soup.find_all(class_="CE7XkkTw")
            dianzan = str(data_list[0]).split('class="CE7XkkTw">')[-1].split('<')[0]
            #dianzan_size = getsize(dianzan)
            pinglun = str(data_list[1]).split('class="CE7XkkTw">')[-1].split('<')[0]
            #pinglun_size = getsize(pinglun)
            shoucang = str(data_list[2]).split('class="CE7XkkTw">')[-1].split('<')[0]
            data_list =soup.find_all(class_="aQoncqRg")
            time = str(data_list[0]).split('class="aQoncqRg">')[-1].split('</span>')[0]
            time = time.replace('<!-- -->','')
            author_data = soup.find_all(class_="EobDY8fd")
            huozan = str(author_data[0]).split('class="EobDY8fd">')[-1].split('<')[0]
            fan = str(author_data[1]).split('class="EobDY8fd">')[-1].split('<')[0]

            #获取logo长宽
            logo = BuildImage(0,0,background=(os.path.join(os.path.dirname(__file__), f'res/douyin_logo.png')))
            logo_w = logo.w
            logo_h = logo.h
            #获取点赞，评论，收藏logo长宽
            dz = BuildImage(0,0,background=(os.path.join(os.path.dirname(__file__), f'res/douyin_dianzan.png')))
            dz_w = dz.w
            dz_h = dz.h
            pl = BuildImage(0,0,background=(os.path.join(os.path.dirname(__file__), f'res/douyin_pinglun.png')))
            pl_w = dz.w
            pl_h = dz.h
            sc = BuildImage(0,0,background=(os.path.join(os.path.dirname(__file__), f'res/douyin_shoucang.png')))
            sc_w = dz.w
            sc_h = dz.h

            #组合图片
            A = BuildImage(cover_w+100,cover_h+logo_h+150,font_size=15,color='#161722')
            await A.apaste(logo,(10,10),alpha=True)
            await A.apaste(author_cover_,(logo_w+50,10),alpha=True)
            await A.atext((logo_w+60+author_cover_w,10),author,'#FFFFF1')
            name_size = A.getsize(author)
            data = '粉丝 '+fan+' 获赞 '+huozan
            await A.atext((logo_w+60+author_cover_w,10+name_size[1]),data,'#FFFFF1')
            await A.apaste(cover_,(A.w//2-cover_w//2,logo_h+80),alpha=True)
            await A.aline((A.w//2-cover_w//2,logo_h+100+cover_h,A.w//2+cover_w//2,logo_h+100+cover_h),'#FFFFF1',3)

            # title = BuildImage(cover_w+100,10+logo_h,font_size = 37,color='#161722')
            # await title.atext((0,0),name,'#FFFFF1')

            # await A.apaste(title,(0,10+logo_h),alpha=True)

            await A.apaste(dz,(A.w//2-cover_w//2,logo_h+120+cover_h),alpha=True)
            await A.atext((A.w//2-cover_w//2+dz_w+5,logo_h+120+cover_h),dianzan,'#FFFFF1')
            dianzan_size = A.getsize(dianzan)

            await A.apaste(pl,(A.w//2-cover_w//2+dz_w+15+dianzan_size[0],logo_h+120+cover_h),alpha=True)
            await A.atext((A.w//2-cover_w//2+dz_w+20+dianzan_size[0]+pl_w,logo_h+120+cover_h),pinglun,'#FFFFF1')
            pinglun_size = A.getsize(pinglun)

            await A.apaste(sc,(A.w//2-cover_w//2+dz_w+30+dianzan_size[0]+pl_w+pinglun_size[0],logo_h+120+cover_h),alpha=True)
            await A.atext((A.w//2-cover_w//2+dz_w+35+dianzan_size[0]+pl_w+pinglun_size[0]+sc_w,logo_h+120+cover_h),shoucang,'#FFFFF1')
            shoucang_size = A.getsize(shoucang)

            await A.atext((A.w//2-cover_w//2+dz_w+45+dianzan_size[0]+pl_w+pinglun_size[0]+sc_w+shoucang_size[0],logo_h+120+cover_h),time,'#FFFFF1')

            return A.pic2bs4()
        except IndexError as e:
            logger.info('抖音解析尝试重连……')
            await al_video(orurl,laiyuan,url)

    # if laiyuan == 'bili':
    #     res = requests.get(orurl)
    #     orurl = res.url
    #     s =requests.Session()
    #     r = s.post(orurl,headers=getHeaders())
    #     html = r.text


