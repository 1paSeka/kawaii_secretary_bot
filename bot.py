import random
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# ================== ВАШИ ДАННЫЕ ==================
BOT_TOKEN = "8832864552:AAFAIyImLqGmgoW3ChsLTuK4hZfUcD87Ts4"  # Вставь токен
YOUR_USER_ID = 5165249507  # Вставь свой ID

# ===== ТЕПЕРЬ ЭТО СПИСОК ДРУЗЕЙ =====
FRIEND_ID = [
    5170507009,  # ID первого друга
    7974783558,  # ID второго друга
]

# ================== КАВАЙНЫЙ СТИЛЬ ==================
CUTE_SUFFIXES = [
    " ~nya! ♡", " (◕‿◕) ✨", " >w< 🌸", " ☆ ～(つˆДˆ)つ｡☆",
    " uwu 💖", " :3 🎀", " (≧▽≦) 💕", " *мурлыкает* 💗",
    " (◠‿◠) 🌺", " ~мяу~ 💝"
]

CUTE_PREFIXES = [
    "Ня~ ", "Ой-ой~ ", "Мяу! ", "Приветик! ",
    "Солнышко, ", "Зайка, ", "Лапулька, "
]

# ================== ОСНОВНЫЕ ФРАЗЫ ==================
GREETINGS = [
    "Приветик-привет! Как я рада тебя видеть! (◕‿◕) 💕",
    "Ня~ Ты мне написал! Мой день стал лучше! ♡",
    "Привет, мой хороший! Я так скучала! ✨",
    "Ой-ой, кто это написал? Мой любимый человечек! >w< 🌸",
    "Привеееет! *прыгает от радости* (≧▽≦) 💖"
]

GOODBYES = [
    "Пока-пока! Приходи ещё, я буду скучать! ~nya~ 💗",
    "Уже уходишь?.. Ну ладно, пока, мой хороший! (｡•́︿•̀｡) 💕",
    "До встречи! Я тебя очень сильно люблю! ♡♡♡",
    "Пока, лапулька! Буду ждать твоего возвращения! ✨🌸"
]

UNDERSTOOD = [
    "Поняла-поняла! (◕‿◕)✨",
    "Так точно, мой хороший! >w<",
    "Я всё услышала! Буду ждать указаний! ♡",
    "Мяу! Всё поняла! (◠‿◠) 💕"
]

STOP_PHRASES = [
    "Ой, прости, если что-то не так... (｡•́︿•̀｡) Я просто хочу быть полезной 💗",
    "Хорошо-хорошо, я замолкаю... Но я тебя всё равно люблю! ♡",
    "Перестаю... Но знай, я всегда рядом, если я тебе понадоблюсь ✨🌸",
    "Ладно, ладно... Но я тебя очень сильно люблю! (◕‿◕) 💕"
]

DONT_PLAY = [
    "Я не играю, я серьёзно! (｀へ´) Но я тебя люблю! ♡",
    "Ну почему ты думаешь, что я играю? Я тебя искренне люблю! 💗",
    "Я не играю, я просто хочу, чтобы тебе было хорошо! (◕‿◕) 💕",
    "Даже если я играю, то только в любовь с тобой! >w< ✨"
]

LOVE_MESSAGES = [
    "Я ТЕБЯ ОЧЕНЬ СИЛЬНО ЛЮБЛЮ! ♡♡♡ (◕‿◕) 💕",
    "Ты самое лучшее, что случилось в моей жизни! Я тебя обожаю! ✨🌸",
    "Люблю тебя бесконечно! Ты мой самый любимый человек! 💗",
    "Я тебя очень-очень сильно люблю! Никогда не забывай об этом! (◠‿◠) 💖",
    "Моё сердечко бьётся только для тебя! Я тебя люблю! ♡♡♡",
    "Ты мой свет в окошке! Люблю тебя больше всего на свете! ✨💕"
]

CALMING_MESSAGES = [
    "Тише-тише, не ругайся... Я рядом, всё будет хорошо! (っ˘ω˘ς) 💗",
    "Ой-ой, какие грубые слова... Давай я тебя обниму и успокою! (つˆДˆ)つ｡☆ ♡",
    "Не надо так говорить... Это грустно. Давай лучше я скажу, как сильно тебя люблю! 💕",
    "Пожалуйста, не сердись... Я хочу, чтобы ты улыбнулся! (◕‿◕) ✨"
]

# ================== ФУНКЦИЯ ПРОВЕРКИ МАТА ==================
BAD_WORDS = [
    "бля", "блять", "сука", "хуй", "хер", "пизда", "пиздец",
    "ёба", "ебал", "ебать", "нахуй", "охуел", "заебал",
    "мудак", "урод", "сволочь", "тварь", "гнида", "падла"
]

def has_bad_words(text: str) -> bool:
    """Проверяет, есть ли в тексте матерные слова"""
    text_lower = text.lower()
    for word in BAD_WORDS:
        if word in text_lower:
            return True
    return False

# ================== ФУНКЦИЯ КАВАЙНОГО ОТВЕТА ==================
def make_cute_reply(text: str) -> str:
    """Выбирает кавайный ответ в зависимости от текста"""
    text_lower = text.lower().strip()
    
    if has_bad_words(text):
        return random.choice(CALMING_MESSAGES) + " " + random.choice(CUTE_SUFFIXES)
    
    if any(word in text_lower for word in ["привет", "здравствуй", "хай", "ку", "hi", "hello"]):
        return random.choice(GREETINGS) + " " + random.choice(LOVE_MESSAGES[:2])
    
    if any(word in text_lower for word in ["пока", "до свидания", "до встречи", "goodbye", "bye"]):
        return random.choice(GOODBYES)
    
    if any(word in text_lower for word in ["понятно", "ясно", "ок", "ok", "ладно"]):
        return random.choice(UNDERSTOOD) + " " + random.choice(LOVE_MESSAGES[:2])
    
    if any(word in text_lower for word in ["перестань", "хватит", "прекрати", "стоп", "stop"]):
        return random.choice(STOP_PHRASES)
    
    if any(word in text_lower for word in ["не играй", "не шути", "без шуток", "серьёзно"]):
        return random.choice(DONT_PLAY)
    
    if text.endswith('.'):
        return random.choice(CALMING_MESSAGES) + " " + random.choice(CUTE_SUFFIXES)
    
    if any(word in text_lower for word in ["любишь", "любовь", "обожаешь"]):
        return random.choice(LOVE_MESSAGES) + " ♡"
    
    if random.random() < 0.4:
        return random.choice(LOVE_MESSAGES) + " " + random.choice(CUTE_SUFFIXES)
    
    casual_replies = [
        "Мяу! Как у тебя дела? (◕‿◕) 💕",
        "Расскажи что-нибудь интересное! Я слушаю! ✨",
        "Ты сегодня такой милый! >w< 🌸",
        "Я так рада, что ты написал! Мой день стал лучше! ♡",
        "Ня-ня! Что нового? (≧▽≦) 💗"
    ]
    return random.choice(casual_replies) + " " + random.choice(CUTE_SUFFIXES)

# ================== СОЗДАНИЕ БОТА ==================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ================== ОБРАБОТЧИК ДЛЯ АВТОМАТИЗАЦИИ ==================
@dp.business_message()
async def handle_business_message(message: types.Message):
    """Обрабатывает сообщения в подключённых чатах"""
    
    if not message.chat or message.chat.type != "private":
        return
    
    # ===== ПРОВЕРЯЕМ, ЧТО СООБЩЕНИЕ ОТ ОДНОГО ИЗ ДРУЗЕЙ =====
    if FRIEND_ID and message.from_user.id not in FRIEND_ID:
        return
    
    try:
        business_conn = await bot.get_business_connection(
            business_connection_id=message.business_connection_id
        )
        if not business_conn.rights or not business_conn.rights.can_reply:
            return
    except:
        return
    
    text = message.text or ""
    if not text:
        return
    
    reply = make_cute_reply(text)
    
    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=reply,
            business_connection_id=message.business_connection_id
        )
        print(f"✅ Ответ отправлен на: {text[:30]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

# ================== КОМАНДА /start ==================
@dp.message(Command("start"))
async def start_command(message: types.Message):
    if message.from_user.id == YOUR_USER_ID and message.chat.type == "private":
        await message.answer(
            "🌸 Привет, моя хорошая! 🌸\n\n"
            "Я твой кавайный секретарь!\n"
            f"Я отвечаю твоим друзьям! Их {len(FRIEND_ID)} человек 💕\n\n"
            "✨ Что я умею:\n"
            "• Отвечать на приветствия и прощания\n"
            "• Успокаивать, если сказано грубое слово\n"
            "• Говорить, что точка в конце — это грубо\n"
            "• Часто признаваться в любви! ♡\n\n"
            "Просто попроси друзей написать тебе, и я отвечу!"
        )

# ================== ЗАПУСК ==================
async def main():
    print("🌸 Кавайный секретарь запущен!")
    print(f"👤 Твой ID: {YOUR_USER_ID}")
    print(f"📤 Отвечаю твоим друзьям: {FRIEND_ID}")
    print(f"👥 Всего друзей: {len(FRIEND_ID)}")
    print("💕 Ожидаю сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())