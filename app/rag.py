def split_pages_into_chunks(pages):

    chunks = []

    for page in pages:

        text = page["text"]

        # Split whenever a new numbered question starts
        sections = text.split("\n")

        current_chunk = ""

        for line in sections:

            line = line.strip()

            if not line:
                continue

            # Detect a new question: 1. , 2. , 3. etc.
            if line[0].isdigit() and ". " in line[:4]:

                if current_chunk:
                    chunks.append({
                        "text": current_chunk.strip(),
                        "page": page["page"]
                    })

                current_chunk = line

            else:

                current_chunk += " " + line

        # Add final chunk
        if current_chunk:
            chunks.append({
                "text": current_chunk.strip(),
                "page": page["page"]
            })

    return chunks