#Translation of disease discription by baidu api 
#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
A python translation scripts according to the Baidu Fanyi API.
"""
import sys
import json
import hashlib
import random
import requests

def dataConfig(queryString):
    data = {}

    # appid = '20180210000122126'
    # secretKey = 'kDUsUVdbd25gWfpXyobS'
    appid = '20180210000122125'
    secretKey = 'eH86rX8rzVE4Hnz8E920'
    salt = str(random.randint(32768, 65536))
    sign = hashlib.md5((appid + queryString + salt + secretKey).encode("utf-8")).hexdigest()

    data['q'] = queryString
    data['appid'] = appid
    data['secretKey'] = secretKey
    data['salt'] = salt
    data['sign'] = sign
    data['salt'] = salt
    data['from'] = 'auto'
    data['to'] = 'auto'

    return data


def searchQuery(data):

    BaseURL = 'http://api.fanyi.baidu.com/api/trans/vip/translate?'
    try:
        response = requests.post(BaseURL, data=data)
        result = json.loads(response.text)
        # print result
        if 'error_code' in result:
            print('ErrorCode: ' + result['error_code'])
        else:
            print(result['trans_result'][0]['dst'])
            # print(result)
            return(result['trans_result'][0]['dst'])
    except Exception as e:
        print(e)


def main(queryString):

    data = dataConfig(queryString)
    result = searchQuery(data)
    return(result)

if __name__ == "__main__":

    # if len(sys.argv) < 2:
    #     print('Usage: python %s <queryString>' % sys.argv[0])
    #     exit(1)
    en_words = 'KRT6A	The protein encoded by this gene is a member of the keratin gene family. The type II cytokeratins consist of basic or neutral proteins which are arranged in pairs of heterotypic keratin chains coexpressed during differentiation of simple and stratified epithelial tissues. As many as six of this type II cytokeratin (KRT6) have been identified; the multiplicity of the genes is attributed to successive gene duplication events. The genes are expressed with family members KRT16 and/or KRT17 in the filiform papillae of the tongue, the stratified epithelial lining of oral mucosa and esophagus, the outer root sheath of hair follicles, and the glandular epithelia. This KRT6 gene in particular encodes the most abundant isoform. Mutations in these genes have been associated with pachyonychia congenita. In addition, peptides from the C-terminal region of the protein have antimicrobial activity against bacterial pathogens. The type II cytokeratins are clustered in a region of chromosome 12q12-q13. [provided by RefSeq, Oct 2014].'
    # en_words = input('input words: ')
    queryString = en_words
    # queryString = sys.argv[1]
    result = main(queryString)
    print(result)
    # with open("code_test",'w',encoding='utf-8') as odata:
    #     odata.write(result)
