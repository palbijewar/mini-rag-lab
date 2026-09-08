import re


def clean_text(text: str) -> str:

    # Fix missing spaces after punctuation
    text = re.sub(r"([;,:])([A-Za-z])", r"\1 \2", text)

    # Fix common PDF heading/word concatenation
    replacements = {
        "OverviewWelcome": "Overview\nWelcome",
        "DataStructures": "Data Structures",
        "ProgrammingLanguages": "Programming Languages",
        "Behavioraland": "Behavioral and",
        "SystemArchitecture": "System Architecture",
        "Problem-solvingand": "Problem-solving and",
        "Domainsand": "Domains and",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Normalize spaces within each line
    lines = []

    for line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", line)
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)
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