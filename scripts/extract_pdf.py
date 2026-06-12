from pathlib import Path
from pypdf import PdfReader


PDF_PATH = Path("data/IPL_LangGraph_RAG_Dataset.pdf")
OUTPUT_PATH = Path("data/ipl_dataset_text.txt")


def extract_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(pdf_path)

    all_pages_text = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            all_pages_text.append(f"\n--- Page {page_number} ---\n")
            all_pages_text.append(text)

    return "\n".join(all_pages_text)


def main():
    if not PDF_PATH.exists():
        print(f"PDF not found: {PDF_PATH}")
        return

    extracted_text = extract_pdf_text(PDF_PATH)

    OUTPUT_PATH.write_text(extracted_text, encoding="utf-8")

    print("PDF text extracted successfully!")
    print(f"Saved to: {OUTPUT_PATH}")
    print()
    print("Preview:")
    print(extracted_text[:1000])


if __name__ == "__main__":
    main()