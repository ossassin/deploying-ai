from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import os

# Manually gathered the data from here: https://capd.mit.edu/resources/make-a-career-plan/

career_plan_content = [
    "Step 1: Identify Your Career Options. Develop a refined list of career options by examining your interests, skills, and values through self-assessment. Narrow your career options by reviewing career information, researching companies, and talking to professionals in the field. You can further narrow your list when you take part in experiences such as shadowing, volunteering, and internships.",
    
    "Step 2: Prioritize. It's not enough to list options. You have to prioritize. What are your top skills? What interests you the most? What's most important to you? Whether it's intellectually challenging work, family-friendly benefits, the right location or a big paycheck, it helps to know what matters to you and what's a deal-breaker.",
    
    "Step 3: Make Comparisons. Compare your most promising career options against your list of prioritized skills, interests and values.",
    
    "Step 4: Consider Other Factors. Consider factors beyond personal preferences. What is the current demand for this field? If the demand is low or entry is difficult, are you comfortable with risk? What qualifications are required to enter the field? Will it require additional education or training? How will selecting this option affect you and others in your life? Gather advice from friends, colleagues, and family members. Consider potential outcomes and barriers for each of your final options.",
    
    "Step 5: Make a Choice. Choose the career paths that are best for you. How many paths you choose depends upon your situation and comfort level. If you're early in your planning, then identifying multiple options may be best. Conversely, narrowing to one or two options may better focus your job search or graduate school applications.",
    
    "Step 6: Set SMART Goals. Develop an action plan to implement your decision. Set short-term goals to be achieved in one year or less and long-term goals to be achieved in one to five years. Goals should be Specific, Measurable, Attainable, Relevant, and Time-bound.",
    
    "Step 7: Create Your Career Action Plan. Be realistic about expectations and timelines. Write down specific action steps to achieve your goals and help yourself stay organized. Check them off as you complete them, but feel free to amend your career action plan as needed. Your goals and priorities may change, and that's perfectly okay.",
    
    "Step 8: Meet with a Career Advisor. Career advisors can help you make effective career decisions. Talk about your career options and concerns with a professional.",
    
    "A career plan lists short- and long-term career goals and the actions you can take to achieve them. Career plans can help you make decisions about what classes to take, and identify the extracurricular activities, research, and internships that will make you a strong job candidate."
]

chunks = career_plan_content

embedding_fn = OpenAIEmbeddingFunction(
    api_key="any value",
    api_base="https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1",
    model_name="text-embedding-3-small",
    default_headers={"x-api-key": os.getenv('API_GATEWAY_KEY')}
)

chroma_client = chromadb.HttpClient(host="http://localhost:8000")

# Delete old collection if it exists
try:
    chroma_client.delete_collection(name="career_plan")
except:
    pass

# Create with embedding function — Chroma handles embedding automatically
collection = chroma_client.create_collection(
    name="career_plan", 
    embedding_function=embedding_fn
)

ids = [f"step_{i}" for i in range(len(chunks))]

# No need to pass embeddings — Chroma will use embedding_fn automatically
collection.add(documents=chunks, ids=ids)