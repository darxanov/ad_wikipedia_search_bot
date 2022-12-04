from telegram.ext import Updater, Dispatcher, CommandHandler, CallbackContext, MessageHandler
from telegram.update import Update
import settings
import requests
from telegram.ext.filters import Filters

updater = Updater(token=settings.TELEGRAM_TOKEN)

def start(update: Update, context: CallbackContext):
    # print(update)
    update.message\
    .reply_text('Assalomu alaykum! Vikipediadan ma\'lumot qidiruvchi '
                'botga hush kelibsiz! Biron nima izlash uchun /search '
                'va so\'rovingizni yozing. Misol uchun /search Amir Temur')
    # context.bot.send_message(chat_id=update.message.chat_id, text='Salom yana bir bor')

def search(update: Update, context: CallbackContext):
    args = context.args
    if len(args) == 0:
        update.message.reply_text('Nimadir kiriting! Misol uchun /search Amir Temur')
    else:
        search_text = ' '.join(args)
        # print(search_text)
        response = requests.get('https://en.wikipedia.org/w/api.php', {
            'action': 'opensearch',
            'search': search_text,
            'limit': 1,
            'namespace': 0,
            'format': 'json'
        })
        result = response.json()
        link = result[3]
        if len(link):
            update.message.reply_text('Sizning so\'rovingiz bo\'yicha havola: ' + link[0])
        else:
            update.message.reply_text('So\'rovingizga mos bo\'lgan ma\'lumot topilmadi')
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('search', search))
dispatcher.add_handler(MessageHandler(Filters.all, start))

updater.start_polling()
updater.idle()