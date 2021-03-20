# encoding:utf-8

import csv
import jieba
import jieba.posseg as pseg
import re


def tinyproc(word: str, line: list):
    # 先把当前处理条目的名字加入词表
    jieba.add_word(word)
    # 通过正则表达式将提到别名的第一个句段提取出来,存在biemingline
    test_pa = re.compile(u"[?:又|俗|别|简|称][?:为|名|称|叫][\uff1a]*([\u3001]*[\u4e00-\u9fa5]+[\u3001]*){1,9}")
    try:
        biemingline = re.search('[^?:又|俗|别|简|称][^?:为|名|称|叫][\uff1a]*(.+)[\u3001]*', test_pa.search(line)[0]).group(0).split('、')
    except (TypeError, AttributeError):
        biemingline = []

    # 别名处理再放送
    lent = len(biemingline) - 1
    if lent >= 0:
        if re.search(u'[为名称叫][\uff1a]*', biemingline[0]):
            biemingline[0] = biemingline[0].replace(re.findall(u'[为名称叫][\uff1a]*', biemingline[0])[0], '')
        if re.search(u'[等][\u3001\u3002\uff0c]*$', biemingline[lent]):
            biemingline[lent] = biemingline[lent].replace(re.findall(u'[等][\u3001\u3002\uff0c]*$', biemingline[lent])[0], '')

    # 通过另一个正则提取所有提到别名的句子中的别名，只能提取每个句子出现的第一个别名。别问为什么要提两次，菜
    pattern = re.compile(u"[?:又|俗|别|简|称][?:为|名|称|叫][\uff1a]{0,1}([\u201c\u201d]{0,1}[\u4e00-\u9fa5]+[\u201c\u201d]{0,1})+[\u3001\u3002\uff0c]{1}")
    listo = pattern.findall(line, re.M)
    for item in listo:
        if item not in biemingline:
            biemingline.append(item)

    if len(biemingline) > 0:
        biemingline = list(set(biemingline))


    # jieba切分提取地名
    words = pseg.cut(line)
    ns_list = []
    for w in words:
        #分布表填充
        if w.flag == 'ns':
            ns_list.append(w.word)

    return([biemingline,ns_list])


with open('file.csv','r',encoding='utf-8') as r:
    reader = csv.reader(r)
    rows = [row[1:4] for row in reader]

for i in range(1, len(rows)):
    rows[i][1] = rows[i][1].split()[1]
    rows[i].append(tinyproc(rows[i][1], rows[i][2])[0])
    rows[i].append(tinyproc(rows[i][1], rows[i][2])[1])

with open('output.csv','w',newline='', encoding='utf-8-sig') as t:
    csv_write = csv.writer(t, delimiter=',', lineterminator='\n')
    csv_write.writerows(rows)
    print('write over')



