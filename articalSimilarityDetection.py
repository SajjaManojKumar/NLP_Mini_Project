import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords 
from nltk.stem import PorterStemmer  
from nltk.tokenize import word_tokenize 

def subjectOfArticle(url):
    # INPUT: url of article
    # OUTPUT: speech tagged of the body of the article
    # REQUIRED: requests , bs4[BeautifulSoup] , nltk , nltk.corpus[stopwords] , nltk.stem[PorterStemmer] , nltk.tokenize[word_tokenize]

    req = requests.get(url)
    articlePage = req.content

    # loading html libs
    soup = BeautifulSoup(articlePage, 'html5lib')

    # getting content (of all) within <div class='ga-headlines'> tag in the html page.
    article_news = soup.find_all('div', class_='ga-headlines')

    data = article_news[0].get_text()

    stop_words = set(stopwords.words('english')) 
    ps = PorterStemmer()

    # Tokenizing the text
    word_tokens = word_tokenize(data)

    filtered_sentence = []  

    # Removing stop words
    for w in word_tokens:  
        if w.lower() not in stop_words:  
            filtered_sentence.append(w)  

    stemed_words = []

    # Stemming words
    for w in filtered_sentence:
        stemed_words.append(ps.stem(w))

    # Speech Tagging
    speechTagged = nltk.pos_tag(stemed_words)

    return(speechTagged)

def compareTwoArticle(_urlLink1, _urlLink2):
    # INPUT: url's of 2 articles
    # OUTPUT: boolean True is both have 80% similar words, else False

    dataOfURL1 = subjectOfArticle(_urlLink1)
    dataOfURL2 = subjectOfArticle(_urlLink2)

    similarWordsCount = 0

    averageWords = (len(dataOfURL1)+len(dataOfURL2))/2

    for taggedSpeech in dataOfURL1:
        if taggedSpeech in dataOfURL2:
            similarWordsCount += 1
    
    if similarWordsCount >= (0.8 * averageWords):
        return True

    return False

def main():
    # ---MAIN FUNCTION---

    urlLink1 = input("Enter the first URL :")
    urlLink2 = input("Enter the second URL :")

    print("\n\n")

    if (compareTwoArticle(urlLink1, urlLink2)):
        print("Both are similar articles !")
    else:
        print("Both are different articles !")


if __name__ == "__main__":
    main()