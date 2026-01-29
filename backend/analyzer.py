from sentence_transformers import SentenceTransformer, util
import torch
import fitz  # PyMuPDF

# Load a lightweight, free model
# all-MiniLM-L6-v2 is fast and accurate for semantic similarity
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file using PyMuPDF."""
    text = ""
    try:
        print(f"Attempting to extract text from: {file_path}")
        with fitz.open(file_path) as doc:
            print(f"PDF opened. Pages: {len(doc)}")
            for i, page in enumerate(doc):
                page_text = page.get_text().strip()
                if page_text:
                    text += page_text + "\n"
                else:
                    print(f"Warning: Page {i} appears to be empty or image-based.")
        
        final_text = text.strip()
        print(f"Extraction complete. Characters extracted: {len(final_text)}")
        return final_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def analyze_resume(resume_text, job_description):
    """
    Analyzes the resume against the job description using a weighted scoring system.
    Score = 70% Semantic Similarity + 30% Keyword Matching.
    """
    
    # 1. Compute Semantic Similarity (70% of total score)
    embeddings = model.encode([resume_text, job_description], convert_to_tensor=True)
    cosine_score = util.cos_sim(embeddings[0], embeddings[1])
    semantic_score = float(cosine_score[0][0]) * 100
    
    # 2. Keyword Matching (30% of total score)
    common_skills = {
        "python", "javascript", "react", "fastapi", "sql", "aws", "docker", 
        "kubernetes", "machine learning", "data analysis", "c++", "java", 
        "typescript", "node.js", "graphql", "rest api", "git", "ci/cd",
        "aws lambda", "terraform", "django", "flask", "postgresql", "redis",
        "pandas", "numpy", "pytorch", "tensorflow", "scikit-learn"
    }
    
    jd_skills = []
    resume_skills = []
    missing_skills = []
    
    jd_lower = job_description.lower()
    resume_lower = resume_text.lower()
    
    for skill in common_skills:
        if skill in jd_lower:
            jd_skills.append(skill)
            if skill in resume_lower:
                resume_skills.append(skill)
            else:
                missing_skills.append(skill.upper())
    
    if jd_skills:
        keyword_score = (len(resume_skills) / len(jd_skills)) * 100
    else:
        keyword_score = 100 
        
    # 3. Balanced Weighted Score
    final_score = (semantic_score * 0.7) + (keyword_score * 0.3)
    final_score = round(max(0, min(100, final_score)), 1)

    # 4. Improvement Tips
    tips = []
    if semantic_score < 60:
        tips.append("The overall language of your resume doesn't strongly align with this job. Use more industry-specific terminology.")
    
    if len(missing_skills) > 0:
        tips.append(f"Essential skills like {', '.join(missing_skills[:3])} are missing. Consider adding these if you have relevant experience.")
    
    if keyword_score < 50 and semantic_score > 70:
        tips.append("Your resume has the right context, but is missing specific tool keywords. Mention your tech stack explicitly.")

    if len(resume_text) < 500:
        tips.append("Your resume is quite brief. Elaborate on your projects and concrete achievements to increase your score.")

    if not tips:
        tips.append("Excellent alignment! Ensure you use quantifiable metrics (e.g., 'Reduced latency by 15%') to further distinguish yourself.")

    return {
        "match_score": final_score,
        "missing_skills": missing_skills,
        "improvement_tips": tips
    }
