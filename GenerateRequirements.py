#used to check if file exists
import os.path

#pretty print if necessary
from pprint import pprint

#Get the lemmatizer from NLTK
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

#Get the annonator from practNLPtools
from practnlptools.tools import Annotator
annotator=Annotator()

#import the semlink verbnet-propbank mapping (also check if file exists)
import xml.etree.cElementTree as ET
predargs = False
if os.path.exists('C:\Python27\ReqAnalyzing\pred-args-map.xml'):
    verbtree = ET.ElementTree(file='C:\Python27\ReqAnalyzing\pred-args-map.xml')
    predargs = True

#use standard python randomizer
import random

#glob needed to find files
import glob

#nltk
import nltk

#sense2vec in combination with Spacy
import spacy
from sense2vec import Sense2VecComponent
spacynlp = spacy.load('en')
s2v = Sense2VecComponent('C:/Python27/ReqAnalyzing/reddit_vectors-1.1.0')
spacynlp.add_pipe(s2v)

#make deepcopy available
import copy

#grammar check
import grammar_check
tool = grammar_check.LanguageTool('en-GB')

'''
Construct requirements starts here

Proposed order.
1. Pick verb from allparts list
2. Check which frames/arguments are needed with verbnet
3. Find a semantically matching argument pair in allparts files
4. Construct sentence with verbnet proposed structure

'''

#First check if files with parts exist
if os.path.exists('C:\Python27\ReqAnalyzing\parts.p'):
    import pickle
    if not os.path.exists('C:\Python27\ReqAnalyzing\eparts.p'):

        allparts = pickle.load(open("C:\Python27\ReqAnalyzing\parts.p","rb"))
        extended_parts = copy.deepcopy(allparts)
        
        for key in allparts:
            for value in allparts[key]:
                doc = spacynlp(value.decode('utf-8'))
                for item in doc:
                    try:
                        most_similar = item._.s2v_most_similar(1)
                        if most_similar[0][0][1] == u'NOUN':
                            multiple_similar = item._.s2v_most_similar(250)
                            i = 0
                            for similarity in multiple_similar:
                                if similarity[1] < 0.75: 
                                    replacement = value.replace(str(item),str(similarity[0][0]),1)
                                    break
                                else: 
                                    i += 1
                            if i == 250:
                                replacement = value.replace(str(item),str(similarity[0][0]),1)

                            
                            if key in extended_parts:
                                if not replacement in extended_parts[key]:
                                    extended_parts[key].append(replacement)
                            else:
                                extended_parts[key] = []
                                extended_parts[key].append(replacement)
                            
                    except KeyError:
                        error = "KeyError"
        pickle.dump(extended_parts, open("C:\Python27\ReqAnalyzing\eparts.p","wb"))
    else:
        extended_parts = pickle.load(open("C:\Python27\ReqAnalyzing\eparts.p","rb"))

    new_reqs_file = open('new_reqs_file.txt', 'a')
    i = 0
    while i < 100:
        #Pick a random verb
        verb = random.choice(extended_parts['V'])
        lemma = lemmatizer.lemmatize(verb, pos='v')

        vclass = "Variable for verbclass"
        #get verb class, just the first one for now
        searchlemma = 'predicate[@lemma="' + lemma + '"]'
        for predicate in verbtree.iterfind(searchlemma):
            for argmap in predicate:
                vclass = argmap.attrib['vn-class']
                break

        if not vclass == "Variable for verbclass":
            #use verbclass to find right file with the parts needed
            #things after the - are not in filenames
            if "-" in vclass:
                vclass = vclass.split("-", 1)[0]
            
            searchfile = "C:\\Python27\\ReqAnalyzing\\vn3.2\\*" + vclass + ".xml"
            for file in glob.glob(searchfile):
                verbfile = file

            #create requirement with agent first
            #As a [Agent], I want to [rest]
            verbnettree = ET.ElementTree(file=verbfile)
            falserequirement = False
            for syntax in verbnettree.iter(tag = 'SYNTAX'):
                requirement = "As a "
                counter = 0
                for part in syntax:
                    if part.tag == "VERB" and counter == 0:
                        break
                    elif 'value' not in part.attrib.keys() and counter == 0:
                        break
                    elif counter == 0 and part.attrib['value'] == "Agent":
                        thematicrolepart = random.choice(extended_parts[part.attrib['value']])
                        requirement += thematicrolepart + ", I want to"
                    elif counter == 0:
                        break
                    elif part.tag == "VERB":
                        requirement += " " + lemma
                    elif part.tag == "PREP":
                        if 'value' in part.attrib:
                            requirement += " " + part.attrib['value']
                    elif 'value' in part.attrib:
                        if part.attrib['value'] in extended_parts: 
                            thematicrolepart = random.choice(extended_parts[part.attrib['value']])
                            requirement += " " + thematicrolepart
                        else:
                            falserequirement = True
                            break
                    counter += 1

                if falserequirement:
                    break


                if len(requirement) > 7:
                    matches = tool.check(requirement)
                    corrected_req = grammar_check.correct(requirement, matches)
                    new_reqs_file.write(corrected_req)
                    new_reqs_file.write("\n")
                    print corrected_req
                    i += 1
    new_reqs_file.close()    
else:
    print "Files with identified parts of requirements do not exist. Please make sure to run AnalyzeRequirements.py first"
    


'''
Constructing requirements ends here
'''
