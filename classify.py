import csv
import datetime
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

import multiprocessing as mp

def mySvm(training, training_labels, testing, testing_labels):
    #Support Vector Machine
    start = datetime.datetime.now()
    clf = svm.SVC()
    clf.fit(training, training_labels)
    print "+++++++++ Finishing training the SVM classifier ++++++++++++"
    result = clf.predict(testing)

    print "SVM accuracy:", accuracy_score(testing_labels, result)
    #keep the time
    finish = datetime.datetime.now()
    print (finish-start).seconds

def myTree(training, training_labels, testing, testing_labels):
    #Decision Tree
    start = datetime.datetime.now()
    clf = DecisionTreeClassifier(random_state=0)
    result = clf.fit(training, training_labels).predict(testing)
    print "+++++++++ Finishing training the Decision Tree classifier ++++++++++++"
    print "Decision Tree accuracy:", accuracy_score(testing_labels, result)

    #keep the time
    finish = datetime.datetime.now()
    print (finish-start).seconds

def produceTrainingSet(mid, end, path):
    training, testing = [], []
    for i in xrange(mid):
        f = open(path+"result/features"+str(i)+".csv", 'rb')
        reader = csv.reader(f)
        reader.next()
        training.extend(list(reader))
        f.close()

    print "+++++++++ Finishing reading training set +++++++++++"

    for i in xrange(mid,end):
        f = open(path+"result/features"+str(i)+".csv", 'rb')
        reader = csv.reader(f)
        reader.next()
        testing.extend(list(reader))
        f.close()

    print "+++++++++ Finishing reading testing set ++++++++++++"

    train = open(path+"result/training.csv", 'wb')
    test = open(path+"result/testing.csv", 'wb')

    features = ["cn","aa","ra","jc","pa","delta_cn", "delta_aa", "delta_ra", "delta_jc", "delta_pa", "postive"]
    wr = csv.writer(train, delimiter=',', quoting=csv.QUOTE_ALL)
    wr.writerow(features)
    print len(training), len(testing)
    for i in training:
        wr.writerow(i)

    wr1 = csv.writer(test, delimiter=',', quoting=csv.QUOTE_ALL)
    wr1.writerow(features)
    for i in testing:
        wr1.writerow(i)

    train.close(); test.close()
if __name__ == "__main__":
    path = "data/gap30/"
    mid, end = 30, 56
    produceTrainingSet(mid, end, path)

    path = "data/gap90/"
    mid, end = 9, 18
    produceTrainingSet(mid, end, path)

    path = "data/gap180/"
    mid, end = 5, 9
    produceTrainingSet(mid, end, path)

    path = "data/gap300/"
    mid, end = 3, 5
    produceTrainingSet(mid, end, path)

    '''
    training_labels = [i.pop() for i in training]
    testing_labels = [i.pop() for i in testing]

    p1 = mp.Process(target=mySvm, args=(training, training_labels, testing, testing_labels))
    p2 = mp.Process(target=myTree, args=(training, training_labels, testing, testing_labels))
    p1.start()
    p2.start()'''
