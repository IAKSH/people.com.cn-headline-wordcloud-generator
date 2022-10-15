import matplotlib.pyplot as plt
import wordcloud
import urllib3
import jieba
import time
import re
import os

count = 0
while(count < 3):
    pool = urllib3.PoolManager()
    #res = pool.request("GET","https://www.backweb.org.cn/web/202209/15/http://www.people.com.cn/")
    res = pool.request("GET","http://www.people.com.cn/")
    #entrance = re.search("<h1 class=\"fbold\" id=\"rm_topline\"><a href=\"(.*?)\"",res.data.decode())
    entrance = re.search("<h1 class=\"fbold\" id=\"rm_topline\"><a href=\"(.*?)\"",res.data.decode("gb2312"))
    entrance2 = re.findall("\"(.*?)\"",entrance.group())
    print("解析到头条文章链接：" + entrance2[2])

    res2 = pool.request("GET",entrance2[2])
    headLineHTML = res2.data.decode("gbk")
    headLineHTML.encode()#转utf-8

    content = re.findall("<p>\n(.*?)</p>",headLineHTML)# 这里还是不行，它们的html一点都不规范，有时候换行有时候不换，有时候还把p大写
    print(content)
    with open("all.txt",mode="a",encoding="utf-8") as allFile:
        with open(time.strftime('%Y-%m-%d', time.localtime()) + ".txt",mode="a",encoding="utf-8") as file:
            for i in content:
                line = i.replace("&nbsp;&nbsp;","\n").replace("</strong>","").replace("<strong>","").replace("<span id=\"paper_num\">　　","").replace("</span>","").replace("	　　","") + "\n"        
                print("saving line: " + line)
                file.write(line)
                allFile.write(line)
    
    # 生成词云
    # 临时放在这里
    allText = ""
    with open("all.txt",mode="r",encoding="utf-8") as file:
        lines = file.readlines()
        for i in lines:
            allText += i
    
    cuts = jieba.lcut(allText)
    wordDic = {}
    for i in cuts:
        if i in wordDic.keys():
            wordDic[i] += 1
        else:
            wordDic[i] = 0
    wordDic.pop("\n")

    wordList = []
    for i in wordDic:
        j = 0
        while(j < wordDic[i]):
            wordList.append(i)
            j += 1
    
    wordCloudImage = wordcloud.WordCloud(  background_color='white',font_path = 'msyh.ttc', width=1000, height=860, margin=2).generate('/'.join(wordList))

    plt.imshow(wordCloudImage)
    plt.axis('off')
    plt.show()

    print("work done, see you next day.")
    while(True):
        time.sleep(10)
        if time.strftime("%H:%M:%S") == "20:00:00" or input() == "n":
            count += 1
            break

