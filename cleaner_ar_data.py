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

def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

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

def convert_N(text):
    text = text.replace('۰', '0')
    text = text.replace('۱', '1')
    text = text.replace('۲', '2')
    text = text.replace('۳', '3')
    text = text.replace('٤', '4')
    text = text.replace('۵', '5')
    text = text.replace('٦', '6')
    text = text.replace('۶', '6')
    text = text.replace('۷', '7')
    text = text.replace('۸', '8')
    text = text.replace('۹', '9')
    return text

# convert all PERSIAN numbers into normal english one.
def convert_PERSIAN_to_ENnumbers(text):
    numbers = re.findall(r"\b\d+\b",text)
    numbers = sorted(list(set(numbers)), reverse=True, key=len)
    for number in numbers:
        for n in number:
           if n in num_dic:
            text = text.replace(n,num_dic[n])
    return text

# Convert digit to chars
def digit2word(text):
    # numbers = re.findall(r"\b\d+[\.\d]*\b",text)
    numbers = re.findall("[0-9]*",text)
    numbers = sorted(list(set(numbers)), reverse=True, key=len)
    for n in numbers:
        try:
            number_in_letter = num2words(float(n), lang="ar")
            x = number_in_letter.replace('،','فاصيله')
            text = text.replace(n,x)
        except :
            pass
    return text

def digit2word2(text):
    numbers = re.findall(r"\b\d+[\.\d]*\b",text)
    numbers = sorted(list(set(numbers)), reverse=True, key=len)
    for n in numbers:
        try:
            number_in_letter = num2words(float(n), lang="ar")
            x = number_in_letter.replace('،','فاصيله')
            text = text.replace(n,x)
        except :
            pass
    return text

#convert pounctuation marks into string or another one

def normalize_arabic(text):
    text = re.sub('[ٶۊۋۅۇۏۉۈۇۆۄٷ]','و',str(text))
    text = re.sub('[ۓٸ]','ئ',str(text))
    text = re.sub('[ۍېۑےێێی]','ي',str(text))
    text = re.sub('[ٔٲٵ۽ٳٴٱ]','أ',str(text))
    text = re.sub('[ؼڲڰڭگڱڳڬڮکڴڪګػ]','ك',str(text))
    text = re.sub('[٫ڑړږژڗڕڙڔڒۯ]','ر',str(text))
    text = re.sub('[ڸڷڶڵ]+','ل',str(text))
    text = re.sub('[ډڊڌڍڏڋڎڐۮڈ]','د',str(text))
    text = re.sub('[ڛڜښ]','س',str(text))
    text = re.sub('[ڞڟ؃ڝ]','ص',str(text))
    text = re.sub('ڟ','ط',str(text))
    text = re.sub('[ڢڣڤڦڥڡ]','ف',str(text))
    text = re.sub('[ټٺٽٿٽٹ]','ت',str(text))
    text = re.sub('[ڨٯڧ]','ق',str(text))
    text = re.sub('[ڻںڼڽڹ]','ن',str(text))
    text = re.sub('[ۀہەۿۂھ]','ه',str(text))
    text = re.sub('ڿ','ج',str(text))
    text = re.sub('[ۍۑېێے]','ج',str(text))
    text = re.sub('[#$&()*+/<=>@[^_`|~٪٬]',' ',str(text))
    return text

# convert punctuations by any other things 
def convert_punct_by_others(text):
    text = text.replace('.',' نقتوقوف ')
    text = text.replace('!',' وحدتتعجب ')
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
    text = text.replace(' .','.')
    text = text.replace(' !','!')
    text = text.replace(' ؟','؟')
    text = text.replace(' ،','،')
    return text

def remove_url(text):
    text = re.sub('http://\S+|https://\S+', " ", text)
    return text

def separator(text):
    text = text.replace("."," .<stop> ")
    text = text.replace("؟"," ؟<stop> ")
    text = text.replace("!"," !<stop> ")
    text = text.replace("،"," ،<stop> ")
    text = text.split("<stop>")
    text = [s.strip() for s in text]
    return text

def symbols2name(text):
    text = text.replace("$", " دولار ")
    text = text.replace("€", " يورو ")
    text = text.replace("£", " بوند ")
    text = text.replace("¥", " يان ")
    text = text.replace("₹", " روبل ")
    text = text.replace("%", " بالمئة ")
    text = text.replace("٪", " بالمئة ")
    return text

def normalize_punct(text):
    text = re.sub("[;؛]",".",text)
    text = re.sub("[:,]","،",text)
    text = re.sub("[-_]"," ",text)
    return text

def wrong2true(text):
    text = re.sub('[ٶۊۋۅۇۏۉۈۇۆۄٷ]','و',str(text))
    text = re.sub('[ۓٸ]','ئ',str(text))
    text = re.sub('[ۍېۑےێێی]','ي',str(text))
    text = re.sub('[ٔٲٵ۽ٳٴٱ]','أ',str(text))
    text = re.sub('[ؼڲڰڭگڱڳڬڮکڴڪګػ]','ك',str(text))
    text = re.sub('[٫ڑړږژڗڕڙڔڒۯ]','ر',str(text))
    text = re.sub('[ڸڷڶڵ]+','ل',str(text))
    text = re.sub('[ډڊڌڍڏڋڎڐۮڈ]','د',str(text))
    text = re.sub('[ڛڜښ]','س',str(text))
    text = re.sub('[ڞڟ؃ڝ]','ص',str(text))
    text = re.sub('ڟ','ط',str(text))
    text = re.sub('[ڢڣڤڦڥڡ]','ف',str(text))
    text = re.sub('[ټٺٽٿٽٹ]','ت',str(text))
    text = re.sub('[ڨٯڧ]','ق',str(text))
    text = re.sub('[ڻںڼڽڹ]','ن',str(text))
    text = re.sub('[ۀہەۿۂھ]','ه',str(text))
    text = re.sub('ڿ','ج',str(text))
    text = re.sub('[ۍۑېێے]','ج',str(text))
    return text

def delet_non_need(text):
    text = re.sub(r'[\u0600-\u0620]+','',text)
    text = re.sub(r'[\u0677-\u06FF]+','',text)
    text = re.sub(r'[\u063B-\u063F]+','',text)
    return text

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--punctuation', help= "-", action = "store_true", default=False)
    parser.add_argument('--forlm', help= "-", action = "store_true", default=False)
    parser.add_argument('--input', help= " path to the text for cleaning", type=str, default=None)
    parser.add_argument('--output', help= "path for the cleaning text ", type=str, default=None)
    args = parser.parse_args()

    if args.punctuation:
        with open(args.input, 'r', encoding='utf-8') as file_in, open(args.output, "a", encoding='utf-8')  as output_res:  
            Lines = file_in.readlines()
            for line in Lines:
                post = remove_url(line)
                post = normalize_punct(post)
                post = symbols2name(post)
                post = digit2word(post)
                post = digit2word2(post)
                post = normalize_arabic(post)
                post = remove_diacritics(post)
                output_res.writelines(post)
        output_res.close()
    elif args.forlm:
        with open(args.input, 'r', encoding='utf-8') as file_in, open(args.output, "a", encoding='utf-8')  as output_res:  
            Lines = file_in.readlines()
            for line in Lines:
                post = remove_url(line)
                post = symbols2name(post)
                post = separator(post)
                post = wrong2true(post)
                post = convert_N(post)
                post = digit2word(post)
                post = remove_emoji(post)
                post = re.findall(r"[\u0621-\u0651]+", post)
                post = " ".join(post)+'\n'
                post = delet_non_need(post)
                post = remove_diacritics(post)
                post = re.sub(r"[؟!؛،._,:;ـ]"," ",post)
                output_res.writelines(post)
                output_res.flush()
        output_res.close()
        