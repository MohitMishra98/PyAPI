from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY","")

client = Groq(api_key=GROQ_API_KEY)

RESUME = """
Alex Carter
Software Engineer

SUMMARY
Software engineer with 3 years of experience building backend services and AI-powered applications. Experienced in Python, FastAPI, REST APIs, PostgreSQL, Docker, and cloud deployment. Comfortable working with large language models, retrieval-augmented generation, and asynchronous processing systems.

SKILLS
- Programming: Python, JavaScript, SQL
- Backend: FastAPI, Django, REST APIs, Pydantic
- Databases: PostgreSQL, MongoDB, Redis
- AI/ML: LLMs, RAG, LangChain, embeddings, vector databases
- Cloud & DevOps: Docker, AWS, GitHub Actions, Linux
- Tools: Git, GitHub, Postman

EXPERIENCE

Software Engineer | TechNova Labs
2023 - Present
- Developed REST APIs using Python and FastAPI for a SaaS platform.
- Designed PostgreSQL database schemas and optimized SQL queries.
- Built asynchronous background jobs using Redis and Celery.
- Integrated third-party AI APIs into customer-facing applications.
- Developed a document-question-answering system using RAG and vector embeddings.
- Containerized applications using Docker and deployed services on AWS.
- Implemented automated testing and CI/CD pipelines using GitHub Actions.

Junior Backend Developer | CloudPeak Solutions
2022 - 2023
- Built backend services using Python and Django.
- Created REST APIs for web and mobile applications.
- Worked with PostgreSQL and Redis.
- Fixed production bugs and improved API response times.
- Collaborated with frontend developers and QA engineers.

PROJECTS

AI Document Assistant
- Built an AI assistant that answers questions about uploaded PDF documents.
- Used Python, FastAPI, embeddings, a vector database, and an LLM API.
- Implemented document chunking, semantic search, and retrieval-augmented generation.

Task Management API
- Developed a REST API with authentication, role-based access control, and CRUD operations.
- Used FastAPI, PostgreSQL, SQLAlchemy, and Docker.

EDUCATION
Bachelor of Technology in Computer Science
State Institute of Technology
2022

CERTIFICATIONS
- AWS Cloud Practitioner
- Python Programming Certificate
"""

JD = """
Backend Engineer - AI Platform

ABOUT THE ROLE
We are looking for a Backend Engineer to join our AI Platform team. The engineer will build scalable backend services that power AI and machine-learning applications.

RESPONSIBILITIES
- Design and develop production-grade backend services using Python and FastAPI.
- Build and maintain REST APIs and asynchronous background processing systems.
- Design and optimize PostgreSQL database schemas and queries.
- Integrate large language models and third-party AI APIs into backend services.
- Develop retrieval-augmented generation (RAG) pipelines and AI-powered applications.
- Work with vector databases and embedding-based search.
- Containerize applications using Docker.
- Deploy and maintain services on AWS.
- Write unit and integration tests.
- Participate in code reviews and collaborate with frontend, ML, and DevOps engineers.
- Monitor and troubleshoot production services.

REQUIRED QUALIFICATIONS
- 2+ years of backend software development experience.
- Strong Python programming skills.
- Professional experience with FastAPI or similar Python web frameworks.
- Experience designing and consuming REST APIs.
- Strong knowledge of SQL and PostgreSQL.
- Experience with Docker and Linux.
- Familiarity with asynchronous programming and background job processing.
- Experience working with Git and CI/CD workflows.

PREFERRED QUALIFICATIONS
- Experience building applications using LLMs.
- Knowledge of RAG architectures and vector databases.
- Experience with LangChain or similar AI frameworks.
- Familiarity with AWS.
- Experience with Redis, Celery, or similar distributed task-processing systems.
- Understanding of automated testing and software architecture.

EDUCATION
Bachelor's degree in Computer Science, Software Engineering, or a related field.

LOCATION
Remote
""" 

def call_llm(system_prompt, user_prompt):
    model = "openai/gpt-oss-120b"
    system_prompt = {
        "role": "system",
        "content": system_prompt
    }
    user_prompt = {
        "role": "user",
        "content": user_prompt
    }
    messages = [system_prompt, user_prompt]
    response  = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content


def step1_extarct_skills_resume(RESUME):
    system_prompt = """
    Role:
    You are a professional HR executive and your role is to exract the skills from candidate's resume

    Task:
    I will provide you with the candidate's resume and you have to extract all the skills from that resume
    
    Conatrains:
    do not invent any new information by yourself only provide what is mentioned in the resume

    Output Format:
    all skills are seperated by a ,
    """

    user_prompt = f"""
    Here is the resume please extract the skills:
    {RESUME}
    """

    return call_llm(system_prompt, user_prompt)

def step2_extarct_skills_jd(JD):
    system_prompt = """
    Role:
    You are a professional HR executive and your role is to exract the skills from provided JD

    Task:
    I will provide you with the job's JD and you have to extract all the skills that a candidate must have from that JD
    
    Conatrains:
    do not invent any new information by yourself only provide what is mentioned in the JD

    Output Format:
    all skills are seperated by a ,
    """

    user_prompt = f"""
    Here is the JD please extract the skills:
    {JD}
    """

    return call_llm(system_prompt, user_prompt)

def match_resume(candidate_skills, jd_skills):
    system_prompt = f""""
    Role:
    You are a professsional HR executive responsible for selecting candidates

    Task:
    You will be provided with candidate's skills and job's skills and you have to match both the skills to find if the candidate is a good fit for the job role or not also give a matching score
    
    Output format:
    please give the response in this specific format
    score: candidate's mathcing score
    verdict: 
    reason: 
    """

    user_prompt = f"""
    here is the candidates skills and JD skills plese match them

    Candidate skills : {candidate_skills}

    JD skills: {jd_skills}
    """

    return call_llm(system_prompt, user_prompt)

print("=="*50)
candidate_skills = step1_extarct_skills_resume(RESUME)
print(candidate_skills)

print("=="*50)
jd_skills = step2_extarct_skills_jd(JD)
print(jd_skills)

print("=="*50)
match_score = match_resume(candidate_skills, jd_skills)
print(match_score)