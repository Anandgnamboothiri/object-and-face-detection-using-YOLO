import cv2 
from ultralytics import YOLO

# Load models
body_model = YOLO("yolov8n.pt")         # Full body detection
face_model = YOLO("yolov8n-face.pt") 
object_model =YOLO("" )                       # Face detection (custom-trained)


cap = cv2.VideoCapture(0)  # Replace with your video file path or 0 for webcam
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect people (bodies)
    body_results = body_model(frame)
    face_results = face_model(frame)
    

    annotated_frame = frame.copy()

    # Draw bodies
    for r in body_results:
        for box in r.boxes:
            cls = int(box.cls[0])
            if cls == 0:  # class 0 = person
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(annotated_frame, "Body", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Draw faces
    for r in face_results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(annotated_frame, "Face", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow("YOLOv8 - Face + Body Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()









