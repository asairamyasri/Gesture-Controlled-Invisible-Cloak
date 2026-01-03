# run the below code first to save your background
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Capture Background", frame)
    # press 'b' to save your background
    if cv2.waitKey(1) & 0xFF == ord('b'):
        cv2.imwrite("background.jpg", frame)
        print("Background saved!")
        break

cap.release()
cv2.destroyAllWindows()
