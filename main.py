import fextractor
import filehandler
import numpy as np
import pymysql
import pandas
from google_drive_downloader import GoogleDriveDownloader as gdd
import tfidf

# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='',
#                              db='db_sistem_ats')
# cursor = connection.cursor()

# name = filehandler.buat_nama()
id_chat = ''
filepath = "data/" + id_chat

gdd.download_file_from_google_drive(file_id=id_chat,
                                    dest_path=filepath,
                                    unzip=True)

df = filehandler.exctract_chat(filepath, id_chat, "123")
df = df[(df.date == '21/07/21')]

dokumen = ""
for content in df['sentence']:
  dokumen+= content + "."

best_term = tfidf.best_term(dokumen)
print(best_term)



title = "kelas"

weight = {
    "1": 0.787,
    "2": 0.498,
    "3": 1,
    "4": 1,
    "5": 0.566,
    "6": 0.979,
    "7": 3
}

scoref1 = fextractor.sentence_location(df)
scoref2 = fextractor.sentence_length(df)
# scoref3 = fextractor.positive_word(df)
# scoref4 = fextractor.negative_word(df)
scoref5 = fextractor.numerical_feature(df)
# # scoref6 = fextractor.entity_feature(df)
scoref7 = fextractor.similarity_to_title("kelas", df)
#

#
data1 = filehandler.ubah_data_ke_array(scoref1)

data1 = np.array(data1)
print(data1)
datamin1 = data1.min()
datamax1 = data1.max()

data2 = filehandler.ubah_data_ke_array(scoref2)

data2 = np.array(data2)
datamin2 = data2.min()
datamax2 = data2.max()

# data3 = filehandler.ubah_data_ke_array(scoref3)
#
# data3 = np.array(data3)
# datamin3 = data3.min()
# datamax3 = data3.max()
#
# data4 = filehandler.ubah_data_ke_array(scoref4)
#
# data4 = np.array(data4)
# datamin4 = data4.min()
# datamax4 = data4.max()

data5 = filehandler.ubah_data_ke_array(scoref5)

data5 = np.array(data5)
datamin5 = data5.min()
datamax5 = data5.max()

# data6 = filehandler.ubah_data_ke_array(scoref6)
#
# data6 = np.array(data2)
# datamin6 = data6.min()
# datamax6 = data6.max()

data7 = filehandler.ubah_data_ke_array(scoref7)

data7 = np.array(data7)
datamin7 = data7.min()
datamax7 = data7.max()
if datamax7 == 0:
    datamax7 = 1

print("\n data min 1: " + str(datamin1) + "\n data max : " + str(datamax1))
print("\n data min 2: " + str(datamin2) + "\n data max : " + str(datamax2))
# print("\n data min : " + str(datamin3) + "\n data max : " + str(datamax3))
# print("\n data min : " + str(datamin4) + "\n data max : " + str(datamax4))
print("\n data min 5: " + str(datamin5) + "\n data max : " + str(datamax5))
# print("\n data min : " + str(datamin6) + "\n data max : " + str(datamax6))
print("\n data min 7: " + str(datamin7) + "\n data max : " + str(datamax7))

score = {}
for index, content in zip(df['sentence_index'], df['sentence']):
    key = str(index)

    n_scoref1 = weight['1'] * ((scoref1[key] - datamin1) / (datamax1 - datamin1))
    n_scoref2 = weight['2'] * ((scoref2[key] - datamin2) / (datamax2 - datamin2))
    # n_scoref3 = weight['3'] * ((scoref3[key] - datamin3) / (datamax3 - datamin3))
    # n_scoref4 = weight['4'] * ((scoref4[key] - datamin4) / (datamax4 - datamin4))
    n_scoref5 = weight['5'] * ((scoref5[key] - datamin5) / (datamax5 - datamin5))
    # n_scoref6 = weight['6'] * ((scoref6[key] - datamin6) / (datamax6 - datamin6))
    n_scoref7 = weight['7'] * ((scoref7[key] - datamin7) / (datamax7 - datamin7))

    sscore = (n_scoref1 + n_scoref2 + n_scoref5 + n_scoref7)

    print("score s" + str(key) +
          "= (" + str(n_scoref1) + ") + ("
          + str(n_scoref2) + ") + ("
          + str(n_scoref5) + ") + ("
          + str(n_scoref7)
          + ") = " + str(sscore) + "\n")

    score.update({key: sscore})



sentences_rangking = sorted(score.items(), key=lambda x: x[1], reverse=True)

# print(score)

js = round(0.50 * len(score))
print(len(score))
best_sentences = []


def search_key(value, unsortedscore):
    posisi_ss = 1
    for keyscore in unsortedscore.values():
        skey = str(posisi_ss)
        if keyscore == value:
            best_sentences.append(posisi_ss)
            print("key found : " + skey)
            break
        posisi_ss += 1
    return posisi_ss


posisi_s = 1
for value in sentences_rangking:
    search_key(value[1], score)
    if posisi_s == js:
        break
    posisi_s += 1

best_sentences.sort()

summarization = ""
for key in best_sentences:
    posisi_s = 1
    for sentence in df['sentence']:
        if key == posisi_s:
            summarization+= sentence + "."
            break
        posisi_s += 1

print(summarization)