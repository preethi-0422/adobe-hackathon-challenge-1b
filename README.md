# **Challenge 1b: Multi-Collection PDF Analysis Solution**

## Overview

This repository contains a solution for **Challenge 1b** of the Adobe India Hackathon 2025. The solution is designed to analyze multiple PDF document collections and extract relevant content tailored to specific personas and real-world use cases. The application is fully containerized using Docker and meets all performance, resource, and architecture constraints specified in the challenge guidelines.

---

## Features

- **Persona-based content extraction:** Analyzes PDFs to extract sections most relevant to the persona and task defined in each collection's input.
- **Importance ranking:** Each extracted section is ranked by relevance to the job to be done.
- **Multi-collection batch processing:** Automatically handles multiple, independent collections in one run.
- **Structured JSON output:** Results are saved in a standardized format, matching the provided schema.
- **Resource-aware & offline:** Runs efficiently on CPU, within memory limits, and without internet access at runtime.
- **Cross-platform:** Designed for AMD64 (x86_64) architecture.

---

## Solution Architecture

- **Main Analysis Script:** Scans each collection directory, loads `challenge1b_input.json`, processes the listed PDFs, and generates `challenge1b_output.json`.
- **PDF Extraction:** Uses open-source Python libraries (such as `PyPDF2`, `pdfminer.six`, or similar) to extract text and structure from each PDF.
- **Content Analysis:** Applies ranking and selection logic to identify and organize the most relevant content per persona and use case.
- **Output Generation:** Results are written in the required output JSON schema for each collection.

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) installed on your system.
- Input data (PDFs and JSON) organized as described below.

---

## Build & Run Commands

### Build the Docker Image

```sh
docker build --platform linux/amd64 -t pdf-analyzer-1b .
```

### Run the Container

```sh
docker run --rm -v "D:/Adobe/Challenge_1b:/app" pdf-analyzer-1b
```

- The `/app` directory inside the container should be mapped to your local Challenge_1b root directory.
- All collections (Collection 1, Collection 2, Collection 3, ...) should be inside the mapped directory.

---

## Directory Structure

```
Challenge_1b/
├── Collection 1/                    
│   ├── PDFs/                       
│   ├── challenge1b_input.json      
│   └── challenge1b_output.json     
├── Collection 2/                    
│   ├── PDFs/                       
│   ├── challenge1b_input.json      
│   └── challenge1b_output.json     
├── Collection 3/                    
│   ├── PDFs/                       
│   ├── challenge1b_input.json      
│   └── challenge1b_output.json     
├── ... (more collections)          
└── README.md
```

---

## Input & Output Format

### Input (`challenge1b_input.json`)

```json
{
  "challenge_info": {
    "challenge_id": "round_1b_XXX",
    "test_case_name": "specific_test_case"
  },
  "documents": [{"filename": "doc.pdf", "title": "Title"}],
  "persona": {"role": "User Persona"},
  "job_to_be_done": {"task": "Use case description"}
}
```

### Output (`challenge1b_output.json`)

```json
{
  "metadata": {
    "input_documents": ["list"],
    "persona": "User Persona",
    "job_to_be_done": "Task description"
  },
  "extracted_sections": [
    {
      "document": "source.pdf",
      "section_title": "Title",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "source.pdf",
      "refined_text": "Content",
      "page_number": 1
    }
  ]
}
```

---

## Libraries & Models Used

- **PDF Extraction:** [PyPDF2](https://pypi.org/project/PyPDF2/), [pdfminer.six](https://github.com/pdfminer/pdfminer.six)
- **JSON Handling:** Python standard library (`json`)
- **All dependencies are open source and bundled in the Docker image. No external downloads are required at runtime.**

---

## Performance & Resource Constraints

- **Execution Time:** Designed for fast batch processing.
- **Model Size:** No external ML models; all libraries ≤200MB combined.
- **Memory:** ≤16GB RAM.
- **CPU:** Supports up to 8 CPU cores.
- **Architecture:** AMD64 (x86_64) only.
- **Offline:** No network access required at runtime.

---

## Validation Checklist

- [x] All collections processed automatically.
- [x] `challenge1b_output.json` generated for each collection, matching the required schema.
- [x] Output format validated against the sample schema.
- [x] Solution works without internet access.
- [x] Resource and architecture constraints met.

---

## Team

- Team Name: Code Crafters
- Members: Ch.Preethi, M.Sreeja, Reddy.M.Sam Abhishek
