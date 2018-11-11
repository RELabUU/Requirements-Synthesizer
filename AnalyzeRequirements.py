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
    tree = ET.ElementTree(file='C:\Python27\ReqAnalyzing\pred-args-map.xml')
    predargs = True

#open the file with the requirements
filewithrequirements = False
if os.path.exists('C:\Python27\ReqAnalyzing\ResearchRequirements.txt'):
    reqListFile = "C:\Python27\ReqAnalyzing\ResearchRequirements.txt"
    reqs = open(reqListFile).readlines()
    filewithrequirements = True

#make a dictionary to store the thematic roles
#user story  always starts with want or need as a verb, check if the verbs are different after that part
#so make two dictionaries instead of one
#verbs are present next to the different thematic roles, so define verb lists
allparts = {}
allparts['V'] = []
allparts['Agent'] = []

#arguments you want to save
wanted_args = ['A0', 'A1', 'A2', 'A3', 'A4', 'A5']


'''
Analyzing known requirements start here

Steps should be as follows:
1. Strip requirement: As a [Agent], I want (to) [rest requirement], so that [argument]
   --> save [Agent], keep [rest requirement]
2. Do srl per rest requirement
3. Check per verb which arguments it has in the srl, do take into account that one agent is missing (in step 4)
4. Check which arguments the verb needs according to the xml
   (for example rise needs different arguments per verb-class)
5. Assign the roles to the arguments and add them to the total list if the sets ar the same. Skip agents as they are already saved.
'''

if predargs and filewithrequirements:
    i = 0
    for requirement in reqs:

        # Step 1, strip the requirements
        start, req = requirement.split(', I want ')
        if len(req.split(', so that')) > 1:
            req = req.split(', so that')[0]
        req = req.split(' ',1)[1]
        print req

        # Agent already known
        if not start.split(' ', 2)[2] in allparts['Agent']:
            allparts['Agent'].append(start.split(' ', 2)[2])

        # Step 2, do srl (with practNLPtools)
        srlreq = annotator.getAnnotations(req)['srl']
        
        # Step 3, check arguments per verb available
        for verb in srlreq:
            available_arguments = set()
            for argument in verb.keys():
                if argument in wanted_args:
                    available_arguments.add(argument)
            
            # Step 4, check which arguments are needed
            lemma = lemmatizer.lemmatize(verb["V"], pos='v')
            search = 'predicate[@lemma="' + lemma + '"]'
            for predicate in tree.iterfind(search):
                for argmap in predicate:
                    needed_arguments = set()
                    agentNeeded = False
                    agentAValue = ""
                    for role in argmap:
                        argument = "A" +  role.attrib['pb-arg']
                        needed_arguments.add(argument)
                        if role.attrib['vn-theta'] == "Agent":
                            agentNeeded = True
                            agentAValue = argument
                    
                    #If an agent is needed it could be possible that it isn't available in the available arguments
                    #if so --> go to the elif
                    startAdd = False
                    extraArgument = ""
                    if set(available_arguments) == set(needed_arguments):
                        startAdd = True 
                    elif agentNeeded:
                        available_arguments.add(agentAValue)
                        if set(available_arguments) == set(needed_arguments):
                            startAdd = True

                    #If one the available sets matches with the needed set, the adding can start
                    if startAdd:
                        #Add verb first if it doesn't exist
                        if not verb['V'] in allparts['V']:
                            allparts['V'].append(verb['V'])

                        #Then the roles, if they don't exist. Mind the extra cheating argument for the Agent, so skip Agents
                        for role in argmap:
                            argument = "A" +  role.attrib['pb-arg']
                            thematicrole = role.attrib['vn-theta']

                            if thematicrole != "Agent":
                                if thematicrole in allparts:
                                    if extraArgument != argument:
                                        if not verb[argument] in allparts[thematicrole]:
                                            allparts[thematicrole].append(verb[argument])
                                else:
                                    if extraArgument != argument:
                                        allparts[thematicrole] = []
                                        allparts[thematicrole].append(verb[argument])

                    if agentNeeded:
                        available_arguments.remove(agentAValue)
                        agentNeeded = False
                        agentAValue = ""
                                
        i += 1

    print "There are " + str(i) + " requirements analyzed."
    print ""
    print "Parts added:"
    pprint(allparts)

    #write the requirements to a file
    import pickle
    pickle.dump(allparts, open("C:\Python27\ReqAnalyzing\parts.p","wb"))

else:
    print "Files are missing! Requirements cannot be analyzed"
    print ""
    print "Make sure the followin files are available:"
    print "C:\Python27\ReqAnalyzing\pred-args-map.xml"
    print "C:\Python27\ReqAnalyzing\ResearchRequirements.txt"

'''
Analyzing requirements ends here
'''
