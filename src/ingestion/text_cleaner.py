import re


def clean_text(text: str) -> str:

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    text = re.sub(
        r"3GPP TS 23\.501 version 18\.10\.0 Release 18.*?ETSI TS 123 501 V18\.10\.0 \(2025-07\)",
        "",
        text
    ) 
    text = re.sub(r"\n\s*ETSI\s*$", "", text, flags=re.MULTILINE)

    
    text = re.sub(r"[ \t]+", " ", text)

    
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()