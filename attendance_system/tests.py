from django.test import TestCase
from blockchain.facial_recognition_service import compare_faces, register_face
import os

class FacialRecognitionTest(TestCase):
    def test_compare_faces(self):
        # Replace 'path_to_known_face.jpg' with the actual path to a known face image
        known_face_image_path = 'path/to/upload/image4.jpeg'

        # Replace 'path_to_user_image.jpg' with the actual path to an image received from the user
        image_to_check_path = 'path/to/upload/image3.jpeg'

        # Check if the known face image file exists
        if os.path.isfile(known_face_image_path):
            known_face_encoding = register_face(known_face_image_path)

            # Check if the user image file exists
            if os.path.isfile(image_to_check_path):
                result = compare_faces(known_face_encoding, image_to_check_path)
                self.assertTrue(result)
            else:
                self.fail(f"User image file not found at: {image_to_check_path}")
        else:
            self.fail(f"Known face image file not found at: {known_face_image_path}")
