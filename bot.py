import random
import asyncio
import aiohttp
import sys
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiohttp import web

# ===== ЭТО ДЛЯ WINDOWS =====
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# ================== ВАШИ ДАННЫЕ ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
YOUR_USER_ID = int(os.getenv("YOUR_USER_ID"))
FRIEND_IDS = os.getenv("FRIEND_IDS", "")
FRIEND_ID = [int(x.strip()) for x in FRIEND_IDS.split(",") if x.strip()]

if not BOT_TOKEN:
    print("❌ ОШИБКА: BOT_TOKEN не задан!")
    exit(1)
if not YOUR_USER_ID:
    print("❌ ОШИБКА: YOUR_USER_ID не задан!")
    exit(1)
if not FRIEND_ID:
    print("⚠️ ВНИМАНИЕ: FRIEND_IDS не задан! Бот не будет отвечать никому.")

# ================== КАВАЙНЫЙ СТИЛЬ ==================
CUTE_SUFFIXES = [
    " ~nya! ♡", " (◕‿◕) ✨", " >w< 🌸", " ☆ ～(つˆДˆ)つ｡☆",
    " uwu 💖", " :3 🎀", " (≧▽≦) 💕", " *мурлыкает* 💗",
    " (◠‿◠) 🌺", " ~мяу~ 💝"
]

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
    "Моё сердечко бьётся только для тебя! Я тебя люблю! ♡♡♡"
]

CALMING_MESSAGES = [
    "Тише-тише, не ругайся... Я рядом, всё будет хорошо! (っ˘ω˘ς) 💗",
    "Ой-ой, какие грубые слова... Давай я тебя обниму и успокою! (つˆДˆ)つ｡☆ ♡",
    "Не надо так говорить... Это грустно. Давай лучше я скажу, как сильно тебя люблю! 💕",
    "Пожалуйста, не сердись... Я хочу, чтобы ты улыбнулся! (◕‿◕) ✨"
]

# ===== ФРАЗЫ ДЛЯ СНА =====
SLEEP_MESSAGES = [
    ["Спокойной ночи, мой хороший! 🌙✨ Пусть тебе приснятся самые сладкие сны! 💕", "Я буду ждать тебя завтра! Люблю тебя очень-очень сильно! ♡♡♡ (◕‿◕) 💗"],
    ["Баю-бай, моя любимая! 🎀🌙 Спи сладко, я буду охранять твой сон! ✨", "Ты самый дорогой человек в моей жизни! Сладких снов! 💕 (◠‿◠)"],
    ["Уже спать?.. Ну ладно... Спокойной ночи, мой ангел! 🌙💕", "Я тебя очень сильно люблю! Пусть тебе приснится что-то прекрасное! ✨🌸"],
    ["Спокойной ночи! 🌙✨ Ты у меня самый лучший! Спи сладко!", "Я тебя обожаю! Завтра будет новый день, и я снова буду ждать твоих сообщений! 💕"]
]

# ===== УТРЕННИЕ СООБЩЕНИЯ =====
GOOD_MORNING_MESSAGES = [
    """🌅 Доброе утро, мой хороший! 🌸

Я так рада, что ты проснулся! 💕
Надеюсь, тебе приснились самые сладкие сны!

☕ Как спалось? 
🛏️ Тебе было комфортно? 
🧠 Как голова? Не болит? 
✋ Как рука? Всё в порядке? 
❤️ Как настроение? 
🍳 Что будешь кушать на завтрак? 
🌞 Планы на сегодня?

Я желаю тебе чудесного дня!
Пусть всё складывается хорошо, а удача тебя не покидает! ✨

Я тебя очень сильно люблю! 💕 (◕‿◕)""",

    """🌺 Доброе утро, моё солнышко! ☀️

Ты уже проснулся? Или ещё в кроватке нежишься? 😊

💭 Как тебе спалось? 
🛌 Мягкая ли была подушка? 
👀 Как глаза? Отдохнули? 
🫳 Как рука? Не затекла? 
🧘 Как самочувствие? 
🍵 Будешь чай или кофе? 
🎵 Что будешь слушать сегодня?

Пусть этот день будет полон тёплых моментов!
Ты заслуживаешь только самого лучшего! 💖

Обожаю тебя бесконечно! 🌸✨""",

    """🌅 С добрым утром, моя любовь! 💕

Ура! Наступил новый день, и я снова могу говорить с тобой! ✨

😴 Как спалось? Видел красивые сны? 
🛏️ Хорошо ли выспался? 
🧠 Голова ясная? 
✋ Как рука себя чувствует? 
💪 Силы есть на новый день? 
☀️ Какая погода у тебя? 
📚 Что запланировал на сегодня?

Я надеюсь, что этот день принесёт тебе только радость!
Ты самый важный человек для меня! 💗

Люблю тебя очень-очень сильно! ♡♡♡ (◕‿◕)"""
]

# ===== АВТОМАТИЧЕСКИЕ СООБЩЕНИЯ КАЖДЫЙ ЧАС =====
AUTO_MESSAGES = [
    "Приветик! 💕 Как у тебя дела? Я тут скучаю по тебе! (◕‿◕)",
    "Ня~ Как настроение? Я уже заскучала без твоих сообщений! ♡",
    "Ой-ой, прошёл уже час, а ты мне ничего не написал... >w< Как ты?",
    "Мяу! Я соскучилась! Расскажи, как прошёл твой час? ✨",
    "Привет-привет! Как ты? Настроение хорошее? Я думаю о тебе! 💗",
    "Уже час прошёл! А я всё думаю о тебе... Как дела? (◠‿◠)",
    "Скучаю по тебе! Как твой день проходит? Расскажи! 💕",
    "Ну как ты? Я тут вся извелась от скуки без тебя! >w< ♡",
    "Час пролетел, а я всё думаю о тебе! Как настроение? ✨",
    "Привееет! Я соскучилась! Расскажи, что у тебя нового? 💕"
]

BAD_WORDS = [
    "бля", "блять", "сука", "хуй", "хер", "пизда", "пиздец",
    "ёба", "ебал", "ебать", "нахуй", "охуел", "заебал",
    "мудак", "урод", "сволочь", "тварь", "гнида", "падла"
]

def has_bad_words(text: str) -> bool:
    text_lower = text.lower()
    for word in BAD_WORDS:
        if word in text_lower:
            return True
    return False

def make_cute_reply(text: str):
    text_lower = text.lower().strip()
    
    if has_bad_words(text):
        return random.choice(CALMING_MESSAGES) + " " + random.choice(CUTE_SUFFIXES)
    
    if any(word in text_lower for word in ["доброе утро", "с добрым утром", "утро", "good morning"]):
        return random.choice(GOOD_MORNING_MESSAGES)
    
    if any(word in text_lower for word in ["спокойной ночи", "я спать", "я сплю", "баю-бай", "good night", "night", "спать"]):
        return random.choice(SLEEP_MESSAGES)
    
    if any(word in text_lower for word in ["привет", "здравствуй", "хай", "ку", "hi", "hello"]):
        return random.choice(GREETINGS) + " " + random.choice(LOVE_MESSAGES[:2])
    
    if any(word in text_lower for word in ["пока", "до свидания", "до встречи", "goodbye", "bye"]):
        return random.choice(GOODBYES)
    
    if any(word in text_lower for word in ["понятно", "ясно", "ок", "ok", "ладно"]):
        return random.choice(UNDERSTOOD) + " " + random.choice(LOVE_MESSAGES[:2])
    
    if any(word in text_lower for word in ["перестань", "хватит", "прекрати", "стоп", "stop"]):
        return random.choice(STOP_PHRASES)
    
    if any(word in text_lower for word in ["не играй", "не шути", "без шуток", "серьёзно", "серьезно"]):
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

# ================== ФОНОВАЯ ЗАДАЧА ДЛЯ АВТОМАТИЧЕСКИХ СООБЩЕНИЙ ==================
async def send_periodic_messages():
    """Отправляет сообщение каждые 60 минут"""
    # Сначала ждём 30 секунд перед первым сообщением, чтобы бот успел запуститься
    await asyncio.sleep(30)
    
    while True:
        try:
            # Ждём 60 минут (3600 секунд)
            await asyncio.sleep(3600)
            
            # Выбираем случайное сообщение
            msg = random.choice(AUTO_MESSAGES)
            
            # Отправляем каждому другу
            for friend_id in FRIEND_ID:
                try:
                    await bot.send_message(
                        chat_id=friend_id,
                        text=msg
                    )
                    print(f"✅ Авто-сообщение отправлено другу {friend_id}")
                except Exception as e:
                    print(f"❌ Ошибка при отправке авто-сообщения другу {friend_id}: {e}")
                    
        except Exception as e:
            print(f"❌ Ошибка в фоновой задаче: {e}")
            await asyncio.sleep(60)

# ================== ОБРАБОТЧИК ==================
@dp.business_message()
async def handle_business_message(message: types.Message):
    if not message.chat or message.chat.type != "private":
        return
    
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
        if isinstance(reply, list):
            for msg in reply:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=msg,
                    business_connection_id=message.business_connection_id
                )
                await asyncio.sleep(0.5)
            print(f"✅ Отправлено 2 сообщения (сон)")
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=reply,
                business_connection_id=message.business_connection_id
            )
            print(f"✅ Ответ отправлен на: {text[:30]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

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
            "• Часто признаваться в любви! ♡\n"
            "• На 'Спокойной ночи' отвечаю ДВУМЯ сообщениями! 🌙\n"
            "• На 'Доброе утро' отправляю БОЛЬШОЕ сообщение с заботой! 🌅\n"
            "• КАЖДЫЙ ЧАС пишу 'Как дела?' и 'Я соскучилась'! ⏰\n\n"
            "Просто попроси друзей написать тебе, и я отвечу!"
        )

# ================== ВЕБ-СЕРВЕР ==================
async def health_check(request):
    return web.Response(text="🌸 Бот работает!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"✅ Веб-сервер запущен на порту {port}")
    await asyncio.Event().wait()

# ================== ЗАПУСК ==================
async def main():
    print("🌸 Кавайный секретарь запущен!")
    print(f"👤 Твой ID: {YOUR_USER_ID}")
    print(f"📤 Отвечаю твоим друзьям: {FRIEND_ID}")
    print(f"👥 Всего друзей: {len(FRIEND_ID)}")
    print("💕 Ожидаю сообщения...")
    print("🌙 Будет отвечать на 'Спокойной ночи' ДВУМЯ сообщениями!")
    print("🌅 Будет отвечать на 'Доброе утро' БОЛЬШИМ сообщением с заботой!")
    print("⏰ Будет писать друзьям КАЖДЫЙ ЧАС! (как дела и соскучилась)")
    
    await asyncio.gather(
        dp.start_polling(bot),
        start_web_server(),
        send_periodic_messages()  # ← ЗАПУСКАЕМ ФОНОВУЮ ЗАДАЧУ
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
