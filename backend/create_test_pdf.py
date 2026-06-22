from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Create a PDF
pdf_path = "sample_document.pdf"
c = canvas.Canvas(pdf_path, pagesize=letter)

# Add title
c.setFont("Helvetica-Bold", 20)
c.drawString(50, 750, "Introduction to Machine Learning")

# Add content
c.setFont("Helvetica", 12)
y = 700
content = """
Machine Learning is a subset of artificial intelligence that enables systems to learn 
and improve from experience without being explicitly programmed.

Key Concepts:
1. Supervised Learning - Learning from labeled data
2. Unsupervised Learning - Finding patterns in unlabeled data
3. Reinforcement Learning - Learning through interaction with environment

Applications:
- Image recognition
- Natural language processing
- Recommendation systems
- Autonomous vehicles
- Fraud detection

Benefits:
- Automates decision-making
- Improves efficiency
- Enables new capabilities
- Processes large datasets quickly

Challenges:
- Requires large amounts of data
- Can be computationally expensive
- May introduce bias
- Requires skilled engineers

Machine learning is transforming industries and creating new opportunities 
for innovation and growth.
"""

for line in content.split('\n'):
    c.drawString(50, y, line)
    y -= 20

c.save()
print(f"✓ Created: {pdf_path}")