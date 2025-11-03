from django.apps import AppConfig
import os
import joblib
from django.conf import settings

class SurvivalPredictorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'survival_predictor'
    MODEL_FILE = os.path.join(settings.BASE_DIR, 'survival_predictor/ml_models/random_forest_survival_model.pkl')
    model = None

    def ready(self):
        # This method is called when the app is ready.
        # We load the model here to ensure it's loaded only once.
        if os.path.exists(self.MODEL_FILE):
            self.model = joblib.load(self.MODEL_FILE)
            print("Survival prediction model loaded successfully.")
        else:
            # Handle the case where the model file is missing
            print(f"Warning: Survival prediction model file not found at {self.MODEL_FILE}")
