网站信息爬取与百度翻译api
===

从[Experimental Factor Ontology](https://www.ebi.ac.uk/efo/)网站爬取疾病信息并使用百度api进行翻译
---
## 项目亮点

本项目从文件中提取EFO编号并拼成URL，然后使用这些URL去爬取网页html并提取所需信息。<br>
为了能够快速稳定的爬取网页的基本信息，本项目采用了如下技巧：<br>
* 爬虫浏览器伪装
* 爬虫超时防假死设置
* 爬虫超时重试
* 爬虫代理
    * 代理IP爬取
    * 低延迟IP过滤
* 多线程爬取
    * 通过信号量设置线程数
    * 设置全局锁
* 百度翻译api(账号目前还可使用)

其中爬虫代理和翻译的功能均以模块导入的方式在主流程中执行，你可以下载代理和百度翻译<br>
api的脚本直接用于自己的脚本。即使你想要爬取的网站并不是该网站，你依旧可以从中得到<br>
很多启发。
## 文件说明
 * python执行脚本
    * [proxy_for_crawler.py](https://github.com/KingCM/crawling-python/blob/master/proxy_for_crawler.py)  代理脚本
    * [baidufanyiapi.py](https://github.com/KingCM/crawling-python/blob/master/baidufanyiapi.py)  百度翻译api脚本
    * [efo_crawler.py](https://github.com/KingCM/crawling-python/blob/master/efo_crawler.py)  爬取疾病描述信息脚本
    * [efo_translation.py](https://github.com/KingCM/crawling-python/blob/master/efo_translation.py)  翻译脚本
 * 项目相关文件
    * [disease_mappings.tsv](https://github.com/KingCM/crawling-python/blob/master/disease_mappings.tsv)  包含EFO编号的起始文件
    * [efo_annotation](https://github.com/KingCM/crawling-python/blob/master/efo_annotation)  爬取的疾病描述信息
    * [efo_translation](https://github.com/KingCM/crawling-python/blob/master/efo_translation)  翻译结果文件

        欢迎你对该代码的进一步改进和建议