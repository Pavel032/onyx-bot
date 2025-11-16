from vkbottle.bot import Bot, Message
import os

bot = Bot(token=os.getenv("TOKEN"))

# Самый надёжный способ ловить ВСЕ сообщения из чатов сообществ
@bot.on.raw_event(2, lambda x: True)  # 2 = новое сообщение в беседе
async def handle_message(event):
    try:
        msg = Message.from_dict(event["object"]["message"], bot)
        text = msg.text.strip().lower() if msg.text else ""

        if text in ["!пинг", ".пинг", "пинг", "!ping"]:
            await msg.answer("Onyx онлайн | 2025 | 100 % живой в чатах сообществ!")

        if text in ["!помощь", "!help", "помощь"]:
            await msg.answer("Onyx полностью работает!\nСкоро добавим все команды")

    except Exception as e:
        print("Ошибка:", e)

print("Onyx запущен и ловит сообщения из чатов сообществ ⚫")
bot.run_polling()
