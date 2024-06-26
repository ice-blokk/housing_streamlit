import joblib
import pandas as pd
import sklearn

model = joblib.load("housing_predictor.sav")

file_path = "ActiveListingsAsOfJun24_model.csv"
df = pd.read_csv(file_path)

df = df.dropna(subset=['Postal Code', '# Beds', '# Baths', 'Rent', 'Payment Standard (PS)', 'Ratio']) # drop NaN values
df = df.astype(str) # Convert all columns to object type (if necessary)

predicted_probabilities = model.predict_proba(df)

probability_housed = predicted_probabilities[:, 1]  # Probability of being housed (class 1) for all entries

df['Probability'] = probability_housed # Add the 'Probability' column to the DataFrame

output_file_path = "ActiveListingsAsOfJun24_with_probability.csv"
df.to_csv(output_file_path, index=False)

print(f"Updated CSV with probabilities saved to: {output_file_path}")

for i, prob in enumerate(predicted_probabilities):
    probability_housed = prob[1]  # Probability of being housed (class 1)
    print(f"\nProbability of being housed for entry {i+1}: {probability_housed:.2f}")