import sys
import json


def loadTargetTypes(filename):
  map = {}
  with open(filename, 'r') as fin:
    for line in fin:
      seg = line.strip('\r\n').split('\t')
      fbType = seg[0]
      cleanType = seg[1]
      map[fbType] = cleanType
  return map

jsonFname = sys.argv[1]
outFname = sys.argv[2]

mentionTypeRequired = sys.argv[3]
entityTypesFname = sys.argv[4]
relationTypesFname = sys.argv[5]

freebase_dir = sys.argv[6]
mid2typeFname = freebase_dir+'/freebase-mid-type.map'
mid2nameFname = freebase_dir+'/freebase-mid-name.map'
relationTupleFname = freebase_dir+'/freebase-facts.txt'

mid2types = {}
name2mids = {}
mids2relation = {}
targetEMTypes = loadTargetTypes(entityTypesFname)#{'<http://rdf.freebase.com/ns/people.person>':'PERSON', '<http://rdf.freebase.com/ns/organization.organization>':'ORGANIZATION', '<http://rdf.freebase.com/ns/location.location>':'LOCATION'}

with open(mid2typeFname, 'r') as mid2typeFile, open(mid2nameFname, 'r') as mid2nameFile, open(relationTupleFname, 'r') as relationTupleFile:
  for line in mid2typeFile:
    seg = line.strip('\r\n').split('\t')
    mid = seg[0]
    type = seg[1].split('/')[-1][:-1]
    if type in targetEMTypes:
      if mid in mid2types:
        mid2types[mid].add(targetEMTypes[type])
      else:
        mid2types[mid] = set([targetEMTypes[type]])
  print('finish loading mid2typeFile')

  if mentionTypeRequired != 'em':
    targetRMTypes = loadTargetTypes(relationTypesFname)
    for line in relationTupleFile:
      seg = line.strip('\r\n').split('\t')
      mid1 = seg[0]
      type = seg[1].split('/')[-1][:-1]
      mid2 = seg[2]
      if type in targetRMTypes and mid1 in mid2types and mid2 in mid2types:
        key = (mid1, mid2)
        if key in mids2relation:
          mids2relation[key].add(targetRMTypes[type])
        else:
          mids2relation[key] = set([targetRMTypes[type]])
    print('finish loading relationTupleFile')

  for line in mid2nameFile:
    seg = line.strip('\r\n').split('\t')
    mid = seg[0]
    name = seg[1].lower()
    if mid in mid2types and name.endswith('@en'):
      name = name[1:].replace('"@en', '')
      if name in name2mids:
        name2mids[name].add(mid)
      else:
        name2mids[name] = set([mid])
  print('finish loading mid2nameFile')

with open(jsonFname, 'r') as fin, open(outFname, 'w') as fout:
  linkableCt = 0
  for line in fin:
    sentDic = json.loads(line.strip('\r\n'))
    entityMentions = []
    em2mids = {}
    for em in sentDic['entityMentions']:
      emText = em['text'].lower()
      types = set()
      if emText in name2mids:
        linkableCt += 1
        mids = name2mids[emText]
        em2mids[(int(em['start']), em['text'])] = set(mids)
        for mid in mids:
          types.update(set(mid2types[mid]))
        em['label'] = ','.join(types)
      if len(types) > 0:
        entityMentions.append(em)
    sentDic['entityMentions'] = entityMentions

    if mentionTypeRequired != 'em':
      sentDic['relationMentions'] = []
      for (eid1, e1text) in em2mids:
        for (eid2, e2text) in em2mids:
          if eid2 != eid1:
            rmDic = dict()
            rmDic['em1Text'] = e1text
            rmDic['em2Text'] = e2text
            labels = set()
            for mid1 in em2mids[(eid1, e1text)]:
              for mid2 in em2mids[(eid2, e2text)]:
                if (mid1, mid2) in mids2relation:
                  labels.update(set(mids2relation[(mid1, mid2)]))
            if len(labels) > 0:
              rmDic['label'] = ','.join(labels)
              sentDic['relationMentions'].append(rmDic)

    if mentionTypeRequired == 'rm':
      del sentDic['entityMentions']

    fout.write(json.dumps(sentDic) + '\n')
