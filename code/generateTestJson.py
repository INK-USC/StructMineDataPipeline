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
        tokens, ner = [], []
        for sent in result.sentences:
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
            if currNER != '':
              ner.append(currNER.strip())
        return tokens, ner


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
mentionTypeRequired = sys.argv[4]
if mentionTypeRequired not in set(['em', 'rm', 'both']):
  raise Exception('unknown mention type requirement')


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
articleId = inFile
with open(inFile, 'r') as fin, open(outFile, 'w') as fout:
  sentId = 0
  line = 'random'
  while line:
    line = fin.readline()
    sent = line.strip('\r\n')
    em_gts, rm_gts = [], []
    if mentionTypeRequired != 'rm':
      em_line_seg = fin.readline().strip('\r\n').split('\t')
      em_gts = [(em_line_seg[i*2], em_line_seg[i*2+1]) for i in range(len(em_line_seg)/2)]
      if mentionTypeRequired != 'em':
      rm_line_seg = fin.readline().strip('\r\n').split('\t')
      rm_gts = [(rm_line_seg[i*3], rm_line_seg[i*3+1], rm_line_seg[i*3+2]) for i in range(len(rm_line_seg)/3)]

    sentDic = dict()
    sentDic['sentId'] = sentId

    if useNLTK:
      tokens = nltk.word_tokenize(sent)
      if len(tokens) == 0:
        continue
      nps = leaves(cp.parse(nltk.pos_tag(tokens)))
      if len(nps) == 0:
        continue
    else:
      parser = NLPParser()
      tokens, nps = parser.parse(sent)
      #print sent, nps
      if len(tokens) == 0 or len(nps) == 0:
        continue

    skip = False
    for gt in em_gts:
      if gt[0] not in nps:
        skip = True
        break
    if skip:
      continue
    for gt in rm_gts:
      if gt[0] not in nps or gt[1] not in nps:
        skip = True
        break
    if skip:
      continue


    if mentionTypeRequired != 'rm':
      start = 0
      entityMentions = []
      for np in nps:
        entityMention = dict()
        entityMention['text'] = np
        entityMention['label'] = 'None'
        for gt in em_gts:
          if np == gt[0]:
            entityMention['label'] = gt[1]
            break
        entityMention['start'] = start
        entityMentions.append(entityMention)
        start += 1
      sentDic['entityMentions'] = entityMentions

    if mentionTypeRequired != 'em':
      sentDic['relationMentions'] = []
      for em1 in entityMentions:
        for em2 in entityMentions:
          if em1 is not em2:
            rmDic = dict()
            rmDic['em1Text'] = em1['text']
            rmDic['em2Text'] = em2['text']
            rmDic['label'] = 'None'
            for gt in rm_gts:
              if em1['text'] == gt[0] and em2['text'] == gt[1]:
                rmDic['label'] = gt[2]
                break
            sentDic['relationMentions'].append(rmDic)

    sentDic['sentText'] = ' '.join(tokens)
    sentDic['articleId'] = articleId
    fout.write(json.dumps(sentDic) + '\n')
    sentId += 1
