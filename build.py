# -*- coding: utf-8 -*-
"""Generates inner pages (solutions, contacts) from index.html partials."""
import re, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
idx = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()

def part(pattern):
    m = re.search(pattern, idx, re.S)
    assert m, pattern
    return m.group(0)

SPRITE = part(r'<svg width="0" height="0".*?</svg>')
HEADER = part(r'<header class="nav">.*?</header>')
FOOTER = part(r'<footer class="footer">.*?</footer>')
FORM = part(r'<form class="form".*?</form>')
FABS = part(r'<a class="wa-fab".*?</button>')

def cta_block(title, lead, bullets):
    lis = ''.join(f'<li><svg><use href="#i-check"/></svg>{b}</li>' for b in bullets)
    return f'''
<section class="section section--dark cta" id="demo">
  <div class="wrap">
    <div data-reveal="left">
      <p class="eyebrow">Демо</p>
      <h2>{title}</h2>
      <p class="lead" style="margin-top:18px">{lead}</p>
      <ul class="cta__list">{lis}</ul>
      <a class="cta__wa" href="https://wa.me/77779479990" rel="noopener"><svg><use href="#i-wa"/></svg> Или напишите в WhatsApp: +7 777 947 99 90</a>
    </div>
    {FORM}
  </div>
</section>'''

def page(title, desc, path, body, light_nav=True):
    nav = HEADER.replace('<header class="nav">', '<header class="nav is-light">') if light_nav else HEADER
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="https://www.yume.cloud{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="https://www.yume.cloud/assets/img/og.png">
<meta property="og:url" content="https://www.yume.cloud{path}">
<link rel="icon" href="/assets/img/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Golos+Text:wght@400;500;600&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Golos+Text:wght@400;500;600&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Golos+Text:wght@400;500;600&display=swap"></noscript>
<link rel="stylesheet" href="/css/styles.css">
</head>
<body>
{SPRITE}
{nav}
{body}
{FOOTER}
{FABS}
<script src="/js/main.js" defer></script>
</body>
</html>
'''

def write(path, content):
    full = os.path.join(ROOT, path.lstrip('/'))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(content)
    print('wrote', path)

# ------------------------------------------------------------------ data
SEGMENTS = [
 dict(slug='tools', icon='i-drill', name='Строительный инструмент и оборудование', short='Инструмент и оборудование',
  h1='Прокат инструмента без потерь, долгов и тетрадей',
  lead='Перфораторы, бетономешалки, леса, генераторы. Yume знает, где каждая единица, кто её взял, когда вернёт и сколько должен.',
  img='/assets/img/inventory-illustration.webp', imgw=1600,
  pains=[('Не видно, что свободно','Менеджер звонит на склад, чтобы узнать, есть ли перфоратор. Клиент в это время уходит к конкуренту.'),
         ('Долги всплывают поздно','Клиент взял леса на неделю, вернул через месяц. Про доплату вспомнили, когда он уже уехал.'),
         ('Мошенники и невозвраты','Один ушедший генератор стоит как 40 аренд. Проверить человека до выдачи негде.'),
         ('Договор вручную','Word, печать, подпись, скан. Пятнадцать минут на каждого клиента и стопка бумаги.')],
  gains=[('Остатки в реальном времени','Календарь и статусы по каждой единице: свободно, выдано, на ремонте, просрочено. С любой точки и с телефона.','/assets/img/icon-calendar.webp'),
         ('Проверка по ИИН до выдачи','Общий реестр должников прокатчиков и ваш чёрный список. Результат появляется прямо в карточке аренды.','/assets/img/app-table.webp'),
         ('Договор и акт за минуту','Данные клиента подтягиваются, подпись через SMS. Фото состояния при выдаче и возврате хранятся в аренде.','/assets/img/icon-contract.webp'),
         ('Залоги, доплаты, просрочки','Система сама считает просрочку и износ, напоминает клиенту и показывает, кто и сколько должен.','/assets/img/icon-finance.webp')],
  modules=['Учёт аренды и календарь','Каталог и склад','Проверка клиентов','Онлайн-договоры','Финансы и залоги','Мастерская'],
  case=dict(co='StroyПрокат', img='/assets/img/av-stroyprokat.jpg', seg='Строительное оборудование', metric='0', metric_l='мошенников после подключения реестра должников',
            q='Мы значительно уменьшили время оформления договоров. Контроль действующей и просроченной аренды стал проще. А когда появился реестр должников и ЧС, стало быстрее и безопаснее. Мошенники понимают, что с ними мы работать не будем.', who='Фахруддин'),
  faq=[('Как учитывать расходники и износ?','Для каждой единицы ведётся история аренд и ремонтов. Расходники списываются при выдаче, износ и стоимость ремонта видны в доходности единицы.'),
       ('Можно ли работать с несколькими складами?','Да. Остатки ведутся по точкам, перемещение между складами делается в два клика, а календарь показывает загрузку по каждой точке.'),
       ('Как оформить залог?','Залог фиксируется при выдаче деньгами или документом, при возврате автоматически зачитывается в доплату или возвращается клиенту.'),
       ('Работает ли на складе без компьютера?','Да. Приложение для телефона и планшета: выдача, возврат, фото состояния и подпись клиента делаются на месте.')]),
 dict(slug='events', icon='i-party', name='Ивент-инвентарь и мебель', short='Ивент и мебель',
  h1='Комплекты на сотни позиций без наложений и потерь',
  lead='Стулья, столы, шатры, свет, посуда. Yume собирает комплекты под проект, следит за датами и считает, что вернулось, а что нет.',
  img='/assets/img/icon-calendar.webp', imgw=700,
  pains=[('Наложение дат','Два свадебных заказа на одни и те же 200 стульев. Узнаёте об этом в пятницу вечером.'),
         ('Комплектность','Уехало 180 бокалов, вернулось 171. Кто считал и когда, уже никто не помнит.'),
         ('Логистика в чатах','Адреса, время монтажа и водители живут в WhatsApp. Один пропущенный звонок и площадка стоит пустая.'),
         ('Проекты в Excel','Смета в одном файле, состав в другом, оплаты в третьем. Прибыль по мероприятию не считает никто.')],
  gains=[('Календарь по проектам','Каждое мероприятие видно на общем календаре с датами вывоза, монтажа и возврата. Наложение невозможно.','/assets/img/icon-calendar.webp'),
         ('Комплекты и наборы','Соберите набор «Свадьба на 100 гостей» один раз и добавляйте в заказ одним кликом. Состав раскрывается до каждой позиции.','/assets/img/app-table.webp'),
         ('Приёмка по списку','При возврате менеджер отмечает позиции с телефона. Недостача и повреждения сразу превращаются в доплату.','/assets/img/icon-devices.webp'),
         ('Смета и оплата в одном месте','Договор, предоплата, остаток и доплаты по проекту. Прибыль каждого мероприятия видна без таблиц.','/assets/img/icon-finance.webp')],
  modules=['Календарь бронирований','Комплекты и наборы','Онлайн-договоры','Финансы и предоплаты','Доставка и монтаж','Приложение для приёмки'],
  case=dict(co='Prokat Invest', img='/assets/img/av-prokatinvest.png', seg='Инвентарь и оборудование', metric='1 экран', metric_l='вместо блокнотов и таблиц по всем проектам',
            q='Долгое время вели учёт чуть ли не в блокнотах и таблицах. С Yume наконец-то увидели реальные цифры по бизнесу: сразу понятно, на чём мы зарабатываем, а где деньги просто висят.', who='Даулет'),
  faq=[('Можно ли бронировать инвентарь за полгода вперёд?','Да. Бронь ставится на любые даты, календарь показывает загрузку и свободные остатки на выбранный период.'),
       ('Как считать бой и недостачу?','При приёмке отмечаются недостающие и повреждённые позиции, система считает доплату по заранее заданной стоимости.'),
       ('Есть ли доставка и монтаж?','Для заказа задаются адрес, время доставки и монтажа, ответственный сотрудник. Маршрутный лист выгружается водителю.'),
       ('Работает ли несколько менеджеров одновременно?','Да, права доступа настраиваются по ролям: менеджер, склад, бухгалтер, владелец.')]),
 dict(slug='sport', icon='i-ski', name='Спорт и горнолыжный прокат', short='Спорт и горнолыжный',
  h1='Очередь в сезон движется быстро, когда выдача занимает минуту',
  lead='Лыжи, сноуборды, велосипеды, сапы, коньки. Yume выдаёт по размеру и ростовке, принимает оплату и напоминает о возврате.',
  img='/assets/img/app-table.webp', imgw=1600,
  pains=[('Очередь на выдаче','Утром субботы у стойки 30 человек. Каждому подобрать ботинки, записать паспорт, взять залог.'),
         ('Размеры и ростовки','Сорок пар ботинок 42 размера числятся, а в наличии три. Остальные где-то на склоне.'),
         ('Почасовая путаница','Взял на два часа, вернул через пять. Кто и сколько доплачивает, спорят на месте.'),
         ('Сезонная команда','Новые сотрудники каждую зиму. Обучать их тетради и своим правилам некогда.')],
  gains=[('Выдача за минуту с планшета','Клиент по телефону, инвентарь по штрих-коду, размер как атрибут. Договор подписывается на экране.','/assets/img/icon-devices.webp'),
         ('Остатки по размерам','Каталог хранит размеры, ростовки и жёсткость. Видно, что свободно именно в нужном размере прямо сейчас.','/assets/img/app-table.webp'),
         ('Почасовые и дневные тарифы','Час, полдня, день, абонемент. Система считает стоимость и доплату за задержку без споров.','/assets/img/icon-finance.webp'),
         ('Понятно новичку','Один экран выдачи и один экран возврата. Сезонный сотрудник работает самостоятельно с первого дня.','/assets/img/phone.webp')],
  modules=['Быстрая выдача','Каталог с размерами','Почасовые тарифы','Онлайн-договоры','Оплаты и залоги','Мастерская и сервис'],
  case=dict(co='Tobe.kz', img='/assets/img/av-tobe.png', seg='Прокат инвентаря', metric='1 день', metric_l='на обучение нового сотрудника',
            q='Для нас самое главное скорость работы. Сервис позволяет быстро создавать новые сделки и управлять ими без путаницы. Все процессы прозрачны, и даже новички в команде легко справляются.', who='Абулхаир'),
  faq=[('Можно ли выдавать по штрих-коду?','Да. На инвентарь печатаются этикетки, выдача и возврат делаются сканером или камерой телефона.'),
       ('Как учитывать сервис лыж и велосипедов?','Модуль мастерской: заточка, смазка, ремонт. Единица на сервисе не попадает в выдачу.'),
       ('Работает ли без интернета на склоне?','Приложение кэширует данные и синхронизирует их, когда связь появится.'),
       ('Есть ли абонементы?','Да, абонементы и пакеты часов настраиваются в тарифах и списываются при каждой выдаче.')]),
 dict(slug='fashion', icon='i-shirt', name='Одежда, платья и костюмы', short='Одежда и костюмы',
  h1='Каждое платье забронировано, почищено и вернётся вовремя',
  lead='Вечерние и свадебные платья, костюмы, аксессуары. Yume ведёт брони на будущие даты, статус чистки и витрину с фото.',
  img='/assets/img/phone.webp', imgw=900,
  pains=[('Брони на будущее','Платье забронировано на 14 октября, а его сдали ещё двоим на соседние даты. Химчистка между ними не успевает.'),
         ('Статус вещи','Где сейчас платье: у клиентки, в чистке, на ремонте молнии? Ответ знает только администратор, которая в отпуске.'),
         ('Примерки и запись','Запись на примерку в Instagram, бронь в тетради, залог в Kaspi. Три источника, ни одного полного.'),
         ('Залоги и повреждения','Пятно на подоле обнаружили через неделю. Доказать, чьё оно, уже невозможно.')],
  gains=[('Календарь броней с буфером','Между арендами автоматически ставится время на чистку. Забронировать вещь в этот промежуток нельзя.','/assets/img/icon-calendar.webp'),
         ('Статус «в чистке» и «на ремонте»','Каждая вещь проходит цикл: выдана, вернулась, чистка, готова. Витрина показывает только доступное.','/assets/img/app-table.webp'),
         ('Витрина с фото и онлайн-запись','Клиентка выбирает платье на сайте, записывается на примерку, заявка падает в календарь.','/assets/img/icon-devices.webp'),
         ('Фото при выдаче и возврате','Состояние фиксируется с телефона. Повреждение и доплата подтверждаются снимками из карточки аренды.','/assets/img/icon-contract.webp')],
  modules=['Календарь броней','Витрина с фото','Статусы и чистка','Онлайн-договоры','Залоги и оплаты','Запись на примерку'],
  case=dict(co='ToRent', img='/assets/img/av-torent.png', seg='Прокат инвентаря', metric='1 место', metric_l='для всех броней, платежей и клиентов',
            q='Сервис идеально подошёл для нашего бизнеса. Мы используем его для отслеживания инвентаря, учёта платежей и работы с клиентами. Очень удобно, что все данные находятся в одном месте.', who='Дастан'),
  faq=[('Можно ли загрузить витрину с фото?','Да. У каждой вещи несколько фото, размер, цвет и цена. Витрина публикуется по ссылке или встраивается на ваш сайт.'),
       ('Как учитывать химчистку?','После возврата вещь автоматически уходит в статус «чистка» на заданное время и не показывается свободной.'),
       ('Есть ли размерная сетка?','Размеры, рост и обхваты хранятся как атрибуты, по ним работает поиск и фильтр витрины.'),
       ('Можно ли принимать предоплату онлайн?','Да, ссылка на оплату отправляется клиенту в WhatsApp, статус брони меняется автоматически.')]),
 dict(slug='media', icon='i-camera', name='Фото-, видео- и звуковая техника', short='Фото и видео',
  h1='Дорогая техника уходит только проверенным клиентам',
  lead='Камеры, объективы, свет, звук. Yume проверяет клиента по ИИН, хранит серийные номера и сверяет комплектность при возврате.',
  img='/assets/img/icon-devices.webp', imgw=800,
  pains=[('Один невозврат равен месяцу работы','Камера за 1,5 млн уехала с человеком по чужим документам. Проверить его было негде.'),
         ('Комплектность','Вернули кейс, а внутри нет батареи и одной карты памяти. Заметили через день, когда набор уже уехал следующему.'),
         ('Серийные номера','Пять одинаковых объективов, но сломан конкретный. Чей он был в последний раз, неизвестно.'),
         ('Залоги в мессенджерах','Кто, сколько и за что оставил залог, хранится в переписке. Вернуть правильно получается не всегда.')],
  gains=[('Проверка клиента по ИИН','Общий реестр должников и чёрный список прокатчиков. Проверка встроена в оформление аренды.','/assets/img/app-table.webp'),
         ('Серийные номера и история','Каждая единица с серийником, историей аренд, ремонтов и фото. Понятно, кто и когда брал именно этот объектив.','/assets/img/inventory-illustration.webp'),
         ('Комплектность по чек-листу','Состав набора проверяется при выдаче и возврате по списку. Недостача сразу превращается в доплату.','/assets/img/icon-contract.webp'),
         ('Залоги и страховка','Залог, страховка и лимит ответственности фиксируются в договоре, зачёт и возврат считаются автоматически.','/assets/img/icon-finance.webp')],
  modules=['Проверка клиентов','Каталог с серийниками','Комплекты и чек-листы','Онлайн-договоры','Залоги и финансы','Мастерская'],
  case=dict(co='ProRent', img='/assets/img/av-prorent.jpg', seg='Прокат техники и оборудования', metric='15 → 5 мин', metric_l='на оформление одного клиента',
            q='Раньше оформление клиента занимало до 15 минут и было много ручной работы. С Yume сократили это время до 5 минут. Перестали терять оборудование, теперь всё под контролем и без хаоса.', who='Евгений'),
  faq=[('Откуда берутся данные для проверки?','Реестр должников пополняют сами прокатчики на Yume, больше 200 компаний. Плюс ваш собственный чёрный список.'),
       ('Можно ли вести технику по серийным номерам?','Да, каждая единица уникальна, у неё своя история, фото и статус. Одинаковые модели не путаются.'),
       ('Как оформить страховку или ответственность?','Условия прописываются в шаблоне договора и фиксируются при выдаче вместе с залогом.'),
       ('Есть ли интеграция с сайтом для заявок?','Витрина Yume встраивается на сайт, заявки и брони попадают прямо в календарь.')]),
]

ICON_X = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg>'

def solution_page(s, i):
    others = [o for o in SEGMENTS if o['slug'] != s['slug']]
    pains = ''.join(f'<li><i>{ICON_X}</i><div><b>{t}</b><p>{d}</p></div></li>' for t, d in s['pains'])
    gains = ''
    for k, (t, d, img) in enumerate(s['gains']):
        gains += f'''<div class="gain{' gain--rev' if k % 2 else ''}" data-reveal>
  <div class="gain__txt"><small>0{k+1}</small><h3>{t}</h3><p>{d}</p></div>
  <div class="gain__vis"><img src="{img}" alt="" loading="lazy"></div>
</div>'''
    mods = ''.join(f'<a class="mod" href="/#features"><svg><use href="#i-check"/></svg>{m}</a>' for m in s['modules'])
    faq = ''.join(f'<div class="q{" is-open" if k == 0 else ""}"><button>{q}<i></i></button><div class="q__a"><div><p>{a}</p></div></div></div>' for k, (q, a) in enumerate(s['faq']))
    other_links = ''.join(f'<a class="chip" href="/solutions/{o["slug"]}/"><svg><use href="#{o["icon"]}"/></svg>{o["short"]}</a>' for o in others)
    c = s['case']
    body = f'''
<section class="phero">
  <div class="wrap phero__grid">
    <div>
      <nav class="crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span><a href="/solutions/">Решения</a><span>/</span><b>{s['short']}</b></nav>
      <p class="eyebrow"><svg class="eyebrow__i"><use href="#{s['icon']}"/></svg>{s['name']}</p>
      <h1>{s['h1']}</h1>
      <p class="lead">{s['lead']}</p>
      <div class="hero__ctas" style="justify-content:flex-start;opacity:1;animation:none">
        <a class="btn btn--lg" href="https://account.yume.cloud/auth/register">Попробовать бесплатно <svg><use href="#i-arrow"/></svg></a>
        <a class="btn btn--lg btn--ghost" href="#demo">Записаться на демо</a>
      </div>
      <div class="hero__trust" style="justify-content:flex-start;opacity:1;animation:none;color:var(--muted)">
        <span><svg><use href="#i-check"/></svg> Без карты</span><span><svg><use href="#i-check"/></svg> 14 дней бесплатно</span><span><svg><use href="#i-check"/></svg> Настройка за 1 день</span>
      </div>
    </div>
    <div class="phero__vis" data-reveal="scale"><img src="{s['img']}" width="{s['imgw']}" alt="" fetchpriority="high"></div>
  </div>
</section>

<section class="section section--soft">
  <div class="wrap">
    <div class="sec-head">
      <div data-reveal><p class="eyebrow">Как это обычно бывает</p><h2>Четыре проблемы, с которыми приходят к нам прокаты</h2></div>
      <p class="lead" data-reveal style="--d:.1s">Если узнали хотя бы две, дальше будет полезно.</p>
    </div>
    <ul class="pains" data-stagger>{pains}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head sec-head--center" data-reveal><div><p class="eyebrow">Что меняется с Yume</p><h2>Так выглядит тот же прокат через неделю</h2></div></div>
    <div class="gains">{gains}</div>
  </div>
</section>

<section class="section section--soft">
  <div class="wrap">
    <div class="sec-head">
      <div data-reveal><p class="eyebrow">Модули</p><h2>Что включаем для этого сегмента</h2></div>
      <p class="lead" data-reveal style="--d:.1s">Остальные модули подключаются позже, когда понадобятся. Платите только за то, что используете.</p>
    </div>
    <div class="mods" data-stagger>{mods}</div>
  </div>
</section>

<section class="section">
  <div class="wrap bigcase" data-reveal>
    <div class="bigcase__m"><div class="case__co"><img src="{c['img']}" alt=""><div><b>{c['co']}</b><small>{c['seg']}</small></div></div><div class="case__m"><b>{c['metric']}</b><span>{c['metric_l']}</span></div></div>
    <div class="bigcase__q"><div class="stars"><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg></div><q>{c['q']}</q><p class="bigcase__who">{c['who']}, {c['co']}</p><a class="link" href="/#cases">Все клиенты <svg><use href="#i-arrow"/></svg></a></div>
  </div>
</section>

<section class="section section--soft" id="faq">
  <div class="wrap faq">
    <div data-reveal="left"><p class="eyebrow">Вопросы</p><h2>Частые вопросы про {s['short'].lower()}</h2><p class="lead" style="margin-top:18px">Остальные ответы на <a class="link" href="/#faq">главной</a> или в WhatsApp.</p>
      <div class="others"><small>Другие сегменты</small>{other_links}</div></div>
    <div class="faq__list" data-reveal="right">{faq}</div>
  </div>
</section>
''' + cta_block(f'Покажем Yume на примере вашего проката', '20 минут по видеосвязи. Разберём ваш каталог и сценарий выдачи, ответим на вопросы про переезд из таблиц.',
                 ['Перезвоним в течение 15 минут в рабочее время', 'Персональный менеджер на всё время внедрения', 'Данные хранятся в Казахстане'])
    write(f'/solutions/{s["slug"]}/index.html', page(f'{s["name"]} — Yume', s['lead'], f'/solutions/{s["slug"]}/', body))

def solutions_index():
    cards = ''
    for s in SEGMENTS:
        cards += f'''<a class="sol" href="/solutions/{s['slug']}/" data-reveal>
  <div class="sol__txt"><span class="seg__icon"><svg><use href="#{s['icon']}"/></svg></span><h3>{s['name']}</h3><p>{s['lead']}</p><span class="link">Смотреть решение <svg><use href="#i-arrow"/></svg></span></div>
  <div class="sol__vis"><img src="{s['img']}" alt="" loading="lazy"></div>
</a>'''
    body = f'''
<section class="phero phero--center">
  <div class="wrap">
    <nav class="crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span><b>Решения</b></nav>
    <p class="eyebrow">Решения</p>
    <h1>Один продукт, пять готовых сценариев проката</h1>
    <p class="lead">Каталог, шаблоны договоров и логика выдачи уже настроены под сегмент. Выберите свой, а если такого нет, соберём под вас.</p>
  </div>
</section>
<section class="section section--soft" style="padding-top:0">
  <div class="wrap sols">{cards}
    <div class="sol sol--fleet" data-reveal>
      <div class="sol__txt"><span class="seg__icon"><svg><use href="#i-car"/></svg></span><h3>Сдаёте транспорт?</h3><p>Таксопарки, автопрокат, грузовые и спецтехника живут в отдельном продукте со своим аккаунтом: водители, штрафы ПДД, GPS и Kaspi Pay.</p><a class="link" href="https://yume.fleet" rel="noopener">Перейти на yume.fleet <svg><use href="#i-arrow"/></svg></a></div>
      <div class="sol__txt"><h3 style="font-size:17px">Другой вид проката?</h3><p>Детские товары, туристическое снаряжение, медтехника, игровые приставки. Расскажите, что сдаёте, и мы покажем, как это ляжет в Yume.</p><a class="btn btn--light" href="#demo">Рассказать о своём прокате <svg><use href="#i-arrow"/></svg></a></div>
    </div>
  </div>
</section>
''' + cta_block('Не нашли свой сегмент? Покажем на вашем примере', 'Расскажите, что сдаёте в аренду, и за 20 минут по видеосвязи мы соберём каталог и сценарий выдачи под вас.',
                 ['Перезвоним в течение 15 минут в рабочее время', 'Настроим каталог вместе с вами', 'Данные хранятся в Казахстане'])
    write('/solutions/index.html', page('Решения для проката — Yume', 'Готовые сценарии Yume для проката инструмента, ивент-инвентаря, спорта, одежды и техники.', '/solutions/', body))

def contacts():
    body = '''
<section class="phero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span><b>Контакты</b></nav>
    <p class="eyebrow">Контакты</p>
    <h1>Отвечаем за 15 минут в рабочее время</h1>
    <p class="lead">Быстрее всего в WhatsApp. Для договоров, интеграций и партнёрства пишите на почту, ответим в тот же день.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap contacts">
    <div class="ccards" data-stagger>
      <a class="ccard ccard--wa" href="https://wa.me/77779479990" rel="noopener"><i><svg><use href="#i-wa"/></svg></i><div><small>WhatsApp, самый быстрый способ</small><b>+7 777 947 99 90</b><span>Продажи, демо, вопросы по продукту</span></div><svg class="ccard__arr"><use href="#i-arrow"/></svg></a>
      <a class="ccard" href="tel:+77779479990"><i><svg><use href="#i-phone"/></svg></i><div><small>Телефон</small><b>+7 777 947 99 90</b><span>Пн–Пт 9:00–19:00, Сб 10:00–16:00 по Алматы</span></div><svg class="ccard__arr"><use href="#i-arrow"/></svg></a>
      <a class="ccard" href="mailto:sales@yume.cloud"><i><svg><use href="#i-inbox"/></svg></i><div><small>Продажи и партнёрство</small><b>sales@yume.cloud</b><span>Коммерческие предложения, интеграции, договоры</span></div><svg class="ccard__arr"><use href="#i-arrow"/></svg></a>
      <a class="ccard" href="mailto:product@yume.cloud"><i><svg><use href="#i-doc"/></svg></i><div><small>Поддержка клиентов</small><b>product@yume.cloud</b><span>Вопросы по работе системы, идеи и пожелания</span></div><svg class="ccard__arr"><use href="#i-arrow"/></svg></a>
      <div class="ccard ccard--static"><i><svg><use href="#i-store"/></svg></i><div><small>Офис</small><b>Алматы, Казахстан</b><span>Встречи по договорённости. Приезжаем к клиентам в Алматы и Астане, остальным показываем по видеосвязи.</span></div></div>
      <div class="ccard ccard--static"><i><svg><use href="#i-box"/></svg></i><div><small>Мы в сети</small><b><a href="https://www.instagram.com/yumecloudx/" rel="noopener">Instagram</a> · <a href="https://www.linkedin.com/company/yume-cloud/" rel="noopener">LinkedIn</a> · <a href="/feed/">Лента прокатчиков</a></b><span>Новости продукта, кейсы клиентов и советы по прокату</span></div></div>
    </div>
    <div class="contacts__form" data-reveal="right">
      <h2 style="font-size:26px;margin-bottom:8px">Оставьте заявку</h2>
      <p class="lead" style="font-size:15px;margin-bottom:22px">Перезвоним в течение 15 минут в рабочее время или напишем в WhatsApp.</p>
      ''' + FORM.replace('data-reveal="right"', '') + '''
    </div>
  </div>
</section>
<section class="section section--soft">
  <div class="wrap">
    <div class="sec-head"><div data-reveal><p class="eyebrow">Полезное</p><h2>Пока ждёте ответа</h2></div></div>
    <div class="quick" data-stagger>
      <a class="quick__i" href="https://account.yume.cloud/auth/register"><h3>Начать без звонка</h3><p>Регистрация занимает две минуты, первые 14 дней бесплатно и без карты.</p><span class="link">Создать аккаунт <svg><use href="#i-arrow"/></svg></span></a>
      <a class="quick__i" href="/solutions/"><h3>Посмотреть своё решение</h3><p>Инструмент, ивент, спорт, одежда, техника. Что именно меняется в каждом сегменте.</p><span class="link">К решениям <svg><use href="#i-arrow"/></svg></span></a>
      <a class="quick__i" href="/#faq"><h3>Частые вопросы</h3><p>Перенос из Excel, договоры, права доступа, работа с телефона.</p><span class="link">Читать ответы <svg><use href="#i-arrow"/></svg></span></a>
      <a class="quick__i" href="/download/"><h3>Скачать приложение</h3><p>iOS и Android для точки проката, macOS и Windows для офиса.</p><span class="link">Скачать <svg><use href="#i-arrow"/></svg></span></a>
    </div>
  </div>
</section>
'''
    write('/contacts/index.html', page('Контакты — Yume', 'Свяжитесь с Yume: WhatsApp +7 777 947 99 90, sales@yume.cloud. Отвечаем за 15 минут в рабочее время.', '/contacts/', body))

ANALYTICS = re.search(r'<script async src="https://www.googletagmanager.com.*?</script>\n<script>.*?</script>\n<script>.*?</script>', idx, re.S)
ANALYTICS = ANALYTICS.group(0) if ANALYTICS else ''

def check_page():
    demo = part(r'<div class="demo" data-reveal="right">.*?</div>\n    </div>\n  </div>\n</section>')
    demo = demo[:demo.rfind('\n    </div>\n  </div>\n</section>')]
    demo = demo.replace('data-reveal="right"', 'data-reveal="scale"')
    feats = [('i-shield', 'АИС ОИП и eGov', 'Проверка по реестру должников исполнительных производств и данным eGov при каждой новой аренде.'),
             ('i-scan', 'Мгновенный результат', 'Проверка запускается автоматически при создании аренды. Без задержек и ручного поиска по базам.'),
             ('i-alert', 'Чёрный список', 'Ведите собственный список с причинами и заметками. Он виден всем сотрудникам вашего проката.'),
             ('i-box', 'Общий реестр прокатчиков', 'Должники, которых добавили другие прокаты на Yume. Больше 200 компаний пополняют его каждый день.')]
    fh = ''.join(f'<div class="feature-c" data-reveal><svg><use href="#{i}"/></svg><h3>{t}</h3><p>{d}</p></div>' for i, t, d in feats)
    steps = [('Клиент называет ИИН', 'Или вы сканируете удостоверение камерой телефона. Данные попадают в карточку клиента.'),
             ('Yume проверяет за секунду', 'Реестр должников АИС ОИП, данные eGov, общий реестр прокатчиков и ваш чёрный список. Результат прямо в аренде.'),
             ('Вы решаете', 'Выдать, выдать под залог или отказать. Если клиент подвёл, добавьте его в реестр в один клик после просрочки.')]
    sh = ''.join(f'<li><div><h3>{t}</h3><p>{d}</p></div></li>' for t, d in steps)
    faq = [('Откуда данные для проверки?', 'Из реестра должников АИС ОИП (исполнительные производства), данных eGov, общего реестра прокатчиков Yume и вашего собственного чёрного списка.'),
           ('Законно ли это?', 'Да. Проверка выполняется с согласия клиента, которое он даёт при оформлении договора аренды. Персональные данные хранятся в Казахстане и обрабатываются по Закону РК «О персональных данных».'),
           ('Можно ли проверить юрлицо по БИН?', 'Да, проверка работает по ИИН физлица и БИН компании, а также по номеру телефона внутри общего реестра прокатчиков.'),
           ('Что видят другие прокаты, если я добавил должника?', 'Факт долга, сумму, дату, ваш город и категорию инвентаря. Название вашей компании показывается только по вашему желанию.'),
           ('Нужно ли что-то настраивать?', 'Нет. Проверка включена в тарифе «Бизнес» и запускается сама при создании аренды. В тарифе «Старт» её можно подключить отдельно.'),
           ('Проверка доступна без аккаунта Yume?', 'Нет, это часть системы учёта. Зарегистрируйтесь бесплатно, 14 дней все модули открыты без карты.')]
    fq = ''.join(f'<div class="q{" is-open" if k == 0 else ""}"><button>{q}<i></i></button><div class="q__a"><div><p>{a}</p></div></div></div>' for k, (q, a) in enumerate(faq))
    segs = ''.join(f'<a class="chip" href="/solutions/{s["slug"]}/"><svg><use href="#{s["icon"]}"/></svg>{s["short"]}</a>' for s in SEGMENTS)
    body = f'''
<section class="phero phero--center" style="padding-bottom:72px">
  <div class="wrap">
    <nav class="crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span><b>Проверка клиентов</b></nav>
    <p class="eyebrow">Проверка клиентов</p>
    <h1>Проверьте клиента за секунду</h1>
    <p class="lead">Чёрный список прокатчиков Казахстана и реестр должников АИС ОИП по ИИН, ФИО или номеру телефона. Бесплатно и без регистрации.</p>
    <div class="cw" data-check style="width:100%;margin-top:32px">
      <div class="cw__bar">
        <input type="search" inputmode="search" autocomplete="off" placeholder="ИИН, ФИО или номер телефона" aria-label="ИИН, ФИО или номер телефона">
        <button class="btn cw__btn" type="button">Проверить</button>
      </div>
      <div class="cw__hint"><span>Например:</span><button type="button" data-example="900412300587">ИИН 900412300587</button><button type="button" data-example="+7 777 947 99 90">номер телефона</button><button type="button" data-example="Иванов">фамилия</button></div>
      <div class="cw__results" hidden>
        <div class="cw__box" data-box="egov"><div class="cw__head"><b>Реестр должников (АИС ОИП, eGov)</b><small>исполнительные производства</small></div><div class="cw__body"></div></div>
        <div class="cw__box" data-box="bl"><div class="cw__head"><b>Чёрный список прокатчиков</b><small>пополняют компании на Yume</small></div><div class="cw__body"></div></div>
        <p class="cw__foot">Чёрный список формируется компаниями, которые работают на Yume. Хотите добавлять своих проблемных клиентов и видеть причины? <a href="https://account.yume.cloud/auth/register">Зарегистрируйтесь бесплатно</a>.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="wrap">
    <div class="sec-head">
      <div data-reveal><p class="eyebrow">Что проверяем</p><h2>Четыре источника в одном запросе</h2></div>
      <p class="lead" data-reveal style="--d:.1s">Ни один из них по отдельности не спасает. Вместе они закрывают почти все сценарии невозврата.</p>
    </div>
    <div class="feature-grid">{fh}</div>
  </div>
</section>

<section class="section">
  <div class="wrap start">
    <div data-reveal="left">
      <p class="eyebrow">Как это работает</p>
      <h2>Три шага между заявкой и выдачей</h2>
      <ul class="start__steps" style="margin-top:24px">{sh}</ul>
    </div>
    <div class="start__visual" data-reveal="scale"><img width="800" height="1644" src="/assets/img/phone.webp" alt="Проверка клиента в приложении Yume" loading="lazy"></div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap nums-dark" data-stagger>
    <div class="num"><b data-count="200" data-suffix="+">0</b><span>прокатов пополняют общий реестр должников</span></div>
    <div class="num"><b>0,4 сек</b><span>среднее время проверки по всем источникам</span></div>
    <div class="num"><b data-count="1">0</b><span>клик, чтобы добавить должника после просрочки</span></div>
  </div>
</section>

<section class="section section--soft" id="faq">
  <div class="wrap faq">
    <div data-reveal="left"><p class="eyebrow">Вопросы</p><h2>Частые вопросы про проверку</h2><p class="lead" style="margin-top:18px">Проверка входит в решения для всех сегментов проката.</p>
      <div class="others"><small>Решения по сегментам</small>{segs}</div></div>
    <div class="faq__list" data-reveal="right">{fq}</div>
  </div>
</section>
''' + cta_block('Покажем проверку на реальном примере', '20 минут по видеосвязи. Проверим пару ИИН из вашей базы и покажем, как реестр встраивается в выдачу.',
                 ['Перезвоним в течение 15 минут в рабочее время', 'Проверка работает с первого дня, без настройки', 'Данные хранятся в Казахстане']) + '\n<script src="/js/check.js" defer></script>'
    write('/check/index.html', page('Проверка клиентов по ИИН — Yume', 'Реестр должников АИС ОИП, eGov и чёрный список прокатчиков. Проверка клиента за секунду перед выдачей инвентаря.', '/check/', body))

def download_page():
    body = '''
<section class="phero">
  <div class="wrap phero__grid">
    <div>
      <nav class="crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span><b>Скачать</b></nav>
      <p class="eyebrow">Приложения</p>
      <h1>Yume на телефоне, планшете и компьютере</h1>
      <p class="lead">Выдача и возврат с телефона на точке, отчёты и аналитика на компьютере в офисе. Один аккаунт, данные синхронизируются мгновенно.</p>
      <div class="stores" data-stagger>
        <a class="store" href="https://apps.apple.com/kz/app/yume-cloud/id6749707587" rel="noopener"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M16.4 12.6c0-2.5 2-3.7 2.1-3.8-1.2-1.7-3-1.9-3.6-2-1.5-.2-3 .9-3.8.9-.8 0-2-.9-3.3-.9-1.7 0-3.3 1-4.2 2.5-1.8 3.1-.5 7.8 1.3 10.3.9 1.3 1.9 2.7 3.3 2.6 1.3-.1 1.8-.8 3.4-.8s2 .8 3.4.8c1.4 0 2.3-1.3 3.2-2.5 1-1.4 1.4-2.8 1.4-2.9 0 0-2.7-1-2.7-4.2zM14 5.2c.7-.9 1.2-2 1.1-3.2-1 0-2.3.7-3 1.6-.7.8-1.3 2-1.1 3.1 1.1.1 2.3-.6 3-1.5z"/></svg><div><small>Скачать в</small><b>App Store</b></div></a>
        <a class="store" href="https://play.google.com/store/search?q=yume%20cloud&c=apps" rel="noopener"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M3.6 2.3 13 12l-9.4 9.7c-.3-.2-.6-.6-.6-1.1V3.4c0-.5.3-.9.6-1.1zm11 8.2L5.3 2.1 16.8 8.7l-2.2 1.8zm0 3 2.2 1.8L5.3 21.9l9.3-8.4zm5.6-3.1c.6.4 1 .9 1 1.6s-.4 1.2-1 1.6l-2.6 1.5L15 12l2.6-3.1 2.6 1.5z"/></svg><div><small>Скачать в</small><b>Google Play</b></div></a>
        <a class="store" href="https://account.yume.cloud/" rel="noopener"><svg><use href="#i-laptop"/></svg><div><small>macOS и Windows</small><b>Открыть в браузере</b></div></a>
      </div>
      <p class="note-sm">Установочные файлы для macOS и Windows пришлём в WhatsApp, напишите «десктоп» на +7 777 947 99 90.</p>
    </div>
    <div class="phero__vis" data-reveal="scale"><img width="800" height="1644" src="/assets/img/phone.webp" alt="Мобильное приложение Yume" fetchpriority="high"></div>
  </div>
</section>
<section class="section section--soft">
  <div class="wrap">
    <div class="sec-head"><div data-reveal><p class="eyebrow">Что умеет приложение</p><h2>Всё, что нужно на точке проката</h2></div><p class="lead" data-reveal style="--d:.1s">Для владельцев, менеджеров и сотрудников, которые не сидят за компьютером.</p></div>
    <div class="feature-grid">
      <div class="feature-c" data-reveal><svg><use href="#i-scan"/></svg><h3>Выдача и возврат</h3><p>Сканируйте штрих-код, фотографируйте состояние, подписывайте договор на экране телефона.</p></div>
      <div class="feature-c" data-reveal><svg><use href="#i-shield"/></svg><h3>Проверка клиента</h3><p>ИИН или удостоверение камерой, результат из реестра должников за секунду.</p></div>
      <div class="feature-c" data-reveal><svg><use href="#i-wallet"/></svg><h3>Оплаты и долги</h3><p>Принимайте оплату, фиксируйте залог, смотрите, кто и сколько должен, где бы вы ни были.</p></div>
      <div class="feature-c" data-reveal><svg><use href="#i-cal"/></svg><h3>Календарь и уведомления</h3><p>Возвраты на сегодня, просрочки и новые заявки приходят пушами.</p></div>
      <div class="feature-c" data-reveal><svg><use href="#i-inbox"/></svg><h3>Чат с клиентами</h3><p>Сообщения из WhatsApp и заявки с витрины в одном окне приложения.</p></div>
      <div class="feature-c" data-reveal><svg><use href="#i-doc"/></svg><h3>Отчёты для владельца</h3><p>Выручка за день, загрузка инвентаря и долги на одном экране без Excel.</p></div>
    </div>
  </div>
</section>
''' + cta_block('Поможем установить и настроить', 'Если у вас несколько точек или сезонная команда, покажем, как раздать доступы и обучить сотрудников за час.',
                 ['Перезвоним в течение 15 минут в рабочее время', 'Настроим роли и права для команды', 'Пришлём установочные файлы для компьютера'])
    write('/download/index.html', page('Скачать приложение Yume для iOS, Android, macOS и Windows', 'Управляйте прокатом с телефона и компьютера. Приложение Yume для iOS и Android, веб-версия и десктоп для macOS и Windows.', '/download/', body))

def feed_page():
    body = '''
<section class="hero" style="padding-bottom:88px">
  <div class="hero__bg"></div><div class="hero__glow"></div>
  <div class="wrap">
    <div class="hero__inner">
      <div class="hero__pill"><b>ЛЕНТА</b> Новая возможность Yume</div>
      <h1>Первая площадка <span class="hl">для прокатчиков</span> Казахстана</h1>
      <p class="lead">Общайтесь с коллегами, делитесь опытом, задавайте вопросы. Инвентарь и транспорт, оба направления в одном месте. Вход по номеру телефона, аккаунт Yume не нужен.</p>
      <div class="hero__ctas">
        <a class="btn btn--lg" href="https://feed.yume.cloud/" rel="noopener">Открыть ленту <svg><use href="#i-arrow"/></svg></a>
      </div>
      <div class="hero__trust"><span><svg><use href="#i-check"/></svg> Бесплатно</span><span><svg><use href="#i-check"/></svg> Без регистрации в Yume</span><span><svg><use href="#i-check"/></svg> Только прокатчики</span></div>
    </div>
  </div>
</section>
<section class="section section--soft">
  <div class="wrap">
    <div class="sec-head"><div data-reveal><p class="eyebrow">О площадке</p><h2>Здесь говорят о том, что реально происходит в бизнесе</h2></div></div>
    <div class="feature-grid">
      <div class="feature-c" data-reveal><svg><use href="#i-inbox"/></svg><h3>Опыт и советы</h3><p>Как масштабировались, как выстраивали цены, как нашли хороших сотрудников. Реальные истории от людей из индустрии.</p></div>
      <div class="feature-c" data-reveal><svg><use href="#i-doc"/></svg><h3>Новости и тренды</h3><p>Что меняется на рынке аренды, какие решения принимают коллеги, как развивается индустрия в разных городах.</p></div>
      <div class="feature-c" data-reveal><svg><use href="#i-alert"/></svg><h3>Место для своих</h3><p>Угоны, мошенники, провалы. То, о чём не пишут публично, но о чём важно знать.</p></div>
      <div class="feature-c" data-reveal><svg><use href="#i-phone"/></svg><h3>Вход по номеру</h3><p>Не нужно быть клиентом Yume. Достаточно номера телефона, чтобы зайти и читать обсуждения.</p></div>
      <div class="feature-c" data-reveal><svg><use href="#i-box"/></svg><h3>Прокат инвентаря</h3><p>Инструмент, оборудование, техника, всё, что сдают в аренду и нужно контролировать.</p></div>
      <div class="feature-c" data-reveal><svg><use href="#i-car"/></svg><h3>Прокат транспорта</h3><p>Авто, таксопарки, корпоративный прокат и другие транспортные направления.</p></div>
    </div>
    <div style="text-align:center;margin-top:40px" data-reveal><a class="btn btn--lg" href="https://feed.yume.cloud/" rel="noopener">Посмотреть, о чём говорят прокатчики <svg><use href="#i-arrow"/></svg></a></div>
  </div>
</section>
'''
    write('/feed/index.html', page('Лента прокатчиков — Yume', 'Открытая площадка для прокатных компаний Казахстана: опыт, новости, вопросы коллег. Вход по номеру телефона.', '/feed/', body, light_nav=False))

def doc_page(path, title, desc, inner, updated='22 сентября 2026'):
    body = f'''
<section class="phero"><div class="wrap">
  <nav class="crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span><a href="/legal/">Документы</a><span>/</span><b>{title}</b></nav>
  <p class="eyebrow">Документы</p><h1 style="font-size:clamp(30px,3.6vw,44px)">{title}</h1>
  <p class="lead">Редакция от {updated}. ТОО «Yume.Cloud», Республика Казахстан.</p>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap doc">{inner}</div></section>'''
    write(path, page(f'{title} — Yume', desc, path.replace('index.html', ''), body))

def legal_pages():
    priv = open(os.path.join(ROOT, 'privacy-src.html'), encoding='utf-8').read()
    priv = re.sub(r'^<h1>.*?</h1>\n?', '', priv)
    doc_page('/legal/privacy/index.html', 'Политика конфиденциальности', 'Политика конфиденциальности сайта и сервиса Yume: какие данные собираем, зачем и как защищаем.', priv)
    da = '''
<p>Эта страница объясняет, как пользователь мобильного приложения Yume Cloud (разработчик ТОО «Yume.Cloud») может запросить удаление своего аккаунта и связанных с ним данных.</p>
<h2>Как запросить удаление</h2>
<ol>
<li>Напишите на <a href="mailto:support.cloud@yume.kz">support.cloud@yume.kz</a> с адреса электронной почты, привязанного к вашему аккаунту, или в WhatsApp на номер <a href="https://wa.me/77779479990">+7 777 947 99 90</a>.</li>
<li>Укажите в теме письма «Удаление аккаунта».</li>
<li>В письме укажите номер телефона и адрес электронной почты, привязанные к аккаунту, а также название компании, если вы пользуетесь Yume Cloud как сотрудник.</li>
<li>Мы подтвердим, что запрос исходит от владельца аккаунта: отправим одноразовый код на привязанный номер телефона или адрес электронной почты.</li>
<li>После подтверждения мы удалим аккаунт и напишем вам, когда это будет сделано.</li>
</ol>
<p>Запрос обрабатывается в течение 30 дней с момента подтверждения личности. Устанавливать приложение заново или заполнять отдельную форму не нужно, достаточно письма.</p>
<h2>Какие данные удаляются</h2>
<ul><li>Учётная запись: имя, номер телефона, адрес электронной почты и пароль</li><li>Доступ к компаниям и роли внутри них</li><li>Токены push-уведомлений и подписки на уведомления</li><li>Настройки интерфейса и сохранённые предпочтения</li><li>Активные сессии и токены входа</li></ul>
<h2>Какие данные сохраняются</h2>
<p>Yume Cloud сервис для компаний. Записи, которые вы создавали как сотрудник компании (карточки клиентов, договоры аренды, платежи, документы), принадлежат компании, а не вашему личному аккаунту, и остаются у неё после удаления вашего аккаунта. Ваше имя в таких записях обезличивается.</p>
<ul><li>Бухгалтерские и платёжные документы хранятся 5 лет, как того требует законодательство Республики Казахстан</li><li>Резервные копии базы данных хранятся до 30 дней, после чего перезаписываются автоматически</li></ul>
<h2>Если вы владелец компании</h2>
<p>Удаление личного аккаунта не удаляет саму компанию и её данные. Если вы хотите удалить компанию целиком вместе со всеми её записями, напишите об этом отдельно в том же письме.</p>
<h2>Контакты</h2>
<p>ТОО «Yume.Cloud» · <a href="mailto:support.cloud@yume.kz">support.cloud@yume.kz</a> · <a href="tel:+77779479990">+7 777 947 99 90</a></p>'''
    doc_page('/delete-account/index.html', 'Удаление аккаунта', 'Как пользователь приложения Yume Cloud может запросить удаление аккаунта и связанных данных.', da)
    docs = [('Политика конфиденциальности', '/legal/privacy/', 'Какие данные собираем, зачем и как защищаем.', False),
            ('Публичная оферта', 'https://drive.google.com/file/d/1HC2aDhfN5nDlu2q_M73Km5yFUF7t05C7/view', 'Условия предоставления сервиса Yume.', True),
            ('Пользовательское соглашение', 'https://drive.google.com/file/d/1ELSMnaksX3ROz7dSYNvOraV9-jUWjV78/view', 'Правила использования платформы и приложений.', True),
            ('Соглашение о рекуррентных платежах', 'https://drive.google.com/file/d/13ipJMcnRsii1qyfn9vxxOvuGCjWjxFDX/view', 'Как работает автопродление подписки.', True),
            ('Правила отмены и возврата платежей', 'https://drive.google.com/file/d/1Ui87iIFScByKXF-4_j_0rTv3RfT9kr-E/view', 'Когда и как вернуть оплату.', True),
            ('Описание процедуры оплаты', 'https://drive.google.com/file/d/1WLziN6TzG7g-xHzFDxROyK8uxSaAM_3h/view', 'Способы оплаты и порядок выставления счетов.', True),
            ('Удаление аккаунта', '/delete-account/', 'Как запросить удаление аккаунта и данных.', False)]
    items = ''.join(f'<a class="quick__i" href="{u}"{" rel=noopener" if ext else ""}><h3>{t}</h3><p>{d}</p><span class="link">{"Открыть PDF" if ext else "Читать"} <svg><use href="#i-arrow"/></svg></span></a>' for t, u, d, ext in docs)
    body = f'''
<section class="phero"><div class="wrap">
  <nav class="crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span><b>Документы</b></nav>
  <p class="eyebrow">Документы</p><h1 style="font-size:clamp(30px,3.6vw,44px)">Юридические документы Yume</h1>
  <p class="lead">Оферта, соглашения и политика конфиденциальности ТОО «Yume.Cloud». Вопросы по документам: <a class="link" href="mailto:sales@yume.cloud">sales@yume.cloud</a>.</p>
</div></section>
<section class="section section--soft" style="padding-top:48px"><div class="wrap"><div class="quick quick--3" data-stagger>{items}</div></div></section>'''
    write('/legal/index.html', page('Документы — Yume', 'Публичная оферта, пользовательское соглашение, политика конфиденциальности и правила оплаты сервиса Yume.', '/legal/', body))

# inject analytics into generated pages
_page = page
def page(title, desc, path, body, light_nav=True):
    return _page(title, desc, path, body, light_nav).replace('</head>', ANALYTICS + '\n</head>', 1) if ANALYTICS else _page(title, desc, path, body, light_nav)


def service_files():
    pages = ['/', '/solutions/', '/check/', '/contacts/', '/download/', '/feed/', '/legal/', '/legal/privacy/', '/delete-account/'] + [f'/solutions/{s["slug"]}/' for s in SEGMENTS]
    today = __import__('datetime').date.today().isoformat()
    urls = ''.join(f'  <url><loc>https://www.yume.cloud{p}</loc><lastmod>{today}</lastmod><changefreq>{"weekly" if p in ("/", "/solutions/") else "monthly"}</changefreq><priority>{"1.0" if p == "/" else "0.8" if p.startswith("/solutions") or p == "/check/" else "0.5"}</priority></url>\n' for p in pages)
    write('/sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    write('/robots.txt', 'User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: https://www.yume.cloud/sitemap.xml\n')
    body = """
<section class="phero phero--center" style="min-height:70vh;display:grid;align-items:center">
  <div class="wrap">
    <p class="eyebrow">Ошибка 404</p>
    <h1>Такой страницы нет</h1>
    <p class="lead">Возможно, ссылка устарела после обновления сайта. Вот куда можно пойти дальше.</p>
    <div class="hero__ctas" style="opacity:1;animation:none;margin-top:28px">
      <a class="btn btn--lg" href="/">На главную <svg><use href="#i-arrow"/></svg></a>
      <a class="btn btn--lg btn--ghost" href="/solutions/">Решения</a>
      <a class="btn btn--lg btn--ghost" href="/check/">Проверка клиента</a>
    </div>
  </div>
</section>"""
    write('/404.html', page('Страница не найдена — Yume', 'Страница не найдена.', '/404.html', body))

for i, s in enumerate(SEGMENTS):
    solution_page(s, i)
solutions_index()
contacts()
check_page()
download_page()
feed_page()
legal_pages()
service_files()
