# -*- coding: utf-8 -*-
"""Tugas Pekan 5 - NLP - Classification Postagger.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16XpSVcowo8f70Pa1z2i8CtDvSTttUbLy

# **POSTagging : Metode Klasifikasi Konvensional Non-Sekuensial**

---
Clarisa Hasya Y - 1301174256
"""

import pandas as pd
import nltk
nltk.download('punkt')

from sklearn import tree
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline

"""**Read File Data Train TSV**"""

df = pd.read_csv("dataset/train.01.tsv",sep="\t", header=None)
df = df.astype(str)

# df.head()

tmp, temp = [] , [] 
training_sentences, training_tags = [] , []
count_sentences = 0

for index, row in df.iterrows():   
    word = row[0].lower()
    tag = row[1]
    key = (word,tag) # simpan di dictionary kata,tag
    if count_sentences < 50:
        if word != 'nan':
            tmp.append(word)
            temp.append(tag)
            if word == '.' :
                training_sentences.append(tmp)
                training_tags.append(temp)
                tmp = []
                temp = []

    if word == '.' :
        count_sentences += 1      
        if(count_sentences == 50):
            break

# print(training_sentences)

# print(training_tags)

"""**Fungsi untuk Ekstraksi Fitur**"""

def features(sentence, index):
    """ sentence: [w1, w2, ...], index: the index of the word """
    #print("sentence index = ")
    #print(sentence[index])
    prefix_1 = ''
    prefix_2 = ''
    suffix_1 = ''
    suffix_2 = ''
    if (len(sentence[index])>2):
      prefix_1 = sentence[index][0]
      prefix_2 = sentence[index][:2]
      suffix_1 = sentence[index][-1]
      suffix_2 = sentence[index][-2:]
    return {
        'word': sentence[index],
        'prefix-1': prefix_1,
        'prefix-2': prefix_2,        
        'suffix-1': suffix_1,
        'suffix-2': suffix_2,        
        'prev_word': '' if index == 0 else sentence[index - 1],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
    }

"""**Fungsi untuk Transformasi Format Dataset**"""

def transform_to_dataset(sentences, tags):
    X, y = [], []
 
    for sentence_idx in range(len(sentences)):
        for index in range(len(sentences[sentence_idx])):
            X.append(features(sentences[sentence_idx], index))
            y.append(tags[sentence_idx][index])
 
    return X, y

"""**Read File Data Test TSV**"""

dt = pd.read_csv("dataset/test_sentences.tsv",sep="\t", header=None)
dt = dt.astype(str)

# dt.head()

tmpp, tempp = [] , [] 
testing_sentences, testing_tags = [] , []

for index, row in dt.iterrows():   
    wordd = row[0].lower()
    tagg = row[1]
    if wordd != 'nan':
        tmpp.append(wordd)
        tempp.append(tagg)
        if wordd == '.' :
            testing_sentences.append(tmpp)
            testing_tags.append(tempp)
            tmpp = []
            tempp = []

# print(testing_sentences)

# print(testing_tags)

"""**Training**"""

X, y = transform_to_dataset(training_sentences, training_tags)

from sklearn import tree
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
 
clf = Pipeline([
    ('vectorizer', DictVectorizer(sparse=False)),
    ('classifier', tree.DecisionTreeClassifier(criterion='entropy'))
])
clf.fit(X, y)

"""**Testing**"""

X_test, y_test = transform_to_dataset(testing_sentences, testing_tags)


"""**Hasil tagging setiap kalimat uji**"""

for sentence in testing_sentences:
    # print(sentence)
    tags = clf.predict([features(sentence, index) for index in range(len(sentence))])
    for i in range(len(sentence)):
        print('kata:',sentence[i] ,', tag:', tags[i])


"""**Accuracy**"""

print('===============================================================================================')
print('Accuracy Classification: ', clf.score(X_test, y_test))
print('===============================================================================================')