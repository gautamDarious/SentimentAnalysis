import nltk
import random
from nltk.classify import NaiveBayesClassifier,accuracy#NaiveBayesClassifier is a class in a pyhton file within classify folder within nltk package
from nltk.corpus import movie_reviews#movie_reviews is a method in a pyhton file within corpus folder within nltk package
from nltk.tokenize import word_tokenize#word_tokenize is a method in a pyhton file within tokenize folder within nltk package
from nltk.corpus import stopwords#stopwprds is a method in a pyhton file within corpus folder within nltk package
from tweepy import OAuthHandler,API,Stream,StreamListener
consumer_key="IxVKj7ridqKJbSo0zxpIvWL8j"
consumer_secret="lWQUUGL3nAJvSifxbSSE1drXSu2HdeUJriZMiI4QYRwipZSmsB"
access_token="974164217744982017-470JVsCnEXtfREwTnbgbCgHkapxO0y6"
access_tokensecret="e4JbcZPkWShkkBOmdkUhQtMkydvXOl6uXdHt2bye0o8P4"
auth1=OAuthHandler(consumer_key,consumer_secret)
auth1.set_access_token(access_token,access_tokensecret)
stop_words=set(stopwords.words("english"))
#print(len(movie_reviews.fileids()))
def create_word_features(words):
    useful_words = []
    for w in words:
        if w not in stop_words:
            useful_words.append(w)
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict
neg_reviews = []
for file in movie_reviews.fileids("neg"):
    resu = movie_reviews.words(file)
    neg_reviews.append((create_word_features(resu), "negative"))
neg_reviews.append(({"arrogant":True,"coward":True,"insensitive":True},"negative"))
neg_reviews.append(({"arrogant":True},"negative"))
neg_reviews.append(({"arrogant":True},"negative"))
neg_reviews.append(({"arrogant":True},"negative"))
neg_reviews.append(({"arrogant":True},"negative"))
neg_reviews.append(({"threatens":True},"negative"))
neg_reviews.append(({"threatens":True},"negative"))
neg_reviews.append(({"arrogant":True},"negative"))
print(neg_reviews)
pos_reviews = []
for file in movie_reviews.fileids("pos"):
    resu = movie_reviews.words(file)
    pos_reviews.append((create_word_features(resu), "positive"))
print(pos_reviews)
train_set = neg_reviews[500:] + pos_reviews[500:]
random.shuffle(train_set)
test_set =  neg_reviews[:500] + pos_reviews[:500]
classifier = NaiveBayesClassifier.train(train_set)
accuracy = accuracy(classifier, test_set)
print(accuracy * 100)
class MyStreamListener(StreamListener):
    def on_status(self, status):
        str=status.text
        sen1 = word_tokenize(str)
        sen2 = create_word_features(sen1)
        y=classifier.classify(sen2)
        saveFile=open('twitterData.csv','a')
        saveFile.write(y)
        saveFile.write('\n')
        saveFile.close()
        print(str,y)
        return True
    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False
myStreamListener1=MyStreamListener()
twitterStream = Stream(auth1, listener=myStreamListener1)
twitterStream.filter(track=["BJP"])