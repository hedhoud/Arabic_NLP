import re
import pandas as pd
import sys
import os
import argparse as arg
from num2words import num2words
import string
from decimal import Decimal

num_dic = {
            '۰': '0',
            '۱': '1',
            '۲': '2',
            '۳': '3',
            '۴': '4',
            '۵': '5',
            '۶': '6',
            '۷': '7',
            '۸': '8',
            '۹': '9',
        }


arabic_diacritics = re.compile("""
                             ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
def remove_diacritics(text):
    text = re.sub(arabic_diacritics, '', text)
    return text

# convert all PERSIAN numbers into normal english one.
def convert_PERSIAN_to_ENnumbers(text):
    numbers = re.findall(r"\b\d*\b",text)
    numbers = sorted(list(set(numbers)), reverse=True, key=len)
    for number in numbers:
        for n in number:
           if n in num_dic:
            text = text.replace(n,num_dic[n])
    return text

# Convert digit to chars
def digit2word(text):
    numbers = re.findall(r"\b\d+[\.\d]*\b",text)
    numbers = sorted(list(set(numbers)), reverse=False, key=len)
    for n in numbers:
        try:
            number_in_letter = num2words(float(n), lang="ar")
            x = number_in_letter.replace(',','فاصيله')
            text = text.replace(n,x)
        except :
            pass
    return text


#convert pounctuation marks into string or another one

def normalize_arabic(text):
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    return text

# convert punctuations by any other things 
def convert_punct_by_others(text):
    text = text.replace('.','نقتوقوف')
    text = text.replace('!','وحدتتعجب')
    text = text.replace(':','،')
    text = text.replace('؛','،')
    text = text.replace('ـ','،')
    text = text.replace('%','٪')
    text = text.replace(',','،')
    text = text.replace('  ',' ')
    return text

# get back punctuations after cleaning
def GET_BACK_PUNCT(text):    
    text = text.replace('نقتوقوف','.')
    text = text.replace('وحدتتعجب','!')
    text = text.replace('٪',' ٪ ')
    return text

def remove_url(text):
    text = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", text)
    return text

def separator(text):
    text = text.replace("."," .<stop> ")
    text = text.replace("؟"," ؟<stop> ")
    text = text.replace("!"," !<stop> ")
    text = text.replace("،"," ،<stop> ")
    text = text.split("<stop>")
    text = [s.strip() for s in text]
    return text

if __name__ == '__main__':
    with open(sys.argv[1], 'r', encoding='utf-8') as file_in, open(sys.argv[2], "a", encoding='utf-8')  as output_res:  
        Lines = file_in.readlines()
        for line in Lines:
            post = remove_url(line)
            post = digit2word(post)
            post = convert_punct_by_others(post)
            post = re.findall(r"[\u0600-\u06ff]+", post)
            post = " ".join(post)+'\n'
            post = GET_BACK_PUNCT(post)
            post = re.sub(r'(\W)(?=\1)','',post)
            post = separator(post)
            sentence = ["".join(s)+'\n' for s in post]
            output_res.writelines(sentence)
        df = pd.read_csv(sys.argv[2], encoding='utf-8')
        df = df.drop_duplicates()
        df.to_csv(sys.argv[2], index=False, encoding='utf-8')
        output_res.close()



