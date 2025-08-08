# main.py

import streamlit as st
import datetime
from generation_pipeline import get_test_generator

# Page configuration
st.set_page_config(
    page_title="Student Screening Test",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# DARK MODE Compatible CSS with Professional Styling
st.markdown("""
<style>
    /* Base dark theme styling */
    .stApp {
        font-family: 'Times New Roman', Times, serif;
        background-color: #1a1a1a;
        color: #e0e0e0;
    }
    
    .main-header {
        text-align: center;
        color: #64b5f6;
        font-size: 2.8rem;
        margin-bottom: 2rem;
        font-family: 'Times New Roman', Times, serif;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .section-header {
        color: #81c784;
        font-size: 1.6rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-family: 'Times New Roman', Times, serif;
        font-weight: 800;
    }
    
    .info-box {
        background-color: #2d2d2d;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        font-family: 'Times New Roman', Times, serif;
        border: 2px solid #424242;
        color: #e0e0e0;
    }
    
    .success-box {
        background-color: #1b5e20;
        color: #a5d6a7;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        font-family: 'Times New Roman', Times, serif;
        border: 2px solid #2e7d32;
        font-weight: 600;
    }
    
    /* DARK MODE Section and Subsection Headings */
    .section-heading {
        color: #81c784 !important;
        font-family: 'Times New Roman', Times, serif !important;
        font-weight: 900 !important;
        font-size: 1.8rem !important;
        margin: 40px 0 30px 0 !important;
        padding: 15px 0 10px 0 !important;
        border-bottom: 4px solid #81c784 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        background-color: #2d2d2d !important;
        padding-left: 15px !important;
        border-left: 6px solid #81c784 !important;
    }
    
    .subsection-heading {
        color: #64b5f6 !important;
        font-family: 'Times New Roman', Times, serif !important;
        font-weight: 800 !important;
        font-size: 1.4rem !important;
        margin: 30px 0 20px 0 !important;
        padding: 10px 0 8px 0 !important;
        border-bottom: 3px solid #64b5f6 !important;
        text-decoration: underline !important;
        background-color: #1e1e1e !important;
        padding-left: 12px !important;
    }
    
    /* MCQ Container - Dark theme */
    .mcq-container {
        margin: 30px 0;
        padding: 20px;
        background-color: #2d2d2d;
        border: 2px solid #424242;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    /* Question styling - DARK MODE */
    .mcq-question {
        font-weight: 900 !important;
        margin-bottom: 20px;
        color: #e0e0e0 !important;
        font-family: 'Times New Roman', Times, serif;
        font-size: 19px !important;
        line-height: 1.6;
        margin-top: 10px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        background-color: #3a3a3a;
        padding: 10px;
        border-left: 4px solid #81c784;
    }
    
    /* Interactive option styling - DARK MODE */
    .mcq-option {
        display: flex;
        align-items: flex-start;
        margin: 12px 0;
        padding: 12px;
        font-family: 'Times New Roman', Times, serif;
        font-size: 17px;
        line-height: 1.6;
        cursor: pointer;
        transition: all 0.3s ease;
        border-radius: 6px;
        border: 1px solid #505050;
        background-color: #3a3a3a;
        color: #e0e0e0;
    }
    
    .mcq-option:hover {
        background-color: #1e3a5f;
        border-color: #64b5f6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Radio button - DARK MODE compatible */
    .mcq-option input[type="radio"] {
        width: 22px;
        height: 22px;
        margin-right: 15px;
        margin-top: 3px;
        cursor: pointer;
        accent-color: #64b5f6;
        border: 3px solid #64b5f6;
    }
    
    .mcq-option-text {
        color: #e0e0e0;
        flex: 1;
        font-size: 17px;
        cursor: pointer;
        font-weight: 600;
    }
    
    /* Selected option styling - DARK MODE */
    .mcq-option.selected {
        background-color: #1e3a5f !important;
        border: 3px solid #64b5f6 !important;
        box-shadow: 0 4px 8px rgba(100, 181, 246, 0.3) !important;
    }
    
    .mcq-option input[type="radio"]:checked + .mcq-option-text {
        font-weight: 900 !important;
        color: #64b5f6 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Reading passage styling - DARK MODE */
    .reading-passage {
        background-color: #2d2d2d;
        padding: 30px;
        border-radius: 12px;
        margin: 30px 0;
        border: 3px solid #757575;
        font-style: italic;
        line-height: 2.0;
        font-size: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        color: #e0e0e0;
        font-weight: 600;
    }
    
    /* Test content - DARK MODE */
    .test-content {
        background-color: #1a1a1a;
        padding: 0;
        margin: 20px 0;
        line-height: 1.8;
        font-family: 'Times New Roman', Times, serif;
        font-size: 16px;
        color: #e0e0e0;
    }
    
    /* Override Streamlit default markdown styles for DARK MODE */
    .test-content h2 {
        color: #81c784 !important;
        font-family: 'Times New Roman', Times, serif !important;
        font-weight: 900 !important;
        margin-top: 40px !important;
        margin-bottom: 25px !important;
        border-bottom: 4px solid #81c784 !important;
        padding-bottom: 10px !important;
        font-size: 1.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        background-color: #2d2d2d !important;
        padding-left: 15px !important;
        border-left: 6px solid #81c784 !important;
    }
    
    .test-content h3 {
        color: #64b5f6 !important;
        font-family: 'Times New Roman', Times, serif !important;
        font-weight: 800 !important;
        margin-top: 30px !important;
        margin-bottom: 20px !important;
        font-size: 1.4rem !important;
        border-bottom: 3px solid #64b5f6 !important;
        padding-bottom: 8px !important;
        text-decoration: underline !important;
        background-color: #1e1e1e !important;
        padding-left: 12px !important;
    }
    
    /* All text elements - DARK MODE */
    div[data-testid="stMarkdownContainer"] {
        font-family: 'Times New Roman', Times, serif;
        color: #e0e0e0;
    }
    
    .stButton > button {
        font-weight: 700;
        font-family: 'Times New Roman', Times, serif;
        font-size: 16px;
        padding: 12px 24px;
        border: 2px solid;
        border-radius: 8px;
        background-color: #424242;
        color: #e0e0e0;
    }
    
    .stButton > button[kind="primary"] {
        background-color: #1976d2;
        color: white;
        border-color: #1976d2;
    }
    
    .stButton > button:hover {
        background-color: #616161;
        color: #ffffff;
    }
    
    .stSelectbox label, .stTextInput label, .stNumberInput label {
        font-family: 'Times New Roman', Times, serif;
        font-weight: 600;
        color: #e0e0e0;
    }
    
    .stForm {
        font-family: 'Times New Roman', Times, serif;
        background-color: #2d2d2d;
        border: 1px solid #424242;
        border-radius: 8px;
        padding: 20px;
    }
    
    /* Input fields - DARK MODE */
    .stTextInput > div > div > input {
        background-color: #424242;
        color: #e0e0e0;
        border: 1px solid #616161;
    }
    
    .stSelectbox > div > div > div {
        background-color: #424242;
        color: #e0e0e0;
        border: 1px solid #616161;
    }
    
    .stNumberInput > div > div > input {
        background-color: #424242;
        color: #e0e0e0;
        border: 1px solid #616161;
    }
    
    /* Progress styling - DARK MODE */
    .progress-container {
        background-color: #2d2d2d;
        padding: 20px;
        border-radius: 10px;
        margin: 25px 0;
        text-align: center;
        border: 2px solid #424242;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        color: #e0e0e0;
    }
    
    /* Instructions styling - DARK MODE */
    .instructions-box {
        background-color: #1e3a5f;
        padding: 25px;
        border-radius: 12px;
        border: 3px solid #64b5f6;
        margin: 25px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        color: #e0e0e0;
    }
    
    .instructions-box h3 {
        color: #e0e0e0 !important;
        font-weight: 800 !important;
        font-size: 1.3rem !important;
    }
    
    /* Expander styling - DARK MODE */
    .streamlit-expanderHeader {
        background-color: #424242;
        color: #e0e0e0;
    }
    
    .streamlit-expanderContent {
        background-color: #2d2d2d;
        color: #e0e0e0;
    }
    
    /* Success/Error messages - DARK MODE */
    .stSuccess {
        background-color: #1b5e20;
        color: #a5d6a7;
        border: 1px solid #2e7d32;
    }
    
    .stError {
        background-color: #b71c1c;
        color: #ffcdd2;
        border: 1px solid #d32f2f;
    }
    
    .stInfo {
        background-color: #0d47a1;
        color: #bbdefb;
        border: 1px solid #1976d2;
    }
    
    /* Responsive design - DARK MODE */
    @media (max-width: 768px) {
        .mcq-container {
            padding: 15px;
            margin: 20px 0;
            background-color: #2d2d2d;
        }
        
        .mcq-question {
            font-size: 17px !important;
            background-color: #3a3a3a;
        }
        
        .mcq-option {
            font-size: 16px;
            padding: 10px;
            background-color: #3a3a3a;
        }
        
        .test-content {
            padding: 10px;
            background-color: #1a1a1a;
        }
        
        .section-heading {
            font-size: 1.5rem !important;
            background-color: #2d2d2d !important;
        }
        
        .subsection-heading {
            font-size: 1.2rem !important;
            background-color: #1e1e1e !important;
        }
    }
</style>
""", unsafe_allow_html=True)

class StudentInfoManager:
    """Manages student information and form validation"""
    
    @staticmethod
    def get_class_options():
        """Return list of available class/grade options"""
        return [
            "1st Grade", "2nd Grade", "3rd Grade", "4th Grade", "5th Grade", "6th Grade",
            "7th Grade", "8th Grade", "9th Grade", "10th Grade", "11th Grade", "12th Grade"
        ]
    
    @staticmethod
    def validate_required_fields(first_name, last_name, class_level):
        """Validate required form fields"""
        return bool(first_name and last_name and class_level)
    
    @staticmethod
    def create_student_info(first_name, last_name, class_level, age):
        """Create student information dictionary"""
        return {
            "first_name": first_name,
            "last_name": last_name,
            "class_level": class_level,
            "age": age,
            "registration_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

class UIComponents:
    """UI components for the Streamlit app"""
    
    @staticmethod
    def render_header():
        """Render the main header"""
        st.markdown('<h1 class="main-header">📚 Student Screening Test Platform</h1>', unsafe_allow_html=True)
    
    @staticmethod
    def render_info_panel():
        """Render the information panel"""
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### 📋 About This Test")
        st.markdown("""
        This screening test includes:
        - **Phonological Awareness**: Sound recognition and manipulation
        - **Reading Comprehension**: Understanding and analyzing text
        - **Mathematics**: Problem-solving and calculations
        
        **All questions are Multiple Choice Questions (MCQ)** with 4 options each (a, b, c, d).
        The test is automatically adjusted based on your grade level to ensure appropriate difficulty.
        """)
        st.markdown("### ⏱️ Estimated Time")
        st.markdown("**20-30 minutes** to complete all sections")
        st.markdown("### 🎯 Instructions")
        st.markdown("Read each question carefully and click the radio button to select your answer. Take your time!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def render_welcome_message(first_name, class_level):
        """Render welcome message"""
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown(f"### Welcome, {first_name}! 🎉")
        st.markdown(f"You're registered for a **{class_level}** level screening test.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def render_student_summary(student_info):
        """Render student information summary"""
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Your Information:")
            st.write(f"**Name:** {student_info['first_name']} {student_info['last_name']}")
            st.write(f"**Grade:** {student_info['class_level']}")
            st.write(f"**Age:** {student_info['age']}")
        
        with col2:
            st.markdown("### Test Details:")
            st.write(f"**Date:** {student_info['registration_date']}")
    
    @staticmethod
    def render_test_instructions():
        """Render test instructions"""
        st.markdown('<div class="instructions-box">', unsafe_allow_html=True)
        st.markdown("### 📝 Before You Begin:")
        st.markdown("""
        1. **Find a quiet place** where you can focus
        2. **Have paper and pencil** ready for calculations
        3. **Read each question carefully** before selecting an answer
        4. **Click the radio button** to select your answer for each question
        5. **Take your time** - there's no time limit
        6. **Ask for help** if you need clarification on instructions
        """)
        st.markdown('</div>', unsafe_allow_html=True)

class PageManager:
    """Manages different pages of the application"""
    
    def __init__(self):
        self.info_manager = StudentInfoManager()
        self.ui = UIComponents()
        self.init_session_state()
    
    def init_session_state(self):
        """Initialize session state variables"""
        if 'page' not in st.session_state:
            st.session_state.page = 'signup'
        if 'student_info' not in st.session_state:
            st.session_state.student_info = {}
        if 'test_generated' not in st.session_state:
            st.session_state.test_generated = False
        if 'test_content' not in st.session_state:
            st.session_state.test_content = ""
    
    def render_signup_page(self):
        """Render the signup page"""
        st.markdown('<div class="section-header">Welcome! Please fill out your information:</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            with st.form("student_signup"):
                st.subheader("Student Information")
                first_name = st.text_input("First Name *", placeholder="Enter your first name")
                last_name = st.text_input("Last Name *", placeholder="Enter your last name")
                class_options = self.info_manager.get_class_options()
                class_level = st.selectbox("Current Grade Level *", class_options, index=5)
                age = st.number_input("Age", min_value=5, max_value=19, value=11)
                submit_button = st.form_submit_button("Complete Registration", type="primary")
                if submit_button:
                    if self.info_manager.validate_required_fields(first_name, last_name, class_level):
                        st.session_state.student_info = self.info_manager.create_student_info(
                            first_name, last_name, class_level, age
                        )
                        st.session_state.page = 'test_ready'
                        st.rerun()
                    else:
                        st.error("Please fill in all required fields marked with *")
        with col2:
            self.ui.render_info_panel()
    
    def render_test_ready_page(self):
        """Render the test ready page"""
        self.ui.render_welcome_message(
            st.session_state.student_info['first_name'],
            st.session_state.student_info['class_level']
        )
        self.ui.render_student_summary(st.session_state.student_info)
        self.ui.render_test_instructions()
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("📝 Take Test Now", type="primary", use_container_width=True):
                st.session_state.page = 'test'
                st.rerun()
        with col2:
            if st.button("✏️ Edit Information", use_container_width=True):
                st.session_state.page = 'signup'
                st.rerun()
        with col3:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.clear()
                st.rerun()
    
    def render_test_page(self):
        """Render the test page with DARK MODE compatibility"""
        # Header
        st.markdown(f"### 📋 Screening Test - {st.session_state.student_info['class_level']}")
        st.markdown(f"**Student:** {st.session_state.student_info['first_name']} {st.session_state.student_info['last_name']}")
        
        # Instructions
        with st.expander("📋 Test Instructions", expanded=False):
            st.markdown("""
            - **Read each question carefully** before selecting an answer
            - **Click the radio button** to select your answer for each question
            - **Only one answer per question** - selecting a new option will deselect the previous one
            - **Take your time** - there's no time limit
            - **Use scratch paper** for calculations if needed
            - **Ask for help** if you need clarification on instructions
            """)
        
        if not st.session_state.test_generated:
            try:
                with st.spinner("🤖 Loading model and generating your personalized MCQ test... This may take a moment."):
                    generator = get_test_generator()
                    test_content = generator.generate_test(st.session_state.student_info['class_level'])
                    if test_content:
                        st.session_state.test_content = test_content
                        st.session_state.test_generated = True
                    else:
                        st.error("Failed to generate test. Please try again.")
                        self.render_test_error_buttons()
                        return
            except Exception as e:
                st.error(f"Error generating test: {e}")
                self.render_test_error_buttons()
                return
        
        if st.session_state.test_content:
            # Display test content with DARK MODE compatibility
            st.markdown('<div class="test-content">', unsafe_allow_html=True)
            st.markdown(st.session_state.test_content, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("""
            <script>
            function initializeRadioButtons() {
                // Add event listeners to all radio buttons
                document.querySelectorAll('input[type="radio"]').forEach(radio => {
                    radio.addEventListener('change', function() {
                        // Remove selected class from all options of this question
                        const questionName = this.name;
                        document.querySelectorAll(`input[name="${questionName}"]`).forEach(r => {
                            r.closest('.mcq-option').classList.remove('selected');
                        });
                        // Add selected class to chosen option
                        this.closest('.mcq-option').classList.add('selected');
                    });
                });
                
                // Make label clicks work
                document.querySelectorAll('.mcq-option-text').forEach(label => {
                    label.addEventListener('click', function() {
                        const radio = this.previousElementSibling;
                        if (radio && radio.type === 'radio') {
                            radio.checked = true;
                            radio.dispatchEvent(new Event('change'));
                        }
                    });
                });
            }
            
            // Initialize on page load
            document.addEventListener('DOMContentLoaded', initializeRadioButtons);
            
            // Re-initialize after content updates
            setTimeout(initializeRadioButtons, 1000);
            setTimeout(initializeRadioButtons, 2000);
            setTimeout(initializeRadioButtons, 3000);
            </script>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown('<div class="progress-container">', unsafe_allow_html=True)
            st.markdown("### 📊 Test Status")
            st.progress(1.0)
            st.markdown("✅ **Test loaded successfully! Click the radio buttons to select your answers above.**")
            st.markdown('</div>', unsafe_allow_html=True)
            
            self.render_test_completion_buttons()
    
    def render_test_error_buttons(self):
        """Render error buttons for test generation failure"""
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Try Again", type="primary", use_container_width=True):
                st.session_state.test_generated = False
                st.session_state.test_content = ""
                st.rerun()
        with col2:
            if st.button("🏠 Back to Setup", use_container_width=True):
                st.session_state.page = 'test_ready'
                st.rerun()
    
    def render_test_completion_buttons(self):
        """Render test completion buttons"""
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("📤 Submit Test", type="primary", use_container_width=True):
                st.balloons()
                st.success("✅ **Test submitted successfully! Thank you for completing the screening test.**")
                self.collect_answers()
        with col2:
            if st.button("🔄 Generate New Test", use_container_width=True):
                st.session_state.test_generated = False
                st.session_state.test_content = ""
                st.rerun()
        with col3:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.session_state.clear()
                st.rerun()
    
    def collect_answers(self):
        """Collect and display selected answers"""
        st.markdown("### 📝 Answer Summary")
        st.info("**Your test responses have been recorded.** In a real application, the selected answers would be processed and scored automatically.")
        
        st.markdown("""
        <script>
        function getSelectedAnswers() {
            const answers = {};
            let totalQuestions = 0;
            let answeredQuestions = 0;
            
            document.querySelectorAll('input[type="radio"]:checked').forEach(radio => {
                answers[radio.name] = {
                    value: radio.value,
                    text: radio.nextElementSibling.textContent
                };
                answeredQuestions++;
            });
            
            // Count total questions
            const questionNames = new Set();
            document.querySelectorAll('input[type="radio"]').forEach(radio => {
                questionNames.add(radio.name);
            });
            totalQuestions = questionNames.size;
            
            console.log('Selected Answers:', answers);
            console.log(`Answered: ${answeredQuestions}/${totalQuestions} questions`);
            
            return {answers, totalQuestions, answeredQuestions};
        }
        
        // Auto-collect answers
        const results = getSelectedAnswers();
        console.log('Test Results:', results);
        </script>
        """, unsafe_allow_html=True)
    
    def render_current_page(self):
        """Render the current page based on session state"""
        self.ui.render_header()
        if st.session_state.page == 'signup':
            self.render_signup_page()
        elif st.session_state.page == 'test_ready':
            self.render_test_ready_page()
        elif st.session_state.page == 'test':
            self.render_test_page()

def main():
    """Main application function"""
    page_manager = PageManager()
    page_manager.render_current_page()

if __name__ == "__main__":
    main()
