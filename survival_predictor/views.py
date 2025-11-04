from django.apps import apps
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SurvivalPredictionSerializer
import pandas as pd

class SurvivalPredictionView(APIView):
    """
    API view to handle survival prediction requests.
    """
    def post(self, request, *args, **kwargs):
        # Use Django's recommended way to get the app config and the loaded model
        app_config = apps.get_app_config('survival_predictor')
        model = app_config.model

        if model is None:
            # This error now definitively means the model file was not found or failed to load on startup.
            return Response({
                "error": "Model is not available. Please check server startup logs for a 'file not found' warning.",
                "fix": "Ensure 'random_forest_survival_model.pkl' is in 'survival_predictor/ml_models/' and restart the server."
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        serializer = SurvivalPredictionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Define the expected order and names of model features
        feature_names = [
            'Age at Diagnosis', 'Neoplasm Histologic Grade', 'HER2 Status', 'ER Status', 'PR Status',
            'Tumor Size', 'Tumor Stage', 'Lymph nodes examined positive', 'Mutation Count',
            'Nottingham prognostic index', 'Inferred Menopausal State', 'Overall Survival (Months)',
            'Relapse Free Status (Months)', 'TMB (nonsynonymous)',
            'BRCA1', 'BRCA2', 'TP53', 'ERBB2', 'ESR1', 'PGR', 'AKT1', 'PIK3CA', 'MKI67', 'CDH1',
            'BCL10', 'CFH', 'RBM14', 'TAOK2', 'DUSP11', 'ISCU', 'MARCHF6', 'MOB3B', 'DNAJB6', 'ATG12'
        ]

        # Create a dictionary with model-expected keys from the snake_cased serializer fields
        try:
            model_input_data = {name: validated_data[name.lower().replace(' ', '_').replace('(', '').replace(')', '')] for name in feature_names}
        except KeyError as e:
            return Response({"error": f"Missing feature in request data: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a DataFrame with a single row
        df = pd.DataFrame([model_input_data], columns=feature_names)

        try:
            # Get prediction and probability
            prediction = model.predict(df)[0]
            probability = model.predict_proba(df)[0]

            # Assuming the model outputs 0 for 'Deceased' and 1 for 'Living'
            # and predict_proba returns [prob_deceased, prob_living]
            predicted_class = "Living" if prediction == 0 else "Deceased"
            class_probability = probability[0] if predicted_class == "Living" else probability[1]

            response_data = {
                "prediction": predicted_class,
                "probability": round(float(class_probability), 4) # Ensure probability is a float
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Model prediction failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
