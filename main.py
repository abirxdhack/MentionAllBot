import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("mention_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
spam_chats = []

async def is_admin(app, user_id, chat_id):
    try:
        member = await app.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception as e:
        return False

@app.on_message(filters.command(["start"], prefixes=["/", "."]) & (filters.private | filters.group))
async def start(client, message):
    await message.reply(
        "👋 **Welcome to MentionAll Bot!**\n\n"
        "I can help you mention all members in your group or channel with a single command. "
        "Click the buttons below for more information or to get started.\n\n"
        "🔗 **Follow [The Dev](https://github.com/abirxdhack) on GitHub**",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('ℹ️ Help', callback_data='help'),
                    InlineKeyboardButton('📣 Channel', url='https://t.me/abir_x_official')
                ],
                [
                    InlineKeyboardButton('📦 Source', url='https://github.com/abirxdhack/MentionAllBot')
                ]
            ]
        )
    )

@app.on_callback_query(filters.regex("help"))
async def show_help(client, callback_query):
    helptext = """**🆘 Help Menu of MentionAll_Bot**

**Command:** `/mentionall`
__You can use this command with text what you want to say to others.__

`Example: /mentionall Hello , this is the Official Channel Of Abir X Official Community , from here You can get Premium Tips , Premium Account & other giveaways.!`
__You can use this command as a reply to any message. Bot will tag users to that replied message__.

Follow [The Dev](https://github.com/abirxdhack) on Github"""
    await callback_query.message.edit_text(
        helptext,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('🔙 Back', callback_data='start')
                ]
            ]
        )
    )

@app.on_callback_query(filters.regex("start"))
async def show_start(client, callback_query):
    await callback_query.message.edit_text(
        "👋 **Welcome to MentionAll Bot!**\n\n"
        "I can help you mention all members in your group or channel with a single command. "
        "Click the buttons below for more information or to get started.\n\n"
        "🔗 **Follow [The Dev](https://github.com/abirxdhack) on GitHub**",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('ℹ️ Help', callback_data='help'),
                    InlineKeyboardButton('📣 Channel', url='https://t.me/abir_x_official')
                ],
                [
                    InlineKeyboardButton('📦 Source', url='https://github.com/abirxdhack/MentionAllBot')
                ]
            ]
        )
    )

@app.on_message(filters.command(["mentionall"], prefixes=["/", "."]) & filters.group)
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        return await message.reply("❌ **This command can be used in groups and channels!**")
    
    if message.from_user is not None:
        user_id = message.from_user.id
    elif message.sender_chat is not None:
        user_id = message.sender_chat.id
    else:
        return await message.reply("🚫 **Unable to determine user ID!**")
    
    if not await is_admin(client, user_id, chat_id):
        return await message.reply("🚫 **Only admins can mention all members!**")
    
    if message.command and message.reply_to_message:
        return await message.reply("❗ **Give me one argument!**")
    elif message.command:
        mode = "text_on_cmd"
        msg = message.text[len("/mentionall "):]
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if msg is None:
            return await message.reply("⚠️ **I can't mention members for older messages! (messages which are sent before I'm added to this group)**")
    else:
        return await message.reply("❓ **Reply to a message or give me some text to mention others!**")
    
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ''
    
    async for usr in client.get_chat_members(chat_id):
        if chat_id not in spam_chats:
            break
        usrnum += 1
        usrtxt += f"👤 [{usr.user.first_name}](tg://user?id={usr.user.id}) "
        if usrnum == 5:
            if mode == "text_on_cmd":
                txt = f"{usrtxt}\n\n**{msg}**"
                await client.send_message(
                    chat_id, 
                    txt, 
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('📣 Channel', url='https://t.me/abir_x_official'),
                                InlineKeyboardButton('📦 Source', url='https://github.com/abirxdhack/MentionAllBot')
                            ]
                        ]
                    )
                )
            elif mode == "text_on_reply":
                await msg.reply(
                    usrtxt, 
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('📣 Channel', url='https://t.me/abir_x_official'),
                                InlineKeyboardButton('📦 Source', url='https://github.com/abirxdhack/MentionAllBot')
                            ]
                        ]
                    )
                )
            await asyncio.sleep(2)
            usrnum = 0
            usrtxt = ''
    
    try:
        spam_chats.remove(chat_id)
    except:
        pass

@app.on_message(filters.command(["cancel"], prefixes=["/", "."]) & filters.group)
async def cancel_spam(client, message):
    if message.chat.id not in spam_chats:
        return await message.reply('ℹ️ **There is no process ongoing...**')
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply('✅ **Stopped MentionAll**')

print("Bot Successfully Started! 💥")
app.run()
