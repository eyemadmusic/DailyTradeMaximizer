import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class MLPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()

    def prepare_features(self, data):
        features = data[['Open', 'High', 'Low', 'Close', 'Volume', 'EMA9', 'EMA21', 'RSI', 'MACD', 'ATR']].values
        return self.scaler.fit_transform(features)

    def prepare_target(self, data):
        return data['Close'].shift(-1).values[:-1]  # Predict next day's close price

    def train(self, data):
        X = self.prepare_features(data)[:-1]  # Remove last row as we don't have target for it
        y = self.prepare_target(data)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        print(f"Model trained. Train R2: {train_score:.4f}, Test R2: {test_score:.4f}")

    def predict(self, data):
        X = self.prepare_features(data)
        return self.model.predict(X)

def add_ml_predictions(data):
    predictor = MLPredictor()
    predictor.train(data)
    predictions = predictor.predict(data)
    data = data.copy()  # Create a copy to avoid SettingWithCopyWarning
    data['ML_Prediction'] = np.nan
    data.loc[data.index[:-1], 'ML_Prediction'] = predictions[:-1]  # Use .loc to avoid SettingWithCopyWarning
    return data
