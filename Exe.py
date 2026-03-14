import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, ListFlowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT
import io
from datetime import datetime

# Page config
st.set_page_config(page_title="Exercise PDF", layout="wide")

st.title("💪 Exercise Library PDF Generator")

# Sidebar controls
st.sidebar.header("⚙️ Settings")
num_exercises = st.sidebar.slider("Exercises per category", 20, 100, 50)
notes = st.sidebar.text_area("Page 4 Notes", "Your workout notes here...")

@st.cache_data
def generate_pdf(_num, _notes):
    buffer = io.BytesIO()
    
    # Styles
    styles = getSampleStyleSheet()
    title = styles['Title']
    header = styles['Heading2']
    body = styles['BodyText']
    
    # Exercise lists
    abs_ex = [f"Ab #{i}" for i in range(1, _num+1)]
    bodyweight_ex = [f"Bodyweight #{i}" for i in range(1, _num+1)]
    strength_ex = [f"Strength #{i}" for i in range(1, _num+1)]
    
    story = []
    
    # Page 1
    story.extend([
        Paragraph("EXERCISE LIBRARY", title),
        Spacer(1, 20),
        Paragraph(f"Ab Exercises (1-{len(abs_ex)})", header),
        ListFlowable([Paragraph(item, body) for item in abs_ex], 
                    bulletType='1', leftIndent=20),
        PageBreak()
    ])
    
    # Page 2
    story.extend([
        Paragraph(f"Bodyweight Exercises (1-{len(bodyweight_ex)})", header),
        ListFlowable([Paragraph(item, body) for item in bodyweight_ex], 
                    bulletType='1', leftIndent=20),
        PageBreak()
    ])
    
    # Page 3
    story.extend([
        Paragraph(f"Strength Exercises (1-{len(strength_ex)})", header),
        ListFlowable([Paragraph(item, body) for item in strength_ex], 
                    bulletType='1', leftIndent=20),
        PageBreak()
    ])
    
    # Page 4
    story.extend([
        Paragraph("NOTES", header),
        Spacer(1, 20),
        Paragraph(_notes, body)
    ])
    
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

if st.button("🛠️ GENERATE PDF", use_container_width=True):
    with st.spinner("Creating PDF..."):
        pdf = generate_pdf(num_exercises, notes)
        st.download_button(
            "📥 DOWNLOAD PDF",
            pdf,
            f"exercises_{datetime.now().strftime('%Y%m%d')}.pdf",
            "application/pdf"
        )
        st.success("✅ PDF Ready!")
        st.balloons()
