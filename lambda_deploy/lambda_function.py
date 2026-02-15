import pickle
import json

# Load models
with open("anomaly_model.pkl", "rb") as f:
    anomaly_model = pickle.load(f)

with open("trained_model.pkl", "rb") as f:
    predictive_model = pickle.load(f)

with open("log_clustering_model.pkl", "rb") as f:
    clustering_model = pickle.load(f)

with open("tfidf_vectorizer.pkl", "rb") as f:
    tfidf_vectorizer = pickle.load(f)


def handler(event, context):
    # Example: Anomaly Detection
    if event.get("type") == "anomaly_detection":
        data = event.get("data", [])
        predictions = anomaly_model.predict(data)
        return {"predictions": predictions.tolist()}

    # Example: Predictive Maintenance
    elif event.get("type") == "predictive_maintenance":
        features = event.get("features", [])
        prediction = predictive_model.predict([features])
        return {"maintenance_prediction": prediction.tolist()}

    # Example: Log Clustering
    elif event.get("type") == "log_clustering":
        logs = event.get("logs", [])
        transformed_logs = tfidf_vectorizer.transform(logs)
        clusters = clustering_model.predict(transformed_logs)
        return {"log_clusters": clusters.tolist()}

    return {"error": "Invalid event type"}