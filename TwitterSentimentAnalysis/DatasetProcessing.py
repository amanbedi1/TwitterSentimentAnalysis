#Importing for DataManipulation
import re 
import string
import pandas as pd
import numpy as np  

#Importing Dependencies for NLP 
from nltk.corpus import stopwords 
from nltk.corpus import twitter_samples 
from nltk.stem import PorterStemmer 
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer    


# Preprocessing Tweet: 

    # 1:Casing (Converting all letters to lowercase)  

    # 2:Noise Removal (Removing Punctuators,Urls,Mentions,Hashtag etc)  

    # 3:Tokenization  

    # 4:Removing Stopwords 

    # 5:Normalisation(Stemming,Lemmitization)  



#Tokenisation-Converting words,emojis from tweet into list of words   
def Tokenize(text):   

    tk=TweetTokenizer() 
    tokenize_tweet=tk.tokenize(text)   
    return tokenize_tweet   
 
 

#Removing Punctuator(.,;:)
def RemovePunctuators(tweet):  

    cleanTweets=[]  
    
    for word in tweet: 
        if(word not in string.punctuation): 
            cleanTweets.append(word) 
    
    return cleanTweets 



# Removing common words like (I, am, you,are,is,to)
def RemoveStopwords(tweet,stopWords):  
    
    cleanTweets=[] 
    for word in tweet: 
        if(word not in stopWords): 
            cleanTweets.append(word) 
    
    return cleanTweets   


#Stemming 
def Stemming(tweet):  

    stemmer=PorterStemmer() 
    stemTweets=[] 
    
    for word in tweet: 
        stemTweets.append(stemmer.stem(word)) 
        
    return stemTweets


#Lemmitizing
def Lemmitizing(tweet): 
    
    lemmatizer = WordNetLemmatizer()  
    lemmTweets=[] 
    
    for word in tweet: 
        lemmTweets.append(lemmatizer.lemmatize(word)) 
        
    return lemmTweets  



def Preprocessing(tweet): 
    
    #Convert tweet into Lowercase 
    text=tweet.lower()   

    
    #Removing old style retweet tweet RT 
    tweet=re.sub(r'^RT[\s]+', '', tweet) 

    
    #Removing all urls from tweet 
    tweet=re.sub(r'https?:\/\/.*[\r\n]*', '', tweet) 

    
    #Removing all @mentions and Hashtag(#) from tweet
    tweet=re.sub(r'\@\w+|\#','',tweet) 

    
    #Removing all Single Numeric terms from tweet 
    tweet=re.sub(r'[0-9]','',tweet)   

    
    #Tokenizing Tweet 
    tokenizeTweet=Tokenize(tweet)  

    
    #Removing Punctuators(./?!)
    filteredTweet=RemovePunctuators(tokenizeTweet)  

    
    #Removing Stopwords  
    stopWords=set(stopwords.words('english')) 
    cleanTweet=RemoveStopwords(filteredTweet,stopWords)  

    
    #lemmitizing  
    lemmTweet=Lemmitizing(cleanTweet) 

    
    return " ".join(lemmTweet) 

