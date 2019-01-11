# Anthony Vicario
# Second Language Acquisition Lab
# https://slal.commons.gc.cuny.edu/

import argparse
from pandas import *
import eng_to_ipa as ipa
from difflib import SequenceMatcher
import numpy as np
import nltk
import string
from nltk.stem import SnowballStemmer
snowball_stemmer = SnowballStemmer("english")
options.mode.chained_assignment = None

def columnize(df,golden,response):
    df[response] = [i.replace('?', '') for i in df[response]]
    df[response] = [i.replace('x', '').lower() for i in df[response]]
    # Raw Match
    df["match.correct"] = np.where(df[response] == df[golden], 1, 0)
    # Tokenize
    df['token.original'] = [nltk.word_tokenize(i) for i in df[golden]]
    df['token.response'] = [nltk.word_tokenize(i) for i in df[response]]
    # Lemmatize
    df['stem.original'] = [snowball_stemmer.stem(i) for i in df[golden]]
    df['stem.response'] = [snowball_stemmer.stem(i) for i in df[response]]
    # Clean
    df[response] = [i.replace('emare', "i'mer") for i in df[response]]
    # IPA columns
    df['trans.original'] = df[golden].map(lambda x: ipa.convert(x))
    df['trans.response'] = df[response].map(lambda x: ipa.convert(x))
    df["trans.response"] = [i.replace('*', '') for i in df["trans.response"]]
    return df

def Lev(df,golden,response):
    original = [i for i in df[golden]]
    resp = [i for i in df[response]]
    lis = []
    for i in range(len(original)):
        lis.append(SequenceMatcher(None,original[i],resp[i]).ratio())
    return lis

def lev_dist(filename,outname,goldencol,responsecol):
    dfr = DataFrame.from_csv(filename)
    dfr = columnize(dfr,goldencol,responsecol)
    dfr["ortho.correct"] = Lev(dfr,goldencol,responsecol)
    dfr["trans.correct"] = Lev(dfr,"trans.original","trans.response")
    dfr["stem.correct"] = Lev(dfr,"stem.original","stem.response")
    dfr["token.correct"] = Lev(dfr,"token.original","token.response")
    
    writer = ExcelWriter(outname, engine='xlsxwriter')
    dfr.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    return dfr

def param():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)
    parser.add_argument('outname', type=str)
    parser.add_argument('goldencol', type=str)
    parser.add_argument('responsecol', type=str)
    return parser.parse_args()

def main():
    args = param()
    lev_dist(**vars(args))

if __name__ == '__main__':
    main()
