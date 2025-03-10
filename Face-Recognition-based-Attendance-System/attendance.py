import cv2
import numpy as np
import pandas as pd
import os
import pyttsx3
from datetime import datetime

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set to female voice
engine.setProperty('rate', 170)  # Adjust speed for more natural speech

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Create necessary directories
os.makedirs("student_faces", exist_ok=True)
os.makedirs("models", exist_ok=True)

# Load student data
csv_file = "students.csv"
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=["Registration Number", "Name", "Department", "Email", "Check-in", "Check-out"])
    df.to_csv(csv_file, index=False)
else:
    df = pd.read_csv(csv_file)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

def register_student():
    global df
    reg_no = input("Enter Registration Number: ").strip()
    name = input("Enter Name: ").strip()
    department = input("Enter Department: ").strip()
    email = input("Enter Email: ").strip()
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Camera not working!")
        return
    
    count = 0
    print("📸 Capturing images. Please press space to capture each image.")
    while count < 5:
        ret, frame = cap.read()
        if not ret:
            print("❌ Camera error!")
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw rectangle around face
            
        cv2.putText(frame, "Press Space to Capture", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Face Registration", frame)
        
        # Capture when space bar is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord(" "):  # Spacebar
            if len(faces) > 0:  # Only capture if a face is detected
                for (x, y, w, h) in faces:
                    face = gray[y:y + h, x:x + w]
                    face = cv2.resize(face, (200, 200))
                    face = cv2.equalizeHist(face)
                    cv2.imwrite(f"student_faces/{reg_no}_{count}.jpg", face)
                    count += 1
                    print(f"✅ Image {count} captured.")
        
        if count >= 5:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    new_data = pd.DataFrame([[reg_no, name, department, email, "", ""]], 
                            columns=["Registration Number", "Name", "Department", "Email", "Check-in", "Check-out"])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(csv_file, index=False)
    print("🎓 Student registered successfully!")
    speak(f"Student {name} registered successfully.")
    train_model()

def train_model():
    faces, labels = [], []
    
    # Check if 'student_faces' directory exists
    if not os.path.exists("student_faces"):
        print("❌ The 'student_faces' directory does not exist.")
        return
    
    # If the directory exists, proceed with the training
    for file in os.listdir("student_faces"):
        if file.endswith(".jpg"):
            reg_no = file.split("_")[0]
            
            if not reg_no.isdigit():
                print(f"⚠ Skipping invalid file: {file}")
                continue
            
            img_path = os.path.join("student_faces", file)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            
            if img is None:
                print(f"⚠ Warning: Unable to read image {img_path}")
                continue
            
            img = cv2.equalizeHist(img)
            faces.append(img)
            labels.append(int(reg_no))
    
    if len(faces) == 0:
        print("❌ No valid training data found.")
        return
    
    recognizer.train(faces, np.array(labels))
    recognizer.save("models/face_recognition.yml")
    print("✅ Face recognition model trained successfully!")

def mark_attendance(check_out=False):
    global df

    if not os.path.exists("models/face_recognition.yml"):
        print("❌ Face recognition model not found. Please register students first.")
        return

    recognizer.read("models/face_recognition.yml")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Camera not working!")
        return

    checked_in_students = []
    registered_students = df["Registration Number"].astype(str).tolist()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Camera error!")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))
            label, confidence = recognizer.predict(face)

            name = "Unknown"
            if confidence < 50:
                label = str(label)
                student_data = df[df["Registration Number"] == label]
                if not student_data.empty:
                    name = student_data["Name"].values[0]
                    
            # Draw rectangle around face and name
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow("Face Recognition", frame)
        
        # Check-in/out when space is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord(" "):  # Spacebar to check-in or check-out
            for (x, y, w, h) in faces:
                face = gray[y:y + h, x:x + w]
                label, confidence = recognizer.predict(face)
                if confidence < 50:
                    label = str(label)
                    student_data = df[df["Registration Number"] == label]
                    if not student_data.empty:
                        name = student_data["Name"].values[0]
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        
                        if check_out:
                            df.loc[df["Registration Number"] == label, "Check-out"] = current_time
                        else:
                            df.loc[df["Registration Number"] == label, "Check-in"] = current_time
                            checked_in_students.append(label)

                        df.to_csv(csv_file, index=False)
                        print(f"✅ {name} {'checked out' if check_out else 'checked in'} at {current_time}")
            
            if len(checked_in_students) >= 3:
                # List un-checked students
                unchecked_students = [student for student in registered_students if student not in checked_in_students]
                if unchecked_students:
                    unchecked_names = df[df["Registration Number"].isin(unchecked_students)]["Name"].values
                    remaining_names = ", ".join(unchecked_names)
                    speak(f"Students not checked in: {remaining_names}")
                    print(f"Students not checked in: {remaining_names}")

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

while True:
    print("\n1. Register New Student")
    print("2. Check-In")
    print("3. Check-Out")
    print("4. Exit")
    
    choice = input("Enter your choice: ").strip()
    if choice == "1":
        register_student()
    elif choice == "2":
        mark_attendance(check_out=False)
    elif choice == "3":
        mark_attendance(check_out=True)
    elif choice == "4":
        print("👋 Exiting program...")
        break
    else:
        print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

##by Lubaanah and Arshad
