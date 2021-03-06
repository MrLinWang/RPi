##
 #  @filename   :   main.cpp
 #  @brief      :   7.5inch e-paper display demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     July 28 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

import epd7in5b
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import time
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import urllib.request
import jieba
import numpy as np
import json
import gzip
import calendar
import sys
import socket
import struct
import fcntl


EPD_WIDTH = 640
EPD_HEIGHT = 384

#字体地址
Font_bd = 'fonts/msyhbd.ttc'
Font_l = 'fonts/msyhl.ttc'
Font = 'fonts/msyh.ttc'

Info = {"date":0}

def strB2Q(ustring):#半角转全角函数  #后面文字显示需对齐时使用
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 32:    
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:    
            inside_code += 65248
 
        rstring += chr(inside_code)
    return rstring

def getcityname():#获取本地位置
    city_info=urllib.request.urlopen( urllib.request.Request('http://pv.sohu.com/cityjson')).read().decode('gb2312')
    city_name = city_info.split('=')[1].split(':')[3].split('"')[1]
    city_name = jieba.lcut(city_name)[-1]

    #处理城市名不正确问题
    #访问的url，其中urllib.parse.quote是将城市名转换为url的组件
    url = 'http://wthrcdn.etouch.cn/weather_mini?city='+urllib.parse.quote(city_name)
    #发出请求并读取到weather_data
    weather_data = urllib.request.urlopen(url).read()
    #以utf-8的编码方式解压数据
    weather_data = gzip.decompress(weather_data).decode('utf-8')
    #将json数据转化为dict数据
    weather_dict = json.loads(weather_data)
    #print(weather_dict)

    #
    if weather_dict.get('desc') == 'invilad-citykey':
        with open('cityname.txt', 'r',encoding='utf-8') as f:
            city_name = f.readline().rstrip('\n')
    elif weather_dict.get('desc') =='OK' :
        with open('cityname.txt', 'w',encoding='utf-8') as f:
            f.write(city_name)

    return city_name

def weather():#获取天气情况
    #cityname = input('你想查询的城市?\n')
    #cityname = '石家庄'
    cityname = getcityname()

    #访问的url，其中urllib.parse.quote是将城市名转换为url的组件
    url = 'http://wthrcdn.etouch.cn/weather_mini?city='+urllib.parse.quote(cityname)
    #发出请求并读取到weather_data
    weather_data = urllib.request.urlopen(url).read()
    #以utf-8的编码方式解压数据
    weather_data = gzip.decompress(weather_data).decode('utf-8')
    #将json数据转化为dict数据
    weather_dict = json.loads(weather_data)
    #print(weather_dict)
    if weather_dict.get('desc') == 'invilad-citykey':
        print("错误！输入的城市名有误！")
        WF = {"city":cityname,"today1":"null","today2":"null","oneday":"null",\
                "twoday":"null","threeday":"null","fourday":"null",\
                "hightem":"null","lowtem":"null","date":"null","weather_dict":weather_dict}
        return WF
    elif weather_dict.get('desc') =='OK' :
        forecast = weather_dict.get('data').get('forecast')

        today1 = '温度:'+weather_dict.get('data').get('wendu') + '℃\n' \
                +'高温:'+forecast[0].get('high')[3:] + '\n' \
                +'低温:'+forecast[0].get('low')[3:] + '\n'

        today2 = '风向:'+forecast[0].get('fengxiang') +'\n'\
                +'风力:'+forecast[0].get('fengli')[9:-3] + '\n'\
                +'天气:'+forecast[0].get('type') + '\n'

        one_day = forecast[1].get('date')+'   '\
                +'天气:'+forecast[1].get('type')+'   '\
                +'高温:'+forecast[1].get('high')[3:]+'   '\
                +'低温:'+forecast[1].get('low')[3:]+'   '\
                +'风向:'+forecast[1].get('fengxiang')+'   '\
                +'风力:'+forecast[1].get('fengli')[9:-3]+'   '

        two_day = forecast[2].get('date') + '   ' \
                +'天气:' + forecast[2].get('type') + '   ' \
                + '高温:' + forecast[2].get('high')[3:] + '   ' \
                + '低温:' + forecast[2].get('low')[3:] + '   ' \
                + '风向:' + forecast[2].get('fengxiang') + '   ' \
                + '风力:' + forecast[2].get('fengli')[9:-3] + '   '
    
        three_day = forecast[3].get('date') + '   ' \
                + '天气:' + forecast[3].get('type') + '   ' \
                + '高温:' + forecast[3].get('high')[3:] + '   ' \
                + '低温:' + forecast[3].get('low')[3:] + '   ' \
                + '风向:' + forecast[3].get('fengxiang') + '   ' \
                + '风力:' + forecast[3].get('fengli')[9:-3] + '   '

        four_day = forecast[4].get('date') + '   ' \
                + '天气:' + forecast[4].get('type') + '   ' \
                + '高温:' + forecast[4].get('high')[3:] + '   ' \
                + '低温:' + forecast[4].get('low')[3:] + '   ' \
                + '风向:' + forecast[4].get('fengxiang') + '   ' \
                + '风力:' + forecast[4].get('fengli')[9:-3] + '   '


        #hightem = [1,2,3,4,5]
        #lowtem = [1,2,3,4,5]
        date = [1,2,3,4,5]
        for i in range(0,5):
        #   hightem[i] = int(forecast[i].get('high')[3:5])
        #    lowtem[i] = int(forecast[i].get('low')[3:5])
            date[i] = int(forecast[i].get('date')[:-4])

        WF = {"city":cityname,"today1":today1,"today2":today2,"oneday":one_day,\
                "twoday":two_day,"threeday":three_day,"fourday":four_day,\
                "hightem":0,"lowtem":0,"date":date,"weather_dict":weather_dict}
    return WF

def rotateimage(image,angle,width,height):#图像无裁剪旋转函数#有bug
    if width > height:
        size = width
    else:
        size = height
    image_tem = Image.new('1', (size, size), 255)
    image_tem.paste(image,(0,0))
    image_tem = image_tem.rotate(angle)
    box=(0,0,height,width)
    image_tem = image_tem.crop(box)
    return image_tem

def getinfo(Info):#获取/更新显示信息

    datenow = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    if datenow!=Info["date"]:
        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        #日期
        str_year = time.strftime('%Y年%m月%d日', time.localtime(time.time()))

        #时间
        str_time = time.strftime('%H:%M', time.localtime(time.time()))

        #星期
        week = time.strftime('%w', time.localtime(time.time()))
        if week == '0':
            str_week = '星期日'
        elif week == '1':
            str_week = '星期一'
        elif week == '2':
            str_week = '星期二'
        elif week == '3':
            str_week = '星期三'
        elif week == '4':
            str_week = '星期四'
        elif week == '5':
            str_week = '星期五'
        elif week == '6':
            str_week = '星期六'
        else:
            str_week = 'error!'

        #天气
        WF = weather()
        #today
        str_city = WF["city"] +" "+ "今日天气"
        str_tdweather1 = WF["today1"]
        str_tdweather2 = WF["today2"]
        #1234_day
        str_oneday = WF["oneday"]
        str_twoday = WF["twoday"]
        str_threeday = WF["threeday"]
        str_fourday = WF["fourday"]

        #日历
        yy = int(time.strftime('%Y', time.localtime(time.time())))
        mm = int(time.strftime('%m', time.localtime(time.time())))
        str_cal = calendar.month(yy,mm)
        str_B2Qcal = strB2Q(str_cal)

        Info["date"] = date
        Info["year"] = str_year
        Info["time"] = str_time
        Info["week"] = str_week
        Info["city"] = str_city
        Info["td1"] = str_tdweather1
        Info["td2"] = str_tdweather2
        Info["oneday"] = str_oneday
        Info["twoday"] = str_twoday
        Info["threeday"] = str_threeday
        Info["fourday"] = str_fourday
        Info["cal"] = str_B2Qcal
        #Info{"date":date,"year":str_year,"time":str_time,"week":str_week,"city":str_city,"td1":str_tdweather1,\
        #    "td2":str_tdweather2,"oneday":str_oneday,"twoday":str_twoday,"threeday":str_threeday,"fourday":str_fourday,\
        #    "cal":str_B2Qcal}
    else:
        #时间
        str_time = time.strftime('%H:%M', time.localtime(time.time()))
        Info["time"] = str_time
    return Info

def refresh(reverse = False):#刷新内容
    epd = epd7in5b.EPD()
    epd.init()

    info = getinfo(Info)

    # For simplicity, the arguments are explicit numerical coordinates
    image_yellow = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)    # 255: clear the frame
    draw_yellow = ImageDraw.Draw(image_yellow)
    image_black = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)    # 255: clear the frame
    draw_black = ImageDraw.Draw(image_black)
    draw_yellow.line((0,115,640,115),fill=0,width=4)#上横线
    draw_yellow.line((200,0,200,115),fill=0,width=3)#上左竖线
    draw_yellow.line((430,0,430,115),fill=0,width=3)#上右竖线
    draw_yellow.line((0,280,640,280),fill=0,width=5)#下横线
    #font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 24)
    #draw_yellow.rectangle((0, 0, 640, 40), fill = 255)
    #draw_yellow.text((150, 10), 'e-Paper demo for LinWang', font = font, fill = 0)
    #draw_yellow.rectangle((0, 45, 640, 85), fill = 0)
    #draw_red.rectangle((200, 80, 600, 280), fill = 0)
    #draw_red.chord((240, 120, 580, 220), 0, 360, fill = 255)
    #draw_black.rectangle((20, 80, 160, 280), fill = 0)
    #draw_red.chord((40, 80, 180, 220), 0, 360, fill = 0)

    #日期
    #str_year = time.strftime('%Y年%m月%d日', time.localtime(time.time()))
    str_year = info["year"]
    font = ImageFont.truetype(Font, 23)
    draw_black.text((15, 15), str_year, font = font, fill = 0)
    #str_date = time.strftime('%m月%d日', time.localtime(time.time()))
    #font = ImageFont.truetype('fonts/msyhbd.ttc', 40)
    #draw_black.text((25, 55), str_date, font = font, fill = 0)

    #时间
    #str_time = time.strftime('%H:%M', time.localtime(time.time()))
    str_time = info["time"]
    font = ImageFont.truetype(Font_bd, 150)
    draw_black.text((110, 95), str_time, font = font, fill = 0)
    draw_yellow.text((108, 93), str_time, font = font, fill = 0)

    #时间+
    #str_time = time.strftime('%H:%M', time.localtime(time.time()))
    #font = ImageFont.truetype('fonts/msyhbd.ttc', 150)
    #x=30
    #y=95
    #draw_black.text((x, y), str_time, font = font, fill = 0)
    #draw_yellow.text((x-2, y-2), str_time, font = font, fill = 0)
    #draw_yellow.line((470,115,470,280),fill=0,width=4)#中右竖线

    #星期
    #week = time.strftime('%w', time.localtime(time.time()))
    #if week == '0':
    #    str_week = '星期日'
    #elif week == '1':
    #    str_week = '星期一'
    #elif week == '2':
    #    str_week = '星期二'
    #elif week == '3':
    #    str_week = '星期三'
    #elif week == '4':
    #    str_week = '星期四'
    #elif week == '5':
    #    str_week = '星期五'
    #elif week == '6':
    #    str_week = '星期六'
    #else:
    #    str_week = 'error!'
    str_week = info["week"]
    font = ImageFont.truetype(Font_bd, 55)
    draw_black.text((17, 35), str_week, font = font, fill = 0)

    #天气
    #WF = weather()
    #today
    #str_city = WF["city"] +" "+ "今日天气"
    str_city = info["city"]
    font = ImageFont.truetype(Font_bd, 20)
    draw_black.text((230, 5), str_city, font = font, fill = 0)
    #str_tdweather1 = WF["today1"]
    str_tdweather1 = info["td1"]
    font = ImageFont.truetype(Font, 20)
    draw_black.text((215, 33), str_tdweather1, font = font, fill = 0)
    #str_tdweather2 = WF["today2"]
    str_tdweather2 = info["td2"]
    draw_black.text((315, 33), str_tdweather2, font = font, fill = 0)
    #1234_day
    font = ImageFont.truetype(Font_l, 15)
    #str_oneday = WF["oneday"]
    #str_twoday = WF["twoday"]
    #str_threeday = WF["threeday"]
    #str_fourday = WF["fourday"]
    str_oneday = info["oneday"]
    str_twoday = info["twoday"]
    str_threeday = info["threeday"]
    str_fourday = info["fourday"]
    draw_black.text((50, 290), str_oneday, font = font, fill = 0)
    draw_black.text((50, 310), str_twoday, font = font, fill = 0)
    draw_black.text((50, 330), str_threeday, font = font, fill = 0)
    draw_black.text((50, 350), str_fourday, font = font, fill = 0)

    #日历  #待完善，显示不清
    #yy = int(time.strftime('%Y', time.localtime(time.time())))
    #mm = int(time.strftime('%m', time.localtime(time.time())))
    #str_cal = calendar.month(yy,mm)
    #str_B2Qcal = strB2Q(str_cal)
    str_B2Qcal = info["cal"]
    font = ImageFont.truetype(Font_bd, 15)
    image_cal = Image.new('1', (300, 145), 255)
    draw_cal = ImageDraw.Draw(image_cal)
    draw_cal.text((0,0),str_B2Qcal , font = font, fill = 0)
    image_cal= image_cal.resize((200,110))
    image_black.paste(image_cal,(435,3))
    #font = ImageFont.truetype('fonts/msyhbd.ttc', 10)
    #draw_black.text((445,0), strB2Q(str_cal), font = font, fill = 0)


    #日历  #待完善，显示不清
    yy = int(time.strftime('%Y', time.localtime(time.time())))
    mm = int(time.strftime('%m', time.localtime(time.time())))
    str_cal = calendar.month(yy,mm)
    font = ImageFont.truetype(Font_bd, 15)
    image_cal = Image.new('1', (300, 145), 255)
    draw_cal = ImageDraw.Draw(image_cal)
    draw_cal.text((0,0), strB2Q(str_cal), font = font, fill = 0)
    image_cal= image_cal.resize((200,110))
    image_black.paste(image_cal,(435,3))
    #font = ImageFont.truetype('fonts/msyhbd.ttc', 10)
    #draw_black.text((445,0), strB2Q(str_cal), font = font, fill = 0)


    #天气折线图 hightem.png lowtem.png ##失败！无法清晰显示
    #drawline(WF)
    #png_size = (400,384)
    #png_locate  = (0,250)
    #highim=Image.open('hightem.png')
    #highimg=highim.resize(png_size)
    #image_black.paste(highimg,png_locate)
    #lowim=Image.open('lowtem.png')
    #lowimg=lowim.resize(png_size)
    #image_yellow.paste(lowimg,png_locate)

    #图像翻转
    if reverse == True:
        image_black = image_black.transpose(Image.ROTATE_180)
        image_yellow = image_yellow.transpose(Image.ROTATE_180)


    #显示
    epd.display_frame(epd.get_frame_buffer(image_black),epd.get_frame_buffer(image_yellow))

def refresh1(reverse = False):#刷新内容
    epd = epd7in5b.EPD()
    epd.init()

    info = getinfo(Info)

    EPD_WIDTH = 384
    EPD_HEIGHT = 640

    # For simplicity, the arguments are explicit numerical coordinates
    image_yellow = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)    # 255: clear the frame
    draw_yellow = ImageDraw.Draw(image_yellow)
    image_black = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)    # 255: clear the frame
    draw_black = ImageDraw.Draw(image_black)
    draw_yellow.line((0,90,384,90),fill=0,width=4)#上横线
    draw_yellow.line((190,0,190,90),fill=0,width=3)#上竖线
    draw_yellow.line((0,215,384,215),fill=0,width=4)#上2横线
    draw_yellow.line((0,405,384,405),fill=0,width=4)#下横线
    draw_yellow.line((0,475,384,475),fill=0,width=4)#下横线
    #draw_yellow.line((440,0,440,115),fill=0,width=3)#上右竖线
    #draw_yellow.line((0,280,640,280),fill=0,width=5)#下横线
    

    #日期
    #str_year = time.strftime('%Y年%m月%d日', time.localtime(time.time()))
    str_year = info["year"]
    font = ImageFont.truetype(Font, 20)
    draw_black.text((17, 5), str_year, font = font, fill = 0)


    #时间
    #str_time = time.strftime('%H:%M', time.localtime(time.time()))
    str_time = info["time"]
    font = ImageFont.truetype(Font_bd, 130)
    draw_black.text((15, 65), str_time, font = font, fill = 0)
    draw_yellow.text((13, 63), str_time, font = font, fill = 0)

    #星期
    #week = time.strftime('%w', time.localtime(time.time()))
    #if week == '0':
    #    str_week = '星期日'
    #elif week == '1':
    #    str_week = '星期一'
    #elif week == '2':
    #    str_week = '星期二'
    #elif week == '3':
    #    str_week = '星期三'
    #elif week == '4':
    #    str_week = '星期四'
    #elif week == '5':
    #    str_week = '星期五'
    #elif week == '6':
    #    str_week = '星期六'
    #else:
    #    str_week = 'error!'
    str_week = info["week"]
    font = ImageFont.truetype(Font_bd, 45)
    draw_black.text((25, 25), str_week, font = font, fill = 0)

    #天气
    #WF = weather()
    #today
    #str_city = WF["city"] + ' ' + "今日天气"
    str_city = info["city"]
    font = ImageFont.truetype(Font_bd, 15)
    draw_black.text((220, 5), str_city, font = font, fill = 0)
    #str_tdweather1 = WF["today1"]
    str_tdweather1 = info["td1"]
    font = ImageFont.truetype(Font, 15)
    draw_black.text((210, 25), str_tdweather1, font = font, fill = 0)
    #str_tdweather2 = WF["today2"]
    str_tdweather2 = info["td2"]
    draw_black.text((290, 25), str_tdweather2, font = font, fill = 0)
    #1234——day
    font = ImageFont.truetype(Font, 11)
    #str_oneday = WF["oneday"]
    #str_twoday = WF["twoday"]
    #str_threeday = WF["threeday"]
    #str_fourday = WF["fourday"]
    str_oneday = info["oneday"]
    str_twoday = info["twoday"]
    str_threeday = info["threeday"]
    str_fourday = info["fourday"]
    draw_black.text((5, 410), str_oneday, font = font, fill = 0)
    draw_black.text((5, 425), str_twoday, font = font, fill = 0)
    draw_black.text((5, 440), str_threeday, font = font, fill = 0)
    draw_black.text((5, 455), str_fourday, font = font, fill = 0)


    #日历
    #yy = int(time.strftime('%Y', time.localtime(time.time())))
    #mm = int(time.strftime('%m', time.localtime(time.time())))
    #str_cal = calendar.month(yy,mm)
    #str_B2Qcal = strB2Q(str_cal)
    str_B2Qcal = info["cal"]
    font = ImageFont.truetype(Font_bd, 18)
    draw_black.text((13,220),str_B2Qcal , font = font, fill = 0)


    image_black = rotateimage(image_black,-90,EPD_WIDTH,EPD_HEIGHT)
    image_yellow = rotateimage(image_yellow,-90,EPD_WIDTH,EPD_HEIGHT)
    #图像翻转
    if reverse == True:
        image_black = image_black.transpose(Image.ROTATE_180)
        image_yellow = image_yellow.transpose(Image.ROTATE_180)



    #显示
    epd.display_frame(epd.get_frame_buffer(image_black),epd.get_frame_buffer(image_yellow))

def welcome(reverse = False):#显示欢迎语
    # display images
    #frame_black = epd.get_frame_buffer(Image.open('background.bmp'))
    #frame_yellow = epd.get_frame_buffer(Image.open('NULL.bmp'))
    #epd.display_frame(frame_black,frame_yellow)

    print("欢迎使用！时间：{}".format(time.strftime('%H:%M:%S', time.localtime(time.time()))))

    epd = epd7in5b.EPD()
    epd.init()
    
    image_black = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)    # 255: clear the frame
    draw_black = ImageDraw.Draw(image_black)
    image_yellow = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)    # 255: clear the frame
    draw_yellow = ImageDraw.Draw(image_yellow)

    font = ImageFont.truetype(Font, 100)
    draw_black.text((115, 100), '欢迎使用！', font = font, fill = 0)
    font = ImageFont.truetype(Font_bd, 30)
    draw_yellow.text((240,240),'LinWang 制作', font = font, fill = 0)
    draw_black.text((241,241),'LinWang 制作', font = font, fill = 0)

    #图像翻转
    if reverse == True:
        image_black = image_black.transpose(Image.ROTATE_180)
        image_yellow = image_yellow.transpose(Image.ROTATE_180)

    epd.display_frame(epd.get_frame_buffer(image_black),epd.get_frame_buffer(image_yellow))

    print("进入界面。时间：{}".format(time.strftime('%H:%M:%S', time.localtime(time.time()))))

def get_ip(ifname):#获得本机ip地址
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',bytes(ifname[:15],'utf-8')))[20:24])

def welcome1(reverse = False):#显示欢迎语
    # display images
    #frame_black = epd.get_frame_buffer(Image.open('background.bmp'))
    #frame_yellow = epd.get_frame_buffer(Image.open('NULL.bmp'))
    #epd.display_frame(frame_black,frame_yellow)

    print("欢迎使用！时间：{}".format(time.strftime('%H:%M:%S', time.localtime(time.time()))))

    epd = epd7in5b.EPD()
    epd.init()
    
    image_black = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)    # 255: clear the frame
    draw_black = ImageDraw.Draw(image_black)
    image_yellow = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)    # 255: clear the frame
    draw_yellow = ImageDraw.Draw(image_yellow)

    font = ImageFont.truetype(Font, 80)
    draw_black.text((150, 100), '欢迎使用！', font = font, fill = 0)
    font = ImageFont.truetype(Font_bd, 30)
    draw_yellow.text((220,210),'LinWang 制作', font = font, fill = 0)
    draw_black.text((221,211),'LinWang 制作', font = font, fill = 0)
    
    
    font = ImageFont.truetype(Font, 20)
    wlan0ip = get_ip('wlan0')
    #eth0ip = get_ip('eth0')
    #strip = "wlanIP:" + wlan0ip + "\n" + "eth0IP:" + eth0ip
    #draw_black.text((150,340), strip, font = font, fill = 0)
    draw_black.text((150,340), "IP:" + wlan0ip, font = font, fill = 0)

    image_black = image_black.rotate(-90)
    image_yellow = image_yellow.rotate(-90)
    if reverse == True:
        image_black = image_black.transpose(Image.ROTATE_180)
        image_yellow = image_yellow.transpose(Image.ROTATE_180)

    epd.display_frame(epd.get_frame_buffer(image_black),epd.get_frame_buffer(image_yellow))

    print("进入界面。时间：{}".format(time.strftime('%H:%M:%S', time.localtime(time.time()))))

"""def drawline(WF):#绘制天气高低温折线图
    hightemp = WF["hightem"]
    lowtemp = WF["lowtem"]
    date = WF["date"]

    #matplotlib中文显示问题
    #matplotlib.rcParams['font.family']='SimHei'
    matplotlib.rcParams['font.sans-serif']=['Droid Sans Fallback']

    #找出温度最大最小边界
    high = hightemp[0]
    for i in range(0,5):
        if high < hightemp[i]:
                high = hightemp[i]
    low = lowtemp[0]
    for i in range(0,5):
        if low > lowtemp[i]:
                low = lowtemp[i]
    high = high + 1
    low = low - 1
    temphl =np.arange(low,high+1,1)

    #绘制高温图
    fig1=plt.figure()
    ax1=fig1.add_subplot(111)
    x = date
    y = hightemp
    ax1.set_xticks(x)
    ax1.set_yticks(temphl)
    ax1.set_ylim(low,high)
    ax1.set_xlabel("日期")
    ax1.set_ylabel("温度")
    ax1.plot(x,y,'k',color='k',linewidth=1,linestyle="-")
    #ax1.axis('off')
    fig1.savefig("hightem.png")
    
    #绘制低温图
    fig2=plt.figure()
    ax2=fig2.add_subplot(111)
    x = date
    y = lowtemp
    ax2.set_xticks(x)
    ax2.set_yticks(temphl)
    ax2.set_ylim(low,high)
    ax2.set_xlabel("日期")
    ax2.set_ylabel("温度")
    ax2.plot(x,y,'k',color='k',linewidth=1,linestyle="-")
    ax2.axis('off')
    fig2.savefig("lowtem.png")
    """

def main():
    if len(sys.argv)==1 or sys.argv[1]=='1':
        welcome()
        while(True):
            time_start=time.time()
            refresh()
            time_end=time.time()
            print("\r最近刷新时间：{},刷新耗时：{}秒".format(time.strftime('%H:%M:%S', time.localtime(time_start)),int(time_end-time_start)),end="")
            time.sleep(300)
    elif sys.argv[1]=='2':
        welcome(True)
        while(True):
            time_start=time.time()
            refresh(True)
            time_end=time.time()
            print("\r最近刷新时间：{},刷新耗时：{}秒".format(time.strftime('%H:%M:%S', time.localtime(time_start)),int(time_end-time_start)),end="")
            time.sleep(300)
    elif sys.argv[1]=='3':
        welcome1()
        while(True):
            time_start=time.time()
            refresh1()
            time_end=time.time()
            print("\r最近刷新时间：{},刷新耗时：{}秒".format(time.strftime('%H:%M:%S', time.localtime(time_start)),int(time_end-time_start)),end="")
            time.sleep(300)
    elif sys.argv[1]=='4':
        welcome1(True)
        while(True):
            time_start=time.time()
            refresh1(True)
            time_end=time.time()
            print("\r最近刷新时间：{},刷新耗时：{}秒".format(time.strftime('%H:%M:%S', time.localtime(time_start)),int(time_end-time_start)),end="")
            time.sleep(300)
    elif sys.argv[1]=='test1':
        time_start=time.time()
        refresh()
        time_end=time.time()
        print("刷新耗时：{}秒".format(int(time_end-time_start)))
    elif sys.argv[1]=='test2':
        time_start=time.time()
        refresh(True)
        time_end=time.time()
        print("刷新耗时：{}秒".format(int(time_end-time_start)))
    elif sys.argv[1]=='test3':
        time_start=time.time()
        refresh1()
        time_end=time.time()
        print("刷新耗时：{}秒".format(int(time_end-time_start)))
    elif sys.argv[1]=='test4':
        time_start=time.time()
        refresh1(True)
        time_end=time.time()
        print("刷新耗时：{}秒".format(int(time_end-time_start)))
    else:
        print("参数的作用:\n"\
             +"无参\t横置正向\n"\
             +"1\t横置正向\n"\
             +"2\t横置反向\n"\
             +"3\t竖置正向\n"\
             +"4\t竖置反向\n"\
             +"test1\t测试模式 横置正向\n"\
             +"test2\t测试模式 横置反向\n"\
             +"test3\t测试模式 竖置正向\n"\
             +"test4\t测试模式 竖置反向\n"\
             +"Operation terminates!")



if __name__ == '__main__':
    main()
