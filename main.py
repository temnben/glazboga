# First of all, you need to register and get a subscription to this api:
# https://probivapi.com/

from aiogram.types import Message, BufferedInputFile
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import requests
import asyncio
import base64
import io

# Telegram bot token
API_TOKEN = 7977536412:AAGah6_F1UvbSAdkcqHl6q7YQNxWvFvfudY

# ProbivAPI secret key
PROBIVAPI_KEY = 34d4f219-c2fb-4e51-a954-d003d6905dcb

# Initialize bot and dispatcher
bot = Bot(token=7977536412:AAGah6_F1UvbSAdkcqHl6q7YQNxWvFvfudY)
dp = Dispatcher()

print("!BOT STARTED!")

# Message handler that sends greeting when bot started
@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Probiv Bot Template by DimonDev: @probivapi")


# This is the main probiv function that returns a json and formats it, then sends it
@dp.message()
async def text(message: Message):
    # Get the message text and interpret it as a phone number
    nomer = message.text
    print(nomer)

    # The endpoint for the probiv API that passes as a query the phone number
    url = f"https://probivapi.com/api/phone/info/{+79291781964}"
    pic_url = f"https://probivapi.com/api/phone/pic/{+79291781964}"

    # Necessary headers for the API to work
    head = {
        # API key that you can get by subscribing to the API
        "X-Auth": 34d4f219-c2fb-4e51-a954-d003d6905dcb
    }

    # Send the request with all the parameters and print the result for debugging
    response = requests.get(url, headers=head)
    print(response.text)

    # Send the request for the profile picture and print the result for debugging
    pic_response = requests.get(pic_url, headers=head)
    # print(pic_response.text)

    # Load the data of the response into a JSON object
    try:
        json_response = response.json()
    except Exception:
        json_response = {}

    # Decode picture from base64
    try:
        pic_data = base64.b64decode(pic_response.text)
    except Exception:
        pic_data = None

    # Integrated CallApp API
    callapp_data = json_response.get('callapp', {})
    callapp_api_name = callapp_data.get('name', 'Not found')
    callapp_emails = ', '.join([email.get('email') for email in callapp_data.get('emails', [])])
    callapp_websites = ', '.join([site.get('websiteUrl') for site in callapp_data.get('websites', [])])
    callapp_addresses = ', '.join([addr.get('street') for addr in callapp_data.get('addresses', [])])
    callapp_description = callapp_data.get('description', 'Not found')
    callapp_opening_hours = ', '.join([f"{day}: {', '.join(hours)}" for day, hours in callapp_data.get('openingHours', {}).items()])
    callapp_lat = callapp_data.get('lat', 'Not found')
    callapp_lng = callapp_data.get('lng', 'Not found')
    callapp_spam_score = callapp_data.get('spamScore', 'Not found')
    callapp_priority = callapp_data.get('priority', 'Not found')

    # Integrated EyeCon API
    eyecon_api_name = json_response.get('eyecon', 'Not found')
    
    # Integrated ViewCaller API
    viewcaller_name_list = [tag.get('name', 'Not found') for tag in json_response.get('viewcaller', [])]
    viewcaller_api_name = ', '.join(viewcaller_name_list)

    dosie = f"""┏ ✅ Dosie for {nomer}
┣ 📱 ФИО (CallApp): {callapp_api_name}
┣ 📧 Emails (CallApp): {callapp_emails}
┣ 🌐 Сайты (CallApp): {callapp_websites}
┣ 🏠 Адреса (CallApp): {callapp_addresses}
┣ 📝 Описание (CallApp): {callapp_description}
┣ 🕒 Часы работы (CallApp): {callapp_opening_hours}
┣ 🌍 Координаты (CallApp): {callapp_lat}, {callapp_lng}
┣ ⚠️ Spam Score (CallApp): {callapp_spam_score}
┣ ⭐ Priority (CallApp): {callapp_priority}
┣ 🌐 ФИО (EyeCon): {eyecon_api_name}
┣ 🔎 ФИО (ViewCaller): {viewcaller_api_name}
┗ 👇 Еще...

@probivapi
                        
Код бота: https://github.com/dimondevceo/glazboga/

Пробив API: https://probivapi.com"""

    # Send the formatted data to the user on Telegram
    if pic_data:
        pic_bytes = bytes(pic_data)
        await message.answer_photo(BufferedInputFile(pic_bytes, filename=f"{nomer}.jpg"), caption=dosie)
    else:
        await message.answer(dosie)


# Main loop
async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
