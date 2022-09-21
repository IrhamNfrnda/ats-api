import pandas as pd
import numpy as np
import re
import requests
from collections import Counter
import wget
import spacy
from datetime import datetime

# spacy.cli.download("en_core_web_sm")

def baca_file(file):
    x = open(file, 'r', encoding='utf-8')
    y = x.read()
    Sentences = y.splitlines()
    return Sentences


def buat_nama():
    # Penamaan data biar tidak ganda
    now = datetime.now()
    current_time = now.strftime("%d%m%Y%H%M%S")
    dataName = "data" + current_time
    return dataName


def exctract_chat(filepath, idchat, idringkas):

    chat = baca_file(filepath)

    chat = [line.strip() for line in chat]
    clean_chat = [line for line in chat if not "bergabung menggunakan" in line]
    clean_chat = [line for line in clean_chat if len(line) > 1]
    clean_chat = [line for line in clean_chat if not line.endswith("keluar")]
    clean_chat = [line for line in clean_chat if not line.endswith("<Media tidak disertakan>")]
    clean_chat = [line for line in clean_chat if not line.endswith("Pesan ini telah dihapus")]
    msgs = []
    pos = 0
    for line in clean_chat:
        if re.findall("\A\d+[/]", line):
            msgs.append(line)
            pos += 1
        else:
            take = msgs[pos - 1] + ". " + line
            msgs.append(take)
            msgs.pop(pos - 1)
    time = [msgs[i].split(' ')[1].split('-')[0] for i in range(len(msgs))]
    time = [s.strip(' ') for s in time]
    date = [msgs[i].split(' ')[0] for i in range(len(msgs))]
    name = [msgs[i].split('-')[1].split(':')[0] for i in range(len(msgs))]
    sentencesindex = [];
    sentences = []
    index = 1
    # id_datachat = 12345
    iddatachat = []
    listidingkas = []
    for i in range(len(msgs)):
        try:
            sentences.append(msgs[i].split(':')[1])
        except IndexError:
            sentences.append('Missing Text')
        sentencesindex.append(index)
        iddatachat.append(idchat)
        listidingkas.append(idringkas)
        index += 1

    df = pd.DataFrame(list(zip(sentencesindex, date, time, name, sentences, iddatachat, listidingkas)), columns=['sentence_index', 'date', 'time', 'name', 'sentence', 'id_datachat', 'id_ringkas'])

    i = df[(df.sentence == 'Missing Text')].index
    df = df.drop(i)

    i = df[(df.sentence == ' Buka tautan ini untuk bergabung ke grup WhatsApp saya')].index
    df = df.drop(i)

    i = df[(df.sentence == ' Ikuti tautan ini untuk bergabung ke grup WhatsApp saya')].index
    df = df.drop(i)

    i = df[(df.sentence == ' Anda menghapus pesan ini')].index
    df = df.drop(i)
    return df


def sortbydate(date, df):
    specificdate = df[(df.Date == date)]
    return specificdate


def buat_dokumen(df):
    dokumen = ""
    for sentence in df['sentence']:
        dokumen += sentence + "."


def hitung_dkata(df):
    d_kata = 0
    for sentence in df['sentence']:
        jumlah_term = len(sentence.split())
        d_kata += jumlah_term
    return d_kata


def hitung_jumlahkata_sentence(str):
    counts = dict()
    words = str.split()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts


def cek_pword(str):
    words = str.split()
    s_kata = hitung_jumlahkata_sentence(str)
    pw = 0
    for word in words:
        if s_kata[word] > pw:
            pw = s_kata[word]
            p_word = word
    return p_word


def cek_nword(str):
    words = str.split()
    s_kata = hitung_jumlahkata_sentence(str)
    nw = 0
    for word in words:
        if s_kata[word] > nw:
            nw = s_kata()[word]
            n_word = word
    return n_word


def hitung_numerik(str):
    numerik = 0
    words = str.split()

    for word in words:
        if word.isdigit():
            numerik += 1
    return numerik


def hitung_entity(str):
    ner = spacy.load("en_core_web_sm")
    text = ner(str)
    j_ent = 0
    for word in text.ents:
        j_ent = j_ent + 1
    return j_ent


def convert_to_list(string):
    li = list(string.split(" "))
    return li


def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union


def ubah_data_ke_array(score):
    arr_value = []
    for value in score:
        arr_value.append(score[value])
    return arr_value
