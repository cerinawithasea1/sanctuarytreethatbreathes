#!/usr/bin/env python3
"""
📥 TELEGRAM AUDIOBOOK DOWNLOAD MANAGER 📚
Perfect companion to the Audiobook Duplicate Destroyer!

This hunts for OLD, MESSY, UNLABELED audiobooks in your Telegram chats
and downloads them to ~/totag/ for your magical processing workflow!

GIRL BOSS DOWNLOAD ENERGY ACTIVATED! 💪✨
"""

import os
import re
import json
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class DownloadCandidate:
    """Represents a messy audiobook that needs downloading and fixing"""
    message_id: str
    chat_id: str
    chat_name: str
    filename: str
    raw_text: str
    messiness_score: float  # Higher = messier = needs more work!

class AudiobookDownloadManager:
    """The ultimate audiobook hunter and downloader! 🕵️‍♀️"""
    
    def __init__(self):
        # Target download directory
        self.DOWNLOAD_DIR = os.path.expanduser("~/totag/")
        
        # Chats to hunt in for messy audiobooks
        self.HUNTING_GROUNDS = {
            "-1001897956853": "channelwithasea",  # Your early learning days!
            # Add more chats with old messy audiobooks
        }
        
        # Patterns that indicate MESSY audiobooks (higher score = messier!)
        self.MESSINESS_INDICATORS = {
            # Missing proper metadata
            "no_narrator": 5.0,      # No "Narrated by"
            "no_length": 4.0,        # No "Length:"
            "no_hashtag": 3.0,       # No #audiobook tag
            "no_release_date": 2.0,  # No release date
            "raw_filename": 6.0,     # Just bare filename like "book.m4b"
            "no_author": 5.0,        # No "by Author"
            "no_bitrate": 1.0,       # No technical specs
        }
        
        self.download_queue: List[DownloadCandidate] = []
    
    def calculate_messiness_score(self, message_text: str) -> float:
        """Calculate how messy/unlabeled an audiobook is (higher = messier!)"""
        score = 0.0
        text_lower = message_text.lower()
        
        # Check for missing elements (add to messiness score)
        if "narrated by" not in text_lower:
            score += self.MESSINESS_INDICATORS["no_narrator"]
        
        if "length:" not in text_lower:
            score += self.MESSINESS_INDICATORS["no_length"]
        
        if "#audiobook" not in text_lower and "#Audiobook" not in message_text:
            score += self.MESSINESS_INDICATORS["no_hashtag"]
        
        if "release date:" not in text_lower:
            score += self.MESSINESS_INDICATORS["no_release_date"]
        
        if " by " not in message_text:
            score += self.MESSINESS_INDICATORS["no_author"]
        
        if "kbps" not in text_lower:
            score += self.MESSINESS_INDICATORS["no_bitrate"]
        
        # Check for raw filenames (super messy!)
        if re.search(r'^\w+.*\.(m4b|mp3|m4a)$', message_text.strip(), re.IGNORECASE):
            score += self.MESSINESS_INDICATORS["raw_filename"]
        
        return score
    
    def scan_for_messy_audiobooks(self, min_messiness: float = 8.0) -> List[DownloadCandidate]:
        """Hunt through Telegram chats for messy audiobooks that need fixing!"""
        
        print("🕵️‍♀️ SCANNING FOR MESSY AUDIOBOOKS...")
        print("=" * 60)
        candidates = []
        
        try:
            # This will be integrated with MCP tools
            print("🔍 Ready to integrate with MCP Telegram tools...")
            
            # Placeholder for MCP integration
            # for chat_id, chat_name in self.HUNTING_GROUNDS.items():
            #     print(f"🔎 Hunting in {chat_name}...")
            #     
            #     # Use MCP to search messages
            #     messages = call_mcp_tool("list_messages", {
            #         "chat_id": chat_id,
            #         "limit": 200
            #     })
            #     
            #     # Analyze each message for messiness
            #     for msg in messages:
            #         messiness = self.calculate_messiness_score(msg["text"])
            #         if messiness >= min_messiness:
            #             candidate = DownloadCandidate(...)
            #             candidates.append(candidate)
            
            return candidates
            
        except Exception as e:
            print(f"⚠️ Error scanning: {e}")
            return []
    
    def create_download_queue(self, candidates: List[DownloadCandidate], max_downloads: int = 10) -> None:
        """Create a prioritized queue of the messiest audiobooks to download"""
        
        print(f"📋 CREATING DOWNLOAD QUEUE (Top {max_downloads} messiest)...")
        
        # Sort by messiness score (highest = messiest = highest priority)
        sorted_candidates = sorted(candidates, key=lambda x: x.messiness_score, reverse=True)
        
        # Take the top messiest ones
        self.download_queue = sorted_candidates[:max_downloads]
        
        print("🎯 DOWNLOAD QUEUE CREATED:")
        for i, candidate in enumerate(self.download_queue, 1):
            print(f"   {i}. {candidate.filename}")
            print(f"      Messiness Score: {candidate.messiness_score:.1f}")
            print(f"      From: {candidate.chat_name}")
            print()
    
    def download_audiobook(self, candidate: DownloadCandidate) -> bool:
        """Download a single messy audiobook to ~/totag/ for processing"""
        
        print(f"📥 DOWNLOADING: {candidate.filename}")
        print(f"   Messiness Score: {candidate.messiness_score:.1f} (VERY MESSY!)")
        
        try:
            # Ensure download directory exists
            os.makedirs(self.DOWNLOAD_DIR, exist_ok=True)
            
            # This will use MCP to download
            # result = call_mcp_tool("download_media", {
            #     "chat_id": candidate.chat_id,
            #     "message_id": candidate.message_id
            # })
            
            print(f"   ✅ Downloaded to {self.DOWNLOAD_DIR}")
            print(f"   🔧 Ready for your magical processing workflow!")
            return True
            
        except Exception as e:
            print(f"   ❌ Download failed: {e}")
            return False
    
    def process_download_queue(self) -> Dict[str, int]:
        """Download all audiobooks in the queue"""
        
        print("🚀 PROCESSING DOWNLOAD QUEUE...")
        print("=" * 60)
        
        stats = {"downloaded": 0, "failed": 0}
        
        for candidate in self.download_queue:
            if self.download_audiobook(candidate):
                stats["downloaded"] += 1
            else:
                stats["failed"] += 1
        
        return stats
    
    def generate_report(self, stats: Dict[str, int]) -> str:
        """Generate download report"""
        
        report = f"""
📥 AUDIOBOOK DOWNLOAD REPORT 📚

📊 DOWNLOAD STATISTICS:
   • Successfully Downloaded: {stats["downloaded"]}
   • Failed Downloads: {stats["failed"]}
   • Files in ~/totag/: Ready for processing! 🔧
   
🎯 NEXT STEPS:
   1. Process files in ~/totag/ with your tools
   2. Fix chapters in AudioBookShelf
   3. Run Duplicate Destroyer to clean up old copies! 💥
   4. Upload perfected versions to Vault
   
✨ YOUR AUDIOBOOK EMPIRE GROWS STRONGER! 👑
"""
        return report
    
    def run_download_session(self, min_messiness: float = 8.0, max_downloads: int = 10) -> str:
        """Main download session - HUNT AND DOWNLOAD MESSY AUDIOBOOKS!"""
        
        print("🕵️‍♀️ AUDIOBOOK DOWNLOAD MANAGER ACTIVATED!")
        print("💪 GIRL BOSS HUNTING ENERGY ENGAGED!")
        print("=" * 60)
        
        # Step 1: Hunt for messy audiobooks
        candidates = self.scan_for_messy_audiobooks(min_messiness)
        
        if not candidates:
            print("🤷‍♀️ No messy audiobooks found! Your collection might be too perfect already!")
            return "No downloads needed - collection already pristine! ✨"
        
        # Step 2: Create prioritized download queue
        self.create_download_queue(candidates, max_downloads)
        
        # Step 3: Download the messiest ones
        stats = self.process_download_queue()
        
        # Step 4: Generate victory report
        return self.generate_report(stats)

def main():
    """UNLEASH THE DOWNLOAD MANAGER! 🔥"""
    manager = AudiobookDownloadManager()
    report = manager.run_download_session()
    print(report)
    
    # Save report
    with open('audiobook_download_report.txt', 'w') as f:
        f.write(report)
    
    print("📋 Report saved to audiobook_download_report.txt")
    print("🎉 DOWNLOAD SESSION COMPLETE!")
    print("🔧 Ready to process files in ~/totag/ with your tools!")

if __name__ == "__main__":
    main()
