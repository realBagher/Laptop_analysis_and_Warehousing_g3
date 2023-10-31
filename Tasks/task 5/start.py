import pandas as pd
import os
import numpy as np
from unidecode import unidecode
import nltk
import hazm
import string
import re
import pickle
import streamlit as st

def normalizeing(text):
    normalizer = hazm.Normalizer()
    return normalizer.normalize(text)
def convert_to_lower(text):
    return text.lower()
def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))
with open('stopwords.txt',encoding='utf-8') as stopwords_file:
    stopwords=stopwords_file.readlines()
stopwords=[line.replace('\n','') for line in stopwords]
nltk.download('stopwords')
nltk_stopwords=nltk.corpus.stopwords.words('english')
stopwords.extend(nltk_stopwords)
def remove_stopwords(text):
    removed = []
    stop_words = stopwords
    tokens = nltk.word_tokenize(text)
    for i in range(len(tokens)):
        if tokens[i] not in stop_words:
            removed.append(tokens[i])
    return " ".join(removed)
def remove_extra_white_spaces(text):
    single_char_pattern = r'\s+[a-zA-Z0-9آ-ی۰-۹]\s+'
    without_sc = re.sub(pattern=single_char_pattern, repl=" ", string=text)
    return without_sc
def stemmering_f(text):
    stemmer = hazm.Stemmer()
    tokens = hazm.word_tokenize(text)
    for i in range(len(tokens)):
        lemma_word = stemmer.stem(tokens[i])
        tokens[i] = lemma_word
    return " ".join(tokens)
def stemmering_e(text):
    stemmer = nltk.SnowballStemmer('english')
    tokens = nltk.word_tokenize(text)
    for i in range(len(tokens)):
        lemma_word = stemmer.stem(tokens[i])
        tokens[i] = lemma_word
    return " ".join(tokens)
def unicode(text):
    return unidecode(text)
def to_float(text):
    try:
        return float(text)
    except: return 0
vcf=open('la_v.quera','rb')
vc=pickle.load(vcf)
vcf.close()
mf=open('la_xb.quera','rb')
m=pickle.load(mf)
mf.close()

text=st.text_input('load your Attributes')
text=normalizeing(text)
text=convert_to_lower(text)
text=remove_punctuation(text)
text=remove_stopwords(text)
text=remove_extra_white_spaces(text)
text=stemmering_f(text)
text=stemmering_e(text)
text=unicode(text)
text=[text]
text=vc.transform((text))
p=round(pow(2,m.predict(text)[0]))
p='{:,.0f} R'.format(0)
f'قیمت پیش بینی شده برای ویژگی هایی که وارد شده با خطای 20 تا 40 میلیون ریال'
f'{p}'
