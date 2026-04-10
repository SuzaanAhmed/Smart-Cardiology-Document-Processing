from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd

def fetch_csv_data():
    data=pd.read_csv("synthetic_data.csv")
    # print(data.head(5))

    X = data[["HEARTRATE", "PR_INTERVAL", "ST_ELEVATION", "RHYTHM_TYPE", "RISK_SCORE"]]
    Y = data["LABEL"]
    return X,Y

def data_preprocessing(X,Y):
    x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.25,random_state=29,shuffle=True)

    """
    print(x_train)
    print(y_train)
    """

    label_encoding=LabelEncoder()
    y_train_encoded=label_encoding.fit_transform(y_train)
    y_test_encoded=label_encoding.transform(y_test)

    #print(y_test_encoded)
    return x_train,x_test,y_train_encoded,y_test_encoded,label_encoding

def model_training_saving(x_train,x_test,y_train,y_test,encoder):
    classification=GradientBoostingClassifier(
        n_estimators=100,learning_rate=.1,max_depth=1,random_state=22).fit(x_train, y_train)
    print(classification.score(x_test,y_test))

    x_pred=classification.predict(x_test)
    print(accuracy_score(y_test,x_pred))

    joblib.dump(classification, 'cardio_decision_model.pkl')

    joblib.dump(encoder, 'label_encoder.pkl')

if __name__=="__main__":
    X,Y=fetch_csv_data()

    x_train,x_test,y_train,y_test,encoder=data_preprocessing(X,Y)

    model_training_saving(x_train,x_test,y_train,y_test,encoder)