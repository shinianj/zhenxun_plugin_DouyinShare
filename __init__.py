import os
from utils.message_builder import custom_forward_msg
import re
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from utils.message_builder import image
import os
from urllib.request import urlopen
from nonebot import on_message
from nonebot.plugin.plugin import PluginMetadata
from utils.utils import get_bot
from services.log import logger
from nonebot.rule import T_State
from nonebot.adapters.onebot.v11 import  GroupMessageEvent ,Message,MessageSegment,Bot
import requests
from .model import al_video,getHeaders


__plugin_meta__ = PluginMetadata("抖音分享",'抖音分享','抖音分享',
    extra={
        "unique_name": "DS",
        "example": "抖音分享(发送抖音链接自动推送)",
        "author": "shinian <2581846402@qq.com>",
        "version": "0.0.1",})

__plugin_type__ = ("群内功能",)

# Config.add_plugin_config(
#         "DY_SHARE",
#         "DEFAULT_DY_SHARE_SAVE",
#         'http',
#         help_="抖音分享格式（可选http与file,file则会在本地存档视频）",
#         default_value='http',
#     )

sv = on_message(priority=15,block= True)
#save = Config.get_config('DY_SHARE',"DEFAULT_DY_SHARE_SAVE",'http')

#此处为废弃的自动下载方法
def download_from_url(url, dst):
    """
    @param url: 下载网址
    @param dst: 文件自定义名称
    :return: bool
    """
    # 获取文件长度
    try:
        file_size = int(urlopen(url).info().get('Content-Length', -1))
    except Exception as e:
        logger.info(e)
        logger.info("错误，访问url: %s 异常" % url)
        return False

    # print("file_size",file_size)
    # 判断本地文件存在时
    if os.path.exists(os.path.join(os.path.dirname(__file__), f'/res/{dst}')):
        # 获取文件大小
        first_byte = os.path.getsize(dst)
    else:
        # 初始大小为0
        first_byte = 0

    # 判断大小一致，表示本地文件存在
    if first_byte >= file_size:
        logger.info("文件已经存在,无需下载")
        return True


    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}

    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=url.split('/')[-1])

    # 访问url进行下载
    req = requests.get(url, headers=header, stream=True)
    try:
        with(os.path.join(os.path.dirname(__file__), f'/res/{dst}'), 'ab')as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
    except Exception as e:
        logger.info(e)
        return False

    pbar.close()
    return True

@sv.handle()
async def sv_handle(bot: Bot,event: GroupMessageEvent, state: T_State):
    bot = get_bot()
    url = event.get_plaintext()
    flag1 = re.match('.*v.douyin.com.*?',str(url))
    flag2 =  re.match(r"(b23.tv)|(bili(22|23|33|2233).cn)|(.bilibili.com)|(^(av|cv)(\d+))|(^BV([a-zA-Z0-9]{10})+)|",str(url))
    flag3 =  re.match(r"(\[\[QQ小程序\]哔哩哔哩\])|(QQ小程序&amp;#93;哔哩哔哩)|(QQ小程序&#93;哔哩哔哩)",str(url))
    if flag1 != None :
        head = "https://api.nxvav.cn/api/jiexi/?url="
        index = url.find('https:')
        orurl = url[index:]#原视频链接
        url = head + orurl
        res = {}
        res = requests.get(url,timeout= 15)
        if res.status_code == 200 and res.json['code'] != 201:
            res = res.json()
            name ="标题 ：" +res['data']['title']
            author = "作者 ：" +res['data']['author']
            msgs = []
            if await al_video(orurl,'douyin',url) != None:
                await sv.send(image(b64 =await al_video(orurl,'douyin',url)))
            msgs.append(name)
            msgs.append(author)
            # name = res['data']['title']
            # name  = name + '.mp4'
            #path = Path(TEMP_PATH)/name
            # if save == 'file':
            #     try:
            #         if  download_from_url(res['play'], name) == True:
            #             pass
            #     except FileNotFoundError:
            #         logger.info("文件已经存在,无需下载")
            msgs.append(Message(MessageSegment.image(res['data']['cover'])))
            msgs.append(Message(MessageSegment.video(res['data']['url'])))
            # result = MessageSegment.record(res['data']['music']['url'])
            # msgs.append((result))
            #msgs.append(image(b64 =await al_video(orurl,'douyin',url)))
            msgs.append('直链 ：'+res['data']['url'])
            msgs.append('作者制作不易，喜欢的话请去视频点个赞吧~')
            # img =  str((Path(IMAGE_PATH)/"ark" / random.choice(os.listdir(Path(IMAGE_PATH)/"ark"))).absolute())
            # cmd = f"""ffmpeg -r 5 -loop 1 -i {img} -i {res['play']} -shortest -preset ultrafast -vcodec libx264 {TEMP_PATH}/{name} -y """
            # subprocess.Popen(cmd, shell=True)
            await bot.send_group_forward_msg(
                group_id=event.group_id, messages=custom_forward_msg(msgs, bot.self_id))
            #await sv.finish(MessageSegment.video(res['play']))
        else:
            await sv.finish('网络不佳，抖音分享出错')
