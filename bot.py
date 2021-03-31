###库###
import pymysql
import time
import random
import asyncio
import re
from graia.broadcast import Broadcast
from graia.application.entry import *
from graia.application.message.elements.internal import *
########
qqbot_item = ['QQid', 'good' ,'times', 'pull', 'admin','sign_in','game_1']


class variables:
    memberid = 0
    i = 0
    guess_chances = 7
    num = 0
vari = variables()
###检查数据库这个人的资料
def checkdb(account,item):
    conn = pymysql.connect(host='localhost',user='root',password='richard5296867',db="qqmember",charset='utf8mb4')
    try:
        cur = conn.cursor()
        cur.execute('SELECT {} FROM qqbot where qqid={}'.format(item,account))
        result = cur.fetchall()
        if len(result) == 0 :
            return 0
        else:
            return result[0][0]
    except Exception as e:
        print("出问题了",e)
        pass
    finally:
        cur.close()
        conn.close()

###更新数据库
def updatedb(account,item,value):
    #item:你要改的数值,pull,like之类的
    conn = pymysql.connect(host='localhost',user='root',password='richard5296867',db="qqmember",charset='utf8mb4')
    try:
        cur = conn.cursor()
        cur.execute('select {} from qqbot where qqid={}'.format(item, account))
        result = cur.fetchall()
        if len(result) == 0:
            #如果没有则新建  
            cur.execute('insert into qqbot (qqid,good,times,pull,admin,sign_in,game_1) values({},0,0,0,0,0,0)'.format(account))
            cur.execute('update qqbot set {}={} where qqid={}'.format(item, value, account))
            conn.commit()
            return 1
        else:
            cur.execute('update qqbot set {}={} where qqid={}'.format(item, value, account))
            conn.commit()
    except Exception as e:
        print(e)
        return "cnmd 数据库出问题了",e
        pass
    finally:
        cur.close()
        conn.close()


##重置
def reset():
    conn = pymysql.connect(host='localhost',user='root',password='richard5296867',db="qqmember",charset='utf8mb4')
    try:
        cur = conn.cursor()
        cur.execute('update qqbot set times = 0 ,pull = 0,sign_in = 0, game_1 = 0')
        conn.commit()
        return "重置好啦主人"
    except Exception as e:
        print(e)
        return "cnmd 数据库出问题了",e
        pass
    finally:
        cur.close()
        conn.close()


####参数####
loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080", # 填入 httpapi 服务运行的地址
        authKey="graia-mirai-api-http-authkey", # 填入 authKey
        account=3062873067, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)
###东西###
@bcc.receiver("GroupMessage")
async def group_message_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group,member: Member):
    if message.asDisplay().find("gura") != -1 or message.asDisplay().find("A") != -1:
        choose = random.randint(0,1)
        if choose == 1:  
            await app.sendGroupMessage(group, MessageChain.create([
                Plain("A！"),
            ]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([
                Image.fromLocalFile("./source/memes/5.jpg")
            ]))
    elif message.asDisplay().startswith("早"):
        times = int(time.strftime("%H", time.localtime()))
        if times >= 12 and times <= 17:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id),Plain("笨蛋,都中午啦"),
                ]))
        elif times <= 5 :
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id),Plain("已经午夜了..."),
            ]))
        elif times >= 17 and times <= 24:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id),Plain("都已经晚上了..."),
            ]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id),Plain("早上好啊~"),
            ]))
    elif message.asDisplay().startswith("伸手指"):
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Plain("啊呜！(一口含住)"),
        ]))
    elif message.asSerializationString().find('[mirai:at:2365895696,]') != -1:
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("找我主人吗?"),
        ]))
    elif message.asSerializationString().find('[mirai:at:3062873067,]') != -1:
        if member.id == 2365895696:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id),Plain("主人~"),
            ]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([
                Plain("我是电子鲨鲨！\n"),At(2365895696),Plain("是我主人!\n"),Plain("输入!help以获得帮助")
            ]))
    elif message.asDisplay().startswith("!help"):
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("目前能实现的功能不多,主要有:\n"),
            Plain("1.摸尾巴\n"),
            Plain("2.我永远单推鲨鲨\n"),
            Plain("3.伸手指\n"),
            Plain("4.签到\n"),
            Plain("6.猜数字\n"),
            Plain("5.还有各种好玩的触发词23333(未来会有更多小游戏)\n"),
        ]))
    elif message.asDisplay().find("涩图")  != -1 or message.asDisplay().find("色图") != -1:
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("哼,真是的...给你就是了"),Image.fromLocalFile("./source/gura/{}.jpg".format((random.randint(1,21))))
        ]))
    elif message.asDisplay().startswith("喵"):
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("喵~"),Image.fromLocalFile("./source/表情包/mua.jpg")
        ]))
    elif message.asDisplay().startswith("啊这") or message.asDisplay().startswith("az"):
        await app.sendGroupMessage(group, MessageChain.create([
            Image.fromLocalFile("/Users/richard/source/表情包/河里.png")
        ]))
    elif message.asDisplay().find('音游') != -1:
        await app.sendGroupMessage(group, MessageChain.create([
            Plain('音游我可擅长了！'),Image.fromLocalFile("./source/表情包/音游鲨.gif")
        ]))
    elif message.asDisplay().find('好耶') != -1:
        await app.sendGroupMessage(group, MessageChain.create([
            Plain('好耶~')
        ]))
    elif message.asDisplay().startswith('我永远单推'):
        if message.asDisplay().startswith('我永远单推鲨鲨') or message.asDisplay().startswith('我永远单推古拉') or message.asDisplay().startswith('我永远单推高古拉'):
            relation = checkdb(member.id,qqbot_item[1])
            count = checkdb(member.id, qqbot_item[3])
            if member.id == 2365895696:
                if checkdb(member.id, qqbot_item[3]) == 0:
                    updatedb(member.id, qqbot_item[1],relation+10)
                    updatedb(member.id, qqbot_item[3], 1)
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("主人最棒了~\n"),Plain("好感度+10")
                    ]))
                    pass
                else:
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("主人最棒了~")
                    ]))
                    pass
            else:
                if relation >= 100:
                    if checkdb(member.id, qqbot_item[3]) == 0 :
                        updatedb(member.id, qqbot_item[1],relation+10)
                        updatedb(member.id, qqbot_item[3], 1)
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("好耶~！\n"),Plain("好感度+10")
                        ]))
                        pass
                    else:
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("好耶~！")
                        ]))
                        pass
                elif relation >= 0:
                    if checkdb(member.id, qqbot_item[3]) == 0:
                        updatedb(member.id, qqbot_item[1],relation+5)
                        updatedb(member.id, qqbot_item[3], 1)
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("谢谢~\n"),Plain("好感度+2")
                        ]))
                        pass
                    else:
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("谢谢~")
                        ]))
                        pass
                elif relation >= 600:
                    if checkdb(member.id, qqbot_item[3]) == 0:
                        updatedb(member.id, qqbot_item[1],relation+40)
                        updatedb(member.id, qqbot_item[3], 1)
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("我爱你~\n"),Plain('好感度+40')
                        ]))
                        pass
                    else:
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("我爱你~")
                        ]))
                        pass
                elif relation >= 300:
                    if checkdb(member.id, qqbot_item[3]) == 0:
                        updatedb(member.id, qqbot_item[1],relation+20)
                        updatedb(member.id, qqbot_item[3], 1)
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("啾~\n"),Plain("好感度+10")
                        ]))
                        pass
                    else:
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("啾~")
                        ]))
                        pass
        elif message.asDisplay == '我永远单推' or message.asDisplay == '我永远单推（）' or message.asDisplay == '我永远单推 ' or message.asDisplay == '我永远单推()':
            await app.sendGroupMessage(group,MessageChain.create([
                Plain('你要单推谁？我吗?(期待.jpg)')
            ]))
        else:
            if member.id == 2365895696:
                await app.sendGroupMessage(group,MessageChain.create([
                    Plain('主人不要我了吗??!!')
                ]))
            else:
                await app.sendGroupMessage(group,MessageChain.create([
                    Plain('啊...你不要我了吗..呜呜呜')
                ]))
    elif message.asDisplay().find('脑力') != -1:
        await app.sendGroupMessage(group,MessageChain.create([
            Plain("LET THE BASS KICK"),
        ]))
        time.sleep(1.5),
        await app.sendGroupMessage(group,MessageChain.create([
            Plain('O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-A-U-U-A- E-eee')
        ]))
    elif message.asDisplay().startswith("摸尾巴"):
        relation = checkdb(member.id,qqbot_item[1])
        count = checkdb(member.id, qqbot_item[2])
        if member.id == 2365895696:
            if checkdb(member.id,qqbot_item[2]) < 7:
                updatedb(member.id, qqbot_item[1],relation+10)
                updatedb(member.id, qqbot_item[2], count + 1)
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain("主人轻点~\n"),Plain("好感度+10")
                ]))
                pass
            else:
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain("主人轻点~")
                ]))
            pass
        else:
            if relation >= 20:
                if count < 7:
                    updatedb(member.id, qqbot_item[1],relation+3)
                    updatedb(member.id, qqbot_item[2], count+1)
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("只能摸一下哦...\n"),Plain("好感度+3")
                    ]))
                    pass
                else:
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("只能摸一下哦...")
                    ]))
                    pass
            elif relation >= 0:
                if count < 7:
                    updatedb(member.id, qqbot_item[1],relation+1)
                    updatedb(member.id, qqbot_item[2], count+1)
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("鲨鲨躲开了\n"),Plain("但好感度+1")
                    ]))
                    pass
                else:
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("鲨鲨躲开了")
                    ]))
                    pass
            elif relation >= 5000:
                if count < 7:
                    updatedb(member.id, qqbot_item[1],relation+20)
                    updatedb(member.id, qqbot_item[2], count+1)
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("主人我爱你~\n"),Plain('好感度+20')
                    ]))
                    pass
                else:
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("主人我爱你~")
                    ]))
                    pass
            elif relation >= 100:
                if count < 7:
                    updatedb(member.id, qqbot_item[1],relation+4)
                    updatedb(member.id, qqbot_item[2], count+1)
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("别摸啦，好痒的~\n"),Plain('好感度+10')
                    ]))
                    pass
                else:
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("别摸啦，好痒的~")
                    ]))
                    pass
            elif relation >= 300:
                if count < 7:
                    updatedb(member.id, qqbot_item[1],relation+4)
                    updatedb(member.id, qqbot_item[2], count+1)
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("啊~好舒服~\n"),Plain('好感度+4')
                    ]))
                    pass
                else:
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("啊~好舒服~")
                    ]))
                    pass
    elif message.asDisplay().startswith("摸头"):
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("*你摸了摸鲨鲨的头发，软软的，还有股香味(海草味?)\n"),Plain("好舒服...")
        ]))
    elif message.asDisplay().startswith("好感度"):
        relation = checkdb(member.id,qqbot_item[1])
        if 0 <= relation <= 20 :
            await app.sendGroupMessage(group, MessageChain.create([
                    Plain("鲨鲨觉得你是个陌生人\n"),Plain("当前好感度:{}".format(relation))
            ]))
        elif 21 <= relation <= 60:
            await app.sendGroupMessage(group, MessageChain.create([
                    Plain("鲨鲨跟你比较熟\n"),Plain("当前好感度:{}".format(relation))
            ]))
        elif relation > 60:
            await app.sendGroupMessage(group, MessageChain.create([
                    Plain("鲨鲨和你是好朋友\n"),Plain("当前好感度:{}".format(relation))
            ]))
        elif relation > 100:
            await app.sendGroupMessage(group, MessageChain.create([
                    Plain("鲨鲨和你是值得信赖的朋友\n"),Plain("当前好感度:{}".format(relation))
            ]))
        elif relation > 200:
            await app.sendGroupMessage(group, MessageChain.create([
                    Plain("鲨鲨只要和你在一起就很开心\n"),Plain("当前好感度:{}".format(relation))
            ]))
        elif relation > 400:
            await app.sendGroupMessage(group, MessageChain.create([
                    Plain("鲨鲨看你的眼神充满爱意\n"),Plain("当前好感度:{}".format(relation))
            ]))
    elif message.asDisplay().startswith('sudo shark-reset'):
        admin = checkdb(member.id, qqbot_item[4])
        if admin == 1:
            await app.sendGroupMessage(group, MessageChain.create([
                Plain(reset())
            ]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([
                Plain("权限不足")
            ]))
    elif message.asDisplay().startswith('小色鲨'):
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("才不是呢~!")
        ]))
    elif message.asDisplay().startswith('签到'):
        relation = checkdb(member.id,qqbot_item[1])
        sign_in_times = checkdb(member.id,qqbot_item[5])
        if sign_in_times == 0:
            point = random.randint(1,10)
            updatedb(member.id,qqbot_item[1],relation+point)
            updatedb(member.id,qqbot_item[5],1)
            await app.sendGroupMessage(group, MessageChain.create([
                Plain("签到成功！\n"),Plain('好感度+{}'.format(point))
            ]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([
                Plain("今天已经签到过了哦~")
            ]))
    elif message.asDisplay().startswith('摸下排牙'):
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("*你什么也没摸到，除了一手口水，真好喝")
        ]))
    elif message.asDisplay().find("BUG") != -1 or message.asDisplay().find("bug") != -1 or message.asDisplay().find("Bug") != -1:
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("1 bug fixed, 255 bug increased")
        ]))
    elif message.asDisplay() == "晚安" or message.asDisplay().startswith("晚安"):
        times = int(time.strftime("%H", time.localtime()))
        if times >= 12 and times <= 17:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id),Plain(" 才中午.."),
                ]))
        elif times <= 5 :
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id),Plain(" 晚安,快去睡觉！"),
            ]))
        elif times >= 5 and times <= 12:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id),Plain(" 都已经早上了..."),
            ]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id),Plain(" 晚安~"),
                ]))
    elif message.asDisplay().find("memes") != -1 or message.asDisplay().find("梗图") != -1:
        await app.sendGroupMessage(group, MessageChain.create([
            Image.fromLocalFile("./source/memes/{}.jpg".format(random.randint(1,9)))
        ]))
    elif message.asDisplay().startswith("猜数字"):
        if vari.memberid == 0:
            vari.memberid = member.id   
            vari.num = random.randint(1,100)
            vari.guess_chances = 7
            await app.sendGroupMessage(group, MessageChain.create([
                Plain('你只有7次猜数字的机会哦！(1-100)\n'),Plain("输入!quit退出")
            ]))
        elif vari.memberid != member.id and vari.memberid != 0:
            await app.sendGroupMessage(group, MessageChain.create([
                Plain('别人在玩呢，先等等...')
            ]))
        else:
            pass
    elif message.asDisplay().startswith("!quit"):
        if vari.memberid == 0:
            await app.sendGroupMessage(group, MessageChain.create([
                Plain('目前没有游戏开始,输入"猜数字"开始游戏~')
            ]))
        elif vari.memberid != member.id and vari.memberid != 0:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id),Plain('这是别人的游戏哦!'),Image.fromLocalFile("./source/表情包/angry.jpg")
            ]))
        else:
            vari.memberid = 0
            vari.i = 0
            vari.guess_chances = 7
            vari.num = 0
            await app.sendGroupMessage(group, MessageChain.create([
                Plain('已退出~')
            ]))
    try:
        msg = int(message.asDisplay())
        if member.id == vari.memberid and 1 <= msg <= 100 and vari.i != 7 :
            vari.i += 1
            if msg < vari.num:
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain('你输入的数字太小了，还有' + str(vari.guess_chances - vari.i)+'次机会，请重新输入：')
                ]))
            elif msg > vari.num:
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain('你输入的数字太大了，还有' + str(vari.guess_chances - vari.i)+'次机会，请重新输入：')
                ]))
            elif msg == vari.num and checkdb(member.id, qqbot_item[6]) != 1:
                relation = checkdb(member.id,qqbot_item[1])
                updatedb(member.id, qqbot_item[1],relation+10)
                updatedb(member.id, qqbot_item[6], 1)
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain('猜对了!\n'),Plain('好感度+10')
                ]))
                vari.memberid = 0
                vari.i = 0
                vari.guess_chances = 7
                vari.num = 0
            elif msg == vari.num :
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain('猜对了!')
                ]))
                vari.memberid = 0
                vari.i = 0
                vari.guess_chances = 7
                vari.num = 0
        elif member.id == vari.memberid and vari.i == 7:
            await app.sendGroupMessage(group, MessageChain.create([
                Plain('你没猜到...看来得多练习呢!')
            ]))
            vari.memberid = 0
            vari.i = 0
            vari.guess_chances = 7
            vari.num = 0
    except Exception as e:
        print(e)
        pass
    time.sleep(2)


    # elif message.asDisplay().



###开始运行###
app.launch_blocking()
