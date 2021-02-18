## 3.27
1. web页面（前端）与flask服务器（后台）通讯交互修改告一段落，具体修改：两种参数传递方式
   - 响应web的点击事件并通过URL传递参数，实现功能：进行设置，设备切换，等页面的跳转；传递参数指令使设备待命
   - 点击事件不能影响web页面传感器参数实时更新，故而使用socketIO建立B-S通信连接进行web端实时动态刷新
2. 测试microduino模块的通信测试，建立wifi链接，使用microduino语言尝试简单的链接建立反馈，输出到其自带的OLED屏幕
3. 待完善：python后台对于数据库的操作支持。具体功能：
   - Wi-Fi连入后的设备认证【token】，注册【ID】，验证【已存在ID对比】
   - 支持设备注册查看与在线状态监测
4. 需要探索：使用microduino封装好的mqtt接口，通过WI-FI与树莓派进行信息交流

## 4.1
1. 使用mdxly给mCookie编程，进行硬件测试：
   - 实现Wi-Fi自动链接
   - 温湿度传感器获得数据并串口显示。
2. 尝试使用mqtt进行服务器链接，其中mqtt的编程模块部分暂时没有具体的说明书，计划搁置
3. 添加python后台对于数据库的操作支持
   - Wi-Fi连入后的设备认证【token】，注册【ID】，验证【已存在ID对比】

## 4.4
1. 已实现功能：
   - 通过手机等终端接入树莓派热点，访问mSpace控制web，并实现操控
   - mCookie可以自行接入树莓派热点， 
2. 现有问题：
   - 树莓派Wi-Fi GUI消失，只能连接设置好的wifi，会影响接入外网的便捷性
   - 树莓派可以访问外网，但通过其热点无法访问外网，会使接入树莓派热点的使用者无法访问外网
3. 修改原有mCookie与树莓派后台链接方案，tcp代替mqtt
4. mSpace未做完功能：
   1. mCookie与树莓派flask后台通过Wi-Fi使用TCP链接（先建立模拟测试，再使用mCookie做链接测试）
   2. 侦测接入Wi-Fi的mCookie设备，将其注册信息存入mysql数据库，
   3. 从mCookie设备获取传感器数据，并写入数据库
   4. Flask后台通过TCP连接，控制mCookie进行对应操作
   
## 4.8
1. 在Flask后台主进程开使TCP服务器子进程
2. 通过本地IP测试，已实现交互功能

## 4.12
1. 修复flask与tcp server同步启动无法正常使用tcp的BUG
2. 添加tcp server到flask后台的传感器数据实时传输功能，频率3s/次，并且显示到web
3. 修改web界面：去掉多余测试按钮🔘，去掉echo输入框，添加具有滚动条的文本框，以供传感器数据实时显示
4. 出现问题：
   - 用来临时存储数据的FIFO序列出现tcp server子进程无法进行下一循环的情况。应该是逻辑问题，需要重新设计与子进程tcp server的数据交换通道。

## 4.15
1. 配置数据库远程开发环境，设计mSpace传感器节点的数据库
2. 确定传感器节点传递参数为：
	设备ID，设备类型，设备注册状态，设备开关状态，传感器数据
	使用的serversocket得到的数据需要设计字义解析，提取数据存入数据库
3. 使用进程通信,队列multiprocessing.Queue()，进行子进程tcp server与父进程的数据交换任然失败，改为pipe双向通信，又遇到尝试同时读取或写入管道的同一端，管道中的数据可能会损坏的问题，打算使用manage进行数据交换
   
## 4.16
1. 放弃进程间通信的方案，改为线程调用，设置全局共享变量参数，使用队列类型Queue存储全局参数
2. 修复遗留Bug：web实时显示需要使用原来的按钮才能加载显示数据的问题
3. 设计[数据库处理流程图](https://www.processon.com/view/link/5cb68b83e4b06bcc137f2129)

## 4.17
1. 重新设计传感器数据处理流程，改为从TCP得到传感器数据，直接存入数据库，以便多个传感器接入时，数据的存取。具体[架构图](https://www.processon.com/view/link/5cb6d47de4b09b16ffbb5a7d)
2. 传感器数据TCP字段添加“警报”位，并设计在小于3秒的轮询时间内直接通知flask server警报消息，
3. 修改开关控制指令，使其通过TCP立即向传感器端发送指令

## 4.19
1. 将TCP代码和flask代码合并，以便于共用全局共享变量参数
2. 添加“控制”共享变量，完成“警报和控制”共享变量在flask线程与tcp线程之间的共享，使其能够回传控制指令从而控制传感器的开关
3. 完成在tcp线程中，得到数据直接存入数据库；在flask线程中，每3秒就查询一次数据库，每0.5秒监测来自tcp的警报，并且自动显示在web界面上。
4. 进行mysql数据库测试，修复若干bug

## 4.22
1. 添加web界面数据实时显示自动滚动功能
2. 修复flask与tcp服务器之间传输编码的问题
3. 修复偶尔，在每0.5秒监测来自tcp的警报时，无法每3秒将数据自动显示在web界面上的阻塞问题
4. 修复当传感器关闭时数据依然自动显示在web界面上的问题

## 5.7
1. 修复开关按钮无法关闭后再次开启的问题
2. 发现轮询监视线程在重新开启后会重新出现一个线程，正在寻找解决方法
3. 和官祥锦讨论tcp字段结构，确定socket传输编码

## 5.31
### 整理以下修改部分
- 数据库
  1. 将用于本地测试的数据库，改成用于对接的数据库
  2. 数据库加入新设计的一个表，用于长久保留已注册的设备ID与类型
  3. 修改数据库生成逻辑，使得当设备接入树莓派时，新创建一个以设备ID命名的表，以后该设备的数据记录只在这个表中进行操作
  4. 增添数据清空功能，实现关闭该传感器，则清空其对应表的数据
- 网页
  1. 网页前端的开关按钮改为非刷新整个页面的按钮
  2. 将后台主动发送开关信号和警报信号到网页，改为网页定时请求这两者的信号标志
   
## 6.4-6.6
### 数据库部分需重新设计
- 数据库要求
    1. 存储接入注册设备的ID与类型，是否首次接入：注册则直接将数据插入对应表，未注册则创建新表。

        |**设备注册表说明**|设备ID（主键）|设备类型|注册状态|开关状态|警报状态|
        |:---:|:---:|:---:|:---:|:---:|:---:|
        |数据类型|int|string|bool|bool|bool|
        |参数名称|id|name|registered|status|alert|
    2. 不同设备ID对应不同表，存储接入设备实时数据，以便web服务器使用，需按照存入顺序主键进行读取。

        |**数据存取表说明**|存入顺序|数据|
        |:---:|:---:|:---:|:---:|:---:|
        |数据类型|int|float|
        |参数名称|count|data|

## 6.10 6.11
### 数据库要求
- 两个表，设备列表和数据列表
    1. 查询设备列表是否首次接入：已经注册则直接将数据插入对应数据表，未注册则在设备表增加相应新字段，之后在数据表直接插入数据。

        |**设备注册表说明**|设备ID（主键）|设备类型|在线状态|开关控制
        |:---:|:---:|:---:|:---:|:---:|:---:|
        |数据类型|int|string|bool|bool
        |参数名称|id|name|status|switch
    2. 数据表存储设备实时数据，以便web前端访问使用，需按照时间戳进行读取。

        |**数据存取表说明**|设备ID|设备类型|数据时间戳|数据|警报状态|
        |:---:|:---:|:---:|:---:|:---:|:---:|
        |数据类型|int|string|timestamp|float|bool|
        |参数名称|id|name|ctime|data|alert|
- 设备接入，对设备注册表查询id注册状态
- WEB查询设备注册表设备在线状态，根据每一个上线设备的id去设备存取表查询数据，显示在web上
- 将得到的数据存入数据库
- 设备不在线，开关控制设置为开
- [数据流程图](https://www.processon.com/view/link/5cff12cbe4b091a8f23ddb0a)

## 6.19
### 设计测试用例
- 测试注册函数
  - 已注册设备接入：t1
  - 未注册设备接入：t2
- 测试设备注册表增改数据函数
  - 更新在线状态：t1
  - 更新控制状态：t2
- 设备开关控制：t4

## 7.02
### 修改需求数据库
- 3个表，设备列表,数据列表,用户自定映射表
    1. 查询设备列表是否首次接入：已经注册则直接将数据插入对应数据表，未注册则在设备表增加相应新字段，之后在数据表直接插入相应数据。

        |**设备注册表**|设备ID（主键）|设备类型编号|属性个数|在线状态|最后一次心跳时间
        |:---:|:---:|:---:|:---:|:---:|:---:|:---:|
        |参数名称|id|typeid|pnumber|status|htime
        |数据类型|int|int|int|bool|timestamp
    2. 数据表存储设备实时数据和指令，以便web前端访问使用与控制，需按照与设备属性约定的规则执行相应逻辑。

        |**数据存取表**|设备ID|属性编号|数据时间戳|上行数据|下行数据|警报状态|阈值
        |:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
        |参数名称|id|pid|ctime|updata|downdata|alert|threshold
        |数据类型|int|int|timestamp|float|float|bool|float
    3. typeid与propertyID映射表说明（供用户增删改查）
        |**用户自定映射表**|设备类型编号|用户定义类型|属性编号|用户定义属性
        |:---:|:---:|:---:|:---:|:---:|
        |参数名称|typeid|utype|pid|upid|
        |数据类型|int|string|int|string|


- 下位机上传数据格式说明
  - 仅上传id,typeid,pnumber则是心跳模式
  - 上行数据字段格式：
    |**上传数据格式**|设备ID|设备类型编号|属性个数|属性编号|上行数据|警报状态
    |:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
    |参数名称|id|typeid|pnumber|pid|updata|alert|
    |数据类型|int|int|int|int|float|int|


## 7.08
- 修改超时逻辑，在timeout后，直接从设备数据库htime里提取时间，如果时间加上超时设定时长大于现有时间则设备仍是在线状态，若小于则离线。
- 上位机下传指令数据格式说明：
    |**下传数据格式**|属性编号|下行数据|阈值
    |:---:|:---:|:---:|:---:|:---:|
    |参数名称|pid|downdata|threshold|
    |数据类型|int|float|float|
    |数据定长数组个数|2|3|6（第四位小数点）|

- TODO处理粘包问题


# 整理开发文档
## 1. 开发环境
*具体用到的库见代码*
- Python 3.5.3
- SQLAlchemy (1.3.4)
- Flask (1.0.2)
- Flask-SocketIO (3.3.2)
- Flask-SQLAlchemy (2.3.2)
- greenlet (0.4.15)
- eventlet (0.24.1)
- pip (9.0.1)
- mysql  Ver 15.1 Distrib 10.1.38-MariaDB, for debian-linux-gnueabihf (armv7l) using readline 5.2

## 2. 使用外置无线网卡配置AP
+ [树莓派加无线网卡配置WIFI热点的方法 | 树莓派实验室](http://shumeipai.nxez.com/2018/03/13/raspberry-pi-double-network-cards-for-wireless-hotspot.html)
+ [可能的错误:Job for hostapd.service failed because the control process exited with error code.](https://unix.stackexchange.com/questions/415405/cant-start-hostapd-because-multiple-errors?rq=1)

## 3. mysql数据库说明
- mysql命令行登陆：
  - sudo mysql -u test -p mspace 
  - 密码：xxxxxx
- 数据库主要结构
  - 数据库
    ``` 
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | mspace             |
    +--------------------+
    ```
  - 表结构
    ```
    +------------------+
    | Tables_in_mspace |
    +------------------+
    | data_table       |
    | device_table     |
    +------------------+
    ```
- 3个表，设备列表,数据列表,用户自定映射表（第三表未创建）
    1. 查询设备列表是否首次接入：已经注册则直接将数据插入对应数据表，未注册则在设备表增加相应新字段，之后在数据表直接插入相应数据。

        |**设备注册表**|设备ID（主键）|设备类型编号|属性个数|在线状态|最后一次心跳时间
        |:---:|:---:|:---:|:---:|:---:|:---:|:---:|
        |参数名称|id|typeid|pnumber|status|htime
        |数据类型|int|int|int|bool|timestamp
    2. 数据表存储设备实时数据和指令，以便web前端访问使用与控制，需按照与设备属性约定的规则执行相应逻辑。

        |**数据存取表**|设备ID|属性编号|数据时间戳|上行数据|下行数据|警报状态|阈值
        |:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
        |参数名称|id|pid|ctime|updata|downdata|alert|threshold
        |数据类型|int|int|timestamp|float|float|bool|float
    3. typeid与propertyID映射表说明（供用户增删改查）
        |**用户自定映射表**|设备类型编号|用户定义类型|属性编号|用户定义属性
        |:---:|:---:|:---:|:---:|:---:|
        |参数名称|typeid|utype|pid|upid|
        |数据类型|int|string|int|string|



## 4. 上位机下传指令数据格式说明：

- |**下传数据格式**|属性编号|下行数据|阈值
    |:---:|:---:|:---:|:---:|:---:|
    |参数名称|pid|downdata|threshold|
    |数据类型|int|float|float|
    |数据定长数组个数|2|3|6（第四位小数点）|


## 5. 代码结构说明
- 路径：/home/pi/webServer/sub-version
  
```
sub-version
├── configs.py          (mysql设置连接) 
├── dbio.py             (数据库主要接口函数)
├── flaskWeb.py         (Flask主体框架)
├── models.py           (使用systemctl restart mariadb.service指令创建的模型实例仅做参考)
├── __pycache__         (python自动生成文件)
├── socketTS.py         (socket TCP通信主体)
├── socketv1.py         (socket TCP备份文件)
├── socketv2.py         (socket TCP备份文件)
├── templates           (web网页前端模版文件夹)
│   ├── home-backup.html(模版备份)
│   └── home.html       (socket TCP)
├── test                (本地模拟测试socket连接与数据库通讯)
│   ├── t1.py
│   ├── t2.py
│   ├── t3.py
│   ├── t4.py
│   └── test.py         (本地模拟测试备份文件)
├── testCtrl.py         (本地模拟测试)
└── testlocal.py        (本地测试文件)
```

## 6. 现有问题说明
- 向下传数据与指令存在丢失数据问题
- TCP处理粘包问题

## 7. 图示
- [数据流程图](https://www.processon.com/view/link/5cff12cbe4b091a8f23ddb0a)
- [架构图](https://www.processon.com/view/link/5cb6d47de4b09b16ffbb5a7d)
## N. 杂项说明
- ssh登陆： ssh pi@192.168.7.180
  - 密码 xxxxxx

- 如何控制mSpace系统
  1. 连接树莓派WI-FI
  2. WIFI: mSpacePi
  3. Password: mspacepi
  4. 浏览器打开网址：http://192.168.88.1:5000/

