import argparse
import pickle
import pandas as pd
from azureml.logging import get_azureml_logger
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import precision_recall_curve
from sklearn.pipeline import Pipeline

# initialize the logger
logger = get_azureml_logger()
vect = CountVectorizer()

def read_reviews_from_csv(dataset):
    
    df = pd.read_csv(dataset, encoding="utf8", sep=",")
    return df

def train_model(dataset):
    df = read_reviews_from_csv(dataset)
    X_train = df.Text
    X_train.shape
    y_train = df.Label
    y_train.shape

    pipe1 = Pipeline([('vect', CountVectorizer(stop_words='english')),
                      ('nb', MultinomialNB())
    ])

    model = pipe1.fit(X_train, y_train)

    return model

def predict_review(model, test_dataset): 
    test = read_reviews_from_csv(test_dataset)
    X_test = test.Text
    X_test.shape
    y_test = test.Label
    y_test.shape
    
    y_pred_class = model.predict(X_test)

    # evaluate the test set
    accuracy = model.score(X_test, y_test)
    print("Accuracy is {}".format(accuracy))

    # log accuracy which is a single numerical value
    logger.log("Accuracy", accuracy)

    return y_pred_class

dataset = "./data/preprocessed-data.csv"
dataset_test = "./data/preprocessed-test.csv"

model = train_model(dataset)
prediction = predict_review(model, dataset_test)

print("")
print("==========================================")
print("Serialize and deserialize using the outputs folder.")
print("")

# serialize the model on disk in the special 'outputs' folder
print ("Export the model to model.pkl")
f = open('./outputs/model.pkl', 'wb')
pickle.dump(model, f)
f.close()