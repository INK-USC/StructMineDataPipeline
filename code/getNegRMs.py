import sys
import json

jsonFname = sys.argv[1]
outputFname = sys.argv[2]

with open(jsonFname, 'r') as fin, open(outputFname, 'w') as fout:
  for line in fin:
    sentDic = json.loads(line.strip('\r\n'))
    rms = set()
    ems = set()
    newRms = []
    relationMentions = []
    for em in sentDic['entityMentions']:
      ems.add(em['text'])
    for rm in sentDic['relationMentions']:
      relationMentions.append(rm)
      rms.add(frozenset([rm['em1Text'], rm['em2Text']]))
    for em1 in ems:
      for em2 in ems:
        if em1 != em2:
          if frozenset([em1, em2]) not in rms:
            newRm = dict()
            newRm['em1Text'] = em1
            newRm['em2Text'] = em2
            newRm['label'] = 'None'
            newRms.append(newRm)
            rms.add(frozenset([em1, em2]))
        #break

    for rm in newRms:
      relationMentions.append(rm)
    if len(relationMentions) > 0:
      sentDic['relationMentions'] = relationMentions
      fout.write(json.dumps(sentDic)+'\n')
