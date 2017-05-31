import sys
import nltk
from stanza.nlp.corenlp import CoreNLPClient
import json



class NLPParser(object):
    """
    NLP parse, including Part-Of-Speech tagging.
    Attributes
    ==========
    parser: StanfordCoreNLP
        the Staford Core NLP parser
    """
    def __init__(self):
        self.parser = CoreNLPClient(default_annotators=['ssplit', 'tokenize', 'ner'])

    def parse(self, sent):
        result = self.parser.annotate(sent)
        tokens_list, ner_list = [], []
        for sent in result.sentences:
            tokens, ner = [], []
            currNERType = 'O'
            currNER = ''
            for token in sent:
                tokens += [token.word]
                if token.ner == 'O':
                  if currNER != '':
                    ner.append(currNER.strip())
                  currNER = ''
                elif token.ner == currNERType:
                  currNER += token.word + ' '
                else:
                  if currNER != '':
                    ner.append(currNER.strip())
                  currNERType = token.ner
                  currNER = token.word + ' '
                #ner += [token.ner]
            if currNER != '':
              ner.append(currNER.strip())
            if len(tokens) == 0 or len(ner) == 0:
              continue
            tokens_list.append(tokens)
            ner_list.append(ner)
        return tokens_list, ner_list


def extract_np(data):
    nps = []
    for d in data:
        np = ""
        for tup in d:
            if len(np) == 0:
                np = tup[0]
            else:
                np += " "+tup[0]

        nps.append(np)

    return nps

def leaves(tree):
    #Finds NP (nounphrase) leaf nodes of a chunk tree.
    nps = []
    for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
        nps.append(subtree.leaves())

    return extract_np(nps)


inFile = sys.argv[1]
outFile = sys.argv[2]
parseTool = sys.argv[3]
if parseTool == 'stanford':
  useNLTK = False
elif parseTool == 'nltk':
  useNLTK = True
else:
  raise Exception('parse tool has to be \'stanford\' or \'nltk\'')

grammar = r"""
 NBAR:
    {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
 NP:
    {<NBAR>}
    {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
"""
cp = nltk.RegexpParser(grammar) #chunk parser
with open(inFile, 'r') as fin, open(outFile, 'w') as fout:
  articleId = 0
  for line in fin:
    doc = line.strip('\r\n')
    if useNLTK:
      sents = nltk.sent_tokenize(doc)
      tokens_list = []
      nps_list = []
      for sent in sents:
        tokens = nltk.word_tokenize(sent)
        if len(tokens) == 0:
          continue
        nps = leaves(cp.parse(nltk.pos_tag(tokens)))
        if len(nps) == 0:
          continue
        tokens_list.append(tokens)
        nps_list.append(nps)
    else:
      parser = NLPParser()
      tokens_list, nps_list = parser.parse(doc)

    sentId = 0
    for i in range(len(tokens_list)):
      tokens = tokens_list[i]
      nps = nps_list[i]

      sentDic = dict()
      sentDic['sentId'] = sentId
      entityMentions = []
      start = 0
      for np in nps:
        entityMention = dict()
        entityMention['text'] = np
        entityMention['label'] = 'None'
        entityMention['start'] = start
        entityMentions.append(entityMention)
        start += 1

      sentDic['entityMentions'] = entityMentions
      sentDic['sentText'] = ' '.join(tokens)
      sentDic['articleId'] = articleId
      fout.write(json.dumps(sentDic) + '\n')
      sentId += 1

    articleId += 1
