import os
import joblib
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientDataSerializer

# Define the absolute path to the model file
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'xgboost_all_treatments.pkl')

class PredictView(APIView):
    """
    An API View for making predictions on cancer patient data.
    Accepts a POST request with JSON data and returns treatment recommendations.
    """

    def post(self, request, *args, **kwargs):
        serializer = PatientDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Load the pre-trained model
        try:
            model = joblib.load(MODEL_PATH)
        except FileNotFoundError:
            return Response({"error": "Model file not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"Error loading model: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # The serializer's `source` argument maps the JSON keys to the correct
        # field names. We can pass the validated data directly to the DataFrame.
        df = pd.DataFrame([serializer.validated_data])
        # Rename columns to match the model's expected input
        df.rename(columns={
            'age_at_diagnosis': 'Age at Diagnosis',
            'neoplasm_histologic_grade': 'Neoplasm Histologic Grade',
            'her2_status': 'HER2 Status',
            'er_status': 'ER Status',
            'pr_status': 'PR Status',
            'tumor_size': 'Tumor Size',
            'tumor_stage': 'Tumor Stage',
            'lymph_nodes_examined_positive': 'Lymph nodes examined positive',
            'mutation_count': 'Mutation Count',
            'nottingham_prognostic_index': 'Nottingham prognostic index',
            'inferred_menopausal_state': 'Inferred Menopausal State',
            'brca1': 'BRCA1',
            'brca2': 'BRCA2',
            'tp53': 'TP53',
            'erbb2': 'ERBB2',
            'esr1': 'ESR1',
            'pgr': 'PGR',
            'akt1': 'AKT1',
            'pik3ca': 'PIK3CA',
            'mki67': 'MKI67',
            'cdh1': 'CDH1',
        }, inplace=True)

        # Make predictions
        try:
            predictions = model.predict(df)
        except Exception as e:
            return Response({"error": f"Prediction failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Map predictions to "Yes"/"No"
        treatment_map = {1: "Yes", 0: "No"}
        chemo_pred, radio_pred, hormone_pred = predictions[0]

        response_data = {
            "Chemotherapy": treatment_map.get(chemo_pred, "No"),
            "Radio Therapy": treatment_map.get(radio_pred, "No"),
            "Hormone Therapy": treatment_map.get(hormone_pred, "No"),
        }

        return Response(response_data, status=status.HTTP_200_OK)
