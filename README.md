# Requirements Synthesizer
The Requirements Synthesizer is created by Niels Wever for his Master Thesis: Synthesizing Creative Requirements with Natural Language Processing. The files that are created for the thesis are AnalyzeRequirements.py and GenerateRequirements.py

Installing the libraries which are used is described below for a Windows machine (tested with Windows 10 Home). If you are using another operating system, please follow the links to get instructions

## Installing the libraries before using the Requirements Sythesizer
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
 
