import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="KP Board 1st Year Entry Test Prep", page_icon="🎓", layout="wide")

st.title("🎓 KP Board 1st Year MCQ Prep Portal (With ETEA & NMDCAT Past Papers)")
st.subheader("Comprehensive Prep for Chemistry, Physics, Maths, English, Urdu, Mutala-e-Quran, & Islamiat")

# Subject Mapping
SUBJECTS = {
    "Chemistry": "data/chemistry.csv",
    "Physics": "data/physics.csv",
    "Mathematics": "data/mathematics.csv",
    "English": "data/english.csv",
    "Urdu": "data/urdu.csv",
    "Mutala-e-Quran": "data/mutala_e_quran.csv",
    "Islamiat": "data/islamiat.csv"
}

st.sidebar.header("🎯 Entrance Exam Control Panel")
selected_subject = st.sidebar.selectbox("Select Subject", list(SUBJECTS.keys()))

@st.cache_data
def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        # Fallback template
        return pd.DataFrame({
            "Chapter": ["General Past Papers"],
            "Question": ["[ETEA Past Paper] Which of the following defines absolute zero?"],
            "Option_A": ["-273.15 C"], "Option_B": ["0 C"], "Option_C": ["273.15 C"], "Option_D": ["100 C"],
            "Correct_Answer": ["A"]
        })

df = load_data(SUBJECTS[selected_subject])

# Advanced Filtering for ETEA / NMDCAT
exam_filter = st.sidebar.radio("Filter Question Source", ["All Questions", "ETEA Only", "NMDCAT Only"])
if exam_filter == "ETEA Only":
    df = df[df["Question"].str.contains("ETEA", case=False, na=False)].reset_index(drop=True)
elif exam_filter == "NMDCAT Only":
    df = df[df["Question"].str.contains("NMDCAT", case=False, na=False)].reset_index(drop=True)

chapters = ["All Chapters"] + list(df["Chapter"].unique())
selected_chapter = st.sidebar.selectbox("Filter by Chapter", chapters)

if selected_chapter != "All Chapters":
    df = df[df["Chapter"] == selected_chapter].reset_index(drop=True)

state_key = f"{selected_subject}_{selected_chapter}_{exam_filter}"
if "current_state_key" not in st.session_state or st.session_state.current_state_key != state_key:
    st.session_state.current_state_key = state_key
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected_option = None

total_questions = len(df)

if total_questions == 0:
    st.warning("No questions match your filter criteria in the data package.")
else:
    progress = (st.session_state.current_index + 1) / total_questions
    st.progress(progress)
    st.write(f"**Question {st.session_state.current_index + 1} of {total_questions}** | Current Score: `{st.session_state.score}/{total_questions}`")
    
    row = df.iloc[st.session_state.current_index]
    st.info(f"📖 **{row['Chapter']}**")
    st.markdown(f"#### Q: {row['Question']}")
    
    options = [f"A) {row['Option_A']}", f"B) {row['Option_B']}", f"C) {row['Option_C']}", f"D) {row['Option_D']}"]
    
    user_choice = st.radio(
        "Choose your answer:", 
        options, 
        index=None if not st.session_state.answered else ["A", "B", "C", "D"].index(st.session_state.selected_option),
        disabled=st.session_state.answered,
        key=f"q_{st.session_state.current_index}"
    )
    
    col1, col2 = st.columns()
    with col1:
        if st.button("Submit Answer", disabled=st.session_state.answered or user_choice is None):
            st.session_state.answered = True
            choice_letter = user_choice[0]
            st.session_state.selected_option = choice_letter
            if choice_letter == str(row['Correct_Answer']).strip().upper():
                st.session_state.score += 1
            st.rerun()

    if st.session_state.answered:
        correct_letter = str(row['Correct_Answer']).strip().upper()
        if st.session_state.selected_option == correct_letter:
            st.success("🎉 Correct Answer!")
        else:
            st.error(f"❌ Incorrect. The correct answer was **{correct_letter}**.")
            
        with col2:
            if st.session_state.current_index < total_questions - 1:
                if st.button("Next Question ➡️"):
                    st.session_state.current_index += 1
                    st.session_state.answered = False
                    st.session_state.selected_option = None
                    st.rerun()
            else:
                st.balloons()
                st.success(f"🏆 Completed! Final Score: {st.session_state.score} / {total_questions}")
