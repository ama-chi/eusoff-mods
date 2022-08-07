import psycopg2 as pg2
import os

DB_URL = os.environ.get('DATABASE_URL')
conn = pg2.connect("DB_URL")
cur = conn.cursor()

account_create = '''
        CREATE TABLE accounts (
            id SERIAL PRIMARY KEY
            ,username varchar(50) UNIQUE
            ,name varchar(50) NOT NULL
            ,roomnumber varchar(10) NOT NULL
            ,faculty varchar(50) NOT NULL
            ,course varchar(50) NOT NULL
            ,year varchar(50)
            ,chat_id int UNIQUE
        );
        '''

create_faculty = '''
        CREATE TABLE faculties (
            faculty_id SERIAL PRIMARY KEY
            ,faculty_name varchar(50) NOT NULL
        );
        '''

create_all_modules = '''
        CREATE TABLE all_modules (
            mod_id SERIAL PRIMARY KEY
            ,mod_name varchar(50) UNIQUE
            ,faculty_id integer references faculties(faculty_id) NOT NULL
            ,link varchar(512)
            ,Link_sender varchar(50)
        );
        '''
create_mods = '''
        CREATE TABLE mods (
            account_id integer references accounts(id)
            ,mod_id integer references all_modules(mod_id)
            ,faculty_id integer references faculties(faculty_id)
        );
        '''

insert_faculties = '''
        INSERT INTO faculties(faculty_name)
        VALUES
        ('biz'),
        ('computing'),
        ('chs mods'),
        ('engineering'),
        ('fass'),
        ('ge mods'),
        ('law'),
        ('music'),
        ('public health'),
        ('public policy'),
        ('science'),
        ('sde'),
        ('others');
        '''

actions = [account_create, create_faculty, create_all_modules, create_mods, insert_faculties]
for action in actions:
  cur.execute(action)

conn.commit()


# query1 = '''
#         CREATE TABLE modules (
#             account_id integer references accounts(id)
#             ,faculty_id integer references faculty(faculty_id)
#             ,faculty_id integer references faculties(faculty_id)
#         );
#         '''

# query1 = '''
#         SELECT faculty_id FROM faculties
#         WHERE faculty_name = 'science'
#         '''
# query1 = '''
#         SELECT faculty_name, mod_name FROM all_modules
#         INNER JOIN faculties
#         ON all_modules.faculty_id = faculties.faculty_id
#         '''


# temp_dict = {}
# for key,value in data:
#     if key.upper() not in temp_list:
#         temp_list.append(key.upper())
# print(temp_list)

# faculty = []
# for key, value in data:
#     if key.upper() not in faculty:
#         faculty.append(key.upper())
#     if key not in temp_dict:
#         temp_dict[key.upper()] = []
#     temp_dict[key.upper()] = [value]

# # print(data)
# print(temp_dict)
# print(faculty)


# conn.commit()

# MONGODB = 'mongodb+srv://yeechern123:t3y9adg2@cluster0.h45sj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
# cluster = MongoClient(MONGODB)
# db = cluster['Eusoff-Mods']
# collection = db['accounts']
# modules_collection = db['faculties']

# def initialise_account(user):
#     with open('data.json', 'r+') as f:
#         data = json.load(f)
#         username = str(user)
#         if username not in data['accounts']:
#             data['accounts'][username] = {}
#         data['accounts'][username]['roomnumber'] = newaccount.roomnumber
#         data['accounts'][username]['faculty'] = newaccount.faculty
#         data['accounts'][username]['course'] = newaccount.course
#         data['accounts'][username]['mods'] = newaccount.mods
#         f.seek(0)
#         json.dump(data, f, indent=4)
#
#
# def initialise_modules(user):
#     username = str(user)
#     with open('data.json', 'r+') as f:
#         data = json.load(f)
#         for fac in newaccount.mods:
#             for mod in newaccount.mods[fac]:
#                 if mod not in data['Faculties'][fac]:
#                     data['Faculties'][fac][mod] = []
#                 data['Faculties'][fac][mod].append('@' + username)
#         f.seek(0)
#         json.dump(data, f, indent=4)




""" 
account_create = '''
        CREATE TABLE accounts (
            id SERIAL PRIMARY KEY
            ,username varchar(50) UNIQUE
            , name varchar(50) NOT NULL
            , roomnumber varchar(10) NOT NULL
            ,faculty varchar(50) NOT NULL
            ,course varchar(50) NOT NULL
        );
        '''

create_faculty = '''
        CREATE TABLE faculties (
            id SERIAL PRIMARY KEY
            ,faculty_name varchar(50) NOT NULL
        );
        '''

create_modules = '''
        CREATE TABLE all_modules (
            mod_id SERIAL PRIMARY KEY
            ,mod_name varchar(50) NOT NULL
            ,faculty_id integer references faculties(faculty_id) UNIQUE (mod_name)
            ,link varchar(512)
        );
        '''

insert_faculties = '''
        INSERT INTO faculties(faculty_name)
        VALUES ('science')
        );
        ''' """