from pypdf import PdfReader


def parse_pdf(file_path: str):
    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()

        pages.append({
            "page_number": page_number + 1,
            "text": text
        })

    return pages


if __name__ == "__main__":
    pages = parse_pdf("data/demopdf.pdf")

    print(f"Total pages: {len(pages)}")

    for page in pages[:2]:
        print("\n" + "=" * 80)
        print(f"PAGE {page['page_number']}")
        print("=" * 80)
        print(page["text"][:1000])