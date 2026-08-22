from pypdf import PdfReader
from cleaner import clean_text


def parse_pdf(file_path: str):
    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages):

        raw_text = page.extract_text()

        cleaned_text = clean_text(raw_text)

        pages.append({
            "page_number": page_number + 1,
            "text": cleaned_text
        })

    return pages


if __name__ == "__main__":

    pages = parse_pdf("data/demopdf.pdf")

    print(f"\nTotal pages: {len(pages)}")

    for page in pages[:2]:

        print("\n" + "=" * 80)
        print(f"PAGE {page['page_number']}")
        print("=" * 80)

        print(page["text"][:1000])