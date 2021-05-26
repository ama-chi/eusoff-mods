from telegram import *
from telegram.ext import *
import logging
import psycopg2 as pg2

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

''''''''


class Account:
    def __init__(
            self,
            username=None,
            name=None,
            roomnumber=None,
            faculty=None,
            course=None,
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

ROOMNUMBER, FACULTY, COURSE, MODS1_F, MODS1, MODS2_F, MODS2, MODS3_F, MODS3, MODS4_F, MODS4, MODS5_F, MODS5, MODS6_F, MODS6, MODS7_F, MODS7, MODS8_F, MODS8 = range(
    19)


def initialise_account():
    conn = pg2.connect(host=host, database=database,
                       user=user_database,
                       password=password)
    cur = conn.cursor()
    insert_account = '''
           INSERT INTO accounts(username,name,roomnumber,faculty,course)
            VALUES (%s,%s,%s,%s,%s)
            ON CONFLICT (username) DO NOTHING
            '''
    cur.execute(insert_account,
                (newaccount.username, newaccount.name, newaccount.roomnumber, newaccount.faculty, newaccount.course))
    for fac in newaccount.mods:
        for mod in newaccount.mods[fac]:
            insert_to_all_modules = '''
                        INSERT INTO all_modules(mod_name,faculty_id)
                        VALUES(%s,(SELECT faculty_id FROM faculties
                        WHERE faculty_name = %s))
                        ON CONFLICT (mod_name) DO NOTHING
                         '''
            cur.execute(insert_to_all_modules, (mod, fac.lower()))
    conn.commit()
    for fac in newaccount.mods:
        for mod in newaccount.mods[fac]:
            insert_to_mods = '''
                        INSERT INTO mods(account_id,mod_id,faculty_id)
                        VALUES((SELECT id FROM accounts
                        WHERE username = %s),(SELECT mod_id FROM all_modules
                        WHERE mod_name = %s), (SELECT faculty_id FROM all_modules
                        WHERE mod_name = %s))
                         '''
            cur.execute(insert_to_mods, (newaccount.username, mod, mod))
    conn.commit()
    conn.close()


def start(update: Update, _: CallbackContext):
    user = update.message.from_user
    logger.info("User %s started the bot", user.username)
    reply_keyboard = [['/register']]
    update.message.reply_text(
        'Welcome to Eusoff Mods, this is a bot to identify a community of Eusoffians taking the same mods, especially GE '
        'mods, as well as the group chats created, firstly, please register with /register.', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def register(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s is registering", user.username)
    data = update.effective_chat
    username = data['username']
    name = data['first_name']
    global newaccount
    newaccount = Account()
    newaccount.username = username
    newaccount.name = name
    update.message.reply_text(
        'Please key in your ROOM NUMBER. \nIf you make a mistake anytime, '
        'restart by typing /cancel. \nYou can edit your mods via /deletemod or /addmod anytime after registration. '
        '\nIf you are a groupchat admin, type /groupchatcreated after registration.')
    return ROOMNUMBER


def roomnumber(update: Update, _: CallbackContext) -> int:
    reply_keyboard = [['Biz', 'Computing', 'SDE', 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ],
                      ['ISE', 'Music', 'Public Health']]
    user = update.message.from_user
    logger.info("Room Number of %s: %s", user.username, update.message.text.upper())
    newaccount.roomnumber = update.message.text.upper()
    update.message.reply_text(
        'Please indicate your faculty',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return FACULTY


def faculty(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Faculty of %s: %s", user.username, update.message.text)
    newaccount.faculty = update.message.text
    update.message.reply_text(
        'Please indicate your course',
        reply_markup=ReplyKeyboardRemove())
    return COURSE


def course(update: Update, _: CallbackContext) -> int:
    reply_keyboard = [['Biz', 'Computing', 'GE Mods', 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ],
                      ['ISE', 'Music', 'Public Health', 'SDE']]
    user = update.message.from_user
    logger.info("Course of %s: %s", user.username, update.message.text.upper())
    newaccount.course = update.message.text.upper()
    update.message.reply_text(
        'Please indicate the faculty of your first MOD, e.g. "FASS" for PL1101E, "Science" for MA1101R, "GE Mods" for '
        'GER1000, "Biz" for ACC1002 etc. Please check and input the correct faculty and /cancel whenever you make a '
        'mistake.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return MODS1_F


temp_faculty = ''


def mods1_f(update: Update, _: CallbackContext) -> int:
    global temp_faculty
    temp_faculty = update.message.text
    if temp_faculty not in newaccount.mods:
        newaccount.mods[temp_faculty] = []
    update.message.reply_text(
        'Please indicate the name of your first mod e.g. CS1010S or /done when you have enumerated all your courses '
        'or /cancel to restart',
        reply_markup=ReplyKeyboardRemove())
    return MODS1


def mods1(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Biz', 'Computing', 'GE Mods', 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ],
                      ['ISE', 'Music', 'Public Health', 'SDE']]
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
    reply_keyboard = [['Biz', 'Computing', 'GE Mods', 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ],
                      ['ISE', 'Music', 'Public Health', 'SDE']]
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
    reply_keyboard = [['Biz', 'Computing', 'GE Mods', 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ],
                      ['ISE', 'Music', 'Public Health', 'SDE']]
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
    reply_keyboard = [['Biz', 'Computing', 'GE Mods', 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ],
                      ['ISE', 'Music', 'Public Health', 'SDE']]
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
    reply_keyboard = [['Biz', 'Computing', 'GE Mods', 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ],
                      ['ISE', 'Music', 'Public Health', 'SDE']]
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
    reply_keyboard = [['Biz', 'Computing', 'GE Mods', 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ],
                      ['ISE', 'Music', 'Public Health', 'SDE']]
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
    reply_keyboard = [['Biz', 'Computing', 'GE Mods', 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ],
                      ['ISE', 'Music', 'Public Health', 'SDE']]
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
    reply_keyboard = [['Biz', 'Computing', 'GE Mods', 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ],
                      ['ISE', 'Music', 'Public Health', 'SDE']]
    newaccount.mods[temp_faculty].append(update.message.text.upper())
    print(newaccount.mods)
    update.message.reply_text(
        'Please indicate the faculty of your mods',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def done(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(
        'Your data is being stored in the system, this may take a while')
    initialise_account()
    reply_keyboard = [['/mods', '/cancel', '/help'],
                      ['/groupchatcreated', '/deletemod', '/addmod']]
    update.message.reply_text(
        'Your data has been stored into the system, please type /mods and follow instructions to find people who are '
        'taking the same '
        'mods as you do', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False))
    logger.info("%s has initialised their account", user.username)

    return ConversationHandler.END


def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.username)
    reply_keyboard = [['/mods', '/cancel', '/help'],
                      ['/groupchatcreated', '/deletemod', '/addmod']]
    update.message.reply_text(
        'Cancelled, you may run another command \n /register to register \n /mods to check mods \n /groupchatcreated '
        'to insert groupchat link', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    )
    return ConversationHandler.END


def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Selected option: {query.data}")


GETFACULTIES, GETMODS, LINK = range(3)

temp_dict = {}


def mods(update: Update, _: CallbackContext) -> None:
    user = update.message.from_user
    logger.info("User %s has run /mods", user.username)
    conn = pg2.connect(host=host, database=database,
                       user=user_database,
                       password=password)
    cur = conn.cursor()
    getfaculty = '''
    SELECT faculty_name, mod_name FROM all_modules
    INNER JOIN faculties
    ON all_modules.faculty_id = faculties.faculty_id
    '''
    cur.execute(getfaculty)
    data = cur.fetchall()
    faculty = []
    global temp_dict
    for key, value in data:
        if key.title() not in faculty:
            faculty.append(key.title())
        if key.title() not in temp_dict:
            temp_dict[key.title()] = []
        temp_dict[key.title()].append(value)
    faculty.sort()
    keyboard = []
    for i in faculty:
        keyboard.append([InlineKeyboardButton(i, callback_data=str(i))])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose the faculty:', reply_markup=reply_markup)
    return GETFACULTIES


temp_faculty_chosen = ''


def getfaculties(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.edit_message_text(text=f"Selected option: {query.data}")
    global temp_faculty_chosen
    global temp_dict
    temp_faculty_chosen = query.data
    mods = temp_dict[temp_faculty_chosen]
    temp_dict = {}
    mods.sort()
    keyboard = []
    for i in mods:
        keyboard.append([InlineKeyboardButton(i, callback_data=i)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_message.reply_text('Please choose the module:', reply_markup=reply_markup)
    return GETMODS


def getmods(update: Update, _: CallbackContext):
    update.effective_message.reply_text('Fetching data from database, may take a while...')
    mod_chosen = str(update.callback_query.data)
    query = update.callback_query
    query.edit_message_text(text=f"Selected option: {query.data}")
    names = []
    conn = pg2.connect(host=host, database=database,
                       user=user_database,
                       password=password)

    cur = conn.cursor()
    get_namelist = '''
            SELECT username FROM mods
            INNER JOIN accounts
            ON mods.account_id = accounts.id
            AND
            mod_id = (SELECT mod_id FROM all_modules
            WHERE mod_name = %s)
    '''
    cur.execute(get_namelist, (mod_chosen,))
    data = cur.fetchall()
    get_link = '''
            SELECT link FROM all_modules
            WHERE mod_name = %s
    '''
    cur.execute(get_link, (mod_chosen,))
    temp_link = cur.fetchone()
    mod_link = ''
    for link in temp_link:
        mod_link = link
    if mod_link is not None:
        namelist = 'Usernames of Eusoffians taking' + ' ' + mod_chosen + '\n' + mod_link + '\n'
    else:
        namelist = 'Usernames of Eusoffians taking' + ' ' + mod_chosen + '\n' + 'No groupchat created yet \n/groupchatcreated to add groupchat ' \
                                                                                'link' + '\n '
    for i in data:
        namelist += ('@' + i[0] + '\n')
    update.effective_message.reply_text(namelist)
    return ConversationHandler.END


temp_mod_chosen = ''


def groupchatcreated(update: Update, _: CallbackContext):
    user = update.effective_message.from_user
    logger.info("User %s has run /groupchatcreated", user.username)
    mod_chosen = str(update.callback_query.data)
    global temp_mod_chosen
    temp_mod_chosen = mod_chosen
    query = update.callback_query
    query.edit_message_text(text=f"Selected option: {query.data}")
    update.effective_message.reply_text('Please copy and paste the group link here.')
    return LINK


def link(update: Update, _: CallbackContext):
    link_submitted = update.message.text
    account_username = update.message.from_user.username
    conn = pg2.connect(host=host, database=database,
                       user=user_database,
                       password=password)
    cur = conn.cursor()
    createlink = '''
                UPDATE all_modules
                SET link = %s
                ,link_sender = %s
                WHERE mod_name = %s
    '''
    cur.execute(createlink, (link_submitted, str(account_username), temp_mod_chosen))
    conn.commit()
    conn.close()
    update.effective_message.reply_text('Link has been added, /mods to check')
    return ConversationHandler.END


def delete_account(update: Update, _: CallbackContext):
    user = update.message.from_user
    logger.info("User %s has deleted account", user.username)
    username = update.message.from_user.username
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
module_dict = {}
account_id = 0


def deletemod(update: Update, _: CallbackContext):
    user = update.message.from_user
    logger.info("User %s has run /deletemod", user.username)
    username = update.message.from_user.username
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
    module_dict.clear()
    for i, j, k in modules:
        module_dict[i] = j
        global account_id
        account_id = k
    keyboard = []
    for i in module_dict:
        keyboard.append([InlineKeyboardButton(i, callback_data=i)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_message.reply_text('Please choose the module you wish to delete', reply_markup=reply_markup)
    return CHOOSEMODULE


def choosemodule(update, context):
    mod_chosen = str(update.callback_query.data)
    global module_dict
    global account_id
    mod_id = module_dict[mod_chosen]
    conn = pg2.connect(host=host, database=database,
                       user=user_database,
                       password=password)
    cur = conn.cursor()
    query = '''
            DELETE FROM mods
            WHERE mods.mod_id = %s 
            AND account_id = %s
            '''
    cur.execute(query, (mod_id, account_id))
    conn.commit()
    conn.close()
    module_dict.clear()
    account_id = 0
    update.effective_message.reply_text('Module has been deleted from your account')
    return ConversationHandler.END


STATEFACULTIES, STATEMODULE = range(2)


def add_module(update, context):
    user = update.message.from_user
    logger.info("User %s has run /addmod", user.username)
    reply_keyboard = [['Biz', 'Computing', 'GE Mods', 'Engineering'], ['FASS', 'Science', 'Law', 'Public Policy', ],
                      ['ISE', 'Music', 'Public Health', 'SDE']]
    update.message.reply_text(
        'Please indicate the faculty of your MOD, e.g. "FASS" for PL1101E, "Science" for MA1101R, "GE Mods" for '
        'GER1000, "Biz" for ACC1002 etc. Please check and input the correct faculty and /cancel whenever you make a '
        'mistake.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return STATEFACULTIES


def statefaculties(update: Update, _: CallbackContext):
    global temp_faculty
    temp_faculty = update.message.text.upper()
    print(temp_faculty)
    update.message.reply_text(
        'Please indicate the name of your mod e.g. CS1010S',
        reply_markup=ReplyKeyboardRemove())
    return STATEMODULE


def statemodule(update: Update, _: CallbackContext):
    module = update.message.text.upper()
    user = update.message.from_user.username
    global temp_faculty
    conn = pg2.connect(host=host, database=database,
                       user=user_database,
                       password=password)
    cur = conn.cursor()
    insert_to_all_modules = '''
                INSERT INTO all_modules(mod_name,faculty_id)
                VALUES(%s,(SELECT faculty_id FROM faculties
                WHERE faculty_name = %s))
                ON CONFLICT (mod_name) DO NOTHING
                 '''
    cur.execute(insert_to_all_modules, (module, temp_faculty.lower()))
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
    reply_keyboard = [['/mods', '/cancel', '/help'],
                      ['/groupchatcreated', '/deletemod', '/addmod']]
    conn.commit()
    update.message.reply_text(
        'Your data has been stored into the system, please type /addmod to add another module',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False))
    return ConversationHandler.END


def help(update, context):
    user = update.message.from_user
    logger.info("User %s has run /help", user.username)
    reply_keyboard = [['/mods', '/cancel', '/help'],
                      ['/groupchatcreated', '/deletemod', '/addmod']]
    update.message.reply_text("/start - Register with your room, faculty, mods "
                              "etc \n/done - Run after you are done entering all "
                              "your mods \n/cancel - Cancel to type another "
                              "command \n/mods - Obtain list of people studying "
                              "the particular mod \n/groupchatcreated - Run if "
                              "you have created a group chat for a mod "
                              "\n/addmod - Add additional mod \n/deletemod - Delete mods that are wrongly added "
                              "\n/deleteaccount - Deletes your account \nPM "
                              "@chernanigans for any help", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False))


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command. Please "
                                                                    "type /cancel to restart this.")


def main():
    ## account creator
    account_initialisation = ConversationHandler(
        entry_points=[CommandHandler('register', register)],
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
            MODS2: [MessageHandler(Filters.text & ~Filters.command, mods2), CommandHandler('done', done)],
            MODS3_F: [MessageHandler(Filters.regex('^(Biz|Computing|Engineering|FASS|Science|Law|Medicine|SDE|Public '
                                                   'Policy|ISE|Music|Public Health|GE Mods)$'), mods3_f),
                      CommandHandler('done', done)],
            MODS3: [MessageHandler(Filters.text & ~Filters.command, mods3), CommandHandler('done', done)],
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
        fallbacks=[CommandHandler('cancel', cancel)], )
    dispatcher.add_handler(account_initialisation)

    # getting the mods from database
    module_recall = ConversationHandler(
        entry_points=[CommandHandler('mods', mods)],
        states={
            GETFACULTIES: [CallbackQueryHandler(getfaculties)],
            GETMODS: [CallbackQueryHandler(getmods)],
        },
        fallbacks=[CommandHandler('cancel', cancel)], )
    dispatcher.add_handler(module_recall)

    ## inserting link for group chat into database
    create_group = ConversationHandler(
        entry_points=[CommandHandler('groupchatcreated', mods)],
        states={
            GETFACULTIES: [CallbackQueryHandler(getfaculties)],
            GETMODS: [CallbackQueryHandler(groupchatcreated)],
            LINK: [MessageHandler(Filters.text & ~Filters.command, link)]
        },
        fallbacks=[CommandHandler('cancel', cancel)], )
    dispatcher.add_handler(create_group)

    ##delete_mod
    delete_mod = ConversationHandler(
        entry_points=[CommandHandler('deletemod', deletemod)],
        states={
            CHOOSEMODULE: [CallbackQueryHandler(choosemodule)]
        },
        fallbacks=[CommandHandler('cancel', cancel)], )
    dispatcher.add_handler(delete_mod)

    # add mod
    add_mod = ConversationHandler(
        entry_points=[CommandHandler('addmod', add_module)],
        states={
            STATEFACULTIES: [MessageHandler(Filters.text & ~Filters.command, statefaculties)],
            STATEMODULE: [MessageHandler(Filters.text & ~Filters.command, statemodule)]
        },
        fallbacks=[CommandHandler('cancel', cancel)], )
    dispatcher.add_handler(add_mod)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    delete_handler = CommandHandler('deleteaccount', delete_account)
    dispatcher.add_handler(delete_handler)

    cancel_handler = CommandHandler('cancel', cancel)
    dispatcher.add_handler(cancel_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
