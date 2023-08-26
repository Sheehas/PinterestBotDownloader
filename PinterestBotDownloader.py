from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import Message
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import aiohttp
import re
import os
import io

load_dotenv()

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

async def send_media(url, chat_id, sent_message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    html_content = await response.text()
                    soup = BeautifulSoup(html_content, "html.parser")
                    img_tags = soup.find_all("img")[:-1]

                    if len(img_tags) > 0:
                        saved_images = set()

                        for img in img_tags:
                            img_url = img["src"]
                            img_name = img_url.split("/")[-1]

                            if img_name not in saved_images:
                                img_data = requests.get(img_url).content
                                document = types.InputFile(io.BytesIO(img_data), filename=img_name)
                                await sent_message.edit_text('Sending photo!')
                                await bot.send_document(chat_id, document)
                                saved_images.add(img_name)
                    else:
                        video_content = await response.text()
                        video_url = video_content.split('contentUrl":"')[1].split('"')[0]
                        await sent_message.edit_text('Page found!\nSending video!')
                        await bot.send_video(chat_id, video_url)
                else:
                    await sent_message.edit_text("An error occurred while fetching the page.")
    except aiohttp.client_exceptions.InvalidURL:
        await sent_message.edit_text("Invalid link. Please provide a valid Pinterest link.")

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Hi! Send me a link to a photo or video, and I'll upload it as a document.")

@dp.message_handler()
async def handle_message(message: types.Message):
    sent_message = await message.reply(text='Processing...')  # Sending a message via the bot

    if re.match(r"https?://pin\.it/[A-Za-z0-9]+", message.text):
        link_code = message.text.split("/")[-1]
        api_link = f"https://api.pinterest.com/url_shortener/{link_code}/redirect/"
        response = requests.get(api_link, allow_redirects=False)
        redirect_location = response.headers.get('Location')

        pin_link = redirect_location.split('?')[0].rstrip('/sent')
        profile_link = redirect_location.split('&')[1].split('=')[1]

        inline_buttons = [
            types.InlineKeyboardButton(text="Original Link", url=f'{pin_link}/'),
            types.InlineKeyboardButton(text="Link to the creator's profile.", url=f"https://www.pinterest.ch/{profile_link}/")
        ]

        inline_keyboard = types.InlineKeyboardMarkup().add(*inline_buttons)

        await message.reply("Choose the desired link:", reply_markup=inline_keyboard)

        await send_media(pin_link, message.chat.id, sent_message)

    else:
        url = message.text.strip()
        if url.startswith("https://"):
            try:
                await send_media(url, message.chat.id, sent_message)
            except:
                pass
        else:
            await sent_message.edit_text("Please send a link from Pinterest platform.")

if __name__ == '__main__':
    executor.start_polling(dp)