import sys
import os
import logging
from joblib import dump
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import lightgbm as lgb
from scipy.stats import pearsonr
import mlflow
import mlflow.sklearn


# Specify the tracking URI for the MLflow server.
mlflow.set_tracking_uri("http://localhost:5000")
print("TRACKING URI:", mlflow.get_tracking_uri())
# Specify the experiment you just created for your LLM application or AI agent.
#mlflow.set_experiment("My Application")

# Enable automatic tracing for all OpenAI API calls.
#mlflow.openai.autolog()

#client = OpenAI()
# The trace of the following is sent to the MLflow server.
#client.chat.completions.create(
#    model="o4-mini",
#    messages=[
#        {"role": "system", "content": "You are a helpful weather assistant."},
#        {"role": "user", "content": "What's the weather like in Seattle?"},
#    ],
#)

df_cond = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-03-03/tortoise_body_condition_cleaned.csv')
df_cl = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-03-03/clutch_size_cleaned.csv')
df_cond['individual'] = df_cond['individual'].astype(str)
df_cl['individual'] = df_cl['individual'].astype(str)

df_cl['year'] = pd.to_datetime(df_cl['date']).dt.year

df_agg = df_cond.groupby(['individual']).agg({
    'body_mass_grams': 'mean',
    'season': lambda x: x.mode()[0] if not x.mode().empty else np.nan, 
    'locality': lambda x: x.mode()[0] if not x.mode().empty else np.nan,
    'body_condition_index': 'mean',
    'straight_carapace_length_mm': 'mean',
    'sex': 'first' 
}).reset_index()

df = df_cl.merge(df_agg, on=['individual'], how='inner')
cols = ['season', 'sex', 'locality']
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')

encoded_array = encoder.fit_transform(df[['season', 'sex', 'locality_x', 'locality_y']])
kega = pd.DataFrame(
    encoded_array,
    columns=encoder.get_feature_names_out(['season', 'sex', 'locality_x', 'locality_y']),
    index=df.index
)


df = df.drop(columns=['season', 'sex', 'locality_x', 'locality_y', 'date']).join(kega)

X = df.drop(['eggs', 'individual'], axis = 1)
y = df['eggs']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15,random_state=67)

mlflow.set_experiment("turtle")

with mlflow.start_run(run_name="linearregression"):
    mlflow.log_param("model_type", "LinearRegression")
    params = {"tol": 2.5e-06}
    mlflow.log_params(params)
    model = LinearRegression(**params)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    corr, pval = pearsonr(y_test, y_pred)
    mlflow.log_metric("MSE", mse)
    mlflow.log_metric("Pearson Correlation coeff", corr)
    mlflow.log_metric("Pearson Correlation p-val", pval)
    mlflow.sklearn.log_model(model, "model")

with mlflow.start_run(run_name="lgbmregressor"):
    mlflow.log_param("model_type", "LGBMRegressor")
    params = {"n_estimators": 67,  "max_depth": 2, "learning_rate": 0.05, "min_child_samples": 2, "colsample_bytree": 0.8}
    mlflow.log_params(params)
    boosting = lgb.LGBMRegressor(**params)
    boosting.fit(X_train, y_train)
    y_pred = boosting.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    corr, pval = pearsonr(y_test, y_pred)
    mlflow.log_metric("Pearson Correlation coeff", corr)
    mlflow.log_metric("Pearson Correlation p-val", pval)
    mlflow.log_metric("MSE", mse)

    mlflow.sklearn.log_model(model, "model")
