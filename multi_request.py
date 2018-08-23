#!/user/bin/env python
#coding=utf-8

import requests
import datetime
import time
import threading
import json

class url_request():
    times = []
    error = []
    def req(self,AppID,url):
        myreq=url_request()
        headers = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
                   'content-type': 'application/json',
        payload = { 'a':'b','c':'d'}
        r = requests.post("http://xxxxxx",data=json.dumps(payload),headers=headers)
        print "\n  [%d] code: %d resp: %s \n" % ( AppID,r.status_code,r.text)
        ResponseTime=float(r.elapsed.microseconds)/1000 #获取响应时间，单位ms
        myreq.times.append(ResponseTime) #将响应时间写入数组
        if r.status_code !=200 :
            myreq.error.append("0")

if __name__=='__main__':
    myreq=url_request()
    threads = []
    starttime = datetime.datetime.now()
    print "request start time %s" %starttime 
    nub = 5#设置并发线程数
    ThinkTime = 0.01#设置思考时间
    for i in range(1, nub+1): 
        t = threading.Thread(target=myreq.req, args=(i,'http://m.ctrip.com/webapp/cpage/#mypoints'))
        threads.append(t)
    for t in threads:
        time.sleep(ThinkTime) 
        #print "thread %s" %t #打印线程
        t.setDaemon(True)
        t.start()
    t.join()
    endtime = datetime.datetime.now()
    print "request end time %s" %endtime  
    time.sleep(3)
    AverageTime = "{:.3f}".format(float(sum(myreq.times))/float(len(myreq.times))) #计算数组的平均值，保留3位小数
    print "Average Response Time %s ms" %AverageTime #打印平均响应时间
    usetime = str(endtime - starttime)
    hour = usetime.split(':').pop(0)
    minute = usetime.split(':').pop(1)
    second = usetime.split(':').pop(2)
    totaltime = float(hour)*60*60 + float(minute)*60 + float(second) #计算总的思考时间+请求时间
    print "Concurrent processing %s" %nub #打印并发数
    print "use total time %s s" %(totaltime-float(nub*ThinkTime)) #打印总共消耗的时间
    print "fail request %s" %myreq.error.count("0") #打印错误请求数

