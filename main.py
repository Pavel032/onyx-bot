# main.py — работает на vkbottle 4.3.3 + Railway
from vkbottle.bot import Bot, Message
import os

# Только токен — group_id не нужен и вызывает ошибки
bot = Bot(token=os.getenv("TOKEN"))

@bot.on.message()  # Ловим ВСЁ, включая чаты сообществ
async def handler(message: Message):
    if not message.text:
        return

    text = message.text.strip().lower()

    if text in ["!пинг", "пинг", ".пинг", "!ping"]:
        await message.answer("Onyx живой!\n17.11.2025 — наконец-то полная победа в чатах сообществ!")

    if text in ["!помощь", "!help"]:
        await message.answer("Onyx 100% работает!")

print("Onyx запущен — ждёт сообщений из чатов сообществ")

if __name__ == "__main__":
    bot.run_forever()   # ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
                        # Именно run_forever(), а НЕ run_polling()!
