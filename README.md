# 🎯 Face Recognition Attendance System

This project is designed to **automate attendance marking** in organizations using **face recognition technology**. It detects and recognizes human faces from live camera feeds and updates attendance records in real-time.

## 📌 Project Description
This is an **AI-based project** that leverages **Computer Vision** to track attendance.  
It captures images using a webcam, detects human faces, and matches them with registered users. If a face is recognized, the system marks attendance automatically.

### 💡 Key Features
- 📷 **Real-time Face Recognition** – Detects multiple faces in a single frame.
- 📜 **Automated Attendance Logging** – Updates attendance in real-time.
- 🔍 **Unknown Face Detection** – Identifies unregistered users.
- 📊 **CSV-based Attendance Record** – Stores attendance in a structured format.
- 🔊 **Voice Alerts** – Announces attendance using **Text-to-Speech (TTS)**.

## 🤝 Community
- **Code of Conduct**
- **Contributing to the Project**
- **Issues & Discussions**

---

## 🚀 Novelty
Unlike traditional face recognition systems, this project introduces:
- 📌 **Multi-Face Recognition** – Detects multiple people in a single frame.
- 📌 **Instant Attendance Marking** – Automatically logs entry times.
- 📌 **Real-Time Updates** – Attendance data is updated instantly.

## 🏗️ Hardware & Software Requirements

### 🖥️ Hardware:
- Laptop/Desktop with a **Webcam**
- Minimum Specs: **4GB RAM, Dual-core processor, 80GB HDD**

### 🛠️ Software:
- **OS:** Windows, macOS, or Linux
- **Programming Language:** Python 3.6+
- **Libraries Required:**  
  - `opencv-python`
  - `face_recognition`
  - `numpy`
  - `pandas`
  - `pyttsx3`

## 📂 Project Structure


---

## 🔄 Steps to Run the Project

1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/yourusername/face-recognition-attendance.git
cd face-recognition-attendance

2️⃣ Install Required Dependencies

pip install opencv-python numpy pandas pyttsx3 face_recognition

3️⃣ Add New Student Faces

Place images inside the student_faces folder.
Format: Name_RegistrationNo.jpg
(e.g., Std_19BCE10191.jpg)

4️⃣ Run the Attendance System

python face_attendance.py

5️⃣ Check the Attendance Record
Attendance will be saved in students.csv.

🎯 Output Example
Registration No.    	Name	   Entry Time
19BCE10191          	Hardik	    09:10:39
19BCE10118	        Nishant	    09:12:15
19BCE10119	        Ankit      09:12:57

📌 Results & Discussion
✅ Supports multi-person face recognition in real-time.
✅ Ensures high accuracy (>90%) using deep learning-based face recognition.
✅ Saves time & effort compared to traditional manual attendance methods.

🎯 Conclusion
This project provides an efficient, high-precision solution for automated attendance tracking in classrooms, offices, and organizations.
It captures live video, extracts faces, and instantly updates attendance records, ensuring a seamless and error-free process.

🔗 Reference Links
📌 Face Recognition Library Installation Guide
https://ourcodeworld.com/articles/read/841/how-to-install-and-use-the-python-face-recognition-and-detection-library-in-ubuntu-16-04

⭐ Support
If you find this project helpful, don't forget to star this repository! 🌟

👨‍💻 Developed by Mohammed Arshad & Lubaanah Tasnim
