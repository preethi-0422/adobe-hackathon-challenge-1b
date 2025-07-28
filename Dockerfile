FROM python:3.10

WORKDIR /app
COPY analyze_pdfs.py .

RUN pip install PyMuPDF

CMD ["python", "analyze_pdfs.py"]
