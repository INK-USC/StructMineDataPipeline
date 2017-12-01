__author__ = 'ZeqiuWu'
import json
import sys
from collections import defaultdict
import unicodedata


trainFile = sys.argv[1]
testFile = sys.argv[2]
outFile = sys.argv[3]
file = open(trainFile, 'r')
f = open(outFile, 'w')
writtenSents = set()
for line in file.readlines():
    sent = json.loads(line)
    sentText = unicodedata.normalize('NFKD', sent['sentText']).encode('ascii','ignore').rstrip('\n').rstrip('\r')
    if sentText in writtenSents:
        continue
    f.write(sentText)
    f.write('\n')
    writtenSents.add(sentText)
file.close()
file = open(testFile, 'r')
for line in file.readlines():
    sent = json.loads(line)
    sentText = unicodedata.normalize('NFKD', sent['sentText']).encode('ascii','ignore').rstrip('\n').rstrip('\r')
    if sentText in writtenSents:
        continue
    f.write(sentText)
    f.write('\n')
    writtenSents.add(sentText)
file.close()
f.close()
