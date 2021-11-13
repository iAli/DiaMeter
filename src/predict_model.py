import pandas as pd
import joblib


std_model = joblib.load('../data/std_model.pkl')
vc_model = joblib.load('../data/vc_model.pkl')


def model_prediction(pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age):

    new_df = pd.DataFrame([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age]])

    new_df_scaled = std_model.transform(new_df)

    prediction = vc_model.predict(new_df_scaled)

    return prediction
