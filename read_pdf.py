import sys, subprocess
try:
    import fitz
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymupdf", "--quiet"])
    import fitz

doc = fitz.open("smartengine_kit2_sprint2.pdf")
text = ""
for page in doc:
    text += page.get_text() + "\n"

with open("pdf_text.txt", "w", encoding="utf-8") as f:
    f.write(text)
