import re
from bs4 import BeautifulSoup


def cleanup_document(document):
    # Function to convert a document to a sequence of words,

    # 1. Remove HTML
    soup = BeautifulSoup(document, 'html5lib') # create a new bs4 object from the html data loaded
    for script in soup(["script", "style", "form"]): # remove all javascript and stylesheet code
        script.extract()
    # get text
    review_text = soup.get_text()

    # 2. Remove non-letters (preserving '.' char to know the ending of sentence)
    review_text = re.sub("[^a-zA-Z.]", " ", review_text)
    review_text = re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', review_text)

    # 4. Replace multiple spaces with single space
    document = re.sub(' +', ' ', review_text).strip()
    return document