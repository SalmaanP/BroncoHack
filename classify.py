from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import string
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import re

trainFile = open("finalTrain.dat", "r").read().splitlines()
trainTweets = []
trainClasses = []
zero = 0
one = 0
for tweet in trainFile:

    tweet = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                           " ", tweet)
    trainTweets.append(tweet.split("\t")[1].lower().translate(None, string.punctuation))
    if int(tweet.split("\t")[0]) == 0:
        zero += 1
    else:
        one += 1
    trainClasses.append(int(tweet.split("\t")[0]))

vectorizer = TfidfVectorizer(ngram_range=(1,2))
train_matrix = vectorizer.fit_transform(trainTweets)

#models = [LogisticRegression(), BernoulliNB(), SVC(), KNeighborsClassifier(), DecisionTreeClassifier()]
models = [LogisticRegression()]

for model in models:

    model.fit(train_matrix, trainClasses)
    testTweet = ["I got food poisoning"]
    test_matrix = vectorizer.transform(testTweet)
    predicted = model.predict(test_matrix)
    print predicted

