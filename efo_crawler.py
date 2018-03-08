#EFO database crawler

import requests
import bs4
import re
import random
import threading
import time
import proxy_for_crawler # my proxy
sema = threading.BoundedSemaphore(5)
lock = threading.Lock()
spyder = proxy_for_crawler.Spyder()
proxies_list = spyder.download_proxy(page_num=3)


def download_html(url,trytime=3):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}

    try:
        ip = random.choice(proxies_list)
        ip_proxy = {'http':'http://' + ip}
        print('IP:{}'.format(ip_proxy))
        responce = requests.get(url,headers=headers,proxies=ip_proxy,timeout=10)
        return(responce.text)
    except:
        if trytime > 0:
            download_html(url,trytime - 1)
        else:
            return(None)
    
def get_description(html):
    soup = bs4.BeautifulSoup(html,'html.parser')
    tag = soup.select('meta[name:"description"]')
    # tag = soup.select('div[property:"description"]')
    return(tag)

def re_desc(tag):
    re_str = re.search('content=[\"\']\[([\s\S]*?)\][\"\']',str(tag[0]))#有的注释信息有多行，多行匹配正则
    if re_str != None:
        desc = re.sub('\n','',re_str.group(1))
    else:
        desc = ''
        print('there is none in %s' % tag[0])
    return(desc)

def make_urls():
    """
    all_efo_id structure: [[disGeNetID,diseaseName,efo_id]...]
    """
    disease_data = 'efo_annotation/disease_mappings.tsv'
    all_efo_id = []
    with open(disease_data, 'r', encoding='utf-8') as indata:
        # title = indata.readline()
        for line in indata:
            line_list = line.strip().split()
            if line_list[2] == 'EFO':
                efo_id = line_list[3]
                all_efo_id.append([line_list[0],line_list[1],efo_id])
    return(all_efo_id)

def threading_crawler(efo):
    sema.acquire()
    efo_id = efo[-1]
    url = 'https://www.ebi.ac.uk/ols/ontologies/EFO/terms?iri=http%3A%2F%2Fwww.ebi.ac.uk%2Fefo%2F' + efo_id
    html = download_html(url)
    time.sleep(random.randrange(1,3))
    tag = get_description(html)
    desc = re_desc(tag)
    line = efo + [desc]
    with lock: #添加全局锁防止多线程同时操作同一个文件出现问题
        with open('efo_annotation/efo_annotation','a',encoding='utf-8')as odata:
            odata.write('\t'.join(line) + '\n')
        print('finished:{}'.format(efo))
    sema.release()
def main():
    urls = make_urls()
    i = 0
    for efo in urls:
        i += 1
        if i > 0:
            threading.Thread(target=threading_crawler,args=(efo,)).start()


if __name__ == '__main__':
    main()
    # url = 'https://www.ebi.ac.uk/ols/ontologies/EFO/terms?iri=http%3A%2F%2Fwww.ebi.ac.uk%2Fefo%2FEFO_1000954'
    # url = 'https://www.ebi.ac.uk/ols/ontologies/EFO/terms?iri=http%3A%2F%2Fwww.ebi.ac.uk%2Fefo%2FEFO_1001255'
    # url = "https://www.ebi.ac.uk/ols/ontologies/EFO/terms?iri=http%3A%2F%2Fwww.ebi.ac.uk%2Fefo%2F" + efo_id
    # html = download_html(url)
    # with open('efo_test.html','w',encoding='utf-8') as odata:
    #     odata.write(html)
    # tag = get_description(html)
    # desc = re_desc(tag)
    # print(desc)   # efo_id = 'EFO_0003033'
    # efo_id = 'EFO_1001009'
    # all_efos = make_urls()
    # print(len(all_efos))