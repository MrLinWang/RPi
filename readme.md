电子墨水屏+树莓派制作天气时钟
================
开发环境：
-----
硬件：
-----
1.树莓派3B+  
2.微雪7.5inch e-Paper HAT (C) 带驱动板  

接线：
-----
  EPD    =>    Raspberry Pi
* VCC    ->    3.3
* GND    ->    GND
* DIN    ->    MOSI
* CLK    ->    SCLK
* CS     ->    24 (Physical, BCM: CE0, 8)
* D/C    ->    22 (Physical, BCM: 25)
* RES    ->    11 (Physical, BCM: 17)
* BUSY   ->    18 (Physical, BCM: 24)



软件：
-----
系统：
RASPBIAN STRETCH WITH DESKTOP
Version:June 2018
Release date:2018-06-27
Kernel version:4.14  

开发环境请先依照微雪百科  
http://www.waveshare.net/wiki/Pioneer600_Datasheets  
上步骤进行配置，写的比较详细，按照步骤进行即可  

安装以下两个包：  
SPI library of Python
PIL (Python Imaging Library) library

在树莓派上拉取代码：  
<pre><code>git clone https://github.com/MrLinWang/RPi-Epaper.git</code></pre>

执行：
<pre><code>sudo python3 main.py  </code></pre>
命令即可在墨水屏上显示日历、天气等信息。由于此墨水屏刷新速度较慢，故本程序设置为5分钟刷新一次。

在输入运行命令时可添加参数，如输入：
<pre><code>sudo python3 mian.py 1</code></pre>
为横向放置模式  
输入：
<pre><code>sudo python3 mian.py 2</code></pre>
为竖直放置模式
更多模式可使用：
<pre><code>sudo python3 mian.py help</code></pre>
命令进行查询

声明：
-----
由于本人只是略懂python语言，硬件驱动方面是小白，故本代码主要是以微雪提供的官方示例代码为基础，进行了显示内容的抓取和布置  
<p>
/******************************************************************************
 * File Name          : readme.txt
 * Description        : Readme file
 * Date               : July-28-2017
 ******************************************************************************
 *
 * Copyright (c) 2017 Waveshare
 * All rights reserved.
 *
 * THIS SOFTWARE IS PROVIDED BY COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS, IMPLIED OR STATUTORY WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NON-INFRINGEMENT OF THIRD PARTY INTELLECTUAL PROPERTY
 * RIGHTS ARE DISCLAIMED TO THE FULLEST EXTENT PERMITTED BY LAW. IN NO EVENT
 * SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
 * OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 ******************************************************************************

  == Development Environment ==
  * OS: Raspbian for Raspberry Pi
  * Libraries required:
        SPI library of Python
        PIL (Python Imaging Library) library

  == Raspberry Pi GPIO Pin map ==  
 +-----+-----+---------+------+---+---Pi >3---+---+------+---------+-----+-----+  
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |  
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+  
 |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |  
 |   2 |   8 |   SDA.1 |   IN | 1 |  3 || 4  |   |      | 5v      |     |     |  
 |   3 |   9 |   SCL.1 |   IN | 1 |  5 || 6  |   |      | 0v      |     |     |  
 |   4 |   7 | GPIO. 7 |   IN | 1 |  7 || 8  | 1 | ALT5 | TxD     | 15  | 14  |  
 |     |     |      0v |      |   |  9 || 10 | 1 | ALT5 | RxD     | 16  | 15  |  
 |  17 |   0 | GPIO. 0 |   IN | 0 | 11 || 12 | 0 | IN   | GPIO. 1 | 1   | 18  |  
 |  27 |   2 | GPIO. 2 |   IN | 0 | 13 || 14 |   |      | 0v      |     |     |  
 |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |  
 |     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |  
 |  10 |  12 |    MOSI | ALT0 | 0 | 19 || 20 |   |      | 0v      |     |     |  
 |   9 |  13 |    MISO | ALT0 | 0 | 21 || 22 | 0 | IN   | GPIO. 6 | 6   | 25  |  
 |  11 |  14 |    SCLK | ALT0 | 0 | 23 || 24 | 1 | OUT  | CE0     | 10  | 8   |  
 |     |     |      0v |      |   | 25 || 26 | 1 | OUT  | CE1     | 11  | 7   |  
 |   0 |  30 |   SDA.0 |   IN | 1 | 27 || 28 | 1 | IN   | SCL.0   | 31  | 1   |  
 |   5 |  21 | GPIO.21 |   IN | 1 | 29 || 30 |   |      | 0v      |     |     |  
 |   6 |  22 | GPIO.22 |   IN | 1 | 31 || 32 | 0 | IN   | GPIO.26 | 26  | 12  |  
 |  13 |  23 | GPIO.23 |   IN | 0 | 33 || 34 |   |      | 0v      |     |     |  
 |  19 |  24 | GPIO.24 |  OUT | 1 | 35 || 36 | 1 | OUT  | GPIO.27 | 27  | 16  |  
 |  26 |  25 | GPIO.25 |   IN | 0 | 37 || 38 | 0 | IN   | GPIO.28 | 28  | 20  |  
 |     |     |      0v |      |   | 39 || 40 | 0 | IN   | GPIO.29 | 29  | 21  |  
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+  
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |  
 +-----+-----+---------+------+---+---Pi 3---+---+------+---------+-----+-----+  

  == Hardware connection ==
    EPD    =>    Raspberry Pi
  * VCC    ->    3.3
  * GND    ->    GND
  * DIN    ->    MOSI
  * CLK    ->    SCLK
  * CS     ->    24 (Physical, BCM: CE0, 8)
  * D/C    ->    22 (Physical, BCM: 25)
  * RES    ->    11 (Physical, BCM: 17)
  * BUSY   ->    18 (Physical, BCM: 24)

  == How to use ==
  1, install the Python libraries.
  2, change the current directory to where the demo files located.
  3, run the demo with:
     python main.py

  */
  </p>
