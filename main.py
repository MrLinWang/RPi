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
import numpy as np
import json
import gzip
import calendar

EPD_WIDTH = 640
EPD_HEIGHT = 384

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


def weather():
    #获取天气情况
    #cityname = input('你想查询的城市?\n')
    cityname = '石家庄'

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
    elif weather_dict.get('desc') =='OK' :
        forecast = weather_dict.get('data').get('forecast')

        today1 = '温度:'+weather_dict.get('data').get('wendu') + '℃\n' \
                +'高温:'+forecast[0].get('high')[3:] + '\n' \
                +'低温:'+forecast[0].get('low')[3:] + '\n'

        today2 = '风向:'+forecast[0].get('fengxiang') +'\n'\
                +'风力:'+forecast[0].get('fengli')[9:12] + '\n'\
                +'天气:'+forecast[0].get('type') + '\n'

        one_day = forecast[1].get('date')+'   '\
                +'天气:'+forecast[1].get('type')+'   '\
                +'高温:'+forecast[1].get('high')[3:]+'   '\
                +'低温:'+forecast[1].get('low')[3:]+'   '\
                +'风向:'+forecast[1].get('fengxiang')+'   '\
                +'风力:'+forecast[1].get('fengli')[9:12]+'   '

        two_day = forecast[2].get('date') + '   ' \
                +'天气:' + forecast[2].get('type') + '   ' \
                + '高温:' + forecast[2].get('high')[3:] + '   ' \
                + '低温:' + forecast[2].get('low')[3:] + '   ' \
                + '风向:' + forecast[2].get('fengxiang') + '   ' \
                + '风力:' + forecast[2].get('fengli')[9:12] + '   '
    
        three_day = forecast[3].get('date') + '   ' \
                + '天气:' + forecast[3].get('type') + '   ' \
                + '高温:' + forecast[3].get('high')[3:] + '   ' \
                + '低温:' + forecast[3].get('low')[3:] + '   ' \
                + '风向:' + forecast[3].get('fengxiang') + '   ' \
                + '风力:' + forecast[3].get('fengli')[9:12] + '   '

        four_day = forecast[4].get('date') + '   ' \
                + '天气:' + forecast[4].get('type') + '   ' \
                + '高温:' + forecast[4].get('high')[3:] + '   ' \
                + '低温:' + forecast[4].get('low')[3:] + '   ' \
                + '风向:' + forecast[4].get('fengxiang') + '   ' \
                + '风力:' + forecast[4].get('fengli')[9:12] + '   '


        hightem = [1,2,3,4,5]
        lowtem = [1,2,3,4,5]
        date = [1,2,3,4,5]
        for i in range(0,5):
            hightem[i] = int(forecast[i].get('high')[3:5])
            lowtem[i] = int(forecast[i].get('low')[3:5])
            date[i] = int(forecast[i].get('date')[:-4])

        WF = {"city":cityname,"today1":today1,"today2":today2,"oneday":one_day,\
                "twoday":two_day,"threeday":three_day,"fourday":four_day,\
                "hightem":hightem,"lowtem":lowtem,"date":date,"weather_dict":weather_dict}
    return WF

def refresh():
    #刷新内容
    epd = epd7in5b.EPD()
    epd.init()

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
    str_year = time.strftime('%Y年%m月%d日', time.localtime(time.time()))
    font = ImageFont.truetype('fonts/msyh.ttc', 23)
    draw_black.text((15, 15), str_year, font = font, fill = 0)
    #str_date = time.strftime('%m月%d日', time.localtime(time.time()))
    #font = ImageFont.truetype('fonts/msyhbd.ttc', 40)
    #draw_black.text((25, 55), str_date, font = font, fill = 0)

    #时间
    str_time = time.strftime('%H:%M', time.localtime(time.time()))
    font = ImageFont.truetype('fonts/msyhbd.ttc', 150)
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
    font = ImageFont.truetype('fonts/msyhbd.ttc', 55)
    draw_black.text((17, 35), str_week, font = font, fill = 0)

    #天气
    WF = weather()
    #today
    str_city = WF["city"] + ' ' + "今日天气"
    font = ImageFont.truetype('fonts/msyhbd.ttc', 20)
    draw_black.text((245, 5), str_city, font = font, fill = 0)
    str_tdweather1 = WF["today1"]
    font = ImageFont.truetype('fonts/msyh.ttc', 20)
    draw_black.text((215, 33), str_tdweather1, font = font, fill = 0)
    str_tdweather2 = WF["today2"]
    draw_black.text((315, 33), str_tdweather2, font = font, fill = 0)
    #1234_day
    font = ImageFont.truetype('fonts/msyhl.ttc', 15)
    draw_black.text((50, 290), WF["oneday"], font = font, fill = 0)
    draw_black.text((50, 310), WF["twoday"], font = font, fill = 0)
    draw_black.text((50, 330), WF["threeday"], font = font, fill = 0)
    draw_black.text((50, 350), WF["fourday"], font = font, fill = 0)

    #日历  #待完善，显示不清
    yy = int(time.strftime('%Y', time.localtime(time.time())))
    mm = int(time.strftime('%m', time.localtime(time.time())))
    str_cal = calendar.month(yy,mm)
    font = ImageFont.truetype('fonts/msyhbd.ttc', 15)
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

    #显示
    epd.display_frame(epd.get_frame_buffer(image_black),epd.get_frame_buffer(image_yellow))

def welcome():
    #显示欢迎语
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

    font = ImageFont.truetype('fonts/msyh.ttc', 100)
    draw_black.text((115, 100), '欢迎使用！', font = font, fill = 0)
    font = ImageFont.truetype('fonts/msyhbd.ttc', 30)
    draw_yellow.text((240,240),'LinWang 制作', font = font, fill = 0)
    draw_black.text((241,241),'LinWang 制作', font = font, fill = 0)

    epd.display_frame(epd.get_frame_buffer(image_black),epd.get_frame_buffer(image_yellow))

    print("进入界面。时间：{}".format(time.strftime('%H:%M:%S', time.localtime(time.time()))))

def drawline(WF):
    #绘制天气高低温折线图
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

def main():
    welcome()
    while(True):
        refresh()
        print("\r最近刷新时间：{}".format(time.strftime('%H:%M:%S', time.localtime(time.time()))),end="")
        time.sleep(300)

if __name__ == '__main__':
    main()
