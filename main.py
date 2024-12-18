import os
from dotenv import load_dotenv
from supabase import create_client, Client
from announcement_processor import AnnouncementProcessor
from message_sender import AnnouncementMessageSender

load_dotenv()

class AnnouncementBot:
    def __init__(self):
        self.supabase: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
        self.processor = AnnouncementProcessor()
        self.sender = AnnouncementMessageSender()

    def get_latest_announcement(self, stock_name: str = "RELIANCE"):
        """
        Fetch the latest announcement for a specific stock from Supabase
        """
        try:
            response = self.supabase.table('recent_announcements') \
                .select('stock_name,content,created_at') \
                .eq('stock_name', stock_name) \
                .order('created_at', desc=True) \
                .limit(1) \
                .execute()
            
            if response.data:
                latest = response.data[0]
                print(f"Processing announcement for {stock_name}...")
                
                processed = self.processor.process_announcement(latest['content'])
                
                if processed:
                    announcement = {
                        'stock_name': latest['stock_name'],
                        'title': processed.title,
                        'summary': processed.summary,
                        'link': processed.link,
                        'date': processed.date,
                        'created_at': latest['created_at']
                    }
                    
                    # Send announcement to subscribers
                    print("Sending announcement to subscribers...")
                    self.sender.send_announcement(announcement)
                    
                    return announcement
            return None
        except Exception as e:
            print(f"Error fetching latest announcement: {e}")
            return None

if __name__ == "__main__":
    bot = AnnouncementBot()
    announcement = bot.get_latest_announcement("RELIANCE")
    
    if announcement:
        print("\n=== Latest Announcement Details ===")
        print(f"Stock: {announcement['stock_name']}")
        print(f"DB Date: {announcement['created_at']}")
        print(f"Announcement Date: {announcement['date']}")
        print(f"\nTitle: {announcement['title']}")
        print(f"\nSummary: {announcement['summary']}")
        print(f"\nLink: {announcement['link']}")
        print("================================")
    else:
        print("No announcements found for RELIANCE")
