import tweepy  
import numpy as np 
import pandas as pd 
import pickle  
import time
import matplotlib.pyplot as plt
from tweepy.streaming import Stream  
from sklearn.feature_extraction.text import CountVectorizer

from DatasetProcessing import * 


consumerKey = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"   

consumer_secretKey = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"   

accessToken = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  

access_secretToken = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"   


def authorizeAccount(): #Function to authorize twiiter api 
    try:
        authorization = tweepy.OAuthHandler(consumerKey,consumer_secretKey) 
        authorization.set_access_token(accessToken,access_secretToken)  
        api=tweepy.API(authorization)  

        print("Connected to twitter successfully!") 
        return api 

    except:  
        print("Error Try Again")  
 

#StreamListener class to stream tweets
class StreamListener(tweepy.StreamListener):   

    def __init__(self): 
        self.tweet_cnt=50  
        self.start_time=time.time()
        self.tweet=[]
        super(StreamListener,self).__init__(api=api)

    def on_status(self, status):   

        try:   
            if(time.time()-self.start_time>60): 
                return False  
           
            if(hasattr(status, 'retweeted_status') and status.retweeted_status): 
                return True    
            self.tweet.append(status.text) 
            return True  

        except:  
            print("Error Occured")
            return False

    def on_error(self, status_code):
        if status_code == 420:
            return False 
    
    def GetTweet(self): 
        return self.tweet 



#Functions for vectorizing tweets
def VectorizeTweets(Tweets):   
    
    #Loading CountVectorizer using pickle 
    buffer=open("model/vectorizer.sav",'rb')   
    vectorizer=pickle.load(buffer)  
    buffer.close()    

    vectorized_tweets=[]

    for tweet in Tweets:
        vectorized_sentence = vectorizer.transform([tweet]).toarray() 
        vectorized_tweets.append(vectorized_sentence) 
    
    return vectorized_tweets



#Model for predicting tweets
def Predict(vector_tweets):    

    #Loading Model using pickle 
    buffer=open("model/Model.sav",'rb')    
    Model=pickle.load(buffer)  
    buffer.close()    

    predicted=[]

    for vectors in vector_tweets: 
        predicted.append(Model.predict(vectors))  
    
    return predicted
 
# Calculating number of possitive and negative tweets 

def stats(prediction):  

    pos=0 
    neg=0 

    for data in prediction: 
        if(data==0): 
            neg=neg+1 
        else: 
            pos=pos+1 
    
    return (pos,neg)


#Authorize account 
api=authorizeAccount()   


#Streaming Tweets based on 
stream_listener = StreamListener() 

print("Fetching Tweets....")
stream = tweepy.Stream(auth=api.auth, listener=stream_listener) 

stream.filter(languages=["en"],track=["Covid-19"])  


# Getting all streamed tweets   
tweets=stream_listener.GetTweet()  
print("Total number of tweets fetched: ",(len(tweets)))


#Cleaning Tweets from Preprocessing functions
cleanTweets=[]   
for tweet in tweets: 
    cleanTweets.append(Preprocessing(tweet))   



vectorized_tweets=VectorizeTweets(cleanTweets)  

prediction=Predict(vectorized_tweets)  

pos,neg=stats(prediction)




# Writing output in  file   

output = open("Data/twitter_out.txt","w",encoding="UTF-8") 
output.write("Total number of tweets fetched: ") 
output.write(str(len(tweets)))  
output.write("\n")
output.write("Total Possitive tweets: ") 
output.write(str(pos)) 
output.write("\n")  
output.write("Total Negative tweets: ") 
output.write(str(neg)) 
output.write("\n")  
output.write("Possitive Tweets % :") 
output.write(str((pos/(pos+neg))*100))  
output.write('\n')
output.write("Negative Tweets % :") 
output.write(str((neg/(pos+neg))*100)) 
output.write("\n\n")


for i in range(len(tweets)):  
    output.write(tweets[i])
    output.write(",\t")
    output.write('pos' if prediction[i]==1 else 'neg')
    output.write('\n') 

output.close()
    