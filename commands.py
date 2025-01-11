from aiogram.client.default import DefaultBotProperties
from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.enums import ParseMode

from utils import *


dp = Dispatcher()
bot = Bot(token=read_from_file("config.json", 'token'), default=DefaultBotProperties(parse_mode = ParseMode.HTML))
db = Database()


async def check_admin_status(message, bot):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    bot = await bot.get_chat_member(message.chat.id, bot.id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR] or bot.status != ChatMemberStatus.ADMINISTRATOR:
        return False
    return True

@dp.message(Command("ban"))
async def command_ban(message: Message, command: CommandObject, bot: Bot):
    try:
        reply_message = message.reply_to_message

        if not await check_admin_status(message, bot):
            raise NotAdmin
        
        date = calc_time(command.args)

        await bot.ban_chat_member(chat_id=message.chat.id, user_id=reply_message.from_user.id)
        db.write_to(reply_message.from_user.username, reply_message.from_user.id, "ban")
        write_to_log('changelog.txt', f'Пользователь {reply_message.from_user.username} был забанен {message.from_user.username} до {date}')
        await message.delete()


    except NotAdmin:
        await message.reply("У вас нет прав, соболезную 🤣")

@dp.message(Command("mute"))
async def command_mute(message: Message, command: CommandObject, bot: Bot):
    try:
        reply_message = message.reply_to_message

        if not await check_admin_status(message, bot):
            raise NotAdmin
        
        date = calc_time(command.args)

        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=reply_message.from_user.id, until_date=date, permissions=types.ChatPermissions(can_send_messages=False))
        db.write_to(reply_message.from_user.username, reply_message.from_user.id, "mute")
        write_to_log('changelog.txt', f'Пользователь {reply_message.from_user.username} получил мут от {message.from_user.username} до {date}')
        await message.delete()

    except NotAdmin:
        await message.reply("У вас нет прав, соболезную 🤣")

@dp.message(Command("unban"))
async def command_unban(message: Message, command: CommandObject, bot: Bot):
    try:
        member=int(str(db.read(str(command.args)[1:])[0])[1:-2])

        if not await check_admin_status(message, bot):
            raise NotAdmin

        await bot.unban_chat_member(chat_id=message.chat.id, user_id=member)
        db.delete_from(str(command.args)[1:])
        write_to_log('changelog.txt', f'Пользователь {command.args} больше не в бане')
        await message.delete()

    except IndexError:
        await bot.send_message(chat_id=message.from_user.id, text="Данный пользователь не в чем не виновен")
    except NotAdmin:
        await message.reply("У вас нет прав, соболезную 🤣")


@dp.message(Command("unmute"))
async def command_unmute(message: Message, command: CommandObject, bot: Bot):
    try:
        if not await check_admin_status(message, bot):
            raise NotAdmin
        
        member=int(str(db.read(str(command.args)[1:])[0])[1:-2])

        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=member, permissions=types.ChatPermissions(can_send_messages=True))
        db.delete_from(str(command.args)[1:])
        write_to_log('changelog.txt', f'Пользователь {command.args} больше не в муте')
        await message.delete()
        
    except IndexError:
        await bot.send_message(chat_id=message.from_user.id, text="Данный пользователь не в чем не виновен")
    except NotAdmin:
        await message.reply("У вас нет прав, соболезную 🤣")

@dp.message(Command("set_admin"))
async def set_all_admin(message: Message):
    members = await bot.get_chat_administrators(message.chat.id)
    for admin in members:
        db.add_admin(admin.user.username)
    await message.delete()

@dp.message(Command("get_admin"))
async def get_all_admin(message: Message):
    admin_list = "Список администраторов:"
    if db.check_admin(message.from_user.username):
        for i in db.get_admin():
            admin_list = admin_list + "\n" + "@" + str(i)[2:-3]
    await message.reply(admin_list)

@dp.message(Command("get_mute"))
async def get_all_admin(message: Message):
    mute_list = "Список пользователей, которые получили мут:"
    if db.check_admin(message.from_user.username):
        for i in db.get_mute():
            mute_list = mute_list + "\n" + "@" + str(i)[2:-3]
    await message.reply(mute_list)

@dp.message(Command("get_ban"))
async def get_all_admin(message: Message):
    ban_list = "Список пользователей, которые получили бан:"
    if db.check_admin(message.from_user.username):
        for i in db.get_ban():
            ban_list = ban_list + "\n" + "@" + str(i)[2:-3]
    await message.reply(ban_list)
        
