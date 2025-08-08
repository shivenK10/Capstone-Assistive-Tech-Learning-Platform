# generation_pipeline.py

from model_loading import ModelLoader
from transformers import pipeline
from peft import PeftModel
import warnings
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_community.llms import HuggingFacePipeline
from logger import Logger
import re

warnings.filterwarnings("ignore")

class TestGenerator:
    def __init__(self):
        self.logger = Logger(
            name="TestGenerator",
            log_file_needed=True,
            log_file_path="Logs/test_generator.log",
            level="DEV"
        )
        self.logger.debug("Initializing TestGenerator")

        self.BASE_MODEL = "meta-llama/Llama-3.2-3B-Instruct"
        self.LORA_PATH = "llama3.2-past-lora"
        self.DEVICE = "mps"
        self.model_loaded = False
        self.gen_pipe = None
        self.langchain_llm = None
        self.output_parser = None
        self.prompt_template = None

        self.logger.debug("Setting up output parser")
        self._setup_output_parser()
        self.logger.debug("Setting up prompt template")
        self._setup_prompt_template()

    def _setup_output_parser(self):
        """Setup structured output parser for test generation"""
        response_schemas = [
            ResponseSchema(name="l1_questions", description="List of 5 L1 (Remembering) level MCQ questions with options"),
            ResponseSchema(name="l2_questions", description="List of 5 L2 (Understanding) level MCQ questions with options"),
            ResponseSchema(name="l3_questions", description="List of 5 L3 (Applying) level MCQ questions with options"),
            ResponseSchema(name="l4_questions", description="List of 5 L4 (Analyzing) level MCQ questions with options"),
            ResponseSchema(name="reading_passage", description="Reading comprehension passage of approximately 100 words"),
            ResponseSchema(name="passage_questions", description="MCQ questions based on the reading passage with options")
        ]
        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        self.logger.debug("Output parser configured with schemas")

    def _setup_prompt_template(self):
        """Setup LangChain prompt template with strict MCQ format"""
        template = """
You are an expert educational assessment creator. Create a comprehensive screening test for {class_level} students based on Bloom's Taxonomy levels.

CRITICAL REQUIREMENT: EVERY SINGLE QUESTION MUST BE IN MULTIPLE CHOICE FORMAT WITH EXACTLY 4 OPTIONS (a, b, c, d). NO EXCEPTIONS.

**Section L1: Remembering (Knowledge Recall)**
Create exactly 5 MCQ questions:
- 2 phonological awareness questions (syllable counting, sound identification)
- 2 mathematics questions ({math_complexity} number operations)
- 1 vocabulary recall question

Format each question EXACTLY like this example:
1. How many syllables are in the word "elephant"?
a) 2
b) 3
c) 4
d) 5

**Section L2: Understanding (Comprehension)**
Create exactly 5 MCQ questions:
- 2 phonological awareness questions (sound manipulation, rhyming patterns)
- 2 mathematics word problems requiring interpretation
- 1 vocabulary comprehension question

**Section L3: Applying (Application)**
Create exactly 5 MCQ questions:
- 1 phonological awareness application (creating words with specific sounds)
- 3 mathematics application problems (real-world scenarios)
- 1 vocabulary application question

**Section L4: Analyzing (Analysis)**
Create exactly 5 MCQ questions:
- 1 phonological awareness analysis (comparing sound patterns)
- 3 mathematics analysis problems (problem-solving strategies)
- 1 vocabulary analysis question

**Reading Comprehension Section:**

### Reading Passage:
Write ONE passage of approximately 100 words appropriate for {reading_level} readers.

### Passage-Based MCQ Questions:
Create exactly 5 multiple-choice questions with a), b), c), d) options testing:
- Main idea identification
- Detail recall
- Inference making
- Vocabulary in context
- Author's purpose/tone

**STRICT FORMATTING RULES:**
- Label each section clearly: "Section L1: Remembering", "Section L2: Understanding", etc.
- Number questions 1-5 in each section
- Every question must have exactly 4 options: a), b), c), d)
- Put each option on a new line
- Use age-appropriate language for {class_level}
- Mathematical problems should use {math_complexity} numbers

**MANDATORY QUESTION FORMAT:**
[Number]. [Question text]
a) [Option 1]
b) [Option 2]
c) [Option 3]
d) [Option 4]

Generate the complete test with ALL questions in MCQ format:
"""
        self.prompt_template = PromptTemplate(
            template=template,
            input_variables=["class_level", "reading_level", "math_complexity"]
        )
        self.logger.debug("Enhanced prompt template configured")

    def load_model(self):
        """Load the base and LoRA-fused model, wrap in a text-generation pipeline"""
        if self.model_loaded:
            self.logger.debug("Model already loaded, skipping")
            return

        try:
            self.logger.debug(f"Loading base model: {self.BASE_MODEL} on device: {self.DEVICE}")
            loader = ModelLoader(self.BASE_MODEL, quantize=False, device=self.DEVICE)
            base_model, tokenizer, device = loader.load_model()

            self.logger.debug("Loading and merging LoRA weights")
            model = PeftModel.from_pretrained(base_model, self.LORA_PATH)
            model = model.merge_and_unload()

            self.logger.debug("Creating HuggingFace text-generation pipeline")
            self.gen_pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=8000,
                do_sample=True,
                temperature=0.1,
                top_p=None,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.eos_token_id,
                return_full_text=False,
                repetition_penalty=1.02,
            )
            self.langchain_llm = HuggingFacePipeline(pipeline=self.gen_pipe)

            self.model_loaded = True
            self.logger.debug("Model and pipeline successfully loaded")
        except Exception as e:
            self.logger.error(f"load_model failed: {e}")
            raise

    def get_class_parameters(self, class_level: str) -> dict:
        """Return reading and math complexity for a given grade"""
        self.logger.debug(f"Determining parameters for class_level='{class_level}'")
        if class_level in ["1st Grade", "2nd Grade"]:
            params = {"reading_level": "1st-grade", "math_complexity": "single-digit"}
        elif class_level in ["3rd Grade", "4th Grade"]:
            params = {"reading_level": "2nd-grade", "math_complexity": "two-digit"}
        elif class_level in ["5th Grade", "6th Grade"]:
            params = {"reading_level": "3rd-grade", "math_complexity": "two-digit"}
        elif class_level in ["7th Grade", "8th Grade"]:
            params = {"reading_level": "4th-grade", "math_complexity": "three-digit"}
        else:  # High school
            params = {"reading_level": "5th-grade", "math_complexity": "multi-digit"}
        self.logger.debug(f"Class parameters: {params}")
        return params

    def parse_generated_output(self, raw_output: str) -> str:
        """Parse raw text into formatted markdown for the test"""
        self.logger.debug("Parsing generated output")
        return self._direct_format_output(raw_output)

    def _direct_format_output(self, raw_output: str) -> str:
        """Enhanced formatting with interactive MCQ structure and proper headings"""
        formatted = []
        lines = raw_output.splitlines()
        i = 0
        question_counter = 0
        
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            if any(sec in line for sec in ("Section L1:", "Section L2:", "Section L3:", "Section L4:")):
                formatted.append(f'\n<h2 class="section-heading">{line}</h2>')
                
            elif "Reading Comprehension Section" in line:
                formatted.append(f'\n<h2 class="section-heading">{line}</h2>')
                
            elif line.startswith("Reading Passage:"):
                formatted.append(f'\n<h3 class="subsection-heading">{line}</h3>')
                i += 1
                passage_content = []
                while i < len(lines) and not lines[i].strip().startswith(("Passage-Based", "1.", "2.", "3.", "4.", "5.")):
                    if lines[i].strip():
                        passage_content.append(lines[i].strip())
                    i += 1
                if passage_content:
                    formatted.append('<div class="reading-passage">')
                    formatted.append(' '.join(passage_content))
                    formatted.append('</div>')
                i -= 1  # Adjust for the outer loop increment
                
            elif "Passage-Based" in line and "Questions" in line:
                formatted.append(f'\n<h3 class="subsection-heading">{line}</h3>')
                
            elif re.match(r'^\d+\.', line):
                question_counter += 1
                formatted.append('<div class="mcq-container">')
                formatted.append(f'<div class="mcq-question">{line}</div>')
                
                i += 1
                options_found = 0
                option_labels = ['a', 'b', 'c', 'd']
                
                while i < len(lines) and options_found < 4:
                    option_line = lines[i].strip()
                    if re.match(r'^[a-d]\)', option_line):
                        option_id = f"q{question_counter}_{option_labels[options_found]}"
                        formatted.append(f'<div class="mcq-option">')
                        formatted.append(f'<input type="radio" id="{option_id}" name="question_{question_counter}" value="{option_labels[options_found]}">')
                        formatted.append(f'<label for="{option_id}" class="mcq-option-text">{option_line}</label>')
                        formatted.append('</div>')
                        options_found += 1
                    elif option_line and not re.match(r'^\d+\.', option_line):
                        if options_found > 0:
                            last_label_index = len(formatted) - 2
                            formatted[last_label_index] = formatted[last_label_index].replace('</label>', f' {option_line}</label>')
                    i += 1
                
                formatted.append('</div>')
                i -= 1
                
            else:
                if line and not re.match(r'^[a-d]\)', line):
                    formatted.append(line)
            
            i += 1
        
        return "\n".join(formatted)

    def generate_test(self, class_level: str) -> str:
        """Generate and return the formatted MCQ test for the given grade"""
        self.logger.debug(f"generate_test called for class_level='{class_level}'")
        if not self.model_loaded:
            self.load_model()

        params = self.get_class_parameters(class_level)
        prompt = self.prompt_template.format(
            class_level=class_level,
            reading_level=params["reading_level"],
            math_complexity=params["math_complexity"]
        )
        self.logger.debug(f"Formatted prompt (first 200 chars): {prompt[:200]}")

        try:
            response = self.langchain_llm(prompt)
            self.logger.debug(f"Raw response length: {len(response)}")
            test_md = self.parse_generated_output(response)
            self.logger.debug("Test generation and parsing succeeded")
            return test_md
        except Exception as e:
            self.logger.error(f"generate_test failed: {e}")
            raise

def generate_screening_test() -> str:
    """Generate a default screening test for 6th grade"""
    gen = TestGenerator()
    return gen.generate_test("6th Grade")

# For Streamlit caching
@st.cache_resource
def get_test_generator() -> TestGenerator:
    """Return a cached TestGenerator instance"""
    gen = TestGenerator()
    gen.load_model()
    return gen
