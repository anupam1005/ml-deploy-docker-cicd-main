import pickle
import logging
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def train_model():
    logger.info("Loading Iris dataset...")
    X, y = load_iris(return_X_y=True)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    logger.info("Initializing Logistic Regression model...")
    model = LogisticRegression(max_iter=200)
    
    logger.info("Training model...")
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    logger.info(f"Model trained successfully. Accuracy: {accuracy:.4f}")
    
    logger.info("Saving model to model.pkl...")
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    logger.info("Training process completed.")

if __name__ == "__main__":
    train_model()

