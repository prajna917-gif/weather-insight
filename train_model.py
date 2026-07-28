import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# 1. Load data
df = pd.read_csv("data/weatherAUS.csv")

# 2. Keep only the columns we need
columns_needed = ["Humidity9am", "Humidity3pm", "Pressure9am", "Pressure3pm",
                   "Temp9am", "Temp3pm", "WindSpeed9am", "WindSpeed3pm", "RainTomorrow"]
df = df[columns_needed]

# 3. Remove rows with missing data
df = df.dropna()

# 4. Convert Yes/No to 1/0
df["RainTomorrow"] = df["RainTomorrow"].map({"Yes": 1, "No": 0})

# 5. Split into features (X) and target (y)
X = df.drop("RainTomorrow", axis=1)
y = df["RainTomorrow"]

# 6. Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 7. Train the model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 8. Check accuracy
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# 9. Save the trained model to a file
joblib.dump(model, "rain_model.pkl")
print("Model saved as rain_model.pkl")