import matplotlib.pyplot as plt
import wordcloud
import urllib3
import jieba
import time
import re
import os

def getHtml(url):
    pool = urllib3.PoolManager()
    homepageRes = pool.request("GET",url)
    headlineURLRegular  = re.findall("\"(.*?)\"",re.search("<h1 class=\"fbold\" id=\"rm_topline\"><a href=\"(.*?)\"",homepageRes.data.decode("gb2312")).group())
    print("解析到头条文章链接：" + headlineURLRegular[2])
    headlineResRegular = pool.request("GET",headlineURLRegular[2])
    headLineHTMLStr = headlineResRegular.data.decode("gbk")
    headLineHTMLStr.encode()#转utf-8
    return headLineHTMLStr

def fixText(text):
    text = text.replace("<p>","")
    text = text.replace("</p>","")
    text = text.replace("</p>","")
    text = text.replace("<strong>","")
    text = text.replace("</strong>","")
    text = text.replace("<p style=\"text-indent: 2em;\">","")
    text = text.replace("<p style=\"text-align: center;\">","")
    text = text.replace("<script src=\"http://tv.people.com.cn/img/player/v.js\"></script><script>showPlayer({id:\"/pvservice/xml/2022/10/13/91067ddb-857a-4bcc-b6e4-c9323326c7d5.xml\",width:640,height:360,skin:2});</script>","")
    return text

def showWordCloud():
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
    if "\n" in wordDic.keys():
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

cycleCount = 0
while cycleCount != 3:
    headlineLines = re.findall("(.*?)\n",getHtml("http://www.people.com.cn/"))
    with open("all.txt",mode="a",encoding="utf-8") as globalWordsFile:
        with open(time.strftime("%Y-%m-%d") + ".txt",mode="a",encoding="utf-8") as file:
            singnal = 0
            for line in headlineLines:
                line += '\n'
                line = fixText(line)
                if "<div class=\"box_pic\"></div>" in line:
                    singnal = 1
                    continue
                if singnal == 1:
                    if "<div class=\"zdfy clearfix\"></div><center><table border=\"0\" align=\"center\" width=\"40%\"><tr></tr></table></center>" in line:
                        singnal = 0
                        break
                    file.write(line)
                    globalWordsFile.write(line)
    showWordCloud()

    print("see you net day.")
    while not time.strftime("%H:%M:%S") == "20:00:00" or input() == "n":
        time.sleep(100)
    cycleCount += 1
