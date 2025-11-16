from vkbottle.bot import Bot, Message
import os

bot = Bot(token=os.getenv("TOKEN"))

# Работаем со строчными буквами вручную (универсально для всех версий)
@bot.on.chat_message()
async def handler(message: Message):
    if not message.text:
        return
    
    text = message.text.strip().lower()
    
    if text in ["!пинг", ".пинг"]:
        await message.answer("Onyx онлайн | <5мс | 100 % живой!")
    
    if text in ["!помощь", "!help"]:
        await message.answer("""Onyx • Чат-менеджер 2025

!пинг — проверка бота
!помощь — это меню
Скоро: !бан, !кик, !варн, статистика, топ, антимат и мини-приложение""")

print("Onyx полностью запущен ⚫")
bot.run_forever()
