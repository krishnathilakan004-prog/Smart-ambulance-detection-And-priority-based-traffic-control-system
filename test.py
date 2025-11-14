import cv2
from ultralytics import YOLO
import time
import serial


ser = serial.Serial("COM10", 115200)
# Load the YOLOv8 model
model = YOLO("best.pt")

# Open the video file or camera
cap = cv2.VideoCapture(1)

# Initialize variables for calculating FPS
prev_time = time.time()
flg=0

while cap.isOpened():
    success, frame = cap.read()

    if success:
        
        results = model(frame)

        annotated_frame = frame.copy()

        # Process detections
        for box in results[0].boxes:
            confidence = float(box.conf)  # Confidence score
            if confidence > 0.9:
                # a+=1
                # if a>10:
                    
                    x0, y0, x1, y1 = map(int, box.xyxy[0])  # Bounding box coordinates
                    label = int(box.cls)  # Class index
                    class_name = model.names[label]  # Class name
    
                    # Draw the bounding box
                    cv2.rectangle(annotated_frame, (x0, y0), (x1, y1), (0, 255, 0), 2)
                    cv2.putText(
                        annotated_frame,
                        f"{class_name} {confidence:.2f}",
                        (x0, y0 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 255, 255),
                        2,
                    )
                    flg+=1
                    
                    #print(flg)
                    if flg==10:
                                              
                        ser.write("k#".encode())
                        print("Sent 'K#' to serial")
                        time.sleep(4)
                        flg=0

        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        
        cv2.putText(
            annotated_frame,
            f"FPS: {fps:.2f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )


        cv2.imshow("YOLOv8 Inference", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
