import json
import re
from pathlib import Path
import fitz  # PyMuPDF
import sys

def clean_text(text: str):
    """Lowercase, remove non-word chars, split into unique keywords"""
    return set(re.findall(r"\w+", text.lower()))

def compute_section_score(title: str, content: str, keywords: set):
    """Calculate relevance score based on keyword matches in title and content"""
    title_l = title.lower()
    content_l = content.lower()
    score = 0
    for kw in keywords:
        if kw in title_l:
            score += 5  # title matches weighted higher
        if kw in content_l:
            score += 1
    return score

def clean_heading(title: str):
    """Clean and normalize extracted headings"""
    title = title.strip()
    title = re.sub(r'[\.,;:\-\–\—\…]+$', '', title)
    if '.' in title:
        title = title.split('.')[0]
    if len(title) > 150:
        title = title[:150] + "..."
    return title

def extract_sections(pdf_path: Path, keywords: set):
    """Extract and score sections from PDF using TOC or fallback to font size heuristics."""
    doc = fitz.open(str(pdf_path))
    sections = []
    seen = set()

    toc = doc.get_toc(simple=True)
    if toc:
        for level, title, page_num in toc:
            if not title or not page_num:
                continue
            key = (title.strip().lower(), page_num)
            if key in seen:
                continue
            page_index = min(max(page_num - 1, 0), len(doc) - 1)
            page_text = doc[page_index].get_text()
            score = compute_section_score(title, page_text, keywords)
            clean_title = clean_heading(title)
            sections.append({
                "section_title": clean_title,
                "page_number": page_num,
                "text": page_text,
                "score": score,
            })
            seen.add(key)
    else:
        # No TOC - fallback extraction by font size
        for page_index, page in enumerate(doc):
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span.get("text", "").strip()
                        size = span.get("size", 0)
                        if len(text) < 4:
                            continue
                        if size >= 12:
                            key = (text.lower(), page_index + 1)
                            if key in seen:
                                continue
                            page_text = page.get_text()
                            score = compute_section_score(text, page_text, keywords)
                            clean_title = clean_heading(text)
                            sections.append({
                                "section_title": clean_title,
                                "page_number": page_index + 1,
                                "text": page_text,
                                "score": score,
                            })
                            seen.add(key)

    # Sort by score desc, then page asc, then title asc
    sections.sort(key=lambda s: (-s['score'], s['page_number'], s['section_title']))
    return sections

def process_collection(collection_path: Path):
    input_json = collection_path / "challenge1b_input.json"
    if not input_json.exists():
        print(f"[WARN] Missing input JSON: {input_json}, skipping.", file=sys.stderr)
        return
    output_json = collection_path / "challenge1b_output.json"

    with input_json.open(encoding="utf-8") as f:
        data = json.load(f)

    persona = data.get("persona", {}).get("role", "")
    # Support both keys for job description
    job = ""
    if "job_to_be_done" in data:
        job = data["job_to_be_done"].get("task", "")
    elif "job" in data:
        job = data["job"] if isinstance(data["job"], str) else data["job"].get("task", "")

    query_text = f"{persona} {job}"
    keywords = clean_text(query_text)

    print(f"[INFO] Processing collection '{collection_path.name}'")
    print(f"[INFO] Persona: '{persona}', Job: '{job}'")
    print(f"[INFO] Keywords: {sorted(keywords)}")

    extracted_sections = []
    subsection_analysis = []

    for doc in data.get("documents", []):
        filename = doc.get("filename")
        if not filename:
            continue
        pdf_path = collection_path / "PDFs" / filename
        if not pdf_path.exists():
            print(f"[ERROR] PDF not found: {pdf_path}", file=sys.stderr)
            continue
        print(f"[INFO] Analyzing PDF: {filename}")
        sections = extract_sections(pdf_path, keywords)

        if not sections:
            print(f"[WARN] No sections extracted from {filename}", file=sys.stderr)

        rank = 1
        seen_titles = set()
        for section in sections[:10]:  # Take more, but output top 5 unique titles
            title_lower = section["section_title"].lower()
            if title_lower in seen_titles:
                continue
            seen_titles.add(title_lower)

            extracted_sections.append({
                "document": filename,
                "section_title": section["section_title"],
                "importance_rank": rank,
                "page_number": section["page_number"],
            })

            refined_text = section["text"].replace("\n", " ").strip()
            if len(refined_text) > 512:
                refined_text = refined_text[:512]

            subsection_analysis.append({
                "document": filename,
                "refined_text": refined_text,
                "page_number": section["page_number"],
            })

            rank += 1
            if rank > 5:
                break

    output = {
        "metadata": {
            "input_documents": [d.get("filename") for d in data.get("documents", [])],
            "persona": persona,
            "job_to_be_done": job,
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis,
    }

    with output_json.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"[INFO] Finished processing '{collection_path.name}'. Output saved to '{output_json}'.")

def main():
    root_path = Path(".")
    for collection_dir in sorted(root_path.iterdir()):
        if not collection_dir.is_dir():
            continue
        if (collection_dir / "challenge1b_input.json").exists():
            process_collection(collection_dir)
    print("[INFO] All collections processed.")

if __name__ == "__main__":
    main()

