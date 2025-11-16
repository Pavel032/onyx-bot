# main.py — правильный бот для ВКонтакте (Onyx)
from vkbottle import Bot, GroupEventType, GroupTypes, VKAPIError
from vkbottle.tools import DocMessagesUploader
import asyncio

token = "vk1.a.shvMGIjJv63BUINdZTS2jXbVB8xUBEYgRCeOgz9dMTg-wQKvCHJUEFUuyEKJWGCel0UrUtmedlV5d46FtW0lkWfKjQGeagp5Z3CDtvyYd6z5inaKTXKHjyORgnznWP4Kn5RLqQlGTmxoqdo_bxARDJpVGRzha-pCvAX02jApDPDDhteoWqOLVp5frt6NHK1IPa4B2Hm2lF1WDkRue-m07Q"  # твой токен

bot = Bot(token)

@bot.on.chat_message(text="!пинг")
async def ping(message):
    await message.answer("Onyx онлайн ⚫")

@bot.on.chat_message(text="!помощь")
async def help_cmd(message):
    await message.answer("""Onyx • Чат-менеджер

!бан @user — бан
!кик @user — кик
!варн @user — предупреждение
!удалить 10 — удалить 10 сообщений
!стата — твоя статистика""")

print("Onyx запущен ⚫")
bot.run_forever()
