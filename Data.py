from pyrogram.types import InlineKeyboardButton


class Data:
    generate_single_button = [
        InlineKeyboardButton(" ابـدا بأسـتخـدام كـود ", callback_data="generate")
    ]

    home_buttons = [
        generate_single_button,
        [InlineKeyboardButton(text=" الرجوع ", callback_data="home")],
    ]

    generate_button = [generate_single_button]

    buttons = [
        generate_single_button,
        [
            InlineKeyboardButton(
                "𝙨𝙚𝙘𝙪𝙧𝙚 𝙥𝙞𝙘𝙩𝙝𝙤𝙣", url="https://t.me/PICTH0N"
            )
        ],
        [
            InlineKeyboardButton(" - طريقة الاستخدام؟ . ", callback_data="help"),
            InlineKeyboardButton(" - حول البوت . ", callback_data="about"),
        ],
        [InlineKeyboardButton("𝗗𝗘𝗩", url="https://t.me/a_t_9")],
    ]

    START = """  - {} اهـلا عـزيـزي 
اهـلاً بـك فـي {}
يـعـمل هـذا الـبوت لـمـساعـدتـك بـطـريقـة سـهله للـحصـول علـى كـود تـيـرمكس او كـود بـايـࢪوجـرام
𝗗𝗘𝗩 :- @a_t_9
    """

    HELP = """
 ** - طريقة الاستخدام؟ . **

/about - لحول البوت
/help - لمساعدتك
/start - لبدء البوت 
/repo - لإعطاء ريبو البوت
/generate - لاستخراج الجلسات 
/cancel - لإلغاء الاستخراج 
/restart - لترسيت اليوت
"""

    # About Message
    ABOUT = """
**حول البوت** 

هذا هو بوت استخراج كود تيرمكس وبايروجرام مقدم من @a_t_9

قناة السورس : [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://t.me/PICTH0N)
لغة البرمجة : [ᴘʏʀᴏɢʀᴀᴍ](docs.pyrogram.org)
اللغة : [ᴘʏᴛʜᴏɴ](www.python.org)
𝗗𝗘𝗩 : @a_t_9
    """

    # Repo Message
    REPO = """
انا بوت وظيفتي اساعدك باستخراج مود بايروغرام و تيرمكس

My . [✨](https://t.me/a_t_9)
𝗗𝗘𝗩𝗦 : [اضغط هنا](https://t.me/a_t_9)
السورس [𝙨𝙚𝙘𝙪𝙧𝙚 𝙥𝙞𝙘𝙩𝙝𝙤𝙣](https://t.me/PICTH0N)

إذا كان لديك أي سؤال ، فراسل » المطور » [𝗗𝗘𝗩] @a_t_9
   """
