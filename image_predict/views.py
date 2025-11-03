import numpy as np
import tensorflow as tf
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploadSerializer
import os
from tensorflow.keras.utils import custom_object_scope

# --- Configuration ---
IMG_SIZE = (224, 224)  # Default image size, update if needed
CLASS_NAMES = ['benign', 'malignant'] # Update with your actual class names

# --- Model Loading ---
# Load the model only once when the server starts
try:
    MODEL_PATH = os.path.join(settings.BASE_DIR, 'cnn_model.h5')
    # Load model with custom objects if needed
    try:
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    except (ValueError, RuntimeError) as e:
        # If there's an unknown layer error, try with custom scope
        with custom_object_scope({'GetItem': tf.keras.layers.Layer()}):
            model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    print("Image prediction model loaded successfully.")
except (IOError, ImportError) as e:
    print(f"Error loading image prediction model: {e}")
    model = None

# --- Image Preprocessing ---
def preprocess_uploaded_image(image_file, img_size):
    """Preprocesses an in-memory uploaded image file."""
    try:
        img_bytes = image_file.read()
        img = tf.io.decode_image(img_bytes, channels=3, expand_animations=False)
        img = tf.image.resize(img, img_size)
        img = tf.cast(img, tf.float32) / 255.0
        img = tf.expand_dims(img, axis=0)  # Add batch dimension
        return img
    except Exception as e:
        return None

# --- API View ---
class ImagePredictionView(APIView):
    """Handles image uploads and returns predictions."""
    def post(self, request, *args, **kwargs):
        if not model:
            return Response(
                {"error": "Model is not loaded. Please check server logs."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        serializer = ImageUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        image = serializer.validated_data['image']
        processed_image = preprocess_uploaded_image(image, IMG_SIZE)

        if processed_image is None:
            return Response(
                {"error": "Invalid or corrupted image file."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            prediction = model.predict(processed_image)
            confidence = float(np.max(prediction))
            predicted_class_index = np.argmax(prediction)
            predicted_class_name = CLASS_NAMES[predicted_class_index]

            return Response(
                {
                    "prediction": predicted_class_name,
                    "confidence": round(confidence, 4)
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"Prediction failed: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

