from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import string
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import re

trainFile = open("testFood.dat", "r").read().splitlines()
trainTweets = []
trainClasses = []
for tweet in trainFile:

    tweet = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                           " ", tweet)
    trainTweets.append(tweet.split("\t")[1].lower().translate(None, string.punctuation))
    trainClasses.append(int(tweet.split("\t")[0]))


vectorizer = TfidfVectorizer(ngram_range=(1,2))
train_matrix = vectorizer.fit_transform(trainTweets)

models = [LogisticRegression(), BernoulliNB(), SVC(class_weight='balanced'), KNeighborsClassifier(), DecisionTreeClassifier()]

for model in models:

    model.fit(train_matrix, trainClasses)
    testTweet = ["Thank you for the food poisoning Jack in the Box My sourdough jack betrayed me"]
    test_matrix = vectorizer.transform(testTweet)
    predicted = model.predict(test_matrix)
    print predicted

