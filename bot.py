###库###

import json
import GuraBotLib as gbl
import pymysql
import time
import random
import asyncio
import glob
import os
from urllib.request import urlretrieve
import numpy as npr
from graia.scheduler import (
    timers,
)
import graia.scheduler as scheduler
from graia.broadcast import Broadcast
from graia.application.entry import *
from graia.application.message.elements.internal import *

###变量####


os.chdir("/Users/richard/")
npr.random.seed(0)
p = npr.array([0.1,0.2, 0.4, 0.15, 0.1, 0.05])
lottery = [0,50,100,150,200,250]
group_black_list = [915889573,]
qqbot_item = ['QQid', 'good' ,'times', 'pull', 'admin','sign_in','game_1']
class variables:
    mode = 0
    memberid = 0
    i = 0
    guess_chances = 6
    num = ""
vari = variables()
####参数####
loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:3080", # 填入 httpapi 服务运行的地址
        authKey="gura-bot", # 填入 authKey
        account=3062873067, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)

###本体###

# sche = scheduler.GraiaScheduler(loop=loop,broadcast=bcc)

# @sche.schedule(timers.every_custom_hours(4))#多久提醒一次
# async def remind_time():
#     times = int(time.strftime("%H", time.localtime())) + 4
#     if  times > 7:
#         await app.sendGroupMessage(915889573, MessageChain.create([
#             At(1927017507),Plain("  记得喝水啊"),
#         ]))
#     else:
#         pass
@bcc.receiver("MemberJoinEvent")
async def MemberJoin(group: Group,member: Member):
    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id),Plain(""" [GuraBot] \-在这里诚挚地欢迎您(大佬)加入!-/,Nya!""")
    ]))
@bcc.receiver("GroupMessage")
async def group_message_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group,member: Member):

    ###log###

    now_time = time.asctime( time.localtime(time.time()))
    log = open("./bots/log.log","a")
    logs = str(now_time)+" "+str(group.name)+"("+str(group.id)+")"+":"+str(member.name)+"("+str(member.id)+'):'+message.asDisplay()
    log.write(str(logs)+"\n")
    log.close()

    ###blacklist###


    with open("/Users/richard/blacklist.json","r") as f:
        blacklist = json.load(f)

    ###指令###

    if message.asDisplay().startswith("!") or message.asDisplay().startswith("！") and member.id not in blacklist:
        if message.asDisplay().startswith("!掷骰子") or message.asDisplay().startswith("！掷骰子"):
            try:
                dice = message.asDisplay().split(" ",3)
                probability = random.randint(int(dice[2]),int(dice[3]))
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain('你{}的概率是{}Nya!'.format(dice[1],probability))
                    ]))
            except:
                await app.sendGroupMessage(group, MessageChain.create([
                    At(member.id),Plain("无法识别!,用法为: !掷骰子 事件 概率(最少) 概率(最多) \n 如: !掷骰子 我是人 1 100")
                    ]))
        elif message.asDisplay().startswith("!图片"):
            command = message.asDisplay().split(" ")
            if command[1] == "上传":
                try:
                    msg_url = message.get(Image)[0].url
                except Exception as e:
                    await app.sendGroupMessage(group, MessageChain.create([
                            Plain('用法错误，正确用法为: !图片 上传 [类别] 图片 \n'),
                            Plain("如要展示图片，则为: !图片 展示 [类别] ，错误信息:{}".format(e))
                        ]))
                    return False
                try:
                    if command[3] == "":
                        pass
                    if not os.path.exists("./source/{}".format(command[2])):
                        os.makedirs("./source/{}".format(command[2]))
                        msg_name = message.get(Image)[0].imageId
                        urlretrieve(msg_url,'./source/{}/{}'.format(command[2],msg_name))
                        time.sleep(0.5)
                        print("ok.")
                        await app.sendGroupMessage(group,MessageChain.create([
                            Plain("已成功将"),Image.fromLocalFile("./source/{}/{}".format(command[2],msg_name)),Plain("上传到类别{}中！".format(command[2]))
                        ]))
                    else:
                        msg_name = message.get(Image)[0].imageId
                        urlretrieve(msg_url,'./source/{}/{}'.format(command[2],msg_name))
                        time.sleep(0.5)
                        print("ok.")
                        await app.sendGroupMessage(group,MessageChain.create([
                            Plain("已成功将"),Image.fromLocalFile("./source/{}/{}".format(command[2],msg_name)),Plain("上传到类别{}中！".format(command[2]))
                        ]))
                except Exception as e:
                    print(e)
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain('用法错误，正确用法为: !图片 上传 [类别] 图片 \n'),
                        Plain("如要展示图片，则为: !图片 展示 [类别] ，错误信息:{}".format(e))
                    ]))
            elif command[1] == '展示':
                if not os.path.exists("./source/{}".format(command[2])):
                    await app.sendGroupMessage(group, MessageChain.create([
                    Plain('类别不存在')
                    ]))
                try:
                    img = glob.glob("./source/{}/*".format(command[2]))
                    print(img)
                    await app.sendGroupMessage(group, MessageChain.create([
                    Image.fromLocalFile(random.choice(img))
                    ]))
                except Exception as e:
                    print(e)
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain('用法错误，正确用法为: !图片 上传 [类别] 图片 \n'),
                        Plain("如要展示图片，则为: !图片 展示 [类别] ，错误信息:{}".format(e))
                    ]))
                    return False
        # elif message.asDisplay().startswith("!抽奖"):
        #     add_point = 0
        #     final_point = 0
        #     command = message.asDisplay().split(" ")
        #     try:
        #         times = int(command[1])
        #     except Exception as e:
        #         print(e)
        #         await app.sendGroupMessage(group, MessageChain.create([
        #             Plain('用法错误.正确抽奖方法为:!抽奖 [次数] ,一次减少100好感度,抽奖随机增加50-150好感度')
        #         ]))
        #     if times <= 0:
        #         await app.sendGroupMessage(group, MessageChain.create([
        #             Plain('抽奖次数不能小于或等于0!')
        #         ]))
        #     else:
        #         relation = gbl.sql.checkdb(member.id,qqbot_item[1])
        #         if times * 100 > relation :
        #             await app.sendGroupMessage(group, MessageChain.create([
        #             Plain('最多抽奖次数不能大于你现在的好感度!')
        #             ]))
        #         else:
        #             relation = gbl.sql.checkdb(member.id,qqbot_item[1])
        #             time.sleep(0.3)
        #             for i in range(times):
        #                 final_point += npr.random.choice(lottery,p=p.ravel())
        #             gbl.sql.updatedb(member.id, qqbot_item[1],relation+final_point-times*100)
        #             await app.sendGroupMessage(group, MessageChain.create([
        #             Plain('抽奖完毕，一共抽了{}次，加了{}好感度,扣除{}好感度'.format(times,final_point,times*100))
        #             ]))
        elif message.asDisplay().startswith("!quit"):
            if vari.mode == 0:
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain('目前没有游戏开始,输入"猜数字"开始游戏~')
                ]))
            else:
                admin = gbl.sql.checkdb(member.id, qqbot_item[4])
                if admin == 1:
                    vari.mode = 0
                    vari.memberid = 0
                    vari.i = 0
                    vari.guess_chances = 6
                    vari.num = 0
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain('主人，已退出~')
                    ]))
                else:
                    if vari.memberid != member.id and vari.memberid != 0:
                        await app.sendGroupMessage(group, MessageChain.create([
                            At(member.id),Plain('这是别人的游戏哦!'),Image.fromLocalFile("./source/表情包/angry.jpg")
                        ]))
                    else:
                        vari.mode = 0
                        vari.memberid = 0
                        vari.i = 0
                        vari.guess_chances = 6
                        vari.num = 0
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain('已退出~')
                        ]))
        elif message.asDisplay().startswith("!help") or message.asDisplay().startswith('！help'):
            await app.sendGroupMessage(group, MessageChain.create([
                Plain("目前能实现的功能不多,主要有:\n"),
                Plain("1.摸尾巴(加好感度)\n"),
                Plain("2.我永远单推鲨鲨(加好感度)\n"),
                Plain("3.伸手指\n"),
                Plain("4.签到(随机加好感度)\n"),
                Plain("5.!猜数字(赢了加好感度)\n"),
                Plain("6.色图\n"),
                Plain("7.摸肚子/屁股\n"),
                Plain("8.闹钟\n"),
                Plain("9.鲨片\n"),
                Plain("10.!掷骰子 事件 概率(最少) 概率(最多)\n"),
                Plain("11.摸耳朵\n"),
                Plain("12.!图片 上传 [类别] 图片 / !图片 展示 [类别]")
            ]))
        elif message.asDisplay().startswith("!猜数字") or message.asDisplay().startswith("！猜数字"):
            ###猜数字初始化###

            if vari.mode == 0:
                vari.mode = 1
                vari.memberid = member.id
                vari.num = gbl.generate.generate()
                vari.guess_chances = 6

            #######
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain('规则:一个四位数，每个数字各不相同（没有0），你需要猜各个位的数字，\n输出A则为当前位数的数字和位置与答案相同；\nB则是当前位数数字在答案内，但位置不相同；\nC则为当前位数数字不在答案内\n'),Plain("输入!quit退出")
                ]))
            elif vari.memberid != member.id and vari.memberid != 0:
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain('别人在玩呢，先等等...')
                ]))
            else:
                pass
        elif message.asDisplay().startswith("!24点") or message.asDisplay().startswith("！24点"):
            ####初始化24点####
            if vari.mode == 0:
                vari.mode = 2
                vari.memberid = member.id
                vari.num = gbl.generate.generate()
                num_list = [1,2,3,4,5,6,7,8,9]
                show_num = ""
                print(vari.num)
            #######
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain('规则:生成4个数，每个数字各不相同（没有0），\n通过加("+")减("-")乘("*")除("/")和括号(必须为英文)来算出24,每个数字只能使用一次(注:不要空格).')
                ]))
                for i in [int(x) for x in vari.num]:
                    show_num += str(i) + " "
                time.sleep(0.5)
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain("现在的数字为：{}".format(show_num))
                ]))
            elif vari.memberid != member.id and vari.memberid != 0:
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain('别人在玩呢，先等等...')
                ]))
            else:
                pass
        elif message.asDisplay().startswith("!好感度"):

            admin = gbl.sql.checkdb(member.id, qqbot_item[4])
            if admin == 1:
                command = message.asDisplay().split(" ")
                if command[1] == "查询":
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("用户{}的好感度为: {} ".format(command[2],gbl.sql.checkdb(int(command[2]),qqbot_item[1])))
                    ]))
                elif command[1] == "增加":
                    relation = int(gbl.sql.checkdb(command[2],qqbot_item[1]))
                    gbl.sql.updatedb(command[2],qqbot_item[1],relation + int(command[3]))
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("已为用户{}增加{}好感度".format(command[2],command[3]))
                        ]))
                elif command[1] == '减少':
                    relation = int(gbl.sql.checkdb(command[2],qqbot_item[1]))
                    gbl.sql.updatedb(command[2],qqbot_item[1],relation - int(command[3]))
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("已为用户{}减少{}好感度".format(command[2],command[3]))
                        ]))
                else:
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("无此指令!")
                        ]))
            else:
                await app.sendGroupMessage(group, MessageChain.create([
                        Plain("权限不足!")
                        ]))
        elif message.asDisplay().startswith("!拉黑"):
            admin = gbl.sql.checkdb(member.id, qqbot_item[4])
            if admin == 1:
                blist = message.asDisplay().split(" ")
                with open("/Users/richard/blacklist.json","r") as f:
                    blacklist = json.load(f)
                blacklist.append(int(blist[1]))
                with open('/Users/richard/blacklist.json', 'w') as f:  
                    json.dump(blacklist, f)
                await app.sendGroupMessage(group, MessageChain.create([
                    At(blist[1]),Plain(' 不理你了!')
                ]))
        elif message.asDisplay().startswith("!禁言"):
            admin = gbl.sql.checkdb(member.id, qqbot_item[4])
            if admin == 1:
                black = message.asDisplay().split(" ")
                await app.mute(group,int(black[1]),int(black[2]))
                await app.sendGroupMessage(group, MessageChain.create([
                    At(int(black[1])),Plain(" 下次小心点~")
                    ]))
            else:
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain("权限不足!")
                    ]))

    ###触发词###
    else:
        if group.id not in group_black_list:
            if member.id not in blacklist:
                if message.asDisplay().find("gura") != -1 or message.asDisplay() == ("A") or message.asDisplay().find("nya") != -1 or message.asSerializationString().find('mirai:atall') != -1 :
                    choose = random.randint(0,1)
                    if choose == 1:  
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("Nya！"),
                        ]))
                    else:
                        await app.sendGroupMessage(group, MessageChain.create([
                            Image.fromLocalFile("./source/memes/5.jpg")
                        ]))
                elif message.asDisplay().startswith("草"):
                    grass_time = 0
                    for i in message.asDisplay():
                        if i == "草":
                            grass_time += 1
                        else:
                            break
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("草"*grass_time)
                        ]))
                elif message.asDisplay().find("😅") != -1:
                    relation = gbl.sql.checkdb(member.id,qqbot_item[1])
                    gbl.sql.updatedb(member.id, qqbot_item[1],relation-5)
                    await app.sendGroupMessage(group, MessageChain.create([
                        At(member.id),Plain("不要发流汗黄豆啊....\n"),Plain("好感度-5"),
                    ]))
                elif message.asDisplay().startswith("早"):
                    times = int(time.strftime("%H", time.localtime()))
                    if times >= 12 and times <= 17:
                        await app.sendGroupMessage(group, MessageChain.create([
                            At(member.id),Plain("笨蛋,都中午啦"),
                            ]))
                    elif times >= 5 :
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
                elif message.asDisplay() == "伸手指":
                    await app.sendGroupMessage(group, MessageChain.create([
                        At(member.id),Plain("啊呜！(一口含住)"),
                    ]))
                elif message.asDisplay().find('[mirai:at:2365895696]') != -1:
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("找我主人吗?"),
                    ]))
                elif message.asSerializationString().find('[mirai:at:3062873067,]') != -1:
                    print(message.asDisplay())
                    if member.id == 2365895696:
                        await app.sendGroupMessage(group, MessageChain.create([
                            At(member.id),Plain("主人~"),
                        ]))
                    elif message.asDisplay() == "@3062873067 ":
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("どうも，鯊魚ですNya~"),At(2365895696),Plain("是我主人Nya!\n"),Plain("输入 !help 来获得命令帮助~")
                        ]))
                    else:
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("如果你要对我下指令，无需使用At.")
                        ]))
                elif message.asDisplay().startswith("闹钟"):
                    await app.sendGroupMessage(group, MessageChain.create([
                        Voice_LocalFile("/Users/richard/source/audio/guraclock.silk")
                    ]))
                elif message.asDisplay().startswith("鲨片"):
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("好康♂的东西: https://www.bilibili.com/video/BV1GJ411x7h7")
                    ]))
                elif message.asDisplay().startswith("涩图") or message.asDisplay().startswith("色图"):
                    setulist = glob.glob("./source/色图/*")
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("哼,真是的...给你就是了"),Image.fromLocalFile((random.choice(setulist)))
                    ]))
                elif message.asDisplay().startswith("喵"):
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("Nya!"),Image.fromLocalFile("./source/表情包/mua.jpg")
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
                        relation = gbl.sql.checkdb(member.id,qqbot_item[1])
                        count = gbl.sql.checkdb(member.id, qqbot_item[3])
                        if member.id == 2365895696:
                            if gbl.sql.checkdb(member.id, qqbot_item[3]) == 0:
                                gbl.sql.updatedb(member.id, qqbot_item[1],relation+10)
                                gbl.sql.updatedb(member.id, qqbot_item[3], 1)
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
                            if 500 >= relation >= 100:
                                if gbl.sql.checkdb(member.id, qqbot_item[3]) == 0 :
                                    gbl.sql.updatedb(member.id, qqbot_item[1],relation+5)
                                    gbl.sql.updatedb(member.id, qqbot_item[3], 1)
                                    await app.sendGroupMessage(group, MessageChain.create([
                                        Plain("好耶~！\n"),Plain("好感度+5")
                                    ]))
                                    pass
                                else:
                                    await app.sendGroupMessage(group, MessageChain.create([
                                        Plain("好耶~！")
                                    ]))
                                    pass
                            elif 1000 >= relation >= 500:
                                if gbl.sql.checkdb(member.id, qqbot_item[3]) == 0:
                                    gbl.sql.updatedb(member.id, qqbot_item[1],relation+6)
                                    gbl.sql.updatedb(member.id, qqbot_item[3], 1)
                                    await app.sendGroupMessage(group, MessageChain.create([
                                        Plain("\n"),Plain("好感度+6")
                                    ]))
                                    pass
                                else:
                                    await app.sendGroupMessage(group, MessageChain.create([
                                        Plain("谢谢~")
                                    ]))
                            elif 100 >= relation >= 0:
                                if gbl.sql.checkdb(member.id, qqbot_item[3]) == 0:
                                    gbl.sql.updatedb(member.id, qqbot_item[1],relation+2)
                                    gbl.sql.updatedb(member.id, qqbot_item[3], 1)
                                    await app.sendGroupMessage(group, MessageChain.create([
                                        Plain("嗯，我相信你哦\n"),Plain("好感度+2")
                                    ]))
                                    pass
                                else:
                                    await app.sendGroupMessage(group, MessageChain.create([
                                        Plain("嗯，我相信你哦")
                                    ]))
                                    pass
                            elif relation >= 2000:
                                if gbl.sql.checkdb(member.id, qqbot_item[3]) == 0:
                                    gbl.sql.updatedb(member.id, qqbot_item[1],relation+10)
                                    gbl.sql.updatedb(member.id, qqbot_item[3], 1)
                                    await app.sendGroupMessage(group, MessageChain.create([
                                        Plain("啾~\n"),Plain('好感度+10')
                                    ]))
                                    pass
                                else:
                                    await app.sendGroupMessage(group, MessageChain.create([
                                        Plain("啾~")
                                    ]))
                                    pass
                            elif 4000 >= relation >= 1000:
                                if gbl.sql.checkdb(member.id, qqbot_item[3]) == 0:
                                    gbl.sql.updatedb(member.id, qqbot_item[1],relation+8)
                                    gbl.sql.updatedb(member.id, qqbot_item[3], 1)
                                    await app.sendGroupMessage(group, MessageChain.create([
                                        Plain("我爱你~\n"),Plain("好感度+8")
                                    ]))
                                    pass
                                else:
                                    await app.sendGroupMessage(group, MessageChain.create([
                                        Plain("我爱你~")
                                    ]))
                                    pass
                            elif relation > 4000:
                                if gbl.sql.checkdb(member.id, qqbot_item[3]) == 0:
                                    gbl.sql.updatedb(member.id, qqbot_item[1],relation+10)
                                    gbl.sql.updatedb(member.id, qqbot_item[3], 1)
                                    await app.sendGroupMessage(group, MessageChain.create([
                                        Plain("你最棒了!\n"),Plain("好感度+10")
                                    ]))
                                    pass
                                else:
                                    await app.sendGroupMessage(group, MessageChain.create([
                                        Plain("你最棒了！")
                                    ]))
                                    pass
                    elif message.asDisplay() == '我永远单推' or message.asDisplay() == '我永远单推（）' or message.asDisplay() == '我永远单推 ' or message.asDisplay() == '我永远单推()':
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
            ###LET
            ###THE
            ###BASS
            ###KICK
            ###O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-A-U-U-A- E-eee-ee-eee 
            ###AAAAE-A-E-I-E-A- JO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA
                elif message.asDisplay().find('脑力') != -1:
                    await app.sendGroupMessage(group,MessageChain.create([
                        Plain("LET THE BASS KICK"),
                    ]))
                    time.sleep(1.5),
                    await app.sendGroupMessage(group,MessageChain.create([
                        Plain('O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-A-U-U-A- E-eee')
                    ]))
                elif message.asDisplay().startswith("摸尾巴"):
                    relation = gbl.sql.checkdb(member.id,qqbot_item[1])
                    count = gbl.sql.checkdb(member.id, qqbot_item[2])
                    if member.id == 2365895696:
                        if gbl.sql.checkdb(member.id,qqbot_item[2]) < 7:
                            gbl.sql.updatedb(member.id, qqbot_item[1],relation+10)
                            gbl.sql.updatedb(member.id, qqbot_item[2], count + 1)
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
                        if 400 >= relation > 100:
                            if count < 7:
                                gbl.sql.updatedb(member.id, qqbot_item[1],relation+3)
                                gbl.sql.updatedb(member.id, qqbot_item[2], count+1)
                                await app.sendGroupMessage(group, MessageChain.create([
                                    Plain("只能摸一下哦...\n"),Plain("好感度+3")
                                ]))
                                pass
                            else:
                                await app.sendGroupMessage(group, MessageChain.create([
                                    Plain("只能摸一下哦...")
                                ]))
                                pass
                        elif 100 >= relation >= 0:
                            if count < 7:
                                gbl.sql.updatedb(member.id, qqbot_item[1],relation+1)
                                gbl.sql.updatedb(member.id, qqbot_item[2], count+1)
                                await app.sendGroupMessage(group, MessageChain.create([
                                    Plain("鲨鲨躲开了\n"),Plain("但好感度+1")
                                ]))
                                pass
                            else:
                                await app.sendGroupMessage(group, MessageChain.create([
                                    Plain("鲨鲨躲开了")
                                ]))
                                pass
                        elif 1000 >= relation > 400:
                            if count < 7:
                                gbl.sql.updatedb(member.id, qqbot_item[1],relation+4)
                                gbl.sql.updatedb(member.id, qqbot_item[2], count+1)
                                await app.sendGroupMessage(group, MessageChain.create([
                                    Plain("别摸啦，好痒的~\n"),Plain('好感度+4')
                                ]))
                                pass
                            else:
                                await app.sendGroupMessage(group, MessageChain.create([
                                    Plain("别摸啦，好痒的~")
                                ]))
                                pass
                        elif 4000 >= relation > 1000:
                            if count < 7:
                                gbl.sql.updatedb(member.id, qqbot_item[1],relation+10)
                                gbl.sql.updatedb(member.id, qqbot_item[2], count+1)
                                await app.sendGroupMessage(group, MessageChain.create([
                                    Plain("啊~好舒服~\n"),Plain('好感度+10')
                                ]))
                                pass
                            else:
                                await app.sendGroupMessage(group, MessageChain.create([
                                    Plain("啊~好舒服~")
                                ]))
                                pass
                        elif relation > 4000:
                            if count < 7:
                                gbl.sql.updatedb(member.id, qqbot_item[1],relation+15)
                                gbl.sql.updatedb(member.id, qqbot_item[2], count+1)
                                await app.sendGroupMessage(group, MessageChain.create([
                                    Plain("再来一下...(脸红)\n"),Plain('好感度+10')
                                ]))
                                pass
                            else:
                                await app.sendGroupMessage(group, MessageChain.create([
                                    Plain("再来一下...(脸红)")
                                ]))
                                pass
                elif message.asDisplay().startswith("摸头"):
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("*你摸了摸鲨鲨的头发，软软的，还有股香味(海草味?)\n"),Plain("好舒服...")
                    ]))
                elif message.asDisplay()== "好感度":
                    relation = gbl.sql.checkdb(member.id,qqbot_item[1])
                    if 100 >= relation >= 0 :
                        await app.sendGroupMessage(group, MessageChain.create([
                                Plain("鲨鲨觉得你是个陌生人\n"),Plain("当前好感度:{}".format(relation))
                        ]))
                    elif 400 >= relation >= 100:
                        await app.sendGroupMessage(group, MessageChain.create([
                                Plain("鲨鲨跟你比较熟\n"),Plain("当前好感度:{}".format(relation))
                        ]))
                    elif 1000 >= relation >= 400:
                        await app.sendGroupMessage(group, MessageChain.create([
                                Plain("鲨鲨和你是好朋友\n"),Plain("当前好感度:{}".format(relation))
                        ]))
                    elif 2500 >= relation >= 1000:
                        await app.sendGroupMessage(group, MessageChain.create([
                                Plain("鲨鲨只要和你在一起就很开心\n"),Plain("当前好感度:{}".format(relation))
                        ]))
                    elif relation > 2500:
                        await app.sendGroupMessage(group, MessageChain.create([
                                Plain("鲨鲨看你的眼神充满爱意\n"),Plain("当前好感度:{}".format(relation))
                        ]))
                elif message.asDisplay().startswith("摸耳朵"):
                    relation = gbl.sql.checkdb(member.id,qqbot_item[1])
                    if 100 >= relation >= 0 :
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("耳朵不要乱摸啦！")
                        ]))
                    elif 400 >= relation >= 100:
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("就算你是我朋友我也不会让你摸的..")
                        ]))
                    elif 1000 >= relation >= 400:
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("最多一下哦..")
                        ]))
                    elif 2500 >= relation >= 1000:
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("啊..好痒..")
                        ]))
                    elif relation >= 2500:
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("Nya~啊呜..饶了我吧..耳朵一直摸下去会很敏感的..")
                        ]))
                elif message.asDisplay().startswith('sudo shark-reset'):
                    admin = gbl.sql.checkdb(member.id, qqbot_item[4])
                    if admin == 1:
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain(gbl.sql.reset())
                        ]))
                    else:
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("权限不足")
                        ]))
                elif message.asDisplay() == 'sudo mysql --all':
                    admin = gbl.sql.checkdb(member.id, qqbot_item[4])
                    if admin == 1:
                        conn = pymysql.connect(host='localhost',user='root',password='richard5296867',db="qqmember",charset='utf8mb4')
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM qqbot')
                        result = cur.fetchall()
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain(str(result))
                        ]))
                    else:
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("权限不足")
                        ]))
                elif message.asDisplay().startswith('小色鲨'):
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("才不是呢~!")
                    ]))
                elif message.asDisplay().startswith('猫鲨'):
                    await app.sendGroupMessage(group, MessageChain.create([
                        At(member.id),Plain("Nyaaaaaaa!")
                    ]))
                elif message.asDisplay().startswith('签到'):
                    relation = gbl.sql.checkdb(member.id,qqbot_item[1])
                    sign_in_times = gbl.sql.checkdb(member.id,qqbot_item[5])
                    if sign_in_times == 0:
                        point = random.randint(1,10)
                        gbl.sql.updatedb(member.id,qqbot_item[1],relation+point)
                        gbl.sql.updatedb(member.id,qqbot_item[5],1)
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
                        Plain("1 bug fixed, 255 bug added")
                    ]))
                elif message.asDisplay().startswith("晚安"):
                    times = int(time.strftime("%H", time.localtime()))
                    if times >= 12 and times <= 17:
                        await app.sendGroupMessage(group, MessageChain.create([
                            At(member.id),Plain(" 才中午.."),
                            ]))
                    elif times >= 5 :
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
                    memelist = glob.glob("./source/memes/*")
                    await app.sendGroupMessage(group, MessageChain.create([    
                        Image.fromLocalFile(random.choice(memelist))
                    ]))
                elif message.asDisplay()== "摸肚子":
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("肚子不能摸啦...")
                    ]))
                elif message.asDisplay().startswith("摸屁股"):
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("hentai!(拍开)")
                    ]))
                elif message.asDisplay().startswith("冲还是不冲?"):
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain(random.choice(['冲!!!', '不冲,注意身体(鲨鲨笑)']))
                    ]))
                ###小游戏###
                if vari.mode == 1:
                    try:
                        if vari.memberid == member.id:
                            msg = int(message.asDisplay())
                            if 1000 <= msg <= 9999 and vari.i != 6:
                                vari.i += 1
                                list_1 = "".join([str(i) for i in vari.num])
                                if gbl.guess.number_guess(msg,int(list_1)) == "AAAA":
                                    if gbl.sql.checkdb(member.id, qqbot_item[6]) != 1:
                                        relation = gbl.sql.checkdb(member.id,qqbot_item[1])
                                        gbl.sql.updatedb(member.id, qqbot_item[1],(10*(vari.guess_chances - vari.i -1)+10)+relation)
                                        gbl.sql.updatedb(member.id, qqbot_item[6], 1)
                                        await app.sendGroupMessage(group, MessageChain.create([
                                            Plain('猜对了!\n'),Plain('好感度+{}'.format(10*(vari.guess_chances - vari.i -1)+10))
                                        ]))  
                                    else:
                                        await app.sendGroupMessage(group, MessageChain.create([
                                            Plain('猜对了!')
                                        ]))
                                    vari.mode = 0
                                    vari.memberid = 0
                                    vari.i = 0
                                    vari.guess_chances = 6
                                    vari.num = ""
                                else:
                                    await app.sendGroupMessage(group, MessageChain.create([
                                        Plain("没猜对，目前进度:\n"+gbl.guess.number_guess(msg,int(list_1))+"\n还剩{}次机会".format(vari.guess_chances-vari.i))
                                    ]))
                            elif member.id == vari.memberid and vari.i == 6 and msg != vari.num:
                                await app.sendGroupMessage(group, MessageChain.create([
                                    Plain('你没猜到...看来得多练习呢!\n'),Plain("数字是:{}".format(vari.num))
                                ]))
                                vari.mode = 0
                                vari.memberid = 0
                                vari.i = 0
                                vari.guess_chances = 6
                                vari.num = ""
                    except Exception as e:
                        print(e)
                elif vari.mode == 2:
                    try: 
                        if vari.memberid == member.id:
                            useless_symbol = ["（","）"," "]
                            useful_symbol = ["(",")",""]
                            expression = message.asDisplay()
                            for i in range(len(useless_symbol)):
                                try:
                                    expression.replace(useless_symbol[i],useful_symbol[i])
                                except Exception as e:
                                    pass
                            eval(expression)
                            print(expression)
                            msg = str(expression)
                            print("here")
                            if gbl.point.point(msg,vari.num) == True:
                                if gbl.sql.checkdb(member.id, qqbot_item[6]) != 1:
                                    relation = gbl.sql.checkdb(member.id,qqbot_item[1])
                                    gbl.sql.updatedb(member.id, qqbot_item[1],(10*(vari.guess_chances - vari.i -1)+10)+relation)
                                    gbl.sql.updatedb(member.id, qqbot_item[6], 1)
                                    await app.sendGroupMessage(group, MessageChain.create([
                                        Plain('答对了!\n'),Plain('好感度+{}'.format(10*(vari.guess_chances - vari.i -1)+10))
                                    ]))
                                    vari.mode = 0
                                    vari.memberid = 0
                                else:
                                    await app.sendGroupMessage(group, MessageChain.create([
                                        Plain('答对了!')
                                    ]))
                                    vari.mode = 0
                                    vari.memberid = 0
                            elif gbl.point.point(msg,vari.num) == False:
                                await app.sendGroupMessage(group, MessageChain.create([
                                    At(member.id),Plain("没猜对，再试试!")
                                ]))
                            elif gbl.point.point(msg,vari.num) == "IncorrectNumber":
                                await app.sendGroupMessage(group, MessageChain.create([
                                    At(member.id),Plain("请使用给出的数字！")
                                ]))
                            elif gbl.point.point(msg,vari.num) == "RepeatNumber":
                                await app.sendGroupMessage(group, MessageChain.create([
                                    At(member.id),Plain("你使用的数字不正确！")
                                ]))
                            # elif gbl.point.point(msg,[int(x) for x in str(vari.num)]) == "IncorrectSymbol":
                            #     await app.sendGroupMessage(group, MessageChain.create([
                            #         At(member.id),Plain("你使用的字符不正确！")
                            #     ]))
                    except:
                        pass
###开始运行###
if __name__ == "__main__":
    app.launch_blocking()
