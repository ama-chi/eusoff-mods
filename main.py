import json

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
            mods=None):
        if mods is None:
            mods = {}
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

# def start(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Eusoff Mods Community, please register with your room "
#                                                                     "number, e.g. D418")
ROOMNUMBER, FACULTY, COURSE, MODS1_F, MODS1, MODS2_F, MODS2, MODS3_F, MODS3, MODS4_F, MODS4, MODS5_F, MODS5, MODS6_F, MODS6, MODS7_F, MODS7, MODS8_F, MODS8 = range(19)

def initialise_account(user):
    with open('data.json', 'r+') as f:
        data = json.load(f)
        username = str(user)
        if username not in data['accounts']:
            data['accounts'][username] = {}
        data['accounts'][username]['roomnumber'] = newaccount.roomnumber
        data['accounts'][username]['faculty'] = newaccount.faculty
        data['accounts'][username]['course'] = newaccount.course
        data['accounts'][username]['mods'] = newaccount.mods
        f.seek(0)
        json.dump(data, f, indent=4)

def initialise_modules(user):
    username = str(user)
    with open('data.json', 'r+') as f:
        data = json.load(f)
        for fac in newaccount.mods:
            for mod in newaccount.mods[fac]:
                if mod not in data['Faculties'][fac]:
                    data['Faculties'][fac][mod] = []
                data['Faculties'][fac][mod].append('@' + username)
        f.seek(0)
        json.dump(data, f, indent=4)
                    
                    

def start(update: Update, _: CallbackContext) -> int:
    data = update.effective_chat
    username = data['username']
    name = data['first_name']
    global newaccount
    newaccount = Account()
    newaccount.username = username
    newaccount.name = name
    update.message.reply_text(
        'Welcome to Eusoff Mods Community, please register with your room number')
    return ROOMNUMBER


def roomnumber(update: Update, _: CallbackContext) -> int:
    reply_keyboard = [['Biz', 'Computing', 'Dentistry', 'Engineering'],['FASS', 'Science', 'Law', 'Medicine', ]]
    user = update.message.from_user
    logger.info("Room Number of %s: %s", user.first_name, update.message.text.upper())
    newaccount.roomnumber = update.message.text.upper()
    update.message.reply_text(
        'Please indicate your faculty',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return FACULTY


def faculty(update: Update, _: CallbackContext) -> int:
    #here we intend to extract all the course that has been input by
    #users, but for testing sake lets just manually input, use the if not in method
    user = update.message.from_user
    logger.info("Faculty of %s: %s", user.first_name, update.message.text)
    newaccount.faculty = update.message.text
    update.message.reply_text(
        'Please indicate your course',
        reply_markup=ReplyKeyboardRemove())
    return COURSE


def course(update: Update, _: CallbackContext) -> int:
    reply_keyboard = [['Biz', 'Computing', 'Engineering'], ['FASS', 'Science', 'GE Mods']]
    user = update.message.from_user
    logger.info("Course of %s: %s", user.first_name, update.message.text.upper())
    newaccount.course = update.message.text.upper()
    update.message.reply_text(
        'Please indicate the faculty of your first mod',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return MODS1_F


temp_faculty = ''


def mods1_f(update: Update, _: CallbackContext) -> int:
    global temp_faculty
    temp_faculty = update.message.text
    if temp_faculty not in newaccount.mods:
        newaccount.mods[temp_faculty] = []
    update.message.reply_text(
        'Please indicate the name of your first mod e.g. CS1010S',
        reply_markup=ReplyKeyboardRemove())
    return MODS1


def mods1(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Biz', 'Computing', 'Engineering'], ['FASS', 'Science', 'GE Mods']]
    logger.info(temp_faculty + " Mod 1 of %s: %s", user.first_name, update.message.text.upper())
    newaccount.mods[temp_faculty].append(update.message.text.upper())
    print(newaccount.mods)
    update.message.reply_text(
        'Please indicate the faculty of your second mod',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return MODS2_F


def mods2_f(update: Update, _: CallbackContext) -> int:
    global temp_faculty
    temp_faculty = update.message.text
    if temp_faculty not in newaccount.mods:
        newaccount.mods[temp_faculty] = []
    update.message.reply_text(
        'Please indicate the name of your second mod e.g. CS1010S',
        reply_markup=ReplyKeyboardRemove())
    return MODS2


def mods2(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Biz', 'Computing', 'Engineering'], ['FASS', 'Science', 'GE Mods']]
    logger.info(temp_faculty + " Mod 2 of %s: %s", user.first_name, update.message.text.upper())
    newaccount.mods[temp_faculty].append(update.message.text.upper())
    print(newaccount.mods)
    update.message.reply_text(
        'Please indicate the faculty of your third mod',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return MODS3_F


def mods3_f(update: Update, _: CallbackContext) -> int:
    global temp_faculty
    temp_faculty = update.message.text
    if temp_faculty not in newaccount.mods:
        newaccount.mods[temp_faculty] = []
    update.message.reply_text(
        'Please indicate the name of your third mod e.g. CS1010S',
        reply_markup=ReplyKeyboardRemove())
    return MODS3


def mods3(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Biz', 'Computing', 'Engineering'], ['FASS', 'Science', 'GE Mods']]
    logger.info(temp_faculty + " Mod 3 of %s: %s", user.first_name, update.message.text.upper())
    newaccount.mods[temp_faculty].append(update.message.text.upper())
    print(newaccount.mods)
    update.message.reply_text(
        'Please indicate the faculty of your fourth mod',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return MODS4_F


def mods4_f(update: Update, _: CallbackContext) -> int:
    global temp_faculty
    temp_faculty = update.message.text
    if temp_faculty not in newaccount.mods:
        newaccount.mods[temp_faculty] = []
    update.message.reply_text(
        'Please indicate the name of your fourth mod e.g. CS1010S',
        reply_markup=ReplyKeyboardRemove())
    return MODS4


def mods4(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Biz', 'Computing', 'Engineering'], ['FASS', 'Science', 'GE Mods']]
    logger.info(temp_faculty + " Mod 4 of %s: %s", user.first_name, update.message.text.upper())
    newaccount.mods[temp_faculty].append(update.message.text.upper())
    print(newaccount.mods)
    update.message.reply_text(
        'Please indicate the faculty of your fifth mod',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return MODS5_F


def mods5_f(update: Update, _: CallbackContext) -> int:
    global temp_faculty
    temp_faculty = update.message.text
    if temp_faculty not in newaccount.mods:
        newaccount.mods[temp_faculty] = []
    update.message.reply_text(
        'Please indicate the name of your fifth mod e.g. CS1010S or /done when you have enumerated all your courses',
        reply_markup=ReplyKeyboardRemove())
    return MODS5


def mods5(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Biz', 'Computing', 'Engineering'], ['FASS', 'Science', 'GE Mods']]
    logger.info(temp_faculty + " Mod 5 of %s: %s", user.first_name, update.message.text.upper())
    newaccount.mods[temp_faculty].append(update.message.text.upper())
    update.message.reply_text(
        'Please indicate the faculty of your sixth mod',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return MODS6_F


def mods6_f(update: Update, _: CallbackContext) -> int:
    global temp_faculty
    temp_faculty = update.message.text
    if temp_faculty not in newaccount.mods:
        newaccount.mods[temp_faculty] = []
    update.message.reply_text(
        'Please indicate the name of your sixth mod e.g. CS1010S or /done when you have enumerated all your courses',
        reply_markup=ReplyKeyboardRemove())
    return MODS6


def mods6(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Biz', 'Computing', 'Engineering'], ['FASS', 'Science', 'GE Mods']]
    logger.info(temp_faculty + " Mod 6 of %s: %s", user.first_name, update.message.text.upper())
    newaccount.mods[temp_faculty].append(update.message.text.upper())
    update.message.reply_text(
        'Please indicate the faculty of your seventh mod',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return MODS7_F


def mods7_f(update: Update, _: CallbackContext) -> int:
    global temp_faculty
    temp_faculty = update.message.text
    if temp_faculty not in newaccount.mods:
        newaccount.mods[temp_faculty] = []
    update.message.reply_text(
        'Please indicate the name of your seventh mod e.g. CS1010S or /done when you have enumerated all your courses',
        reply_markup=ReplyKeyboardRemove())
    return MODS7


def mods7(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Biz', 'Computing', 'Engineering'], ['FASS', 'Science', 'GE Mods']]
    logger.info(temp_faculty + " Mod 7 of %s: %s", user.first_name, update.message.text.upper())
    newaccount.mods[temp_faculty].append(update.message.text.upper())
    update.message.reply_text(
        'Please indicate the faculty of your eighth mod',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return MODS8_F


def mods8_f(update: Update, _: CallbackContext) -> int:
    global temp_faculty
    temp_faculty = update.message.text
    if temp_faculty not in newaccount.mods:
        newaccount.mods[temp_faculty] = []
    update.message.reply_text(
        'Please indicate the name of your eigth mod e.g. CS1010S or /done when you have enumerated all your courses',
        reply_markup=ReplyKeyboardRemove())
    return MODS8


def mods8(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Biz', 'Computing', 'Engineering'], ['FASS', 'Science', 'GE Mods']]
    logger.info(temp_faculty + " Mod 8 of %s: %s", user.first_name, update.message.text.upper())
    newaccount.mods[temp_faculty].append(update.message.text.upper())
    print(newaccount.mods)
    update.message.reply_text(
        'Please indicate the faculty of your mods',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def done(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    initialise_account(user.username)
    initialise_modules(user.username)
    update.message.reply_text(
        'Your data has been stored into the system, please type /mods and follow instructions to find people who are taking the same'
        ' mods as you do'
    )
    return ConversationHandler.END


def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Registration cancelled', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def mods():


# def response(update, context):
#     #if account not in JSON file: carry on, basically you can only type nonsense if you are registering, else you will just clickeroo
#     data = update.effective_chat
#     username = data['username']
#     name = data['first_name']
#     newaccount = Account(username = username, name = name)
#     context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text + ' ' + name)




def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


''''''''

# response_handler = MessageHandler(Filters.text & (~Filters.command), response)
# dispatcher.add_handler(response_handler)

# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)

# Add conversation handler with the states ROOM NUMBER, FACULTY, COURSE and MODS

def main():
    account_initialisation = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ROOMNUMBER: [MessageHandler(Filters.text & ~Filters.command, roomnumber)],
            FACULTY: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|Law|Medicine)$'), faculty)],
            COURSE: [MessageHandler(Filters.text & ~Filters.command, course)],
            MODS1_F: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|GE Mods)$'), mods1_f),
                      CommandHandler('done', done)],
            MODS1: [MessageHandler(Filters.text & ~Filters.command, mods1), CommandHandler('done', done)],
            MODS2_F: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|GE Mods)$'), mods2_f),
                      CommandHandler('done', done)],
            MODS2: [MessageHandler(Filters.text & ~Filters.command, mods2),CommandHandler('done', done)],
            MODS3_F: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|GE Mods)$'), mods3_f),
                      CommandHandler('done', done)],
            MODS3: [MessageHandler(Filters.text & ~Filters.command, mods3),CommandHandler('done', done)],
            MODS4_F: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|GE Mods)$'), mods4_f),
                      CommandHandler('done', done)],
            MODS4: [MessageHandler(Filters.text & ~Filters.command, mods4), CommandHandler('done', done)],
            MODS5_F: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|GE Mods)$'), mods5_f),
                      CommandHandler('done', done)],
            MODS5: [MessageHandler(Filters.text & ~Filters.command, mods5), CommandHandler('done', done)],
            MODS6_F: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|GE Mods)$'), mods6_f),
                      CommandHandler('done', done)],
            MODS6: [MessageHandler(Filters.text & ~Filters.command, mods6), CommandHandler('done', done)],
            MODS7_F: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|GE Mods)$'), mods7_f),
                      CommandHandler('done', done)],
            MODS7: [MessageHandler(Filters.text & ~Filters.command, mods7), CommandHandler('done', done)],
            MODS8_F: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|GE Mods)$'), mods8_f),
                      CommandHandler('done', done)
    ],
            MODS8: [MessageHandler(Filters.text & ~Filters.command, mods8), CommandHandler('done', done)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],)

    dispatcher.add_handler(account_initialisation)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    updater.start_polling()

if __name__ == '__main__':
    main()
