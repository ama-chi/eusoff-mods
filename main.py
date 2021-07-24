import telegram
from telegram import *
from telegram.ext import *
import logging
import psycopg2 as pg2
import re

'''config'''
token = "1783610928:AAFr2EFtaXtbvlfnpuUUXvJ4h-_lBntx1v4"
bot = Bot("1783610928:AAFr2EFtaXtbvlfnpuUUXvJ4h-_lBntx1v4")
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

host = 'ec2-34-195-143-54.compute-1.amazonaws.com'
database = 'd3pb9jkfc1jkat'
user_database = 'ckwbcsfhmslojp'
password = '314cc6f1c2ef1e61c470ce5ebf1b3c1eed63ad8be4376227350ecd1b4acd96fa'

replyKeyboardStandard = [['/mods', '/cancel', '/help', '/mymods'],
                         ['/groupchatcreated', '/deletemod', '/addmod']]

replyKeyboardFaculties = [['Biz', 'Computing', 'CHS(AY21/22 Onwards)', 'Engineering'],
                          ['FASS', 'Science', 'Law', 'Public Policy', ],
                          ['ISE', 'Music', 'Public Health', 'SDE']]

replyKeyboardModFaculties = [['Biz', 'Computing', 'GE Mods', 'Engineering'],
                             ['FASS', 'Science', 'Law', 'Public Policy', ],
                             ['ISE', 'Music', 'Public Health', 'SDE']]
''''''''


class Account:
    def __init__(
            self,
            username=None,
            name=None,
            roomnumber=None,
            faculty=None,
            course=None,
            mods=None,
            year=None,
            chat_id=None):
        if mods is None:
            mods = {}
        self.name = name
        self.username = username
        self.roomNumber = roomnumber
        self.faculty = faculty
        self.course = course
        self.mods = mods
        self.year = year
        self.chat_id = chat_id


updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher
print(Bot.get_me(bot))
''''commands'''

ROOMNUMBER, FACULTY, COURSE, YEAR, MODS1_F, MODS1, MODS2_F, MODS2, MODS3_F, MODS3, MODS4_F, MODS4, MODS5_F, MODS5, MODS6_F, MODS6, MODS7_F, MODS7, MODS8_F, MODS8 = range(
    20)

selectionDict = {}
dictDict = {}
newAccountDict = {}


def input_id_into_selection_dict(username):
    if username not in selectionDict:
        selectionDict[username] = ''


def input_id_into_dict_dict(username):
    if username not in dictDict:
        dictDict[username] = {}


def input_id_into_newAccountDict(username):
    if username not in newAccountDict:
        newAccountDict[username] = Account()


def initialise_account(update: Update):
    newAccount = newAccountDict[update.effective_chat.username]
    conn = pg2.connect(host=host, database=database,
                       user=user_database,
                       password=password)
    cur = conn.cursor()
    insert_account = '''
           INSERT INTO accounts(username,name,roomnumber,faculty,course,year,chat_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (chat_id) DO NOTHING
            '''
    cur.execute(insert_account,
                (newAccount.username, newAccount.name, newAccount.roomNumber, newAccount.faculty, newAccount.course,
                 newAccount.year, newAccount.chat_id))
    for fac in newAccount.mods:
        for mod in newAccount.mods[fac]:
            insert_to_all_modules = '''
                        INSERT INTO all_modules(mod_name,faculty_id)
                        VALUES(%s,(SELECT faculty_id FROM faculties
                        WHERE faculty_name = %s))
                        ON CONFLICT (mod_name) DO NOTHING
                         '''
            cur.execute(insert_to_all_modules, (mod, fac.lower()))
    conn.commit()
    for fac in newAccount.mods:
        for mod in newAccount.mods[fac]:
            insert_to_mods = '''
                        INSERT INTO mods(account_id,mod_id,faculty_id)
                        VALUES((SELECT id FROM accounts
                        WHERE username = %s),(SELECT mod_id FROM all_modules
                        WHERE mod_name = %s), (SELECT faculty_id FROM all_modules
                        WHERE mod_name = %s))
                         '''
            cur.execute(insert_to_mods, (newAccount.username, mod, mod))
            conn.commit()

    for fac in newAccount.mods:
        for mod in newAccount.mods[fac]:
            get_chat_id = '''
                        SELECT chat_id FROM accounts
                        INNER JOIN mods 
                        ON accounts.id = mods.account_id
                        WHERE mods.mod_id = (SELECT mod_id FROM all_modules
                                            WHERE mod_name = %s)
                         '''
            cur.execute(get_chat_id, (mod,))
            data = cur.fetchall()
            for chat_id in data:
                if chat_id[0] == update.effective_message.chat_id:
                    continue
                else:
                    chat_id = chat_id[0]
                    try:
                        bot.send_message(chat_id=chat_id,
                                     text="Someone is now taking " + mod + "! Run /mods to check")
                    except:
                        continue

    conn.close()


def start(update: Update, _: CallbackContext):
    input_id_into_selection_dict(update.effective_chat.username)
    input_id_into_newAccountDict(update.effective_chat.username)
    user = update.message.from_user
    logger.info("User %s started the bot", user.username)
    reply_keyboard = [['/register']]
    update.message.reply_text(
        'Welcome to Eusoff Mods, this is a bot to identify a community of Eusoffians taking the same mods, such as GE '
        'mods, as well as the group chats created, firstly, please register up to 8 mods with /register.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def register(update: Update, _: CallbackContext) -> int:
    input_id_into_selection_dict(update.effective_chat.username)
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    user = update.message.from_user
    logger.info("User %s is registering", user.username)
    data = update.effective_chat
    username = data['username']
    name = data['first_name']
    newAccount.username = username
    newAccount.name = name
    newAccount.chat_id = update.effective_message.chat_id
    update.message.reply_text(
        'Please key in your ROOM NUMBER (for authentication purposes only, will not be disclosed) \nIf you make a '
        'mistake anytime, restart by typing /cancel. \nYou can edit your mods via /deletemod or /addmod anytime after '
        'registration.')
    print(newAccountDict)
    return ROOMNUMBER


def roomnumber(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    user = update.message.from_user
    trueOrFalse = checkvalidroomnumber(update.message.text.upper(), update)
    if trueOrFalse is False:
        return ROOMNUMBER
    logger.info("Room Number of %s: %s", user.username, update.message.text.upper())
    newAccount.roomNumber = update.message.text.upper()
    update.message.reply_text(
        'Please indicate your faculty',
        reply_markup=ReplyKeyboardMarkup(replyKeyboardFaculties, one_time_keyboard=True))
    return FACULTY


def faculty(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    user = update.message.from_user
    trueOrFalse = checkvalidfaculty(update.message.text.upper(), update)
    if trueOrFalse is False:
        return FACULTY
    logger.info("Faculty of %s: %s", user.username, update.message.text)
    newAccount.faculty = update.message.text
    update.message.reply_text(
        'Please indicate your major',
        reply_markup=ReplyKeyboardRemove())
    return COURSE


def course(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    user = update.message.from_user
    logger.info("Course of %s: %s", user.username, update.message.text.upper())
    newAccount.course = update.message.text.upper()
    yearList = ["Year 1", "Year 2", "Year 3", "Year 4"]
    keyboard = []
    for i in yearList:
        keyboard.append([InlineKeyboardButton(i, callback_data=i)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_message.reply_text('Please select your year', reply_markup=reply_markup)
    return YEAR


def year(update: Update, _: CallbackContext):
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    year = str(update.callback_query.data)
    query = update.callback_query
    query.edit_message_text(text=f"Selected option: {query.data}")
    newAccount.year = year
    update.effective_message.reply_text(
        'Please indicate the faculty of your first MOD, e.g. "FASS" for PL1101E, "Science" for MA1101R, "GE Mods" for '
        'GER1000, "Biz" for ACC1002 etc. Please check and input the correct faculty and /back whenever you make a '
        'mistake.',
        reply_markup=ReplyKeyboardMarkup(replyKeyboardModFaculties, one_time_keyboard=True))
    return MODS1_F


def mods1_f(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    tempFaculty = update.message.text
    selectionDict[update.effective_chat.username] = tempFaculty
    trueOrFalse = checkvalidfaculty(tempFaculty.upper(), update)
    if trueOrFalse is False:
        return MODS1_F
    if tempFaculty not in newAccount.mods:
        newAccount.mods[tempFaculty] = []
    update.message.reply_text(
        'Please indicate the name of your first mod e.g. CS1010S or /done when you have enumerated all your courses '
        'or /back to restart.\n\nTip: If you are prone to errors, you can /done after the first module and /addmod '
        'subsequently',
        reply_markup=ReplyKeyboardRemove())
    return MODS1


def mods1(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    user = update.message.from_user
    tempFaculty = selectionDict[update.effective_chat.username]
    trueOrFalseMod = checkvalidmod(update.message.text.upper(), update)
    if trueOrFalseMod is False:
        return MODS1
    newAccount.mods[tempFaculty].append(update.message.text.upper())
    update.message.reply_text(
        'Please indicate the faculty of your second mod',
        reply_markup=ReplyKeyboardMarkup(replyKeyboardModFaculties, one_time_keyboard=True))
    print(newAccountDict)
    return MODS2_F


def mods2_f(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    tempFaculty = update.message.text
    selectionDict[update.effective_chat.username] = tempFaculty
    trueOrFalse = checkvalidfaculty(tempFaculty.upper(), update)
    if trueOrFalse is False:
        return MODS2_F
    if tempFaculty not in newAccount.mods:
        newAccount.mods[tempFaculty] = []
    update.message.reply_text(
        'Please indicate the name of your second mod e.g. CS1010S or /done when you have enumerated all your courses '
        'or /back to restart',
        reply_markup=ReplyKeyboardRemove())
    return MODS2


def mods2(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    user = update.message.from_user
    tempFaculty = selectionDict[update.effective_chat.username]
    trueOrFalseMod = checkvalidmod(update.message.text.upper(), update)
    if trueOrFalseMod is False:
        return MODS2
    newAccount.mods[tempFaculty].append(update.message.text.upper())
    update.message.reply_text(
        'Please indicate the faculty of your third mod',
        reply_markup=ReplyKeyboardMarkup(replyKeyboardModFaculties, one_time_keyboard=True))
    return MODS3_F


def mods3_f(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    tempFaculty = update.message.text
    selectionDict[update.effective_chat.username] = tempFaculty
    trueOrFalse = checkvalidfaculty(tempFaculty.upper(), update)
    if trueOrFalse is False:
        return MODS3_F
    if tempFaculty not in newAccount.mods:
        newAccount.mods[tempFaculty] = []
    update.message.reply_text(
        'Please indicate the name of your third mod e.g. CS1010S or /done when you have enumerated all your courses '
        'or /back to restart',
        reply_markup=ReplyKeyboardRemove())
    return MODS3


def mods3(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    user = update.message.from_user
    tempFaculty = selectionDict[update.effective_chat.username]
    trueOrFalseMod = checkvalidmod(update.message.text.upper(), update)
    if trueOrFalseMod is False:
        return MODS3
    newAccount.mods[tempFaculty].append(update.message.text.upper())
    update.message.reply_text(
        'Please indicate the faculty of your fourth mod',
        reply_markup=ReplyKeyboardMarkup(replyKeyboardModFaculties, one_time_keyboard=True))
    return MODS4_F


def mods4_f(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    tempFaculty = update.message.text
    selectionDict[update.effective_chat.username] = tempFaculty
    trueOrFalse = checkvalidfaculty(tempFaculty.upper(), update)
    if trueOrFalse is False:
        return MODS4_F
    if tempFaculty not in newAccount.mods:
        newAccount.mods[tempFaculty] = []
    update.message.reply_text(
        'Please indicate the name of your fourth mod e.g. CS1010S or /done when you have enumerated all your courses '
        'or /back to restart',
        reply_markup=ReplyKeyboardRemove())
    return MODS4


def mods4(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    user = update.message.from_user
    tempFaculty = selectionDict[update.effective_chat.username]
    trueOrFalseMod = checkvalidmod(update.message.text.upper(), update)
    if trueOrFalseMod is False:
        return MODS4
    newAccount.mods[tempFaculty].append(update.message.text.upper())
    update.message.reply_text(
        'Please indicate the faculty of your fifth mod',
        reply_markup=ReplyKeyboardMarkup(replyKeyboardModFaculties, one_time_keyboard=True))
    return MODS5_F


def mods5_f(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    tempFaculty = update.message.text
    selectionDict[update.effective_chat.username] = tempFaculty
    trueOrFalse = checkvalidfaculty(tempFaculty.upper(), update)
    if trueOrFalse is False:
        return MODS5_F
    if tempFaculty not in newAccount.mods:
        newAccount.mods[tempFaculty] = []
    update.message.reply_text(
        'Please indicate the name of your fifth mod e.g. CS1010S or /done when you have enumerated all your courses '
        'or /back to restart',
        reply_markup=ReplyKeyboardRemove())
    return MODS5


def mods5(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    user = update.message.from_user
    tempFaculty = selectionDict[update.effective_chat.username]
    trueOrFalseMod = checkvalidmod(update.message.text.upper(), update)
    if trueOrFalseMod is False:
        return MODS5
    newAccount.mods[tempFaculty].append(update.message.text.upper())
    update.message.reply_text(
        'Please indicate the faculty of your sixth mod',
        reply_markup=ReplyKeyboardMarkup(replyKeyboardModFaculties, one_time_keyboard=True))
    return MODS6_F


def mods6_f(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    tempFaculty = update.message.text
    selectionDict[update.effective_chat.username] = tempFaculty
    trueOrFalse = checkvalidfaculty(tempFaculty.upper(), update)
    if trueOrFalse is False:
        return MODS6_F
    if tempFaculty not in newAccount.mods:
        newAccount.mods[tempFaculty] = []
    update.message.reply_text(
        'Please indicate the name of your sixth mod e.g. CS1010S or /done when you have enumerated all your courses '
        'or /back to restart',
        reply_markup=ReplyKeyboardRemove())
    return MODS6


def mods6(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    user = update.message.from_user
    tempFaculty = selectionDict[update.effective_chat.username]
    trueOrFalseMod = checkvalidmod(update.message.text.upper(), update)
    if trueOrFalseMod is False:
        return MODS6
    newAccount.mods[tempFaculty].append(update.message.text.upper())
    update.message.reply_text(
        'Please indicate the faculty of your seventh mod',
        reply_markup=ReplyKeyboardMarkup(replyKeyboardModFaculties, one_time_keyboard=True))
    return MODS7_F


def mods7_f(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    tempFaculty = update.message.text
    selectionDict[update.effective_chat.username] = tempFaculty
    trueOrFalse = checkvalidfaculty(tempFaculty.upper(), update)
    if trueOrFalse is False:
        return MODS7_F
    if tempFaculty not in newAccount.mods:
        newAccount.mods[tempFaculty] = []
    update.message.reply_text(
        'Please indicate the name of your seventh mod e.g. CS1010S or /done when you have enumerated all your courses '
        'or /back to restart',
        reply_markup=ReplyKeyboardRemove())
    return MODS7


def mods7(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    user = update.message.from_user
    tempFaculty = selectionDict[update.effective_chat.username]
    trueOrFalseMod = checkvalidmod(update.message.text.upper(), update)
    if trueOrFalseMod is False:
        return MODS7
    newAccount.mods[tempFaculty].append(update.message.text.upper())
    update.message.reply_text(
        'Please indicate the faculty of your eighth mod',
        reply_markup=ReplyKeyboardMarkup(replyKeyboardModFaculties, one_time_keyboard=True))
    return MODS8_F


def mods8_f(update: Update, _: CallbackContext) -> int:
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    tempFaculty = update.message.text
    selectionDict[update.effective_chat.username] = tempFaculty
    trueOrFalse = checkvalidfaculty(tempFaculty.upper(), update)
    if trueOrFalse is False:
        return MODS8_F
    if tempFaculty not in newAccount.mods:
        newAccount.mods[tempFaculty] = []
    update.message.reply_text(
        'Please indicate the name of your last mod e.g. CS1010S or /done when you have enumerated all your courses '
        'or /back to restart',
        reply_markup=ReplyKeyboardRemove())
    return MODS8


def mods8(update: Update, _: CallbackContext):
    input_id_into_newAccountDict(update.effective_chat.username)
    newAccount = newAccountDict[update.effective_chat.username]
    user = update.message.from_user
    tempFaculty = selectionDict[update.effective_chat.username]
    trueOrFalseMod = checkvalidmod(update.message.text.upper(), update)
    if trueOrFalseMod is False:
        return MODS8
    newAccount.mods[tempFaculty].append(update.message.text.upper())
    update.message.reply_text(
        'This is the last mod you can input, please type /done',
        reply_markup=ReplyKeyboardRemove())


def done(update: Update, _: CallbackContext) -> int:
    input_id_into_selection_dict(update.effective_chat.username)
    user = update.message.from_user
    update.message.reply_text(
        'Your data is being stored in the system, this may take a while')
    initialise_account(update)
    update.message.reply_text(
        'Your data has been stored into the system, please type /mods and follow instructions to find people who are '
        'taking the same '
        'mods as you do', reply_markup=ReplyKeyboardMarkup(replyKeyboardStandard, one_time_keyboard=False))
    logger.info("%s has initialised their account", user.username)

    return ConversationHandler.END


def cancel(update: Update, _: CallbackContext) -> int:
    input_id_into_selection_dict(update.effective_chat.username)
    user = update.message.from_user
    if update.effective_chat.username in newAccountDict:
        del newAccountDict[update.effective_chat.username]
    logger.info("User %s canceled the conversation.", user.username)
    update.message.reply_text(
        'Cancelled, you may run another command \n /register to register \n /mods to check mods \n /groupchatcreated '
        'to insert groupchat link', reply_markup=ReplyKeyboardMarkup(replyKeyboardStandard, one_time_keyboard=False)
    )
    print(newAccountDict)
    return ConversationHandler.END


def back(update: Update, _: CallbackContext):
    input_id_into_selection_dict(update.effective_chat.username)
    user = update.message.from_user
    if update.effective_chat.username in newAccountDict:
        newAccountDict[update.effective_chat.username].mods = {}
    update.message.reply_text(
        "Please restart module registration from the first module. If you are prone to errors, just register for one mod first and subsequently add modules individually."
    )
    update.effective_message.reply_text(
        'Please indicate the faculty of your first MOD, e.g. "FASS" for PL1101E, "Science" for MA1101R, "GE Mods" for '
        'GER1000, "Biz" for ACC1002 etc. Please check and input the correct faculty and /back whenever you make a '
        'mistake.',
        reply_markup=ReplyKeyboardMarkup(replyKeyboardModFaculties, one_time_keyboard=True))
    return MODS1_F


def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Selected option: {query.data}")


GETFACULTIES, GETMODS, LINK = range(3)

tempDict = {}


def mods(update: Update, _: CallbackContext) -> None:
    input_id_into_selection_dict(update.effective_chat.username)
    input_id_into_dict_dict(update.effective_chat.username)
    isRegisteredAccount = checkregisteredaccount(update.effective_message.chat_id, update)
    if isRegisteredAccount is False:
        return
    user = update.message.from_user
    logger.info("User %s has run /mods", user.username)
    conn = pg2.connect(host=host, database=database,
                       user=user_database,
                       password=password)
    cur = conn.cursor()
    getFaculty = '''
    SELECT faculty_name, mod_name FROM all_modules
    INNER JOIN faculties
    ON all_modules.faculty_id = faculties.faculty_id
    '''
    cur.execute(getFaculty)
    data = cur.fetchall()
    faculty = []
    tempDict = dictDict[update.effective_chat.username]
    tempDict.clear()
    for key, value in data:
        if key.title() not in faculty:
            faculty.append(key.title())
        if key.title() not in tempDict:
            tempDict[key.title()] = []
        tempDict[key.title()].append(value)
    faculty.sort()
    keyboard = []
    for i in faculty:
        keyboard.append([InlineKeyboardButton(i, callback_data=str(i))])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose the faculty:', reply_markup=reply_markup)
    return GETFACULTIES


def getfaculties(update: Update, _: CallbackContext) -> int:
    input_id_into_selection_dict(update.effective_chat.username)
    input_id_into_dict_dict(update.effective_chat.username)
    query = update.callback_query
    query.edit_message_text(text=f"Selected option: {query.data}")
    tempDict = dictDict[update.effective_chat.username]
    tempFacultyChosen = query.data
    mods = tempDict[tempFacultyChosen]
    mods.sort()
    keyboard = []
    for i in mods:
        keyboard.append([InlineKeyboardButton(i, callback_data=i)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_message.reply_text('Please choose the module:', reply_markup=reply_markup)
    return GETMODS


def getmods(update: Update, _: CallbackContext):
    input_id_into_selection_dict(update.effective_chat.username)
    update.effective_message.reply_text('Fetching data from database, may take a while...')
    modChosen = str(update.callback_query.data)
    query = update.callback_query
    query.edit_message_text(text=f"Selected option: {query.data}")
    conn = pg2.connect(host=host, database=database,
                       user=user_database,
                       password=password)

    cur = conn.cursor()
    getNameList = '''
            SELECT username FROM mods
            INNER JOIN accounts
            ON mods.account_id = accounts.id
            AND
            mod_id = (SELECT mod_id FROM all_modules
            WHERE mod_name = %s)
    '''
    cur.execute(getNameList, (modChosen,))
    data = cur.fetchall()
    getLink = '''
            SELECT link FROM all_modules
            WHERE mod_name = %s
    '''
    cur.execute(getLink, (modChosen,))
    tempLink = cur.fetchone()
    modLink = ''
    for link in tempLink:
        modLink = link
    if modLink is not None:
        namelist = 'Usernames of Eusoffians taking' + ' ' + modChosen + '\n' + modLink + '\n'
    else:
        namelist = 'Usernames of Eusoffians taking' + ' ' + modChosen + '\n' + 'No groupchat created yet \n/groupchatcreated to add groupchat ' \
                                                                               'link' + '\n'
    for i in data:
        namelist += ('@' + i[0] + '\n')
    update.effective_message.reply_text(namelist)
    return ConversationHandler.END


def groupchatcreated(update: Update, _: CallbackContext):
    input_id_into_selection_dict(update.effective_chat.username)
    user = update.effective_message.from_user
    logger.info("User %s has run /groupchatcreated", user.username)
    modChosen = str(update.callback_query.data)
    tempModChosen = modChosen
    selectionDict[update.effective_chat.username] = tempModChosen
    query = update.callback_query
    query.edit_message_text(text=f"Selected option: {query.data}")
    update.effective_message.reply_text('Please copy and paste the group link here.')
    return LINK


def link(update: Update, _: CallbackContext):
    input_id_into_selection_dict(update.effective_chat.username)
    tempModChosen = selectionDict[update.effective_chat.username]
    linkSubmitted = update.message.text
    trueOrFalse = checkvalidlink(linkSubmitted, update)
    if trueOrFalse is False:
        return LINK
    user = update.effective_message.from_user
    logger.info("User %s has added the link of %s", user.username, linkSubmitted)
    accountUsername = update.effective_chat.username
    conn = pg2.connect(host=host, database=database,
                       user=user_database,
                       password=password)
    cur = conn.cursor()
    createLink = '''
                UPDATE all_modules
                SET link = %s
                ,link_sender = %s
                WHERE mod_name = %s
    '''
    cur.execute(createLink, (linkSubmitted, str(accountUsername), tempModChosen))
    conn.commit()
    conn.close()
    update.effective_message.reply_text('Link has been added, /mods to check')
    return ConversationHandler.END


def delete_account(update: Update, _: CallbackContext):
    input_id_into_selection_dict(update.effective_chat.username)
    isRegisteredAccount = checkregisteredaccount(update.effective_message.chat_id, update)
    if isRegisteredAccount is False:
        return
    user = update.message.from_user
    logger.info("User %s has deleted account", user.username)
    username = update.effective_chat.username
    conn = pg2.connect(host=host, database=database,
                       user=user_database,
                       password=password)
    cur = conn.cursor()
    query = '''
            DELETE FROM mods
            WHERE mods.account_id = (SELECT id 
            FROM accounts
            WHERE accounts.username = %s)
    '''
    cur.execute(query, (username,))
    conn.commit()
    conn.close()
    update.effective_message.reply_text('Account has been deleted, please complete registration again if you wish to '
                                        'continue using the bot. \n/register')


CHOOSEMODULE = range(1)


def deletemod(update: Update, _: CallbackContext):
    input_id_into_selection_dict(update.effective_chat.username)
    input_id_into_dict_dict(update.effective_chat.username)
    isRegisteredAccount = checkregisteredaccount(update.effective_message.chat_id, update)
    if isRegisteredAccount is False:
        return
    user = update.message.from_user
    logger.info("User %s has run /deletemod", user.username)
    username = update.effective_chat.username
    conn = pg2.connect(host=host, database=database,
                       user=user_database,
                       password=password)
    cur = conn.cursor()
    query = '''
            SELECT mod_name, mods.mod_id, accounts.id FROM mods
            INNER JOIN accounts ON mods.account_id = accounts.id
            INNER JOIN all_modules ON all_modules.mod_id = mods.mod_id
            WHERE username = %s

    '''
    cur.execute(query, (username,))
    modules = cur.fetchall()
    moduleDict = dictDict[update.effective_chat.username]
    moduleDict.clear()
    for i, j, k in modules:
        moduleDict[i] = j
        accountId = k
        selectionDict[update.effective_chat.username] = accountId
    keyboard = []
    for i in moduleDict:
        keyboard.append([InlineKeyboardButton(i, callback_data=i)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_message.reply_text('Please choose the module you wish to delete', reply_markup=reply_markup)
    return CHOOSEMODULE


def choosemodule(update, context):
    input_id_into_selection_dict(update.effective_chat.username)
    input_id_into_dict_dict(update.effective_chat.username)
    modChosen = str(update.callback_query.data)
    query = update.callback_query
    query.edit_message_text(text=f"Selected option: {query.data}")
    moduleDict = dictDict[update.effective_chat.username]
    accountId = selectionDict[update.effective_chat.username]
    modId = moduleDict[modChosen]
    conn = pg2.connect(host=host, database=database,
                       user=user_database,
                       password=password)
    cur = conn.cursor()
    query = '''
            DELETE FROM mods
            WHERE mods.mod_id = %s 
            AND account_id = %s
            '''
    cur.execute(query, (modId, accountId))
    conn.commit()
    conn.close()
    moduleDict.clear()
    update.effective_message.reply_text('Module has been deleted from your account')
    return ConversationHandler.END


STATEFACULTIES, STATEMODULE = range(2)


def add_module(update, context):
    isRegisteredAccount = checkregisteredaccount(update.effective_message.chat_id, update)
    if isRegisteredAccount is False:
        return
    input_id_into_selection_dict(update.effective_chat.username)
    user = update.message.from_user
    logger.info("User %s has run /addmod", user.username)
    update.message.reply_text(
        'Please indicate the faculty of your MOD, e.g. "FASS" for PL1101E, "Science" for MA1101R, "GE Mods" for '
        'GER1000, "Biz" for ACC1002 etc. Please check and input the correct faculty and /cancel whenever you make a '
        'mistake.',
        reply_markup=ReplyKeyboardMarkup(replyKeyboardModFaculties, one_time_keyboard=True))
    return STATEFACULTIES


def statefaculties(update: Update, _: CallbackContext):
    input_id_into_selection_dict(update.effective_chat.username)
    tempFaculty = update.message.text.upper()
    selectionDict[update.effective_chat.username] = tempFaculty
    trueOrFalse = checkvalidfaculty(tempFaculty.upper(), update)
    if trueOrFalse is False:
        return STATEFACULTIES
    update.message.reply_text(
        'Please indicate the name of your mod e.g. CS1010S',
        reply_markup=ReplyKeyboardRemove())
    return STATEMODULE


def statemodule(update: Update, _: CallbackContext):
    input_id_into_selection_dict(update.effective_chat.username)
    module = update.message.text.upper()
    user = update.effective_chat.username
    trueOrFalseMod = checkvalidmod(update.message.text.upper(), update)
    if trueOrFalseMod is False:
        return STATEMODULE
    tempFaculty = selectionDict[update.effective_chat.username]
    conn = pg2.connect(host=host, database=database,
                       user=user_database,
                       password=password)
    cur = conn.cursor()
    insertToAllModules = '''
                INSERT INTO all_modules(mod_name,faculty_id)
                VALUES(%s,(SELECT faculty_id FROM faculties
                WHERE faculty_name = %s))
                ON CONFLICT (mod_name) DO NOTHING
                 '''
    cur.execute(insertToAllModules, (module, tempFaculty.lower()))
    query = '''
            INSERT INTO mods(account_id,mod_id,faculty_id)
            VALUES((SELECT id FROM accounts
                    WHERE username = %s),
                    (SELECT mod_id FROM all_modules
                    WHERE mod_name = %s), 
                    (SELECT faculty_id FROM all_modules
                    WHERE mod_name = %s))
    '''
    cur.execute(query, (user, module, module))
    update.message.reply_text(
        'Your data is being stored in the system, this may take a while')
    conn.commit()

    get_chat_id = '''
                SELECT chat_id FROM accounts
                INNER JOIN mods 
                ON accounts.id = mods.account_id
                WHERE mods.mod_id = (SELECT mod_id FROM all_modules
                                    WHERE mod_name = %s)
                 '''
    cur.execute(get_chat_id, (module,))
    data = cur.fetchall()
    for chat_id in data:
        if chat_id[0] == update.effective_message.chat_id:
            continue
        else:
            chat_id = chat_id[0]
            try:
                bot.send_message(chat_id=chat_id,
                                 text="Someone is now taking " + module + "! Run /mods to check")
            except:
                continue

    update.message.reply_text(
        'Your data has been stored into the system, please type /addmod to add another module',
        reply_markup=ReplyKeyboardMarkup(replyKeyboardStandard, one_time_keyboard=False))
    return ConversationHandler.END


def help(update, context):
    user = update.message.from_user
    replyKeyboardStandard = [['/mods', '/cancel', '/help', '/mymods'],
                             ['/groupchatcreated', '/deletemod', '/addmod']]
    logger.info("User %s has run /help", user.username)
    update.message.reply_text("/start - Register with your room, faculty, mods "
                              "etc \n/done - Run after you are done entering all "
                              "your mods \n/cancel - Cancel to type another "
                              "command \n/mods - Obtain list of people studying "
                              "the particular mod \n/mymods- View your mods \n/groupchatcreated - Run if "
                              "you have created a group chat for a mod "
                              "\n/addmod - Add additional mod \n/deletemod - Delete mods that are wrongly added "
                              "\n/deleteaccount - Deletes your account \nPM "
                              "@chernanigans for any help",
                              reply_markup=ReplyKeyboardMarkup(replyKeyboardStandard, one_time_keyboard=False))


def mymods(update: Update, _: CallbackContext):
    user = update.message.from_user
    logger.info("User %s has run /mymods to check mods", user.username)
    isRegisteredAccount = checkregisteredaccount(update.effective_message.chat_id, update)
    if isRegisteredAccount is False:
        return
    input_id_into_selection_dict(update.effective_chat.username)
    user = update.effective_chat.username
    conn = pg2.connect(host=host, database=database,
                       user=user_database,
                       password=password)
    cur = conn.cursor()
    getMyMods = '''
                select mod_name from mods 
                inner join all_modules
                on mods.mod_id = all_modules.mod_id
                WHERE mods.account_id = (SELECT id 
                FROM accounts
                WHERE accounts.username = %s)
                 '''
    cur.execute(getMyMods, (user,))
    data = cur.fetchall()
    mods = "The mods that you are taking this semester are \n"
    for i in sorted(data):
        mods += i[0] + '\n'

    update.message.reply_text(
        mods,
        reply_markup=ReplyKeyboardMarkup(replyKeyboardStandard, one_time_keyboard=False))
    return ConversationHandler.END


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command. Please "
                                                                    "type /cancel to restart this.")


def checkvalidfaculty(faculty, update):
    validInput = ['BIZ', 'COMPUTING', 'GE MODS', 'ENGINEERING', 'FASS', 'SCIENCE', 'LAW', 'PUBLIC POLICY',
                  'ISE', 'MUSIC', 'PUBLIC HEALTH', 'SDE', 'CHS(AY21/22 ONWARDS)']
    if faculty not in validInput:
        bot.send_message(chat_id=update.effective_chat.id,
                         text="It appears that you have inputted an invalid faculty, please only select faculty from "
                              "the on-screen keyboard below.")
        return False
    return True


def checkvalidmod(mod, update):
    m = re.match(r"(\D{2,3}\d{2,4}\D{0,2})", mod)
    try:
        start, stop = m.span()
        if stop - start == len(mod):
            return True
        else:
            bot.send_message(chat_id=update.effective_chat.id,
                             text="It appears that you have inputted an invalid mod, please only enter a valid mod "
                                  "code.")
            return False
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                         text="It appears that you have inputted an invalid mod, please only enter a valid mod "
                              "code.")
        return False


def checkvalidroomnumber(roomNumber, update):
    m = re.match(r"([ABCDE][1234][012][0-9])", roomNumber)
    try:
        start, stop = m.span()
        if stop - start == len(roomNumber):
            return True
        else:
            bot.send_message(chat_id=update.effective_chat.id,
                             text="It appears that you have inputted an invalid room number, please only enter a valid "
                                  "room number "
                                  ".")
            return False
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                         text="It appears that you have inputted an invalid room number, please only enter a valid "
                              "room number "
                              ".")
        return False


def checkvalidlink(link, update):
    m = re.match(r"(https://t.me/joinchat/.*)", link)
    try:
        start, stop = m.span()
        if stop - start == len(link):
            return True
        else:
            bot.send_message(chat_id=update.effective_chat.id,
                             text="It appears that you have inputted an invalid link, please only enter a valid telegram group chat"
                                  "link "
                                  ".")
            return False
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                         text="It appears that you have inputted an invalid link, please only enter a valid telegram group chat"
                              "link "
                              ".")
        return False


registeredAccountSet = set()


def checkregisteredaccount(chat_id, update):
    if chat_id in registeredAccountSet:
        return True

    else:
        conn = pg2.connect(host=host, database=database,
                           user=user_database,
                           password=password)
        cur = conn.cursor()
        getChatId = '''
            SELECT chat_id FROM accounts
            '''
        cur.execute(getChatId)
        data = cur.fetchall()
        for id in data:
            id = id[0]
            if id not in registeredAccountSet:
                registeredAccountSet.add(id)

    if chat_id in registeredAccountSet:
        return True

    else:
        bot.send_message(chat_id=update.effective_chat.id,
                         text="Please register before using with /register")
        return False


def main():
    # account creator
    accountInitialisation = ConversationHandler(
        entry_points=[CommandHandler('register', register)],
        states={
            ROOMNUMBER: [MessageHandler(Filters.text & ~Filters.command, roomnumber)],
            FACULTY: [MessageHandler(Filters.text & ~Filters.command, faculty)],
            COURSE: [MessageHandler(Filters.text & ~Filters.command, course)],
            YEAR: [CallbackQueryHandler(year)],
            MODS1_F: [MessageHandler(Filters.text & ~Filters.command, mods1_f),
                      CommandHandler('done', done)],
            MODS1: [MessageHandler(Filters.text & ~Filters.command, mods1), CommandHandler('done', done)],
            MODS2_F: [MessageHandler(Filters.text & ~Filters.command, mods2_f),
                      CommandHandler('done', done)],
            MODS2: [MessageHandler(Filters.text & ~Filters.command, mods2), CommandHandler('done', done)],
            MODS3_F: [MessageHandler(Filters.text & ~Filters.command, mods3_f),
                      CommandHandler('done', done)],
            MODS3: [MessageHandler(Filters.text & ~Filters.command, mods3), CommandHandler('done', done)],
            MODS4_F: [MessageHandler(Filters.text & ~Filters.command, mods4_f),
                      CommandHandler('done', done)],
            MODS4: [MessageHandler(Filters.text & ~Filters.command, mods4), CommandHandler('done', done)],
            MODS5_F: [MessageHandler(Filters.text & ~Filters.command, mods5_f),
                      CommandHandler('done', done)],
            MODS5: [MessageHandler(Filters.text & ~Filters.command, mods5), CommandHandler('done', done)],
            MODS6_F: [MessageHandler(Filters.text & ~Filters.command, mods6_f),
                      CommandHandler('done', done)],
            MODS6: [MessageHandler(Filters.text & ~Filters.command, mods6), CommandHandler('done', done)],
            MODS7_F: [MessageHandler(Filters.text & ~Filters.command, mods7_f),
                      CommandHandler('done', done)],
            MODS7: [MessageHandler(Filters.text & ~Filters.command, mods7), CommandHandler('done', done)],
            MODS8_F: [MessageHandler(Filters.text & ~Filters.command, mods8_f),
                      CommandHandler('done', done)
                      ],
            MODS8: [MessageHandler(Filters.text & ~Filters.command, mods8), CommandHandler('done', done)],
        },
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('back', back)])
    dispatcher.add_handler(accountInitialisation)

    # getting the mods from database
    moduleRecall = ConversationHandler(
        entry_points=[CommandHandler('mods', mods)],
        states={
            GETFACULTIES: [CallbackQueryHandler(getfaculties)],
            GETMODS: [CallbackQueryHandler(getmods)],
        },
        fallbacks=[CommandHandler('cancel', cancel)], )
    dispatcher.add_handler(moduleRecall)

    # inserting link for group chat into database
    createGroup = ConversationHandler(
        entry_points=[CommandHandler('groupchatcreated', mods)],
        states={
            GETFACULTIES: [CallbackQueryHandler(getfaculties)],
            GETMODS: [CallbackQueryHandler(groupchatcreated)],
            LINK: [MessageHandler(Filters.text & ~Filters.command, link)]
        },
        fallbacks=[CommandHandler('cancel', cancel)], )
    dispatcher.add_handler(createGroup)

    # delete_mod
    deleteMod = ConversationHandler(
        entry_points=[CommandHandler('deletemod', deletemod)],
        states={
            CHOOSEMODULE: [CallbackQueryHandler(choosemodule)]
        },
        fallbacks=[CommandHandler('cancel', cancel)], )
    dispatcher.add_handler(deleteMod)

    # add mod
    addMod = ConversationHandler(
        entry_points=[CommandHandler('addmod', add_module)],
        states={
            STATEFACULTIES: [MessageHandler(Filters.text & ~Filters.command, statefaculties)],
            STATEMODULE: [MessageHandler(Filters.text & ~Filters.command, statemodule)]
        },
        fallbacks=[CommandHandler('cancel', cancel)], )
    dispatcher.add_handler(addMod)

    startHandler = CommandHandler('start', start)
    dispatcher.add_handler(startHandler)

    helpHandler = CommandHandler('help', help)
    dispatcher.add_handler(helpHandler)

    deleteHandler = CommandHandler('deleteaccount', delete_account)
    dispatcher.add_handler(deleteHandler)

    cancelHandler = CommandHandler('cancel', cancel)
    dispatcher.add_handler(cancelHandler)

    myModsHandler = CommandHandler('mymods', mymods)
    dispatcher.add_handler(myModsHandler)

    unknownHandler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknownHandler)

    updater.start_polling()


if __name__ == '__main__':
    main()
