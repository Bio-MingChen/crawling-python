# a git submitting to github

import requests
import bs4
import re
import time
import random

class Spyder():
    #伪装浏览器首部 brwoser header simulation
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }

    def download_html(self,url,trytime = 2):
        '''
        get the html from given url and try again when timeout
        '''
        try:
            responce = requests.get(url,headers=self.headers,timeout=5)
            # print('status_code is %s' % responce.status_code)
            # print('raise_for_status is %s' % responce.raise_for_status)
            return(responce.text)
            # if responce.raise_for_status() != 
        except requests.exceptions.Timeout:
            if trytime > 0:
                print("Request timeout and try again...")
                self.download_html(url,trytime - 1) # 在类中使用递归 Using Recursion in Class
            else:
                print("Request Time out!")
                return(None)
        except requests.exceptions.HTTPError as e:
            if hasattr(e,'errno'):
                print(e.errno)
            return(None)
        except requests.exceptions.ConnectionError:
            print('Connection Error,please check whether your url is valid!')
            return(None)
        

    def get_proxy_info(self,html,filtertime=1):
        '''
        getting out the proxies information from html by bs4
        ip_info_list structure: [[IP,PORT,SITE,RespTime,CheckTime]...]
        '''
        
        soup = bs4.BeautifulSoup(html,'html.parser')
        ip_list = soup.select('tr')
        ip_info_list = []
        fast_ip = []
        for ip_info in ip_list:
            # print(ip_info)
            IP = re.search('<td data-title="IP">(.+?)</td>',str(ip_info))
            if IP is not None:
                IP = IP.group(1)
            PORT = re.search('<td data-title="PORT">(.+?)</td>',str(ip_info))
            if PORT is not None:
                PORT = PORT.group(1)
            SITE = re.search('<td data-title="位置">(.+?)</td>',str(ip_info))
            if SITE is not None:
                SITE = SITE.group(1)
            RespTime = re.search('<td data-title="响应速度">(.+?)秒</td>',str(ip_info))
            if RespTime is not None:
                RespTime = RespTime.group(1)
            CheckTime = re.search('<td data-title="最后验证时间">(.+?)</td>',str(ip_info)) 
            if CheckTime is not None:
                CheckTime = CheckTime.group(1)
            ip_info_list.append([IP,PORT,SITE,RespTime,CheckTime])
            # print([IP,PORT,SITE,RespTime,CheckTime])

            if RespTime is not None and float(RespTime) <= float(filtertime):
                fast_ip.append(IP)
        # fast_ip = [str(i[0]) + str(i[1]) for i in ip_info_list if float(i[3]) <= filtertime]
        return(fast_ip)
            

    def download_proxy(self,page_num=1):
        '''
        get the free proxies ip from www.kuaidaili.com
        page_num control ip number and pages of crawling 
        '''
        url = 'https://www.kuaidaili.com/free/inha/'
        if page_num == 1:
            page = [1]
        elif page_num > 1:
            page = [i for i in range(1,page_num+1)]
        n = 0
        all_proxies = []
        while n < len(page):
            url_page = url + str(page[n]) 
            html = self.download_html(url_page)
            print(url_page)
            # print(html)
            fast_ip = self.get_proxy_info(html)
            print(fast_ip)
            if fast_ip is not None:
                all_proxies = all_proxies + fast_ip
            else:
                pass
            n += 1
            sleep_time = 2
            print("Now,let's have a rest for %s sec" % sleep_time)
            time.sleep(sleep_time) # 该网站如果不设置间隔时间会什么都爬不下来
        return(all_proxies)



if __name__ == '__main__':
    spyder = Spyder()
    proxies_ips = spyder.download_proxy(page_num=3) # print the fast ip proxies
    print(proxies_ips)
