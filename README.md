## 🎓 DSU STUDENT FINDER (Student Tracking App)

An interactive voice- and text-based student room locator system built for **Dhanalakshmi Srinivasan University**. This application uses a clean Streamlit interface along with speech recognition to help staff or visitors easily retrieve student room details based on name and register number.

---

##  Features

- 🔍 Search student data using **voice** or **text input**
- 🧠 Fuzzy name matching for better search accuracy
- 🎙️ Browser-based voice input via `streamlit-webrtc`
- 📄 Fetches student room number, floor, department, and year
- 🎨 Modern UI with toggle-based interaction
- 🌐 Deployable publicly using **Streamlit Cloud**

  ##  Technologies Used
- Streamlit

- SpeechRecognition

- FuzzyWuzzy

- streamlit-webrtc

  ##  How It Works

1. User enters or speaks the **student name** and **register number**.
2. App uses `fuzzywuzzy` to intelligently match close name variants.
3. Fetches student data from multiple `.json` files (2nd, 3rd, 4th year).
4. Displays location and academic information in a clean UI.


## ✍️ Author

Hovarthan S

B.Tech AI & Data Science 

Dhanalakshmi Srinivasan Engineering College

GitHub: hovarthan21

