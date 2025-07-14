import streamlit as st
from utils.student_utils import get_student_data
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import speech_recognition as sr
import numpy as np
import av

# Title and styling
st.set_page_config(page_title="🎓 DSU Student Finder", layout="centered")

st.markdown("""
    <style>
    .title {
        font-size: 32px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 20px;
    }
    .info-box {
        background-color: #f0f2f5;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'> DSU AI Student Finder </div>", unsafe_allow_html=True)

# -----------------------------
# Helper to use SpeechRecognition with webrtc
# -----------------------------

class AudioProcessor(AudioProcessorBase):
    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        # Convert audio frame to numpy array
        audio = frame.to_ndarray()
        if audio is not None:
            audio_data = np.array(audio).flatten().tobytes()
            with sr.AudioFile(sr.AudioData(audio_data, frame.sample_rate, 2)) as source:
                recognizer = sr.Recognizer()
                try:
                    text = recognizer.recognize_google(recognizer.record(source))
                    st.session_state['voice_input'] = text
                    st.success(f" Recognized: {text}")
                except sr.UnknownValueError:
                    st.warning("Could not understand audio.")
                except sr.RequestError as e:
                    st.error(f"Google Speech API error: {e}")
        return frame

# -----------------------------
# Input Section
# -----------------------------
st.subheader("Student Details Input")

# Default state
if "voice_input" not in st.session_state:
    st.session_state["voice_input"] = ""

col1, col2 = st.columns(2)

with col1:
    use_voice_name = st.toggle("Use Voice for Name", key="voice_name")
    if use_voice_name:
        st.write("Say the student name")
        webrtc_streamer(key="name", audio_processor_factory=AudioProcessor, media_stream_constraints={"audio": True, "video": False})
        name = st.session_state.get("voice_input", "")
    else:
        name = st.text_input("Enter Student Name")

with col2:
    use_voice_reg = st.toggle("Use Voice for Register No", key="voice_reg")
    if use_voice_reg:
        st.write("Say the register number")
        webrtc_streamer(key="reg", audio_processor_factory=AudioProcessor, media_stream_constraints={"audio": True, "video": False})
        reg_no = st.session_state.get("voice_input", "")
    else:
        reg_no = st.text_input("Enter Register Number")

# -----------------------------
# Process & Display Results
# -----------------------------
if st.button("🔍 Search"):
    if name and reg_no:
        try:
            reg_no_clean = int(reg_no.replace(" ", ""))
            with st.spinner("Fetching data..."):
                student = get_student_data(name, reg_no_clean)
                if student is not None:
                    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                    st.success("✅ Student Found")
                    st.write(f"**Name:** {student['NAME']}")
                    st.write(f"**Register Number:** {student['REG NO']}")
                    st.write(f"**Room No:** {student['ROOM NO']}")
                    st.write(f"**Floor:** {student['FLOOR']}")
                    st.write(f"**Department:** Artificial Intelligence and Data Science")
                    st.write(f"**Year:** {student['YEAR']}")
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error("❌ Student not found. Please check details.")
        except ValueError:
            st.error("Register number must be numeric.")
    else:
        st.warning("Please enter or speak both name and register number.")
