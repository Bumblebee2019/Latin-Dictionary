from secrets import token_urlsafe
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.latin.declension import CollatinusDecliner
from cltk.lemmatize.latin.backoff import BackoffLatinLemmatizer
from cltk.prosody.latin.macronizer import Macronizer
from cltk.tokenize.line import LineTokenizer
from cltk.tokenize.latin.sentence import SentenceTokenizer
from cltk.corpus.utils.formatter import remove_non_latin
from cltk.tokenize.word import WordTokenizer
import re

user_input = input("Latin term: ")

def jvtext(user_input):
  j = JVReplacer()
  user_input = j.replace(user_input)
  return (user_input)

def clean(text, lower = False):
  cleaned = re.sub(r"[\(\[].*?[\)\]]", "", text)
  cleaned = cleaned.replace("   ", " ").replace("  ", " ")
  if lower == True:
    lower_cleaned = cleaned.lower()
    return(cleaned, lower_cleaned)
  return(cleaned)

def decline(words): #assuming input is a lilst of words
  decliner = CollatinusDecliner()
  declined_words = {}
  try:
    for word in words:
      declined_word = decliner.decline(word)
      declined_words[word] = declined_word  #original word is the key and the declined word is the value
      #print(dec_word)
  except:
    Exception
  return(declined_words)

def lemma(tokens):
  lemmatizer = BackoffLatinLemmatizer()
  tokens = lemmatizer.lemmatize(tokens)
  return(tokens)

def macron(text):
  macronizer = Macronizer("tag_ngram_123_backoff")
  text = macronizer.macronize_text(text)
  return (text)

def line_tokenization(text):
  tokenizer = LineTokenizer("latin")
  text = tokenizer.tokenize(text)
  return (text)

def sentence_tokenization(text, punct=True):
  sent_tokenizer = SentenceTokenizer()
  sentences = sent_tokenizer.tokenize(text)
  updated_sentences = []
  if punct == True:
    for word in sentences:
      word = remove_non_latin(word)
      word = word.lower()
      updated_sentences.append(word)
      #print(sent)
    return(updated_sentences)
  return(sentences)


def word_tokenization(text):
  word_tokenizer = WordTokenizer("latin")
  words = word_tokenizer.tokenize(text)
  return (words)

#This step is only needed for text standardization
#user_input = clean(user_input)
#user_input = jvtext(user_input)

#in case user enters a sentence, we need to analyze 
#each word separately
sentences_list = sentence_tokenization(user_input, punct = True)
print("---------SENTENCES---------")
print(sentences_list)
print('\n')
#print("----------------------------")
print("---------SENTENCE---------")
sentence = sentences_list[0]
print(sentence)
print('\n')
words = word_tokenization(sentence)
print("--------------AFTER WORD TOKENIZATION---------")
print(words)
print("--------------AFTER LEMMATIZATION-------------")
words = lemma(words)
print(words)
#now this is the result:
#[('dilecto', 'diligo'), ('filio', 'filius')]

lemma_list = []
for word in words:
  lemma_list.append(word[1])
#this gives the list of just lemmas
#['diligo', 'filius']
print("----------------LIST OF LEMMAS----------------")
print(lemma_list)
print("------------------DECLINED WORD---------------")
declined = decline(lemma_list)
print(declined)



