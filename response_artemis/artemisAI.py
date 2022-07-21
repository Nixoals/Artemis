from queue import Empty
import random
import json
import pickle
from unittest import result
import numpy as np
import nltk
import spacy
from response_artemis.artemisAI_functions import allocate_request

from keras.models import load_model

nlp= spacy.load('fr_core_news_md', exclude=['parser','tagger', 'ner', 'textcat','tokenizer'])
ignore_letters =["?", "!", ".", ",", "-"]



def lemetizer(list_of_words):
  global lemetize
  lemetize=[]
  words = nlp(' '.join(list_of_words))

  for token in words:
      lemetize.append(token.lemma_)

  
  for word in lemetize:
    if word in ignore_letters:
      lemetize.remove(word)
  return lemetize

"""
########################################

Change the directory name to fit your own Raspberry Pi path

"""
intents =  json.loads(open('/home/pi/artemis/response_artemis/intents.json', encoding='utf-8').read())
words= pickle.load(open('/home/pi/artemis/response_artemis/words.pkl', 'rb'))
classes= pickle.load(open('/home/pi/artemis/response_artemis/classes.pkl', 'rb'))
model= load_model('/home/pi/artemis/response_artemis/artemis_model.h5')

"""
########################################
"""

print(classes)

def clean_up_sentence(sentence):
  sentence_words= nltk.word_tokenize(sentence)
  sentence_words= lemetizer(sentence_words)
  print(sentence_words)
  
  return sentence_words

def bag_of_words(sentence):
  sentence_words= clean_up_sentence(sentence)
  bag=[0]*len(words)
  for w in sentence_words:
    for i, word in enumerate(words):
      if word == w:
        print(word)
        bag[i]=1
  return np.array(bag)

def predict_class(sentence):
  bow= bag_of_words(sentence)
  
  res= model.predict(np.array([bow]))[0]
  
  ERROR_THRESHOLD = 0.70
  results =[[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
  results.sort(key = lambda x:x[1], reverse=True) 
  return_list=[]
  
  for r in results:
    return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
  print(return_list)
  return return_list, results

def get_response(intents_list, intens_json):
  if intents_list !=[]:
    tag= intents_list[0]['intent']
    list_of_intents= intens_json['intents']
    for i in list_of_intents:
      
      if i['tag'] == tag:
        tag = i['tag']
        result= random.choice(i['response'])
        allocate_request(tag, result)
        break
  else:
    result="Désolé mais je n'ai pas compris"
    allocate_request('tag', result)
  return result

def responseAI(request):
    message = request
    if message != "":
      ints, results= predict_class(message)
      res= get_response(ints, intents)
      print(res, results)


  
  
  

  
