from asyncio.exceptions import TimeoutError
from Data import Data
from pyrogram import Client, filters
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError,
)


@Client.on_message(filters.private & ~filters.forwarded & filters.command("generate"))
async def main(_, msg):
    await msg.reply(
        "اختر الجلسة المراد استخراجها من الأسفل ",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("بـايـࢪوجـرام", callback_data="pyrogram"),
                    InlineKeyboardButton("تـيلـيثـون", callback_data="telethon"),
                ]
            ]
        ),
    )


async def generate_session(bot, msg, telethon=False):
    await msg.reply(
        "- يـتم الان بـدأ صـنـع الـكود {}...".format(
            "Telethon" if telethon else "Pyrogram"
        )
    )
    user_id = msg.chat.id
    api_id_msg = await bot.ask(
        user_id, "- الان اࢪسـل ايـبـي المـكـون مـن 8 اࢪقـام`API_ID` .", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply(
            "- غـيࢪ مـتاحـه API_ID (which must be an integer). الـࢪجـاء قـم بـاعـاده اخـࢪاج الـجـلسـه مـن الـبدايـه /start.",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    api_hash_msg = await bot.ask(
        user_id, "- الان اࢪسـل ايـبـي هـاش `API_HASH` .", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(
        user_id,
        "الآن أرسل رقم الهاتف الخاص بك`𝘱𝘩𝘰𝘯𝘦_𝘯𝘶𝘮𝘣𝘦𝘳` مع كتابة ࢪمز الـدولـه. \nمثال : `+964xxxxxxxxxx`",
        filters=filters.text,
    )
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("- اࢪسـل لـي الـكـود...")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    else:
        client = Client(":memory:", api_id, api_hash)
    await client.connect()
    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply(
            "- الايـبـي ايـدي والايـبي هـاش فـيهم خـطأ الـࢪجـاء اعادة الاسـتخـࢪاج مـن جـديـد .",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply(
            "`PHONE_NUMBER` رقم الهاتف الخاص بك غير صحيح يرجى إعادة الاستخراج مرة أخرى ",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    try:
        phone_code_msg = await bot.ask(user_id, "- حـسـنًا تـم اࢪسـال كـود الـتحـقـق الـيك مـن قِـبـل تـيـليـكرام   الان انـسـخ الـكود وضـع مـسافـه مـا بـين كـل ࢪقـم هـكذا  : 6 7 7 7 5.", filters=filters.text, timeout=600)
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply(
            "لقد تجاوزت الحد الزمني 10 دقائق أعد استخراج الجلسة مرة أخرى.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply(
            " رقـم الـهاتـف خـطـأ الـࢪجـاء الـتـأكد مـنه واعـادة الاسـتخـراج مـن جـديـد ",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply(
            "الكود الذي أدخلته خاطئ يرجى إعادة الإستخراج مرة أخرى",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(
                user_id,
                "يـبـدو ان حـسـابـد مفعـل ࢪمـز الـتـحـقق بـخـطـوتـين الـرجـاء اࢪسـال الـࢪمـز الان",
                filters=filters.text,
                timeout=300,
            )
        except TimeoutError:
            await msg.reply(
                "لقد تجاوزت المدة الزمنية يجب عليك إعادة استخراج الجلسة مرة أخرى",
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
        try:
            password = two_step_msg.text
            if telethon:
                await client.sign_in(password=password)
            else:
                await client.check_password(password=password)
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply(
                "عـذرًا رمـز التـحقـق غيـر صـحـيح الـࢪجـاء الاسـتـخـࢪاج مـن جـديـد /start",
                quote=True,
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = "**{} Black session ** \n\n`{}` \n\n\ تـم بـنـجـاح اࢪسـال الـكـود الـࢪجـاء الـتـأكـد مـن الرسـائل المحـفوظة  Dev:  @a_t_9".format(
"TELETHON" if telethon else "PYROGRAM", string_session
    )
    try:
        await client.send_message("me", text)
    except KeyError:
        pass
    await client.disconnect()
    await phone_code_msg.reply(
        " {} Black session . \n\n تـم بـنـجـاح اࢪسـال الـكـود الـࢪجـاء الـتـأكـد مـن الرسـائل المحـفوظة  Dev:  @a_t_9 \n\n".format(
            "TELETHON" if telethon else "PYROGRAM"
        )
    )


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply(
            "- تـم الـغاء عـملـية الاسـتـخـراج .",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    elif "/restart" in msg.text:
        await msg.reply(
            "تـم الانـتـه‍اء مـن التـࢪسيـت",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("- تـم الـغاء عـملـية الاسـتـخـراج .", quote=True)
        return True
    else:
        return False 
