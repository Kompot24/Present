@echo off
:: Устанавливаем кодировку UTF-8, чтобы русский текст читался
chcp 65001 >nul

set "REPO_URL=https://github.com/Kompot24/Present.git"
set "FOLDER_NAME=Present"

echo [?] ПРОВЕРКА ОБНОВЛЕНИЙ...

:: 1. Если папка уже есть, просто заходим в неё
if exist "%FOLDER_NAME%" (
    echo [!] Папка %FOLDER_NAME% найдена, перехожу в неё...
    cd /d "%FOLDER_NAME%"
) else (
    echo [!] Папка проекта не найдена. Начинаю загрузку...
    git clone %REPO_URL% %FOLDER_NAME%
    cd /d "%FOLDER_NAME%"
)

:: 2. Если мы внутри папки, обновляем файлы
if exist .git (
    echo [!] Синхронизация файлов с GitHub...
    git fetch --all
    git reset --hard origin/main
)


:: 4. Установка библиотек
echo [!] Проверка библиотек из requirements.txt...
python -m pip install --no-cache-dir -r requirements.txt

:: 5. Запуск
echo [+] Всё готово! Запускаю бота...
start pythonw present.pyw
exit