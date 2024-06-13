import hashlib
from youtube_search import YoutubeSearch
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram import Router

router = Router()


def searcher(text):
    result = YoutubeSearch(text, max_results=8).to_dict()
    return result


@router.inline_query()
async def inline_handler(query: InlineQuery):
    text = query.query or "echo"
    links = searcher(text)

    articles = [
        InlineQueryResultArticle(
            id=hashlib.md5(f'{link["id"]})'.encode()).hexdigest(),
            title=f'{link["title"]}',
            thumbnail_url=f'{link["thumbnails"][0]}',
            input_message_content=InputTextMessageContent(
                message_text=f'https://www.youtube.com/watch?v={link["id"]}'
            ),
        )
        for link in links
    ]

    await query.answer(articles, is_personal=True)
