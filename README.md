# CoTypeDataProcessing
Data Processing Pipeline for CoType, PLE, AFET

## Description
It generates the train & test json files for the above three information extraction models as input files. Each line of a json file contains information of a sentence, including entity mentions, relation mentions, etc.
To generate such json files, you need to provide the following input files (we include examples in ./data folder):

*Training:
Freebase files (download from ???)
Raw training corpus file (each line as a document)
Entity & Relation mention target type mapping from freebase type name to target type name

*Test:
Raw test corpus file with ground truth mention & label pairs with each sentence in the following format: 
```
sentence text.
pairs of entity mention and its label, separated by tab (remove this line if only relation mentions are needed)
triples of relation mention and its label, separated by tab (remove this line if only entity mentions are needed)
```

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
Our example data files are located in ./data folder. You should be able to see these 2 files generated in the same folder after running the above command: train.json and test.json


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
Mention type(s) required to generate. You can choose to generate entity mentions only or relation mentions only or both. The parameter value can be set to 'em' or 'rm' or 'both'.
```
mentionType='both'
```

