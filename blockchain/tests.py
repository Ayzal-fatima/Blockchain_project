from django.test import TestCase
from attendance.models import BiometricData
import os
from .facial_recognition_service import register_face, compare_faces

class BiometricDataTestCase(TestCase):
    def test_register_face(self):
        # Replace with the actual path to an image with a known face
        known_face_image_path = os.path.join('path', 'to', 'upload', 'image4.jpeg')
        
        # Register the known face
        known_face_encoding = register_face(known_face_image_path)
        
        # Check if the registration was successful
        self.assertIsNotNone(known_face_encoding, "Face registration failed")

        # Print the known face encoding
        print("Known Face Encoding:", known_face_encoding)

    def test_compare_faces(self):
        # Replace with the actual path to an image with a known face
        known_face_image_path = os.path.join('path', 'to', 'upload', 'image4.jpeg')
        
        # Register the known face
        known_face_encoding = register_face(known_face_image_path)
        
        # Replace with the actual path to an image to compare
        image_to_check_path = os.path.join('path', 'to', 'upload', 'image3.jpeg')

        # Compare the faces
        match_result = compare_faces(known_face_encoding, image_to_check_path)
        
        # Check if the faces match
        self.assertTrue(match_result, "Faces do not match")

        # Print the known face encoding
        print("Known Face Encoding:", known_face_encoding)
