import hashlib
import os
import string
import random
import sys
import requests
import re
import fnv
import nltk
import sklearn
import math
import numpy as np
import operator
import PIL
from pprint import pprint
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from tkinter import *
from PIL import Image, ImageTk as tk

folder_path = 'C:\\Users\\Ramin Rafi\\AIproject\\corpus\\corpus\\corpus'
folder_path1 ='C:\\Users\\Ramin Rafi\\AIproject\\stopwords.txt'

# This function checks for the required tags in the html string
def req_tags(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# This function uses the previous function to extract only the required text from the html string
def my_html_parser(html_string):
    new_soup = BeautifulSoup(html_string, 'html.parser')
    texts = new_soup.findAll(text=True)
    tags_text = filter(req_tags, texts)
    return u" ".join(y.strip() for y in tags_text)

def occurencecount(my_list): #termid counter for term occurences
    counter = 0
    mycountlist = []
    mytempid = my_list[0]
    for i in range(len(my_list)):
        if my_list[i][0] != mytempid[0]:
            mycountlist.append(counter)
            counter = 1
            mytempid = my_list[i]
        else:
            counter += 1
    mycountlist.append(counter)
    return mycountlist

def docscount(my_list): #totaldocs counter for terms
    counter = 1
    mytempid = my_list[0]
    mycountlist = []
    for i in range(len(my_list)):
        if my_list[i][0] == mytempid[0]:
            if my_list[i][1] != mytempid[1]:
                counter += 1
                mytempid = my_list[i]
        else:
            mycountlist.append(counter)
            mytempid = my_list[i]
            counter = 1
    mycountlist.append(counter)
    return mycountlist


def func(D, tfd, tfq, df, lend, avglend):
    k1 = 1.2
    k2 = 500
    b = 0.75
    K = k1 * ((1-b) + (b*(lend/avglend)))
    temp = ((D + 0.5)/(df+0.5)) * (((1+k1)*tfd)/(K+tfd)) * (((1+k2)*tfq)/(k2 + tfq))
    answer = math.log(temp, 10)
    return answer

def submit():
    query = name_var.get()
    stoplist = open(sl_file).read()
    stoplist = stoplist.splitlines()
    qid = []

    query = query.split()
    query = [x for x in query if x not in stoplist]
    for i in range(len(query)):
        query[i] = ps.stem(query[i])

    qid.append(1)
    print(query)

    file_content = term_index_file.readlines()
    file_content = [x.strip().split()[0:3] for x in file_content]

    tot_words = 0
    for i in td_pairs.keys():
        for j in td_pairs[i].keys():
            tot_words += len(td_pairs[i][j])

    D = len(doc_ids)
    avg_dlen = tot_words / D
    term_freq = 0
    doc_freq = 0
    lend = 0
    tfq = 0
    avglend = 0
    currtermid = 0
    bm25sum = 0
    doc_length = 0
    currscore = 0
    osakafinal = {}

    for i in range(len(query)):
        doc_length = 0
        for k in doc_ids.keys():
            doc_length = 0
            currscore = 0
            for j in range(len(query[i])):
                if query[i][j] in term_content1:
                    currtermid = int(term_content1[query[i][j]])
                    tfq = query[i].count(query[i][j])
                    if currtermid in td_pairs:
                        if int(k) in td_pairs[currtermid]:
                            doc_freq = doc_freqs[k]
                            term_freq = int(tot_term_freqs[str(currtermid)])
                            for l in td_pairs.keys():
                                if int(k) in td_pairs[int(l)]:
                                    doc_length += len(td_pairs[int(l)][int(k)])
                            currscore += func(D, term_freq, tfq, int(doc_freq), doc_length, avg_dlen)
            templst = [doc_ids[k], round(currscore, 3)]
            osakafinal.setdefault(qid[0], []).append(templst)

    for k, v in osakafinal.items():
        v.sort(key=lambda m: m[1], reverse=True)

    for k, v in osakafinal.items():
        root2 = Tk()
        root2.title("My Search Engine")
        root2.geometry("900x450")
        root2.configure(bg='white')
        root2.iconbitmap("C:\\Users\\Ramin Rafi\\AIproject\\Google.ico")
        sb = Scrollbar(root2)
        sb.pack(side=RIGHT, fill=Y)
        mylist = Listbox(root2, yscrollcommand=sb.set)
        i = 1
        for m in v:
            if int(m[1]) > 0:
                strr = str(m[0]) + "---" + str(i) + "---" + str(m[1])
                mylist.insert(END, strr)
                mylist.pack(side=LEFT, fill=BOTH, expand=True)
                i += 1
        root2.mainloop()

    name_var.set("")

# Tokenizing the text on spaces
file_names = os.listdir(folder_path)
stoplist = open(folder_path1).read()
stoplist = stoplist.splitlines()
termid = open("C:\\Users\\Ramin Rafi\\AIproject\\TERMID.txt", "a", errors='ignore')
docid = open("C:\\Users\\Ramin Rafi\\AIproject\\DOCID.txt", "a", errors='ignore')
term_index = open("C:\\Users\\Ramin Rafi\\AIproject\\term_index.txt", "a", errors='ignore')
required_punc = string.punctuation + "—\""
required_punc = required_punc.replace('\'', '')
substr = "<!DOCTYPE"
curr_doc_id = 1
allterms = {}
allterms1 = {}
tuplist = []
curr_term_id = 1
usinghash = {}

ps = PorterStemmer()

for filename in file_names:
    html = open(folder_path + "\\" + filename, errors='ignore').read()
    index = html.find(substr)
    htmlcode = html[index:]
    finaltext = my_html_parser(htmlcode).lower().split()

    result = [x for x in finaltext if x not in stoplist]
    result = [i.translate(str.maketrans('','',required_punc)) for i in result]
    result = [i for i in result if i]
    result = [ps.stem(i) for i in result]
    y = 0
    flagx = 0
    flagy = 0
    for i in result:
        if i not in allterms:
            flagy = 1
            allterms.update({i: curr_term_id})
            curr_term_id += 1
        else:
            flagx = 1
            temp_curr_term_id = curr_term_id
            curr_term_id = allterms.get(i)
        if len(usinghash) == 0:
            usinghash.update({curr_term_id: {}})
        elif curr_term_id not in usinghash:
            usinghash.update({curr_term_id: {}})
        usinghash[curr_term_id].setdefault(curr_doc_id, []).append(y)
        if flagy == 1:
            tuplist.append([curr_term_id - 1, curr_doc_id, y])
            flagy = 0
        else:
            tuplist.append([curr_term_id, curr_doc_id, y])
        y += 1
        if flagx == 1:
            flagx = 0
            curr_term_id = temp_curr_term_id
    docid.write(str(curr_doc_id)+"\t" + filename + "\n")
    curr_doc_id += 1

for x, y in allterms.items():
    termid.write(str(y) + "\t" + str(x) + "\n")

tuplist.sort(key=lambda tup: [tup[0], tup[1]])
# for a, b, c in tuplist:
#     print(str(a) + ":" + str(b) + ":" + str(c))
initialTID = tuplist[0][0]
docs_count = docscount(tuplist)
tot_times_count = occurencecount(tuplist)
my_counter = 0
myflag = 0
term_index.write(str(initialTID)+" "+str(tot_times_count[0])+" "+str(docs_count[0])+" ")
term_index.write(str(tuplist[0][1]) + "," + str(tuplist[0][2]) + " ")
nthterm = 1
for i in range(len(tuplist)):
    if tuplist[i][0] == initialTID:
        if myflag:
            my_counter += 1
            term_index.write(str(tuplist[i][1] - tuplist[i-my_counter][1]) + "," + str(tuplist[i][2]) + " ")
        else:
            myflag = 1
    else:
        term_index.write("\n"+str(tuplist[i][0])+" "+str(tot_times_count[nthterm])+" "+str(docs_count[nthterm])+" ")
        term_index.write(str(tuplist[i][1]) + "," + str(tuplist[i][2]) + " ")
        initialTID = tuplist[i][0]
        my_counter = 0
        myflag = 1
        nthterm += 1

sl_file = 'C:\\Users\\Ramin Rafi\\AIproject\\stopwords.txt'
term_index_file = open("C:\\Users\\Ramin Rafi\\AIproject\\term_index.txt", "r", errors='ignore')
term_id_file = open("C:\\Users\\Ramin Rafi\\AIproject\\TERMID.txt", "r", errors='ignore')
docid = open("C:\\Users\\Ramin Rafi\\AIproject\\DOCID.txt", "r", errors='ignore')

doc_ids = {}
temp = []
doc_id_raw = docid.readlines()
for x in doc_id_raw:
    temp = x.split("\t")
    doc_ids.update({temp[0]: temp[1].strip()})

term_content = term_id_file.readlines()
term_content1 = {}
for x in term_content:
    a = x.split()
    if len(a) == 2:
        term_content1.update({a[1]: a[0]})
templist = ()
td_pairs = {}
tempdocid = 1
tif_dat = [x.split() for x in term_index_file.readlines()]
doc_freqs = {}
tot_term_freqs = {}
for i in range(len(tif_dat)):
    doc_freqs.update({tif_dat[i][0]: tif_dat[i][2]})

for i in range(len(tif_dat)):
    tot_term_freqs.update({tif_dat[i][0]: tif_dat[i][1]})

currtermid = 1
for i in range(len(tif_dat)):
    del(tif_dat[i][1:3])
    td_pairs.update({int(tif_dat[i][0]): {}})
    for j in range(len(tif_dat[i])):
        tif_dat[i][j] = tif_dat[i][j].split(',')
        if j == 0:
            currtermid = int(tif_dat[i][j][0])
        elif j == 1:
            tempdocid = int(tif_dat[i][j][0])
            td_pairs[currtermid].setdefault(int(tempdocid), []).append(int(tif_dat[i][j][1]))
        else:
            td_pairs[currtermid].setdefault(int(tif_dat[i][j][0]) + int(tempdocid), []).append(int(tif_dat[i][j][0]))

root = Tk()
root.title("My Search Engine")
root.geometry("900x450")
root.configure(bg='white')
root.iconbitmap("C:\\Users\\Ramin Rafi\\AIproject\\Google.ico")

try:
    temp = Image.open("googlee.png")
    width, height = temp.size
    temp = temp.resize((int(width / 4), int(height / 4)))
    temp.save("new.png")
except IOError:
    pass

img = PhotoImage(file="new.png")
label = Label(root, image = img,bg='white')
label.pack()

name_var=StringVar()
name_var.set("")
name_entry = Entry(root, textvariable = name_var,font=('calibre',10,'normal'))
name_entry.pack()

sub_btn=Button(root,text = 'Submit', command = submit)
sub_btn.pack()
root.mainloop()

