import re


def clean_text(text: str) -> str:

    # Fix missing spaces after punctuation
    text = re.sub(r"([;,:])([A-Za-z])", r"\1 \2", text)

    # Fix common PDF word/heading concatenation
    replacements = {
        "OverviewWelcome": "Overview\nWelcome",
        "DataStructures": "Data Structures",
        "ProgrammingLanguages": "Programming Languages",
        "Behavioraland": "Behavioral and",
        "SystemArchitecture": "System Architecture",
        "Problem-solvingand": "Problem-solving and",
        "Domainsand": "Domains and",
        "Skills.Domains and Topics": "Skills\nDomains and Topics\n",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove repeated PDF footer
    text = text.replace("aastha-shukla/", "")

    # Put numbered major sections on their own line
    text = re.sub(
        r"(?<!\n)(\d+\.\s+[A-Z][A-Za-z ]+)",
        r"\n\1",
        text
    )

    # Put checklist items on separate lines
    text = re.sub(
        r"\[ \]",
        r"\n[ ]",
        text
    )

    # Normalize spaces within each line
    lines = []

    for line in text.splitlines():

        line = re.sub(r"[ \t]+", " ", line)
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)