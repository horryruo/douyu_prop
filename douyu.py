
import requests,json,os,sys,json,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_secrets(item):
    cookies =  os.environ[item]
    try:
        coo = json.loads(cookies)
        return cookies
    except:
        sp = cookies.split(';')
        list = []
        for number, i in enumerate(sp):
            dict = {}
            spp = i.split('=')
            #if spp[0] in ['dy_auth','dy_did','wan_auth37wan']:
             #   dict['domain'] = '.douyu.com'
            #else:
            #dict['domain'] = '.douyu.com'
            #dict['expirationDate'] = time.time()
            #dict['hostOnly'] =  False
            #dict['HttpOnly'] =  True
            #dict['"expires'] =  ""
            dict['name'] = spp[0]
            #dict['path'] = '/'
            #dict['Secure'] =  False
            #dict['session'] = False
            #dict['storeId'] = "0"
            dict['value'] = spp[1]
            #dict['id'] =  number
            list.append(dict)
        list = json.dumps(list)
        return list
cookies_os = get_secrets("DOUYU")
class Func:
    def __init__(self):
        self.cookies = None
func = Func()
#corpid,corpsecret,agentid,mediaid
class Wecom(object):
    def __init__(self,wecom_cid,wecom_secret,wecom_aid,media_id=None,wecom_touid='@all'):
        self.wecom_cid = wecom_cid
        self.wecom_aid = wecom_aid
        self.wecom_secret = wecom_secret
        self.wecom_touid = wecom_touid
        self.media_id = media_id
        get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.wecom_cid}&corpsecret={self.wecom_secret}"
        response = requests.get(get_token_url).content
        self.access_token = json.loads(response).get('access_token')
    def send(self,text):
        get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.wecom_cid}&corpsecret={self.wecom_secret}"
        response = requests.get(get_token_url).content
        access_token = json.loads(response).get('access_token')
        if access_token and len(access_token) > 0:
            send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
            data = {
                "touser":self.wecom_touid,
                "agentid":self.wecom_aid,
                "msgtype":"text",
                "text":{
                    "content":text
                },
                "duplicate_check_interval":600
            }
            response = requests.post(send_msg_url,data=json.dumps(data)).content
            return response
        else:
            return False
    def send_mpnews(self, title, message):
        if self.access_token and len(self.access_token) > 0:
            send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}'
            data = {
                "touser": self.wecom_touid,
                "msgtype": "mpnews",
                "agentid": self.wecom_aid,
                "mpnews": {
                    "articles": [
                        {
                            "title": title,
                            "thumb_media_id": self.media_id,
                            "author": "Author",
                            "content_source_url": "",
                            "content": message.replace('\n', '<br/>'),
                            "digest": message[:100] + message[-100:]
                        }
                    ]
                }
            }
            response = requests.post(send_msg_url,data=json.dumps(data)).content
            return response
        else:
            return False

def send_message(title,content):
    secret_key = os.environ['WECOM']
    idd = secret_key.split(',')
    wecom = Wecom(idd[0],idd[1],idd[2],idd[3])
    try:
        wecom.send_mpnews(title,content)
    except Exception as e:
        print(e)



class Douyu_chrome(object):
    def __init__(self):
        self.engine = Chrome(True,'https://www.douyu.com/687423')

    def auto(self):
        #滚动到背包
        self.engine.dr.get('https://www.douyu.com/687423')
        time.sleep(5)
        bag = self.engine.dr.find_element(By.CSS_SELECTOR,"[class='BackpackButton']")
        self.engine.dr.execute_script("arguments[0].scrollIntoView();", bag)
        time.sleep(10)
        #重定位背包，点击
        bagg = self.engine.dr.find_element(By.CSS_SELECTOR,"[class='BackpackButton']")
        self.engine.dr.execute_script("arguments[0].click();", bagg)
        time.sleep(1)
        #定位到 知道了，点击
        try:
            sub = self.engine.dr.find_element(By.CSS_SELECTOR,"[class='FansGiftPackage-OK']")
            self.engine.dr.execute_script("arguments[0].click();", sub)
        except:
            pass
        #背包界面
        back = self.engine.dr.find_element(By.CSS_SELECTOR,"[class='Backpack JS_Backpack']")
        #背包界面存在
        if back:
            print('成功打开背包')
        self.engine.dr.quit()
class Chrome(object):
    def __init__(self,is_headless,url):
         #设置
        chrome_options = Options()
        if is_headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--window-size=1080,720")
        chrome_options.add_experimental_option('excludeSwitches', ['disable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('lang=zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7')
        chrome_options.add_argument('blink-settings=imagesEnabled=false')
        chrome_options.add_argument('log-level=1')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
        chrome_options.add_argument("disable-blink-features=AutomationControlled")
        
        if "win" in sys.platform:
            self.dr = webdriver.Chrome(executable_path="chrome/chromedriver.exe", options=chrome_options)
        elif "linux" in sys.platform:
            try:
                self.dr = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
                #self.dr = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
                #self.dr = webdriver.Chrome(executable_path="chrome/chromedriver", options=chrome_options)
            except Exception as e:
                print(e)
                self.dr = webdriver.Chrome(options=chrome_options)
        self.dr.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })
        self.wait = WebDriverWait(self.dr, 30)
        self.dr.get('https://www.douyu.com/directory/myFollow')
        self.dr.delete_all_cookies()
        douyu_cookies = cookies_os
        cookies_list = json.loads(douyu_cookies)
        for cookie in cookies_list:
            if 'expiry' in cookie:
                del cookie['expiry']
            if 'sameSite' in cookie:
                del cookie['sameSite']
            self.dr.add_cookie(cookie)
        self.dr.refresh()
        func.cookies = self.dr.get_cookies()
        self.dr.implicitly_wait(5)



class Douyu(object):
    def __init__(self):
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4851.0 Safari/537.36 Edg/100.0.1156.1',
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'x-requested-with':'XMLHttpRequest',
    }
        douyu_cookies = cookies_os
        cookies_list = json.loads(douyu_cookies)
        cookies = dict()
        for i in cookies_list:
            cookies[i.get('name')] = i.get('value')
        self.session = requests.session()
        self.headers = headers
        self.session.headers.update(headers)
        self.session.cookies.update(cookies)

    def pay(self):
            self.headers['referer'] = 'https://www.douyu.com/687423'
            self.headers['content-type'] = 'application/x-www-form-urlencoded'
            self.headers['origin'] = 'https://www.douyu.com'
            url = 'https://www.douyu.com/japi/prop/donate/mainsite/v1'
            self.session.headers.update(self.headers)
            response = self.session.post(url,params={"propId": '268',
                                                    "propCount": '60',
                                                    "roomId":'687423',
                                                    'bizExt':'{"yzxq":{}}'}).content
            res = json.loads(response.decode("utf-8", "ignore"))
            msg = json.loads(response.decode("utf-8", "ignore")).get('msg')
            if msg == '请登录':
                cookies = dict()
                for i in func.cookies:
                    cookies[i.get('name')] = i.get('value')
                    self.session.cookies.update(cookies)
                response = self.session.post(url,params={"propId": '268',
                                                        "propCount": '60',
                                                        "roomId":'687423',
                                                        'bizExt':'{"yzxq":{}}'}).content
                res = json.loads(response.decode("utf-8", "ignore"))
                msg = json.loads(response.decode("utf-8", "ignore")).get('msg')
            return msg,res
if __name__ == '__main__':
    douyu_chrome = Douyu_chrome()
    douyu_chrome.auto()
    douyu = Douyu()
    msg,res = douyu.pay()
    print(res)
    send_message('斗鱼赠送荧光棒通知:'+str(msg),str(res))
