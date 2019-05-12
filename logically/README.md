# Topic Modelling & NER of NEWS text

Data corpus can be found here - https://research.signal-ai.com/newsir16/signal-dataset.html

There are 2 ipython notebooks in this repository
- TopicModelling.ipynb 
- Spacy-NER Vs Stanford-NER.ipynb

### Some points about TopicModelling.ipynb
- Notebook to perform topic modelling on the news article dataset. The notebook describes the following step
  - Data cleaning
  - Building word corpus
  - Converting document to TF-IDF format
  - Training and creating topic model for the dataset
- Number of topic choosen - 25
- Number of passes over the data-set - 2 times
- Training time - each pass took around 1 hour to run on 1 million news article
- Trained model can be downloaded from here - https://drive.google.com/drive/folders/1VwHhQYacVcW8pRqzxW_U0OL2ZMY5nSXX?usp=sharing
- More work required on getting the optimal number of topics for this dataset
- One can train this model on larger epocs to get a better model

### Some points about Spacy-NER Vs Stanford-NER.ipynb
- This notebook describe the approaches I took to perform NER on the news article dataset.
- Compared results on **PERSON**, **ORG** & **LOCATION**
- I compare the output from the following 2 approaches
  - spaCy's NER Tagger
  - Stanford NER Tagger (More info can be found here - https://nlp.stanford.edu/software/CRF-NER.html)
    - This requires **java8** or above to run the Stanford NER Tagger
- I found Stanford NER Tagger performing better on this dataset. But its quite slow when compared to spaCy NER Tagger
