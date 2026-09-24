# yume.cloud — лендинг

Статический сайт Yume для прокатов инвентаря и оборудования: HTML, CSS, JavaScript. Хостинг: GitHub Pages из ветки `main`.

## Структура

- `index.html` — главная. Шапка и футер отсюда переиспользуются на внутренних страницах.
- `build.py` — генерирует внутренние страницы (`solutions/*`, `contacts/`, `check/`, `download/`, `legal/*`, `delete-account/`), `sitemap.xml`, `robots.txt`, `404.html` и страницы-редиректы со старых адресов. Тексты лежат внутри скрипта.
- `css/styles.css`, `js/main.js` — стили и анимации. `js/check.js` — проверка клиента по API Yume.
- `assets/` — логотипы клиентов, скриншоты продукта, шрифты.
- `api/` — серверные функции для приёма заявок в Telegram и прокси eGov. На GitHub Pages не выполняются, нужен любой serverless-хостинг (Cloudflare Workers, Vercel). Без них форма открывает WhatsApp с текстом заявки.

## Локально

```bash
python3 build.py
python3 -m http.server 4174
```

## Публикация

Любой пуш в `main` публикуется на GitHub Pages автоматически. После правки текстов внутренних страниц запускайте `python3 build.py` и коммитьте сгенерированные файлы.

## Домен

В настройках репозитория Pages → Custom domain указать `www.yume.cloud`, у регистратора создать CNAME `www` → `kabdyzhanzhaina-lang.github.io` и A-записи для корня на IP GitHub Pages (185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153).
