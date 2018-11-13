# Requirements Synthesizer
The Requirements Synthesizer is created by Niels Wever for his Master Thesis: Synthesizing Creative Requirements with Natural Language Processing. The files that are created for the thesis are AnalyzeRequirements.py and GenerateRequirements.py

Installing the libraries which are used is described below for a Windows machine (tested with Windows 10 Home). If you are using another operating system, please follow the links to get instructions

## Installing the libraries
Several libraries are needed to use the Requirements Synthesizer. The needed libraries to install are [NLTK](https://pypi.org/project/nltk/), [PractNLPTools](https://pypi.org/project/practnlptools/), sense2vec](https://github.com/explosion/sense2vec), [spacy](https://spacy.io/), [lib3to2](https://pypi.org/project/3to2/) and [grammar-check](https://pypi.org/project/grammar-check/).
1. Make sure you have installed Python 2.7, a newer version will not work with PractNLPTools
2. Install [NLTK](https://pypi.org/project/nltk/)
    * Install with pip is possible `pip install nltk`
  
3. Download the [NLTK data](http://www.nltk.org/data.html)
    * With python in command prompt is possible `python -m nltk.downloader all`
    * Or use the Python command line tool:
      ```python
	  >>> import nltk
	  >>> nltk.download()
	  ```
3. Install [PractNLPTools](https://pypi.org/project/practnlptools/)
    * Download repository and unzip
  Move to the folder with command prompt ```cd path\to\folder```
  Install with Python: `python setup.py install`
4. Install [sense2vec](https://github.com/explosion/sense2vec) with [spacy](https://spacy.io/)
    * Using command prompt with pip and python is possible to install:
      ```
	  pip install sense2vec
	  pip install -U spacy
	  python -m spacy download en
	  ```
5. Install [grammar-check](https://pypi.org/project/grammar-check/) and [lib3to2](https://pypi.org/project/3to2/) (needed for grammar-check to use it in Python 2.7):
    * Install with pip:
      ```
	  pip install 3to2
	  pip install grammar-check
	  ```
 
## Needed resources
Several resources are needed to use the Requirements Synthesizer. The resources have to be downloaded manually and stored in a resources folder. This section describes where they come from and where to place them
1. [SemLink](https://verbs.colorado.edu/semlink/) is used to have a mapping of VerbNet to PropBank. Download 1.2.2c.zip and place the unpacked foler in the resources folder. The file used is `resources\1.2.2c\vn-pb\vnpbMappings`
2. requirements.txt should contain the requirements that are used as input to analyze and synthesize requirements. Every line should contain a seperate User Story in Connextra template: As a [user], I want [goal], so that [reason]. As test the User Stories of the [Recycling 101](https://warm-beach-37724.herokuapp.com/) app are used (retrieved from: Dalpiaz, Fabiano (2018), “Requirements data sets (user stories)”, Mendeley Data, v1 http://dx.doi.org/10.17632/7zbk8zsd8y.1).
3. The latest reddit vectors models are used by [sense2vec](https://github.com/explosion/sense2vec) and are attached to every latest [release](https://github.com/explosion/sense2vec/releases). Download these vectors and unpack them in the resources folder. The folder used is `resources\reddit_vectors-1.1.0`
4. [VerbNet](http://verbs.colorado.edu/~mpalmer/projects/verbnet/downloads.html) files are used to get the right sentence structure. Download the files and unpack them, so that you have them saved in `resources\new-vn`

## Using the Requirements Synthesizer
To use the requirements synthesizer you should have installed the needed libraries and stored the needed resources in the resources folder. Next, an empty output folder needs to be created and the user stories that need to be analyzed should be stored into the requirements.txt file.
If all these steps are taken, first the AnalyzeRequirements.py file should be runned. This file generates a parts.p file in the output folder. With this file GenerateRequirements.py can do its work. Two files are created after running GenerateRequirements.py, an eparts.p file and synthesized_requirements.txt file. This last file contains the synthesized requirements.
If new requirements need to be synthesized, the output folder needs to be emptied.
