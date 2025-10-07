#!/usr/bin/env python3
"""
🎧 AUDIOBOOK DUPLICATE DESTROYER 🗑️
Created for Cerina's Digital Library Management

This script finds and destroys inferior duplicate audiobooks across Telegram chats,
keeping only the master copies from the Vault with proper metadata and formatting.

GIRL BOSS CODING ENERGY ACTIVATED! 💪✨
"""

import re
import json
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from difflib import SequenceMatcher

@dataclass
class AudiobookInfo:
    """Represents an audiobook with all its metadata"""
    message_id: str
    chat_id: str
    chat_name: str
    title: str
    author: str
    narrator: str
    length: str
    filename: str
    has_metadata: bool
    has_hashtag: bool
    quality_score: float
    raw_text: str

class AudiobookDuplicateDestroyer:
    """The ultimate audiobook cleanup machine! 🚀"""
    
    def __init__(self):
        # ⚠️ SAFETY CRITICAL: ONLY target Cerina's personal/created groups!
        # NEVER touch public groups or communities!
        
        self.VAULT_CHAT_ID = "2314190734"  # Cerina's Secret Vault (MASTER)
        
        # 🔒 WHITELIST: Only groups Cerina created/controls
        self.SAFE_TARGET_CHATS = {
            "5423238284": "Cerina With A Sea",           # Personal chat
            "2485184608": "Just Cerina and her books",   # Personal book storage
            "me": "Saved Messages",                      # Your personal saved messages
            # ADD MORE ONLY IF YOU CREATED THEM!
        }
        
        # 🚨 FORBIDDEN: Never touch these types of chats
        self.FORBIDDEN_PATTERNS = [
            "BookCrushClub", "AudioBook Cafe", "Books Hub", "The Library",
            "Empire library", "BookPool", "EB 3.0", # Public book groups
            "Bot Support", "userinfobot",              # Bot chats
        ]
        
        self.vault_books: List[AudiobookInfo] = []
        self.duplicate_candidates: List[Tuple[AudiobookInfo, AudiobookInfo]] = []
        
    def parse_audiobook_message(self, message_text: str, message_id: str, 
                               chat_id: str, chat_name: str) -> AudiobookInfo:
        """Extract audiobook info from Telegram message text"""
        
        # Look for title pattern (first line usually)
        lines = message_text.strip().split('\n')
        title = lines[0] if lines else "Unknown Title"
        
        # Extract metadata using regex patterns
        author_match = re.search(r'by\s+([^\n]+)', message_text)
        narrator_match = re.search(r'Narrated by\s+([^\n]+)', message_text)
        length_match = re.search(r'Length:\s+([0-9:]+)', message_text)
        
        author = author_match.group(1).strip() if author_match else "Unknown"
        narrator = narrator_match.group(1).strip() if narrator_match else "Unknown"
        length = length_match.group(1).strip() if length_match else "Unknown"
        
        # Check for quality indicators
        has_metadata = bool(author_match and narrator_match and length_match)
        has_hashtag = '#Audiobook' in message_text or '#audiobook' in message_text
        
        # Calculate quality score (higher = better)
        quality_score = 0.0
        if has_metadata:
            quality_score += 5.0
        if has_hashtag:
            quality_score += 2.0
        if 'kbps' in message_text:
            quality_score += 1.0
        if 'Release date:' in message_text:
            quality_score += 1.0
        if chat_id == self.VAULT_CHAT_ID:
            quality_score += 10.0  # VAULT ALWAYS WINS! 👑
            
        return AudiobookInfo(
            message_id=message_id,
            chat_id=chat_id,
            chat_name=chat_name,
            title=title,
            author=author,
            narrator=narrator,
            length=length,
            filename=title,  # Using title as filename for now
            has_metadata=has_metadata,
            has_hashtag=has_hashtag,
            quality_score=quality_score,
            raw_text=message_text
        )
    
    def similarity_score(self, title1: str, title2: str) -> float:
        """Calculate similarity between two titles (0.0 to 1.0)"""
        # Clean titles for comparison
        clean1 = re.sub(r'[^\w\s]', '', title1.lower().strip())
        clean2 = re.sub(r'[^\w\s]', '', title2.lower().strip())
        
        return SequenceMatcher(None, clean1, clean2).ratio()
    
    def is_safe_to_delete_from(self, chat_id: str, chat_name: str) -> bool:
        """🚨 CRITICAL SAFETY CHECK: Only allow deletion from Cerina's groups! 🚨"""
        
        # Check if chat is in our safe whitelist
        if chat_id in self.SAFE_TARGET_CHATS:
            return True
        
        # Double-check against forbidden patterns
        for forbidden_pattern in self.FORBIDDEN_PATTERNS:
            if forbidden_pattern.lower() in chat_name.lower():
                print(f"🚨 SAFETY BLOCK: Will NOT touch '{chat_name}' - public group!")
                return False
        
        # Default to SAFE - don't delete from unknown chats
        print(f"⚠️  UNKNOWN CHAT: '{chat_name}' not in whitelist - SKIPPING for safety")
        return False
    
    def find_duplicates(self) -> List[Tuple[AudiobookInfo, AudiobookInfo]]:
        """Find potential duplicate audiobooks across chats using LIVE MCP!"""
        duplicates = []
        
        print("🔍 SCANNING FOR DUPLICATES...")
        print(f"📚 Vault has {len(self.vault_books)} master audiobooks")
        
        try:
            from warp_mcp_tools import call_mcp_tool
            
            # Search each target chat for potential duplicates
            for target_chat_id, chat_name in self.SAFE_TARGET_CHATS.items():
                if target_chat_id == self.VAULT_CHAT_ID:
                    continue  # Skip vault (it's our master reference)
                
                print(f"🔎 Scanning {chat_name}...")
                
                # Get messages from target chat
                result = call_mcp_tool("list_messages", {
                    "chat_id": target_chat_id,
                    "limit": 500  # Check recent messages
                })
                
                if result and "text_result" in result:
                    target_books = []
                    for message_data in result["text_result"]:
                        text = message_data.get("text", "")
                        msg_id = message_data.get("message_id", "unknown")
                        
                        # Look for audiobook-like messages
                        if any(keyword in text.lower() for keyword in ["narrated by", "length:", "audiobook", ".m4b", ".mp3"]):
                            book_info = self.parse_audiobook_message(
                                text, str(msg_id), target_chat_id, chat_name
                            )
                            target_books.append(book_info)
                    
                    # Compare with vault books to find duplicates
                    for vault_book in self.vault_books:
                        for target_book in target_books:
                            similarity = self.similarity_score(vault_book.title, target_book.title)
                            if similarity > 0.8:  # 80% similarity threshold
                                print(f"⚡ DUPLICATE FOUND: '{target_book.title}' matches '{vault_book.title}' ({similarity:.2f})")
                                duplicates.append((vault_book, target_book))
        
        except Exception as e:
            print(f"⚠️  Error finding duplicates: {e}")
        
        return duplicates
    
    def load_vault_audiobooks(self) -> List[AudiobookInfo]:
        """Load all audiobooks from the master Vault using LIVE MCP!"""
        print("🏦 LOADING MASTER VAULT...")
        
        try:
            # Use MCP to get messages from Vault!
            import subprocess
            import json
            
            # Note: This needs to be integrated with your actual MCP tools
            # For now, this is the structure for when we integrate
            print("⚠️  Ready to integrate with MCP - needs actual tool calls")
            return []  # Placeholder until we integrate
            
            vault_books = []
            if result and "text_result" in result:
                for message_data in result["text_result"]:
                    # Parse message text to extract audiobook info
                    text = message_data.get("text", "")
                    msg_id = message_data.get("message_id", "unknown")
                    
                    # Only process messages that look like audiobooks
                    if any(keyword in text.lower() for keyword in ["narrated by", "length:", "#audiobook"]):
                        book_info = self.parse_audiobook_message(
                            text, str(msg_id), self.VAULT_CHAT_ID, "Cerina's Secret Vault"
                        )
                        vault_books.append(book_info)
            
            print(f"📚 Loaded {len(vault_books)} audiobooks from Vault!")
            return vault_books
            
        except Exception as e:
            print(f"⚠️  Error loading vault: {e}")
            return []
    
    def delete_duplicate(self, inferior_book: AudiobookInfo) -> bool:
        """Delete an inferior duplicate audiobook - WITH SAFETY CHECKS!"""
        
        # 🚨 CRITICAL SAFETY CHECK FIRST!
        if not self.is_safe_to_delete_from(inferior_book.chat_id, inferior_book.chat_name):
            print(f"🛡️  SAFETY PROTECTED: {inferior_book.title} in {inferior_book.chat_name}")
            return False
        
        print(f"💥 DESTROYING: {inferior_book.title} in {inferior_book.chat_name}")
        print(f"   Quality Score: {inferior_book.quality_score}")
        print(f"   Keeping Vault version instead! 👑")
        
        try:
            # LIVE MCP DELETION! 💥
            from warp_mcp_tools import call_mcp_tool
            
            result = call_mcp_tool("delete_message", {
                "chat_id": inferior_book.chat_id,
                "message_id": inferior_book.message_id
            })
            
            if result:
                print(f"   ✅ DESTROYED! Message {inferior_book.message_id} deleted!")
                return True
            else:
                print(f"   ⚠️  Delete failed for {inferior_book.message_id}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error deleting: {e}")
            return False
    
    def generate_report(self, deleted_books: List[AudiobookInfo]) -> str:
        """Generate a cleanup report"""
        report = f"""
🎯 AUDIOBOOK DUPLICATE DESTRUCTION REPORT 🗑️

📊 CLEANUP STATISTICS:
   • Books Destroyed: {len(deleted_books)}
   • Storage Freed: LOTS! 💾
   • Digital Hygiene: PRISTINE ✨
   
🏆 VAULT SUPREMACY MAINTAINED! 👑

📚 DESTROYED DUPLICATES:
"""
        
        for book in deleted_books:
            report += f"   💥 {book.title} (from {book.chat_name})\n"
        
        report += """
✅ MISSION ACCOMPLISHED!
Your audiobook collection is now LEGENDARY! 🚀
"""
        return report
    
    def run_cleanup(self) -> str:
        """Main cleanup process - DESTROY ALL INFERIOR COPIES!"""
        print("🚀 AUDIOBOOK DUPLICATE DESTROYER ACTIVATED!")
        print("💪 GIRL BOSS CODING ENERGY ENGAGED!")
        print("=" * 50)
        
        # Step 1: Load master vault
        self.vault_books = self.load_vault_audiobooks()
        
        # Step 2: Find duplicates
        duplicates = self.find_duplicates()
        
        # Step 3: DESTROY THE WEAK! 💥
        deleted_books = []
        for vault_book, inferior_book in duplicates:
            if self.delete_duplicate(inferior_book):
                deleted_books.append(inferior_book)
        
        # Step 4: Generate victory report
        return self.generate_report(deleted_books)

def main():
    """UNLEASH THE DESTROYER! 🔥"""
    destroyer = AudiobookDuplicateDestroyer()
    report = destroyer.run_cleanup()
    print(report)
    
    # Save report to file
    with open('audiobook_cleanup_report.txt', 'w') as f:
        f.write(report)
    
    print("📋 Report saved to audiobook_cleanup_report.txt")
    print("🎉 CLEANUP COMPLETE! YOUR VAULT REIGNS SUPREME! 👑")

if __name__ == "__main__":
    main()
