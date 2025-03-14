from flask import Flask, request
import jdatetime, datetime
import telepot
import urllib3
from telepot.namedtuple import ReplyKeyboardMarkup
from mtranslate import translate
from random import randint
import requests
from mytoken import mytoken
from scraping import lis
import urls_price
# ======================================================================================================================
# تنظیمات پروکسی برای استفاده از telepot
# ======================================================================================================================
proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (
    urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
# ======================================================================================================================
# تنظیمات اولیه بات تلگرام و اتصال به وب‌هوک
# ======================================================================================================================
secret = "BOT"
bot = telepot.Bot(mytoken)
bot.setWebhook("https://matin200012.pythonanywhere.com/{}".format(secret), max_connections=1)
app = Flask(__name__)
state = {}
# ======================================================================================================================
# تابع برای دریافت اطلاعات آب و هوا از API
# ======================================================================================================================
def weather(city, key, chat_id):
    URL = "https://api.openweathermap.org/data/2.5/weather"
    PARAMS = {'q': city, 'appid': key}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    name = data['name']
    tm = data['main']['temp']
    hmt = data['main']['humidity']
    Condition = data['weather'][0]['description']
    country = data['sys']['country']
    min_temp = data['main']['temp_min']
    max_temp = data['main']['temp_max']
    wind_speed = data['wind']['speed']
    wind_deg = data['wind']['deg']
    sunrise = str(datetime.datetime.fromtimestamp(data['sys']['sunrise'] + 12700))
    sunset = str(datetime.datetime.fromtimestamp(data['sys']['sunset'] + 12650))
    ctime = str(datetime.datetime.fromtimestamp(data['dt'] + 12650))
# ======================================================================================================================
# بازگرداندن اطلاعات آب و هوا به فرمت دلخواه
# ======================================================================================================================
    return (
        f'''
🌍اطلاعات :

کشور : {country}
نام شهر : {name}
زمان : {ctime[11:16]}

⛅️وضعیت هوا :

شرایط : {Condition}
دما : {"%.2f" % (float(tm - 272.15))}C
کمترین دما : {"%.2f" % (float(min_temp - 272.15))}C
بیشترین دما : {"%.2f" % (float(max_temp - 272.15))}C
رطوبت : {hmt}%

☀️طلوع/غروب :

طلوع : {sunrise[11:16]}
غروب : {sunset[11:16]}

🌪باد :

سرعت باد : {wind_speed}km/h
درجه باد : {wind_deg}
            '''
    )
# ======================================================================================================================
# تابع برای انتخاب یک عدد تصادفی
# ======================================================================================================================
def choice(number):
    return randint(1, number)
# ======================================================================================================================
# تابع برای پردازش پیام‌های دریافتی از تلگرام
# ======================================================================================================================
def handle(msg):
    global state
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        if chat_id not in state:
            state[chat_id] = None
# ======================================================================================================================
# پردازش پیام‌های متنی
# ======================================================================================================================
        if msg['text'] == '/start':
            state[chat_id] = None
            reply = """
            سلام به ربات من خوش آمدید ✌
یکی از گزینه های زیر را انتخاب کنید 👇
            """
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    ['دیدن قیمت لحظه طلا و دلار و ارز', 'ترجمه'],
                    ['چت id', 'دیدن اطلاعات آب و هوا', 'زمان شمسی و میلادی']
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
            bot.sendMessage(chat_id, reply, reply_markup=keyboard)

        elif state[chat_id] == 'waiting_for_translation':
            txt = msg['text']
            tr = translate(txt, 'fa', 'auto')
            bot.sendMessage(chat_id, tr)
            state[chat_id] = None

        elif msg['text'] == 'ترجمه':
            bot.sendMessage(chat_id, 'لطفاً متن خود را برای ترجمه بنویسید')
            state[chat_id] = 'waiting_for_translation'
        elif msg['text'] == 'زمان شمسی و میلادی':
            s = str(jdatetime.date.today()).replace('-', '/')
            ad = str(datetime.date.today()).replace('-', '/')
            bot.sendMessage(chat_id, f'☀️{s}☀️\n- - - - - - - - - - - - - - -\n🎄{ad}🎄')

        elif msg['text'] == 'چت id':
            bot.sendMessage(chat_id, chat_id)

        elif msg['text'] == 'دیدن قیمت لحظه طلا و دلار و ارز':
            try:
                s_price = list(map(urls_price.cost, (lis)))
                f_price = urls_price.design(lst=s_price)
                bot.sendMessage(chat_id, f_price)
            except:
                bot.sendMessage(chat_id, 'مشکلی پیش آمد. لطفاً بعداً دوباره تلاش کنید.')

        elif msg['text'] == 'دیدن اطلاعات آب و هوا':
            bot.sendMessage(chat_id, 'لطفاً نام شهر خود را برای اطلاعات آب و هوا بنویسید')
            state[chat_id] = 'waiting_for_weather'

        elif state[chat_id] == 'waiting_for_weather':
            key = 'ce28524cced047e5c594dabe55a408be'
            city = msg['text']
            bot.sendMessage(chat_id, weather(city=city, key=key, chat_id=chat_id))
            state[chat_id] = None

        else:
            bot.sendMessage(chat_id, "دستور نامعتبر. لطفاً از /start برای مشاهده گزینه‌های موجود استفاده کنید.")

    elif content_type == 'callback_query':
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        if query_data == 'price':
            try:
                s_price = list(map(urls_price.cost, (lis)))
                f_price = urls_price.design(lst=s_price)
                bot.sendMessage(from_id, f_price)
            except:
                bot.sendMessage(from_id, 'مشکلی پیش آمد. لطفاً بعداً دوباره تلاش کنید.')

        elif query_data == 'چت id':
            bot.sendMessage(from_id, from_id)

        elif query_data == 'ترجمه':
            bot.sendMessage(from_id, 'لطفاً متن خود را برای ترجمه بنویسید')
            state[from_id] = 'waiting_for_translation'

        elif query_data == 'دیدن اطلاعات آب و هوا':
            bot.sendMessage(from_id, 'لطفاً نام شهر خود را برای اطلاعات آب و هوا بنویسید')
            state[from_id] = 'waiting_for_weather'
# ======================================================================================================================
# تنظیمات وب‌هوک برای دریافت پیام‌های تلگرام
# ======================================================================================================================
@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        handle(update['message'])
    elif "callback_query" in update:
        handle(update['callback_query'])
    return "OK"
# ======================================================================================================================