import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

path = r'Backend/yield_prediction.xlsx'
data = pd.read_excel(path)
data = data.dropna()
data['Yield'] = data['Production'] / data['Area']
working = data.drop(columns=['State_Name'])
dummy = pd.get_dummies(working)
X = dummy.drop(columns=['Crop_Year','Production','Yield'])
y = dummy['Production']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
results = {}
lin = LinearRegression()
lin.fit(X_train, y_train)
lin_pred = lin.predict(X_test)
results['Linear Regression R2'] = r2_score(y_test, lin_pred)
rf = RandomForestRegressor(n_estimators=11, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
results['Random Forest R2'] = r2_score(y_test, rf_pred)
dt = DecisionTreeRegressor(random_state=5)
dt.fit(X_train, y_train)
dt_pred = dt.predict(X_test)
results['Decision Tree R2'] = r2_score(y_test, dt_pred)
svr = SVR(kernel='rbf')
svr.fit(X_train_scaled, y_train)
svr_pred = svr.predict(X_test_scaled)
results['SVR R2'] = r2_score(y_test, svr_pred)
for k,v in results.items():
    print(f"{k}: {v:.4f}")
