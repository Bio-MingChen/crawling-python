#efo translation with baidu api

import baidufanyiapi

with open('efo_annotation/efo_annotation','r',encoding='utf-8') as indata,\
    open('efo_annotation/efo_translation','w',encoding='utf-8') as odata:
    title = 'diseaseID\tdiseaseName\tEFO\tdescription\tdescription_ch\n'
    odata.write(title)
    counter = 0
    for line in indata:
        line_list = line.strip().split('\t')
        counter += 1
        # if counter == 5:
        #     print(line_list)
        #     break
        if len(line_list) > 3:
            desc = line_list[3]
            desc_ch = baidufanyiapi.main(desc)
            line_list.append(desc_ch)
            odata.write('\t'.join(line_list)+'\n')
        else:
            desc = '.'
            desc_ch = '.'
            line_list.append(desc)
            line_list.append(desc_ch)
            odata.write('\t'.join(line_list)+'\n')
            


