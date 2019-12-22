from pyvi.ViTokenizer import tokenize
import re, os, string
import pandas as pd

# remove html tag
def clean_text(text):
  text = re.sub("<.*?>", "", text).strip()
  text = re.sub("(\s)+", r"\1", text)
  return text

# tach cau
def sentence_segment(text):
  sents = re.split("([.?!])?[\n]+|[.?!] ", text)
  return sents

# tach tu
def word_segment(sent):
  sent = tokenize(sent)
  return sent

# chuan hoa data, xoa dau
def normalize_text(text):
  listpunctuation = string.punctuation.replace("_", "")
  for i in listpunctuation:
    text = text.replace(i, " ")
  return text.lower()

# list stopwords
filename = "stopwords.csv"
data = pd.read_csv(filename, sep="\t", encoding="utf-8")
list_stopwords = data["stopwords"]

def remove_stopword(text):
  pre_text = []
  words = text.split()
  for word in words:
    if word not in list_stopwords:
      pre_text.append(word)
  text2 = " ".join(pre_text)
  return text2

path_to_corpus = "wikipediacorpus"

f_w = open("datatrain.txt", "w")
for i, file_name in enumerate(os.listdir(path_to_corpus)):
  with open(path_to_corpus + "/" + file_name) as f_r:
    contents = f_r.read().strip().split("</doc>")
    for content in contents:
      if (len(content) < 5):
        continue
      content = clean_text(content)
      sents = sentence_segment(content)
      for sent in sents:
        if(sent != None):
          sent = word_segment(sent)
          sent = remove_stopword(normalize_text(sent))
          if(len(sent.split()) > 1):
            f_w.write(sent + "\n")
    print("Done ", i + 1)

f_w.close()
