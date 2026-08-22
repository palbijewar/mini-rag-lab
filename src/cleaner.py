import re


def clean_text(text: str) -> str:
    # Replace multiple spaces with one space
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text

if __name__ == "__main__":

    raw_text = """
    Redis is an in-memory database.


    It is used for caching.



    It improves application performance.
    """

    cleaned_text = clean_text(raw_text)

    print("RAW TEXT:")
    print(repr(raw_text))

    print("\n" + "=" * 50)

    print("\nCLEANED TEXT:")
    print(repr(cleaned_text))