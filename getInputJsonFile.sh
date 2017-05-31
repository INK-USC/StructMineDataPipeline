inTestFile='./data/test.txt'
inTrainFile='./data/documents.txt'
mentionType='both' #'em' or 'rm' or 'both'
emTypeMapFile='./data/emTypeMap.txt'
rmTypeMapFile='./data/rmTypeMap.txt'
outTrainFile='./data/train.json'
outTestFile='./data/test.json'
parseTool='stanford' #'nltk' or 'stanford'
testOnly=false
freebaseDir='/shared/data/xren7/EntityLinking/resource'

if [ "$testOnly" = false ] ; then
  echo 'start generating candidate entity mentions'
  python code/generateTrainJson.py $inTrainFile tmp1.json $parseTool
  echo 'start linking to freebase'
  python code/linkToFB.py tmp1.json tmp2.json $mentionType $emTypeMapFile $rmTypeMapFile $freebaseDir
  echo 'start generating negative examples'
  python code/getNegRMs.py tmp2.json $outTrainFile
  echo 'generated the json file'
  echo 'removing tmp files...'
  rm tmp1.json
  rm tmp2.json
fi

echo 'start generating test json file'
python code/generateTestJson.py $inTestFile $outTestFile $parseTool $mentionType
