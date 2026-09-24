# yume.cloud — лендинг

Статический сайт Yume для прокатов инвентаря и оборудования. Без сборщиков и фреймворков: HTML, CSS, JavaScript и две серверные функции Vercel.

## Структура

- `index.html` — главная. Шапка и футер отсюда переиспользуются на внутренних страницах.
- `build.py` — генерирует внутренние страницы: `solutions/*`, `contacts/`, `check/`, `download/`, `feed/`, `legal/*`, `delete-account/`. Тексты страниц лежат внутри скрипта.
- `css/styles.css`, `js/main.js` — стили и анимации. `js/check.js` — живая проверка клиента.
- `api/lead.js` — приём заявок с форм и отправка в Telegram.
- `api/egov.js` — прокси к реестру должников eGov, добавляет токен на сервере.
- `assets/` — логотипы клиентов, скриншоты продукта, иконки.
- `vercel.json` — редиректы со старых адресов, кэш, чистые URL.

## Локально

```bash
python3 build.py
python3 -m http.server 4174
```

Открыть http://localhost:4174

## Деплой

Проект на Vercel: `yume-cloud-zzydfr`. Пуш в `main` деплоит автоматически, вручную:

```bash
python3 build.py && vercel deploy --prod --yes
```

## Переменные окружения (Vercel → Settings → Environment Variables)

| Имя | Зачем |
|---|---|
| `TELEGRAM_BOT_TOKEN` | токен бота, куда падают заявки |
| `TELEGRAM_CHAT_ID` | чат или группа для заявок |
| `YUME_API_TOKEN` | токен для реестра eGov на странице проверки (без него блок показывает заглушку) |
| `YUME_API_BASE` | необязательно, по умолчанию `https://api.yume.cloud` |

После правки текстов внутренних страниц запускайте `python3 build.py` и коммитьте сгенерированные файлы.
