import pymysql

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='db_sistem_ats')

cursor = connection.cursor()


sql = "INSERT INTO `tb_sentences`(`sentence_index`, `sentence`, `id_datachat`) VALUES (%s, %s, %s)"
cursor.execute(sql, (1, 'Sikit lgi ni. Bab 4 tinggal penjelasan. Bab 1 2 3 udh clear. Sma bab 5 yg 1 lembar tpi gatau isinya apa🤣', 1))

# connection is not autocommit by default. So we must commit to save our changes.
connection.commit()

# Execute query
sql = "SELECT * FROM `tb_sentences`"
cursor.execute(sql)
# Fetch all the records
result = cursor.fetchall()
for i in result:
    print(i)

connection.close()
