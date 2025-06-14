import streamlit as st
import PyPDF2
import re

# Role-specific rich keyword sets
ROLE_KEYWORDS = {
    "Developer": ["python", "java", "c++", "react", "node", "docker", "git", "api", "backend", "frontend", "typescript", "graphql"],
    "Data Scientist": ["python", "machine learning", "pandas", "numpy", "statistics", "modeling", "ai", "deep learning", "tensorflow", "pytorch", "visualization"],
    "Designer": ["figma", "adobe xd", "photoshop", "illustrator", "ui", "ux", "design system", "wireframe", "prototype", "accessibility", "user research"],
    "Product Manager": ["roadmap", "agile", "scrum", "stakeholder", "vision", "kpi", "strategy", "backlog", "okrs", "mvp"],
    "Marketing": ["seo", "branding", "analytics", "campaign", "content", "engagement", "lead generation", "social media", "paid ads", "conversion"],
    "Cybersecurity": ["penetration testing", "threat analysis", "incident response", "encryption", "firewall", "vulnerability", "zero trust", "siem"],
    "AI Engineer": ["deep learning", "neural networks", "nlp", "computer vision", "mlops", "tensorflow", "pytorch", "model deployment", "generative ai"],
}

ACTION_VERBS = [
    "developed", "designed", "led", "created", "implemented", "analyzed",
    "managed", "built", "optimized", "improved", "delivered", "architected"
]

def grade_resume(text, role_keywords):
    text_lower = text.lower()
    feedback = []
    score = 0

    # Check contact info
    if re.search(r'\S+@\S+', text_lower) and re.search(r'\d{7,}', text_lower):
        score += 5
        feedback.append("✅ Contact information is complete.")
    else:
        feedback.append("⚠️ Include both email and phone number clearly.")

    # Check sections
    sections = ["education", "experience", "skills", "projects", "summary"]
    found_sections = [sec for sec in sections if sec in text_lower]
    score += len(found_sections) * 2  # 2 points per section
    if len(found_sections) < len(sections):
        missing = set(sections) - set(found_sections)
        feedback.append(f"⚠️ Add missing sections: {', '.join(missing).title()}")

    # Action verbs
    verbs_found = [v for v in ACTION_VERBS if v in text_lower]
    if verbs_found:
        score += 5
        feedback.append(f"✅ Good use of action verbs like: {', '.join(verbs_found[:3])}.")
    else:
        feedback.append("⚠️ Use powerful action verbs to strengthen achievements.")

    # Numbers / metrics
    if re.search(r'\d+%', text) or re.search(r'\d+[km]?', text):
        score += 5
        feedback.append("✅ Includes measurable impact (numbers/metrics).")
    else:
        feedback.append("⚠️ Add numbers or metrics to quantify achievements.")

    # Keyword match
    keyword_hits = [kw for kw in role_keywords if kw in text_lower]
    hit_ratio = len(keyword_hits) / len(role_keywords) if role_keywords else 0
    role_score = int(hit_ratio * 70)
    score += role_score

    if hit_ratio >= 0.6:
        feedback.append(f"✅ Strong match to role keywords ({len(keyword_hits)}/{len(role_keywords)}).")
    elif hit_ratio >= 0.3:
        feedback.append(f"⚠️ Moderate match ({len(keyword_hits)}/{len(role_keywords)}). Add more relevant terms.")
    else:
        feedback.append(f"⚠️ Weak match ({len(keyword_hits)}/{len(role_keywords)}).")

    # Length
    word_count = len(text.split())
    if word_count >= 100:
        score += 5
        feedback.append("✅ Resume length is appropriate.")
    else:
        feedback.append("⚠️ Consider expanding your resume. Aim for 100+ words.")

    return min(score, 100), feedback, keyword_hits

# --- Streamlit App ---
st.set_page_config(page_title="🏆 Hackathon Resume Grader", layout="wide")

st.markdown("""
<style>
h1 {color: #4CAF50;}
.feedback { background: #f7f7f7; padding: 8px; border-radius: 5px; margin: 5px 0; }
.matched { color: #2196F3; font-weight: bold; }
.badge { padding: 0.3em 0.6em; background: #4CAF50; color: white; border-radius: 5px; font-size: 90%; }
</style>
""", unsafe_allow_html=True)

st.title("🏆 Smart Resume Grader")

col1, col2 = st.columns([1,2])

with col1:
    role = st.selectbox("🎯 Target Role", list(ROLE_KEYWORDS.keys()))
    file = st.file_uploader("📤 Upload your resume (PDF only)", type=["pdf"])

with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/1006/1006771.png", width=180)

if file:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    st.subheader("📑 Extracted Text")
    st.text_area("Extracted resume text:", text, height=250)

    if st.button("🚀 Grade Now"):
        keywords = ROLE_KEYWORDS[role]
        score, feedbacks, matched = grade_resume(text, keywords)

        st.subheader("🎯 Resume Score")
        st.progress(score)
        st.markdown(f"<span class='badge'>Score: {score}/100</span>", unsafe_allow_html=True)

        st.subheader("📌 Feedback")
        for f in feedbacks:
            st.markdown(f"<div class='feedback'>{f}</div>", unsafe_allow_html=True)

        if matched:
            st.subheader("🔑 Matched Keywords")
            st.markdown(" ".join([f"<span class='matched'>{m}</span>" for m in matched]), unsafe_allow_html=True)
        else:
            st.warning("No role-specific keywords matched. Consider adding relevant skills/tools.")
