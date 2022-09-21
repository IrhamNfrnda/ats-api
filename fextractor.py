from aifc import Error

import filehandler


def sentence_location(sentences):
    # jumlah sentence di dokumen
    jumlah_s = len(sentences)
    posisi_s = 1
    score_f1 = {}
    for index, content in zip(sentences['sentence_index'], sentences['sentence']):
        # for content in sentences['sentence']:
        s_f1 = ((jumlah_s - posisi_s) / jumlah_s)
        key = str(index)
        score_f1.update({key: s_f1})
        posisi_s += 1
    return score_f1


def sentence_length(sentences):
    posisi_s = 1
    score_f2 = {}
    d_term = filehandler.hitung_dkata(sentences)
    for index, content in zip(sentences['sentence_index'], sentences['sentence']):
        jumlah_term = len(content.split())
        s_f2 = jumlah_term / d_term
        key = str(index)
        score_f2.update({key: s_f2})
        posisi_s += 1
    return score_f2


def positive_word(sentences):
    # hitung semua jumlah term di sentence
    def word_count(str):
        counts = dict()
        words = str.split()

        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1

        return counts

    # hitung jumlah term terbanya di sentence
    def positive_word(str):
        postive = dict()
        words = str.split()

        pw = 0

        for word in words:
            if cterm[word] > pw:
                pw = cterm[word]
                p_word = word

        return p_word

    posisi_s = 1
    for content in df['sentence']:
        # eksekusi semua jumlah term di sentence
        cterm = word_count(content)
        pw = positive_word(content)
        posisi_s += 1
        j_pw = cterm[pw]
        score_f3 = (1 / jumlah_term) * j_pw
        print("S" + str(posisi_s) + " : " + str(score_f3))


def negative_word(sentences):
    posisi_s = 1
    score_f4 = {}
    for index, content in zip(sentences['sentence_index'], sentences['sentence']):
        s_kata = filehandler.hitung_jumlahkata_sentence(content)
        nw = filehandler.cek_nword(content)
        j_nw = s_kata[nw]
        jumlah_term = len(content.split())
        s_f4 = (1 / jumlah_term) * j_nw
        key = str(index)
        score_f4.update({key: s_f4})
        posisi_s += 1
    return score_f4


def numerical_feature(sentences):
    posisi_s = 1
    score_f5 = {}
    jumlah_term = filehandler.hitung_dkata(sentences)
    for index, content in zip(sentences['sentence_index'], sentences['sentence']):
        jumlah_numerik = filehandler.hitung_numerik(content)
        # jumlah_term = len(content.split())
        s_f5 = jumlah_numerik / jumlah_term
        key = str(index)
        score_f5.update({key: s_f5})
        posisi_s += 1
    return score_f5


def entity_feature(sentences):
    posisi_s = 1
    score_f6 = {}
    for content in sentences['sentence']:
        jumlah_entitas = filehandler.hitung_entity(content)
        jumlah_term = len(content.split())
        s_f6 = jumlah_entitas / jumlah_term
        key = str(posisi_s)
        score_f6.update({key: s_f6})
        posisi_s += 1
    return score_f6


def similarity_to_title(title, sentences):
    lt = filehandler.convert_to_list(title)
    posisi_s = 1
    score_f7 = {}
    for index, content in zip(sentences['sentence_index'], sentences['sentence']):
        ls = filehandler.convert_to_list(content)
        s_f7 = filehandler.jaccard(lt, ls)
        key = str(index)
        score_f7.update({key: s_f7})
        posisi_s += 1
    return score_f7
