import json
from telegram import *
from telegram.ext import *
import logging

'''config'''
token = "1783610928:AAFr2EFtaXtbvlfnpuUUXvJ4h-_lBntx1v4"
bot = Bot("1783610928:AAFr2EFtaXtbvlfnpuUUXvJ4h-_lBntx1v4")
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


class Account:
    def __init__(
            self,
            username=None,
            name=None,
            roomnumber=None,
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
        'Welcome to Eusoff Mods Community, please register with your room number, if you make a mistake anytime, restart by typing /cancel')
    return ROOMNUMBER


def roomnumber(update: Update, _: CallbackContext) -> int:
    reply_keyboard = [['Biz', 'Computing', 'SDE', 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ], ['ISE', 'Music', 'Public Health']]
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
    reply_keyboard = [['Biz', 'Computing', 'GE Mods' , 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ], ['ISE', 'Music', 'Public Health','SDE']]
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
        'Please indicate the name of your first mod e.g. CS1010S or /done when you have enumerated all your courses or /cancel to restart',
        reply_markup=ReplyKeyboardRemove())
    return MODS1


def mods1(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Biz', 'Computing', 'GE Mods' , 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ], ['ISE', 'Music', 'Public Health','SDE']]
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
        'Please indicate the name of your second mod e.g. CS1010S or /done when you have enumerated all your courses '
        'or /cancel to restart',
        reply_markup=ReplyKeyboardRemove())
    return MODS2


def mods2(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Biz', 'Computing', 'GE Mods' , 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ], ['ISE', 'Music', 'Public Health','SDE']]
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
        'Please indicate the name of your third mod e.g. CS1010S or /done when you have enumerated all your courses '
        'or /cancel to restart',
        reply_markup=ReplyKeyboardRemove())
    return MODS3


def mods3(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Biz', 'Computing', 'GE Mods' , 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ], ['ISE', 'Music', 'Public Health','SDE']]
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
        'Please indicate the name of your fourth mod e.g. CS1010S or /done when you have enumerated all your courses '
        'or /cancel to restart',
        reply_markup=ReplyKeyboardRemove())
    return MODS4


def mods4(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Biz', 'Computing', 'GE Mods' , 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ], ['ISE', 'Music', 'Public Health','SDE']]
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
        'Please indicate the name of your fifth mod e.g. CS1010S or /done when you have enumerated all your courses '
        'or /cancel to restart',
        reply_markup=ReplyKeyboardRemove())
    return MODS5


def mods5(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Biz', 'Computing', 'GE Mods' , 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ], ['ISE', 'Music', 'Public Health','SDE']]
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
        'Please indicate the name of your sixth mod e.g. CS1010S or /done when you have enumerated all your courses '
        'or /cancel to restart',
        reply_markup=ReplyKeyboardRemove())
    return MODS6


def mods6(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Biz', 'Computing', 'GE Mods' , 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ], ['ISE', 'Music', 'Public Health','SDE']]
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
        'Please indicate the name of your seventh mod e.g. CS1010S or /done when you have enumerated all your courses '
        'or /cancel to restart',
        reply_markup=ReplyKeyboardRemove())
    return MODS7


def mods7(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Biz', 'Computing', 'GE Mods' , 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ], ['ISE', 'Music', 'Public Health','SDE']]
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
        'Please indicate the name of your eigth mod e.g. CS1010S or /done when you have enumerated all your courses '
        'or /cancel to restart',
        reply_markup=ReplyKeyboardRemove())
    return MODS8


def mods8(update: Update, _: CallbackContext):
    user = update.message.from_user
    reply_keyboard = [['Biz', 'Computing', 'GE Mods' , 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ], ['ISE', 'Music', 'Public Health','SDE']]
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
        'Cancelled, you may run another command \n /start to register \n /mods to check mods', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Selected option: {query.data}")


GETFACULTIES, GETMODS = range(2)


def mods(update: Update, _: CallbackContext) -> None:
    with open('data.json', 'r+') as f:
        data = json.load(f)
        faculty = []
        for fac in data['Faculties']:
            faculty.append(fac)
        faculty.sort()
        keyboard = []
        for i in faculty:
            keyboard.append([InlineKeyboardButton(i, callback_data = str(i))])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    return GETFACULTIES


temp_faculty_chosen = ''


def getfaculties(update: Update, _: CallbackContext) -> int:
    faculty_chosen = str(update.callback_query.data)
    query = update.callback_query
    query.edit_message_text(text=f"Selected option: {query.data}")
    global temp_faculty_chosen
    temp_faculty_chosen = query.data
    with open('data.json', 'r+') as f:
        data = json.load(f)
        mods = []
        for mod in data['Faculties'][faculty_chosen]:
            mods.append(mod)
        mods.sort()
        keyboard = []
        for i in mods:
            keyboard.append([InlineKeyboardButton(i, callback_data = i)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_message.reply_text('Please choose:', reply_markup=reply_markup)
    return GETMODS


def getmods(update: Update, _: CallbackContext):
    mod_chosen = str(update.callback_query.data)
    query = update.callback_query
    query.edit_message_text(text=f"Selected option: {query.data}")
    with open('data.json', 'r+') as f:
        data = json.load(f)
        names = []
        for username in data['Faculties'][temp_faculty_chosen][mod_chosen]:
            names.append(username)
    namelist = 'Usernames of Eusoffians taking' + ' ' + mod_chosen + '\n'
    for name in names:
        namelist += name + '\n'
    update.effective_message.reply_text(namelist)
    return ConversationHandler.END


# def groupchatcreated(update: Update, _: CallbackContext):
#     mod_chosen = str(update.callback_query.data)
#     query = update.callback_query
#     query.edit_message_text(text=f"Selected option: {query.data}")
#     link = ChatInviteLink.invite_link
#     print(type(link))
#     print(str(link))
    # with open('data.json', 'r+') as f:
    #     data = json.load(f)
    #     data['Faculties'][temp_faculty_chosen][mod_chosen].insert(0,link)
    #     f.seek(0)
    #     json.dump(data, f, indent=4)


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
            FACULTY: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|Law|Medicine|SDE|Public '
                                                   'Policy|ISE|Music|Public Health)$'), faculty)],
            COURSE: [MessageHandler(Filters.text & ~Filters.command, course)],
            MODS1_F: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|Law|Medicine|SDE|Public '
                                                   'Policy|ISE|Music|Public Health|GE Mods)$'), mods1_f),
                      CommandHandler('done', done)],
            MODS1: [MessageHandler(Filters.text & ~Filters.command, mods1), CommandHandler('done', done)],
            MODS2_F: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|Law|Medicine|SDE|Public '
                                                   'Policy|ISE|Music|Public Health|GE Mods)$'), mods2_f),
                      CommandHandler('done', done)],
            MODS2: [MessageHandler(Filters.text & ~Filters.command, mods2),CommandHandler('done', done)],
            MODS3_F: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|Law|Medicine|SDE|Public '
                                                   'Policy|ISE|Music|Public Health|GE Mods)$'), mods3_f),
                      CommandHandler('done', done)],
            MODS3: [MessageHandler(Filters.text & ~Filters.command, mods3),CommandHandler('done', done)],
            MODS4_F: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|Law|Medicine|SDE|Public '
                                                   'Policy|ISE|Music|Public Health|GE Mods)$'), mods4_f),
                      CommandHandler('done', done)],
            MODS4: [MessageHandler(Filters.text & ~Filters.command, mods4), CommandHandler('done', done)],
            MODS5_F: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|Law|Medicine|SDE|Public '
                                                   'Policy|ISE|Music|Public Health|GE Mods)$'), mods5_f),
                      CommandHandler('done', done)],
            MODS5: [MessageHandler(Filters.text & ~Filters.command, mods5), CommandHandler('done', done)],
            MODS6_F: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|Law|Medicine|SDE|Public '
                                                   'Policy|ISE|Music|Public Health|GE Mods)$'), mods6_f),
                      CommandHandler('done', done)],
            MODS6: [MessageHandler(Filters.text & ~Filters.command, mods6), CommandHandler('done', done)],
            MODS7_F: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|Law|Medicine|SDE|Public '
                                                   'Policy|ISE|Music|Public Health|GE Mods)$'), mods7_f),
                      CommandHandler('done', done)],
            MODS7: [MessageHandler(Filters.text & ~Filters.command, mods7), CommandHandler('done', done)],
            MODS8_F: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|Law|Medicine|SDE|Public '
                                                   'Policy|ISE|Music|Public Health|GE Mods)$'), mods8_f),
                      CommandHandler('done', done)
    ],
            MODS8: [MessageHandler(Filters.text & ~Filters.command, mods8), CommandHandler('done', done)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],)

    dispatcher.add_handler(account_initialisation)

    module_recall = ConversationHandler(
        entry_points=[CommandHandler('mods', mods)],
        states={
            GETFACULTIES: [CallbackQueryHandler(getfaculties)],
            GETMODS: [CallbackQueryHandler(getmods)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],)
    dispatcher.add_handler(module_recall)

    create_group = ConversationHandler(
        entry_points=[CommandHandler('groupchatcreated', mods)],
        states={
            GETFACULTIES: [CallbackQueryHandler(getfaculties)],
            GETMODS: [CallbackQueryHandler(groupchatcreated)],
        },
        fallbacks=[CommandHandler('cancel', cancel)], )
    dispatcher.add_handler(create_group)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    updater.start_polling()

if __name__ == '__main__':
    main()
