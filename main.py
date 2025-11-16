from vkbottle.bot import Bot, Message, BotLabeler
import os

labeler = BotLabeler()
labeler.vbml_ignore_case = True  # игнорируем регистр
labeler.auto_rules = [lambda m: m.from_id > 0]  # разрешаем сообщения из чатов сообществ

bot = Bot(token=os.getenv("TOKEN"), labeler=labeler)

@bot.on.message()
async def handler(message: Message):
    if not message.text:
        return

    text = message.text.strip().lower()

    if text in ["!пинг", ".пинг", "пинг", "!ping"]:
        await message.answer("⚫ Onyx онлайн | 2025 | Работает в чатах сообществ!")

    if text in ["!помощь", "!help", "помощь"]:
        await message.answer("⚫ Onyx живой!\nСкоро добавим все команды")

print("Onyx полностью запущен в чатах сообществ ⚫")
bot.run_polling()
