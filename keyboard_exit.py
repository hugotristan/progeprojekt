import face_recognition
import cv2
import keyboard  # Install with `pip install keyboard`

# Initialize the camera (0 is the default camera)
camera = cv2.VideoCapture(0)

# Variables for face location and other tracking parameters
face_locations = []
d = 0.5  # Downscale factor for faster face detection
s = int(1/d)  # Scale multiplier for bounding box
p = 0  # Count of frames where a face was detected
n = 0  # Count of frames where no face was detected

# Flag to control program execution
running = True

# Function to handle key combination
def on_key_combination():
    print("Hotkey pressed. Exiting...")
    global running
    running = False  # Set the running flag to False to stop the main loop

# Set up an event listener for the 'z+s+w' key combination
keyboard.add_hotkey('z+s+w', on_key_combination)

# Main loop for video processing
while running:
    # Capture a frame from the camera
    ret, frame = camera.read()
    if not ret:
        print("Error: Unable to capture frame.")
        break

    # Process frames only when `check_frame` is True
    small_frame = cv2.resize(frame, (0, 0), fx=d, fy=d)

    # Detect faces in the frame
    face_locations = face_recognition.face_locations(small_frame)

    if face_locations:
        p += 1  # Increment the counter if a face is detected
    else:
        n += 1  # Increment the counter if no face is detected

# Release the camera
camera.release()

# Print analysis results
print("Frames with detected faces:", p)
print("Frames without detected faces:", n)
if n != 0:
    percentage = int(round((p * 100) / (p + n), 0))
    print(f"{percentage}%")
    if (p * 100) / (p + n) > 80:
        print("You focused very much.")
else:
    print("You were focused the entire time.")


