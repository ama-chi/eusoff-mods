host = 'ec2-34-195-143-54.compute-1.amazonaws.com'
database = 'd3pb9jkfc1jkat'
user_database = 'ckwbcsfhmslojp'
password = '314cc6f1c2ef1e61c470ce5ebf1b3c1eed63ad8be4376227350ecd1b4acd96fa'

conn = pg2.connect(host= host, database= database,
                   user= user_database,
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

for i in data:
    print(i)
