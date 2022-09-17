from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telebot.async_telebot import AsyncTeleBot

from utils.logger import log

from utils.database import TagDatabase, AdminDatabase

db_tags = TagDatabase()
db_admins = AdminDatabase()


def create_hashtag_markup() -> InlineKeyboardMarkup:
    """Метод создающий разметку сообщения

    Returns:
        InlineKeyboardMarkup: Разметка сообщения
    """
    hashtag_markup = InlineKeyboardMarkup()
    for hashtag in db_tags.tags:
        print(f'\'{hashtag.get("tag")}\'')
        hashtag_button = InlineKeyboardButton(f'\'{hashtag.get("tag")}\'',callback_data=f'\'{hashtag.get("tag")}\'')
        hashtag_markup.add(hashtag_button)
    return hashtag_markup


def check_permissions(user_id: int):
    return user_id in [item['id'] for item in db_admins.admins]



async def callback_query(call: CallbackQuery, bot: AsyncTeleBot):
    log.info('callback data from callback query id %s is \'%s\'', call.id, call.data)

    #Проверка на наличие пользователя в списке администраторов
    if not check_permissions(call.from_user.id):
        return

    print(call)
    if call.data == 'accept':
        await bot.send_message(call.from_user.id, 'Выберите хештеги для поста', reply_markup=create_hashtag_markup())
    elif call.data == 'decline':
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text=f'{call.message.text}\t😡ОТКЛОНЕНО😡')


async def cmd_add_hashtag(message: Message, bot: AsyncTeleBot):
    if not check_permissions(message.from_user.id):
        bot.reply_to(message, "У вас нет прав на выполнение этой команды!")
    else:
        text = message.text.replace('/add_hashtag', '')
        hashtags = text.split()
        for hashtag in hashtags:
            db_tags.tags = hashtag


async def cmd_add_admin(message: Message, bot: AsyncTeleBot):
    if not check_permissions(message.from_user.id):
        bot.reply_to(message, 'У вас нет прав на выполнение этой команды')
    else:
        contact = message.contact
        db_admins.admins = {'id':contact.user_id, 'fullname': contact.first_name + contact.last_name, 'username':None}


async def cmd_remove_admin(message: Message, bot: AsyncTeleBot):
    if not check_permissions(message.from_user.id):
        bot.reply_to(message, 'У вас нет прав на выполнение этой команды')
    else:
        text = message.text.replace('/remove_admin', '').strip().replace('@','')
        db_admins.remove_admin(username=text)


async def cmd_remove_hashtag(message: Message, bot: AsyncTeleBot):
    if not check_permissions(message.from_user.id):
        bot.reply_to(message, 'У вас нет прав на выполнение этой команды')
    else:
        hashtags = message.text.replace('/remove_hashtag', '').strip().split()
        for hashtag in hashtags:
            db_tags.remove_tag(hashtag)



def on_hashtag_choose():
    pass
