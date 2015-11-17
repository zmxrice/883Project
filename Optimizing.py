__author__ = 'easycui'
from sklearn import linear_model

def optimizing(data,target):
    clf=linear_model.LinearRegression()
    clf.fit(data,target)
    return clf.coef_