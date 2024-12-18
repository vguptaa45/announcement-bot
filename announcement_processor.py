import json
from dataclasses import dataclass
from typing import Optional
from pdf_extractor import download_pdf_from_link
from summary_generator import generate_summary

@dataclass
class Announcement:
    title: str
    summary: str
    link: str
    date: str

class AnnouncementProcessor:
    def __init__(self):
        pass

    def process_announcement(self, content: str) -> Optional[Announcement]:
        """
        Process the announcement content and return structured data
        """
        try:
            # Parse the JSON content as a list
            announcements = json.loads(content)
            
            # Get the first (most recent) announcement
            if not announcements or not isinstance(announcements, list):
                raise ValueError("Invalid announcement format")
                
            latest = announcements[0]
            
            # Extract data from the first announcement
            title = latest.get('title', '')
            link = latest.get('link', '')
            date = latest.get('date', '')
            
            # Download and process PDF
            print(f"Downloading PDF from: {link}")
            pdf_text = download_pdf_from_link(link)
            
            # Generate AI summary
            print("Generating summary...")
            summary = generate_summary(pdf_text)
            
            return Announcement(
                title=title,
                summary=summary,
                link=link,
                date=date
            )
        except Exception as e:
            print(f"Error processing announcement: {e}")
            return None
