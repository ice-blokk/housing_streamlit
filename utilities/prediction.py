import joblib
def predict(data):
    clf = joblib.load('housing_predictor.sav')
    return clf.predict(data)