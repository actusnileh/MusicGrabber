from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from yt_dlp import YoutubeDL

import os

from constant.music import (
    DOWNLOAD_TEXT,
    ERROR_DOWNLOAD_MUSIC_TEXT,
    MAX_LENGTH_ERROR_TEXT,
)
from common.settings import settings

router = Router()

music_max_length = settings.music_max_length


@router.message(F.text)
async def send_music(message: Message):
    download_message = await message.reply(DOWNLOAD_TEXT)
    quality_str = "bestaudio/best"
    ydl_opts = {
        "format": quality_str,
        "outtmpl": "TEMP/%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "merge_output_format": "mp3",
    }

    try:
        ydl = YoutubeDL(ydl_opts)
        info_dict = ydl.extract_info(message.text, download=False)

        if info_dict["duration"] > music_max_length:
            await message.edit_text(MAX_LENGTH_ERROR_TEXT)
            return

        ydl.process_info(info_dict)
        audio_file = ydl.prepare_filename(info_dict)

        audio_path = FSInputFile(audio_file)

        await message.reply_audio(audio=audio_path, caption="")
    except Exception as e:
        print(e)
        await download_message.delete()
        await message.reply(ERROR_DOWNLOAD_MUSIC_TEXT)
        if os.path.exists(audio_file):
            os.remove(audio_file)
    else:
        await download_message.delete()
        if os.path.exists(audio_file):
            os.remove(audio_file)
