from nltk import download, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

import re
import string

import pickle


content_moderation_folder = 'C:/Users/witko/TwitterTwo/TwitterTwo/ContentModeration'


def clean(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub(r"\@w+|\#",'',text)
    text = re.sub(r"[^\w\s]",'',text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    tweet_tokens = word_tokenize(text)
    filtered_tweets=[w for w in tweet_tokens if not w in set(stopwords.words('english'))] #removing stopwords
    return ' '.join(filtered_tweets)



def lemmatizing(tweet):
    download('wordnet')
    lemmatizer=WordNetLemmatizer()
    words = tweet.split()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    lemmatized_tweet = ' '.join(lemmatized_words)
    return lemmatized_tweet


def moderator(X: str) -> str:
    X = [X]
    X = [clean(x) for x in X]
    X = [lemmatizing(x) for x in X]

    with open(f'{content_moderation_folder}/models/tfidf_vectorizer.pkl', 'rb') as file:
        vect = pickle.load(file)   

        X = vect.transform(X) 
    
    with open(f'{content_moderation_folder}/models/logreg_model.pkl', 'rb') as file:
        logreg = pickle.load(file)

        X = logreg.predict(X)

        return X[0]
        
print(moderator('Hate'))



        

