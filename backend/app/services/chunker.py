import re


SECTION_PATTERNS = [

    r"Section\s+\d+[A-Za-z]*",

    r"SECTION\s+\d+[A-Za-z]*",

    r"Article\s+\d+[A-Za-z]*",

    r"ARTICLE\s+\d+[A-Za-z]*"
]


def detect_section(text):

    for pattern in SECTION_PATTERNS:

        match = re.search(
            pattern,
            text
        )

        if match:
            return match.group(0)

    return None


def create_chunks(
    pages,
    chunk_size=1200,
    overlap=200
):

    chunks = []

    current_section = None


    for page in pages:

        text = page["text"]

        page_number = page["page"]


        detected_section = detect_section(
            text
        )


        if detected_section:

            current_section = detected_section


        start = 0


        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]


            chunks.append({

                "text": chunk_text,

                "page": page_number,

                "section": current_section

            })


            start += (
                chunk_size - overlap
            )


    return chunks