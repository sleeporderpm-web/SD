from typing import Dict, Tuple, List
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import json
from pathlib import Path


# Global models and scaler (trained on app startup)
_models = {}
_scaler = StandardScaler()
_feature_names = ['age', 'stress_level', 'systolic_bp', 'heart_rate', 'sleep_duration', 
                  'bmi_numeric', 'snoring_frequency', 'working_hours', 'sleep_quality', 
                  'caffeine_intake', 'exercise_frequency', 'body_temperature']

def _create_training_data():
    """Create synthetic training data for ML models."""
    X = []
    y = []
    
    # Normal sleep patterns (class 0)
    for _ in range(30):
        X.append([np.random.randint(20, 65), np.random.randint(0, 5), 
                  np.random.randint(110, 130), np.random.randint(60, 80),
                  np.random.uniform(7, 9), np.random.uniform(18.5, 24.9),
                  np.random.randint(0, 2), np.random.randint(6, 9),
                  np.random.randint(8, 10), np.random.randint(0, 2),
                  np.random.randint(4, 7), np.random.uniform(36.5, 37.2)])
        y.append(0)
    
    # Moderate sleep issues (class 1)
    for _ in range(25):
        X.append([np.random.randint(30, 60), np.random.randint(5, 8),
                  np.random.randint(130, 150), np.random.randint(80, 95),
                  np.random.uniform(5, 7), np.random.uniform(25, 29.9),
                  np.random.randint(3, 6), np.random.randint(8, 11),
                  np.random.randint(5, 8), np.random.randint(2, 4),
                  np.random.randint(2, 4), np.random.uniform(37.2, 37.5)])
        y.append(1)
    
    # Severe sleep disorders (class 2)
    for _ in range(25):
        X.append([np.random.randint(35, 70), np.random.randint(8, 10),
                  np.random.randint(150, 170), np.random.randint(95, 110),
                  np.random.uniform(3, 5), np.random.uniform(30, 35),
                  np.random.randint(6, 10), np.random.randint(10, 13),
                  np.random.randint(2, 5), np.random.randint(4, 10),
                  np.random.randint(0, 2), np.random.uniform(37.5, 38.5)])
        y.append(2)
    
    return np.array(X), np.array(y)


def _train_models():
    """Train KNN, SVM, and Random Forest models."""
    global _models, _scaler
    
    X, y = _create_training_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    X_train_scaled = _scaler.fit_transform(X_train)
    X_test_scaled = _scaler.transform(X_test)
    
    # KNN Classifier
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train_scaled, y_train)
    knn_accuracy = knn.score(X_test_scaled, y_test)
    
    # SVM Classifier
    svm = SVC(kernel='rbf', probability=True, random_state=42)
    svm.fit(X_train_scaled, y_train)
    svm_accuracy = svm.score(X_test_scaled, y_test)
    
    # Random Forest Classifier
    rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    rf.fit(X_train_scaled, y_train)
    rf_accuracy = rf.score(X_test_scaled, y_test)
    
    _models = {
        'knn': {'model': knn, 'accuracy': knn_accuracy, 'name': 'K-Nearest Neighbors'},
        'svm': {'model': svm, 'accuracy': svm_accuracy, 'name': 'Support Vector Machine'},
        'rf': {'model': rf, 'accuracy': rf_accuracy, 'name': 'Random Forest'}
    }


def _extract_features(inputs: Dict) -> List[float]:
    """Extract and normalize features from input data."""
    bmi_map = {"underweight": 20, "normal": 23, "overweight": 27, "obese": 32}
    bmi_numeric = bmi_map.get(str(inputs.get("bmi_category", "normal")).lower(), 23)
    
    features = [
        float(inputs.get("age", 0)),
        float(inputs.get("stress", 0)),
        float(inputs.get("blood_pressure", 120)),
        float(inputs.get("heart_rate", 75)),
        float(inputs.get("sleep_duration", 7)),
        bmi_numeric,
        float(inputs.get("snoring_frequency", 0)),
        float(inputs.get("working_hours", 8)),
        float(inputs.get("sleep_quality", 5)),
        float(inputs.get("caffeine_intake", 2)),
        float(inputs.get("exercise_frequency", 3)),
        float(inputs.get("body_temperature", 37.0))
    ]
    return features


def classify(inputs: Dict) -> Tuple[str, int, Dict]:
    """
    Classify sleep disorder using ensemble of three ML models.
    
    Returns:
        Tuple of (diagnosis, severity_level, detailed_results)
        - diagnosis: Diagnosis string
        - severity_level: 0-3 (Normal to High Risk)
        - detailed_results: Dict with model predictions and confidence
    """
    # Train models if not already done
    if not _models:
        _train_models()
    
    # Extract and scale features
    features = _extract_features(inputs)
    X_scaled = _scaler.transform([features])
    
    # Get predictions from all models
    predictions = {}
    confidences = {}
    
    for model_key in ['knn', 'svm', 'rf']:
        model_obj = _models[model_key]['model']
        pred = model_obj.predict(X_scaled)[0]
        predictions[model_key] = int(pred)
        
        # Get confidence (probability)
        if hasattr(model_obj, 'predict_proba'):
            probs = model_obj.predict_proba(X_scaled)[0]
            confidences[model_key] = float(max(probs)) * 100
        else:
            confidences[model_key] = 85.0  # Default for KNN
    
    # Ensure we have model details
    for model_key in ['knn', 'svm', 'rf']:
        if model_key not in _models:
            _train_models()
            break
    
    # Find best model (highest accuracy on training set)
    best_model_key = max(_models.keys(), key=lambda k: _models[k]['accuracy'])
    best_prediction = predictions[best_model_key]
    best_confidence = confidences[best_model_key]
    
    # Map prediction to diagnosis
    severity_map = {
        0: ("Normal Sleep Pattern", 0, "Your sleep metrics indicate a normal, healthy sleep pattern. Continue current sleep habits."),
        1: ("Moderate Sleep Issues - Review Recommended", 1, "Your sleep shows some concerning patterns. Consider lifestyle adjustments and consult a healthcare provider."),
        2: ("High Risk Sleep Disorder Detected", 2, "Significant sleep disorder indicators detected. Medical evaluation strongly recommended.")
    }
    
    diagnosis, severity, recommendation = severity_map.get(best_prediction, ("Needs Review", 1, "Please consult a healthcare provider."))
    
    # Build detailed results
    detailed_results = {
        'best_model': best_model_key,
        'best_model_name': _models[best_model_key]['name'],
        'best_model_accuracy': float(_models[best_model_key]['accuracy']) * 100,
        'best_confidence': best_confidence,
        'all_predictions': predictions,
        'all_confidences': confidences,
        'all_model_accuracies': {k: float(v['accuracy']) * 100 for k, v in _models.items()},
        'model_names': {k: v['name'] for k, v in _models.items()},
        'recommendation': recommendation,
        'feature_values': dict(zip(_feature_names, features))
    }
    
    return diagnosis, severity, detailed_results
