from telegram import *
from telegram.ext import *
import logging

'''config'''
token = "1410333251:AAGNcx1rGtrVBAdgvwGPIlrxaia2QCvU5Fo"
bot = Bot("1410333251:AAGNcx1rGtrVBAdgvwGPIlrxaia2QCvU5Fo")
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

class Account():
    def __init__(
            self,
            username = None,
            name = None,
            roomnumber = None,
            faculty = None,
            course = None,
            mods = None):
        self.name = name
        self.username = username
        self.roomnumber = roomnumber
        self.faculty = faculty
        self.course = course
        self.mods = mods




updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher
print(Bot.get_me(bot))
''''commands'''

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Eusoff Mods Community, please register with your room "
                                                                    "number, e.g. D418")

def response(update, context):
    #if account not in JSON file: carry on, basically you can only type nonsense if you are registering, else you will just clickeroo
    data = update.effective_chat
    username = data['username']
    name = data['first_name']
    newaccount = Account(username = username, name = name)
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text + ' ' + name)

def faculty(update: Update, _: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Science", callback_data='1'),
            InlineKeyboardButton("Computing", callback_data='2'),
        ],
        [InlineKeyboardButton("Business", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


''''''''

response_handler = MessageHandler(Filters.text & (~Filters.command), response)
dispatcher.add_handler(response_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Add conversation handler with the states ROOM NUMBER, FACULTY, COURSE and MODS
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        ROOM NUMBER: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender)],
        PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
        LOCATION: [
            MessageHandler(Filters.location, location),
            CommandHandler('skip', skip_location),
        ],
        BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

updater.dispatcher.add_handler(CommandHandler('faculty', faculty))
updater.dispatcher.add_handler(CallbackQueryHandler(button))


'''The below message handler MUST be the last'''
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)



updater.start_polling()


# dispatcher.add_handler(start_value)
# print(bot.get_updates())
#
# test = ConversationHandler()
# print(test)