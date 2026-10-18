import cv2
from pathlib import Path

BASE = Path(__file__).resolve().parent
MODELS = BASE / "models"

detector = cv2.FaceDetectorYN.create(
    str(MODELS / "face_detection_yunet_2026may.onnx"),
    "",
    (320, 320),
    0.9,
    0.3,
    5000
)

recognizer = cv2.FaceRecognizerSF.create(
    str(MODELS / "face_recognition_sface_2021dec.onnx"),
    ""
)

def get_face_features(filename):
    image = cv2.imread(filename)

    if image is None:
        raise FileNotFoundError(f"Cannot read image: {filename}")

    height, width = image.shape[:2]
    detector.setInputSize((width, height))

    _, faces = detector.detect(image)

    if faces is None or len(faces) == 0:
        raise ValueError(f"No face detected in {filename}")

    # Use the largest detected face.
    face = max(faces, key=lambda f: f[2] * f[3])

    aligned = recognizer.alignCrop(image, face)
    return recognizer.feature(aligned)

feature1 = get_face_features("TravisKelce.jpg")
feature2 = get_face_features("JasonKelce.jpg")

score = recognizer.match(
    feature1,
    feature2,
    cv2.FaceRecognizerSF_FR_COSINE
)

threshold = 0.363

print(f"Cosine similarity: {score:.3f}")

if score >= threshold:
    print("Likely the same person")
else:
    print("Not a confident match")