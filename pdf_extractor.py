import requests
import io
from pdfminer.high_level import extract_text

def download_pdf_from_link(pdf_link: str) -> str:
    """
    Download and extract text from a PDF given its URL.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        session = requests.Session()
        response = session.get(pdf_link, headers=headers, allow_redirects=True)
        pdf_content = io.BytesIO(response.content)
        raw_text = extract_text(pdf_content)
        return raw_text
    except Exception as e:
        print(f"Error downloading PDF: {e}")
        return ""
