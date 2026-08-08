import numpy as np
import pandas  as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix,precision_score,recall_score,f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("loan_approval_data.csv")
categorical_cols = df.select_dtypes(include=["object"]).columns
numerical_cols = df.select_dtypes(include=["number"]).columns

col_cat = SimpleImputer(strategy="mean")
col_num = SimpleImputer(strategy="most_frequent")
df[numerical_cols] = col_cat.fit_transform(df[numerical_cols])
df[categorical_cols] = col_num.fit_transform(df[categorical_cols])

# print(df.isnull().sum())
# print(df.head())

## Using EDA

plot = df['Gender'].value_counts()
ax = sns.barplot(x=plot.index, y=plot.values)
# plt.show()

## Feature Engineering

le = LabelEncoder()

df["Education_Level"] = le.fit_transform(df['Education_Level'])
df['Loan_Approved'] = le.fit_transform(df['Loan_Approved'])

cols = ["Employment_Status","Marital_Status",'Loan_Purpose','Property_Area','Gender','Employer_Category']
ohe = OneHotEncoder(drop="first", sparse_output=False , handle_unknown ='ignore')
encoded = ohe.fit_transform(df[cols])
# print(encoded)

encoded_df = pd.DataFrame(
                        encoded, 
                        columns= ohe.get_feature_names_out(cols),
                        index=df.index
                        )
# print(encoded_df.head())
df =pd.concat([df.drop(columns=cols),encoded_df],axis=1)

## Feature Scaling

X = df.drop(columns=["Applicant_ID","Loan_Approved"])
y = df['Loan_Approved']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)


scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled,y_train)
y_predict = model.predict(X_test_scaled)

print(f'Accuracy score For LogisticRegression:',accuracy_score(y_test, y_predict))
print(f'Precision Score For LogisticRegression:',precision_score(y_test, y_predict))


k = KNeighborsClassifier(n_neighbors=3)
k.fit(X_train,y_train)
y_predict = k.predict(X_test)
knn_accuracy = accuracy_score(y_test,y_predict)
print("Accuracy Score For KNN:", knn_accuracy)
print(f'Precision Score For KNN:',precision_score(y_test, y_predict))


nb = GaussianNB()
nb.fit(X_train,y_train)
y_pre = nb.predict(X_test)
naive_accuracy = accuracy_score(y_test,y_pre)
print("Accuracy Score For Naive :", naive_accuracy)
print(f'Precision Score For Naive',precision_score(y_test, y_predict))



