from src.data_loader import load_data, encode_labels
from src.features import create_features
from src.model import train_model, save_model

df = load_data("data/spam.csv")
df = encode_labels(df)
df = create_features(df)

model = train_model(df)

save_model(model, "models/model.pkl")

print("Model saved successfully!")