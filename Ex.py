
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, ListFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import inch
import io
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Exercise Library PDF Generator",
    page_icon="ðŸ’ª",
    layout="centered"
)

# Title
st.title("ðŸ’ª Exercise Library PDF Generator")
st.markdown("Generate a professional 4-page PDF with categorized exercises")

# Sidebar for customization
st.sidebar.header("âš™ï¸ Customization Options")

# Number of exercises per category
num_ab_exercises = st.sidebar.slider("Ab Exercises", 10, 100, 100, 5)
num_bodyweight_exercises = st.sidebar.slider("Bodyweight Exercises", 10, 100, 100, 5)
num_strength_exercises = st.sidebar.slider("Strength Training Exercises", 10, 100, 100, 5)

# Custom notes
custom_notes = st.sidebar.text_area(
    "Custom Notes (Page 4)",
    "Use this page to write workout plans or coaching notes.",
    height=100
)

# Function to create numbered list
def numbered_list(items, text_style):
    """Create a numbered list from items"""
    try:
        list_items = [Paragraph(item, text_style) for item in items]
        return ListFlowable(
            list_items,
            bulletType='1',
            start=1,
            leftIndent=20,
            bulletFontSize=10
        )
    except Exception as e:
        st.error(f"Error creating list: {str(e)}")
        return None

# Function to generate PDF
def generate_pdf(num_abs, num_bodyweight, num_strength, notes_text):
    """Generate the exercise PDF"""
    try:
        # Create a buffer to store PDF
        buffer = io.BytesIO()

        # Setup styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        header_style = styles['Heading2']
        text_style = styles['BodyText']

        # Custom style for better formatting
        text_style.fontSize = 10
        text_style.leading = 14
        text_style.alignment = TA_LEFT

        # Generate exercise lists
        abs_exercises = [f"Ab Exercise {i}" for i in range(1, num_abs + 1)]
        bodyweight_exercises = [f"Bodyweight Exercise {i}" for i in range(1, num_bodyweight + 1)]
        strength_exercises = [f"Strength Training Exercise {i}" for i in range(1, num_strength + 1)]

        # Build PDF content
        story = []

        # Title page content
        story.append(Paragraph("Exercise Library", title_style))
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", text_style))
        story.append(Spacer(1, 0.5 * inch))

        # Page 1 - Ab Exercises
        story.append(Paragraph(f"Page 1 â€“ Ab Exercises (1â€“{num_abs})", header_style))
        story.append(Spacer(1, 0.2 * inch))
        abs_list = numbered_list(abs_exercises, text_style)
        if abs_list:
            story.append(abs_list)
        story.append(PageBreak())

        # Page 2 - Bodyweight Exercises
        story.append(Paragraph(f"Page 2 â€“ Bodyweight Exercises (1â€“{num_bodyweight})", header_style))
        story.append(Spacer(1, 0.2 * inch))
        bodyweight_list = numbered_list(bodyweight_exercises, text_style)
        if bodyweight_list:
            story.append(bodyweight_list)
        story.append(PageBreak())

        # Page 3 - Strength Training
        story.append(Paragraph(f"Page 3 â€“ Strength Training Exercises (1â€“{num_strength})", header_style))
        story.append(Spacer(1, 0.2 * inch))
        strength_list = numbered_list(strength_exercises, text_style)
        if strength_list:
            story.append(strength_list)
        story.append(PageBreak())

        # Page 4 - Notes
        story.append(Paragraph("Page 4 â€“ Notes", header_style))
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph(notes_text, text_style))

        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Build the PDF
        doc.build(story)

        # Get PDF data from buffer
        pdf_data = buffer.getvalue()
        buffer.close()

        return pdf_data

    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return None

# Main content area
st.markdown("---")

# Preview section
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Ab Exercises", num_ab_exercises)
with col2:
    st.metric("Bodyweight Exercises", num_bodyweight_exercises)
with col3:
    st.metric("Strength Exercises", num_strength_exercises)

st.markdown("---")

# Generate button
if st.button("ðŸš€ Generate PDF", type="primary", use_container_width=True):
    with st.spinner("Generating your PDF..."):
        pdf_data = generate_pdf(
            num_ab_exercises,
            num_bodyweight_exercises,
            num_strength_exercises,
            custom_notes
        )

        if pdf_data:
            st.success("âœ… PDF generated successfully!")

            # Download button
            st.download_button(
                label="ðŸ“¥ Download PDF",
                data=pdf_data,
                file_name=f"exercise_library_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

            st.balloons()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 12px;'>
    ðŸ’ª Exercise Library PDF Generator | Built with Streamlit & ReportLab
    </div>
    """,
    unsafe_allow_html=True
)
