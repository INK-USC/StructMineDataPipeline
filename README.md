# CoTypeDataProcessing
Data Processing Pipeline for CoType, PLE, AFET

## Description
It generates the train & test json files for the above three information extraction models as input files. Each line of a json file contains information of a sentence, including entity mentions, relation mentions, etc.
To generate such json files, you need to provide the following input files (we include examples in ./data folder):

### Training:
1. Freebase files (download from [here](https://drive.google.com/file/d/0B--ZKWD8ahE4aXhOLXFUeDZBVzA/view?usp=sharing) (8G) and put the unzipped freebase folder in parallel with code/ and data/ folders)
  
    * The freebase folder should contain: 
    
      freebase-facts.txt (relation triples in the format of 'id of entity 1, relation type, id of entity 2'); 
      
      freebase-mid-name.map (entity id to name map in the format of 'entity id, entity surface name');
      
      freebase-mid-type.map (entity id to type map in the format of 'entity id, entity type'). 

2. Raw training corpus file (each line as a document)

3. Entity & Relation mention target type mapping from freebase type name to target type name

### Test:
1. Raw test corpus file (each line as a document) 

## Dependencies
We will take Ubuntu for example.

* python 2.7
* Python library dependencies
```
$ pip install nltk
```

* [stanford coreNLP 3.7.0](http://stanfordnlp.github.io/CoreNLP/) and its [python wrapper](https://github.com/stanfordnlp/stanza). Please put the library under `CoType/code/DataProcessor/'.

```
$ cd code/
$ git clone git@github.com:stanfordnlp/stanza.git
$ cd stanza
$ pip install -e .
$ wget http://nlp.stanford.edu/software/stanford-corenlp-full-2016-10-31.zip
$ unzip stanford-corenlp-full-2016-10-31.zip
```

## Example Run
Run CoTypeDataProcessing to generate Json input files of CoType for the example training and test raw corpus

```
$ java -mx4g -cp "code/stanford-corenlp-full-2016-10-31/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer
$ ./getInputJsonFile.sh  
```
Our example data files are located in ./data folder. You should be able to see these 2 files generated in the same folder - train.json and test.json, after running the above command.

## Parameters - getInputJsonFile.sh
Raw train & test files to run on.
```
inTrainFile='./data/documents.txt'
inTestFile='./data/test.txt'
```
Output files (input json files for CoType, PLE, AFET).
```
outTrainFile='./data/train.json'
outTestFile='./data/test.json'
```
Directory path of freebase files:
```
freebaseDir='./freebase'
```
Mention type(s) required to generate. You can choose to generate entity mentions only or relation mentions only or both. The parameter value can be set to 'em' or 'rm' or 'both'.
```
mentionType='both'
```
Target mention type mapping files.
```
emTypeMapFile='./data/emTypeMap.txt'
rmTypeMapFile='./data/rmTypeMap.txt' # leave it empty if only entity mention is needed
```
Parsing tool to do sentence splitting, tokenization, entity mention detection, etc. It can be 'nltk' or 'stanford'.
```
parseTool='stanford'
```
Set this parameter to be true if you already have a pretrained model and only need to generate test json file.
```
testOnly=false
```
