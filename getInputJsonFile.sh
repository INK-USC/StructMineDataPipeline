inTestFile='./data/test.txt'
inTrainFile='./data/documents.txt'
mentionType='both' #'em' or 'rm' or 'both'
emTypeMapFile='./data/emTypeMap.txt'
rmTypeMapFile='./data/rmTypeMap.txt'
outTrainFile='./data/train.json'
outTestFile='./data/test.json'
parseTool='stanford' #'nltk' or 'stanford'
testOnly=false
freebaseDir='./freebase'

if [ "$testOnly" = false ] ; then
  echo 'start generating train json file'
  python code/generateJson.py $inTrainFile $outTrainFile $parseTool 1 $mentionType $emTypeMapFile $rmTypeMapFile $freebaseDir

  echo 'removing tmp files...'
  rm tmp1.json
  rm tmp2.json
fi

echo 'start generating test json file'
python code/generateJson.py $inTestFile $outTestFile $parseTool 0 $mentionType
