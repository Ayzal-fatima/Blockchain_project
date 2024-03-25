# import face_recognition
import os
import io
import face_recognition
import json

def register_face(image_path):
    """
    Load an image file and get its face encoding.
    """
    try:
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if face_encodings:
            return face_encodings[0].tolist()
        else:
            print("No face detected in the image provided for registration.")
            return None
    except Exception as e:
        print(f"Error in registering face: {e}")
        return None

def compare_faces(known_face_encoding, image_data_to_check):
    """
    Compare a known face encoding against a candidate image.
    Returns True if they match, False otherwise.
    """


    try:
        if not known_face_encoding:
            print("Known face encoding is invalid.")
            return False

        if not image_data_to_check:
            print("No image data provided.")
            return False

        if not isinstance(known_face_encoding, list):
            known_face_encoding = json.loads(known_face_encoding)

        known_face_encoding_bytes = json.dumps(known_face_encoding).encode()

        unknown_image = face_recognition.load_image_file(io.BytesIO(image_data_to_check))
        unknown_face_encodings = face_recognition.face_encodings(unknown_image)

        print(f"Image Encoding: {unknown_face_encodings}")

        if not unknown_face_encodings:
            print("No face detected in the unknown image.")
            return False

        known_face_encoding = json.loads(known_face_encoding_bytes.decode())

        match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])
        return match_results[0]
    except Exception as e:
        print(f"Error in comparing faces: {e}")
        return False

