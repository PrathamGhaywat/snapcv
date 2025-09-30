import cv2

def main():
    # Open default cam 
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Webcam isn't opening")
        return

    while True:
        # Capture 
        ret, frame = cap.read()
        if not ret:
            print("Failed")
            break

        # Display 
        cv2.imshow("snapcv", frame)

        # Exit with "q"
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release and close
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
