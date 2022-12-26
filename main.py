import logging

from aiogram import Bot, Dispatcher, executor, types
from yt_dlp import YoutubeDL
from datetime import timedelta
from youtube_search import YoutubeSearch

from db import sql_start, sql_add_user, sql_add_user_name

import os
import hashlib

API_TOKEN = '5964990301:AAFh81A_4AOTRS_B_Ua3CEonRMcyoSko--I'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    await sql_start()


MUSIC_MAX_LENGTH = 3600


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await sql_add_user(user_id=message.from_user.id)
    await sql_add_user_name(user_id=message.from_user.id, user_name=message.from_user.username)
    await message.reply("Достаточно отправить мне ссылку на музыку YouTube\n\nИли найти музыку через мой "
                        "собственный поиск, например:\n@allmusictg_bot DESPACITO REMIX")


def searcher(text):
    result = YoutubeSearch(text, max_results=8).to_dict()
    return result


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or 'echo'
    links = searcher(text)

    articles = [types.InlineQueryResultArticle(
        id=hashlib.md5(f'{link["id"]})'.encode()).hexdigest(),
        title=f'{link["title"]}',
        thumb_url=f'{link["thumbnails"][0]}',
        input_message_content=types.InputMessageContent(
            message_text=f'https://www.youtube.com/watch?v={link["id"]}')
    ) for link in links]

    await query.answer(articles, cache_time=60, is_personal=True)


@dp.message_handler()
async def send_music(message: types.Message):
    await sql_add_user(user_id=message.from_user.id)
    await sql_add_user_name(user_id=message.from_user.id, user_name=message.from_user.username)
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': '%(title)s',
        'noplaylist': True,
    }
    ydl = YoutubeDL(ydl_opts)
    info_dict = ydl.extract_info(message.text, download=False)
    if info_dict['duration'] > MUSIC_MAX_LENGTH:
        readable_max_length = str(timedelta(seconds=MUSIC_MAX_LENGTH))
        await message.reply("🎸 Время вашей песни превышает лимит в 1 час.")
        return
    d_status = await message.reply("💾 Скачиваю...", disable_notification=True)
    ydl.process_info(info_dict)
    audio_file = ydl.prepare_filename(info_dict)
    await bot.send_audio(message.from_user.id, audio=open(audio_file, 'rb'))
    await d_status.delete()
    os.remove(audio_file)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
