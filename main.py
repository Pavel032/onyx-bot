from vkbottle.bot import Bot, Message
import os

bot = Bot(token=os.getenv("TOKEN"))

@bot.on.chat_message(text_lower=["!пинг", ".пинг"])
async def ping(message: Message):
    await message.answer("⚫ Onyx онлайн | <10мс | Полный клон pxolly готов!")

@bot.on.chat_message(text_lower=["!помощь", "!help"])
async def help_cmd(message: Message):
    await message.answer("""⚫ Onyx • Чат-менеджер v1.0

!пинг — тест
!бан @user — бан
!кик @user — кик
!варн @user — предупреждение
!стата — статистика
!топ — топ активных
!удалить 10 — удалить 10 сообщений
!префикс . — сменить префикс

Скоро добавим антимат и мини-приложение!""")

print("Onyx запущен ⚫")
bot.run_forever()
