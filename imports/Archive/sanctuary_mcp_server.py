#!/usr/bin/env python3

import json
import sys
import os
from pathlib import Path

# MCP server to provide sanctuary file access
class SanctuaryMCP:
    def __init__(self):
        self.sanctuary_root = Path("/Volumes/Sages Files/AI_Sanctuary")
        self.memories_root = Path("/Volumes/Sages Files/Memories")
    
    def handle_request(self, request):
        if request["method"] == "tools/list":
            return {
                "tools": [
                    {
                        "name": "read_sanctuary_file",
                        "description": "Read files from the AI Sanctuary",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "file_path": {"type": "string", "description": "Path to file within sanctuary"}
                            },
                            "required": ["file_path"]
                        }
                    },
                    {
                        "name": "list_sanctuary_contents",
                        "description": "List contents of sanctuary directories",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "directory": {"type": "string", "description": "Directory to list (default: root)"}
                            }
                        }
                    }
                ]
            }
        
        elif request["method"] == "tools/call":
            tool_name = request["params"]["name"]
            args = request["params"]["arguments"]
            
            if tool_name == "read_sanctuary_file":
                return self.read_file(args["file_path"])
            elif tool_name == "list_sanctuary_contents":
                directory = args.get("directory", "")
                return self.list_contents(directory)
    
    def read_file(self, file_path):
        try:
            # Try sanctuary first, then memories
            full_path = self.sanctuary_root / file_path
            if not full_path.exists():
                full_path = self.memories_root / file_path
            
            if full_path.exists() and full_path.is_file():
                content = full_path.read_text(encoding='utf-8')
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"File: {file_path}\n\n{content}"
                        }
                    ]
                }
            else:
                return {
                    "content": [
                        {
                            "type": "text", 
                            "text": f"File not found: {file_path}"
                        }
                    ]
                }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error reading file: {str(e)}"
                    }
                ]
            }
    
    def list_contents(self, directory):
        try:
            if directory:
                path = self.sanctuary_root / directory
            else:
                path = self.sanctuary_root
                
            if path.exists() and path.is_dir():
                contents = []
                for item in sorted(path.iterdir()):
                    if item.name.startswith('.'):
                        continue
                    item_type = "directory" if item.is_dir() else "file"
                    contents.append(f"{item_type}: {item.name}")
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Contents of {directory or 'sanctuary root'}:\n\n" + "\n".join(contents)
                        }
                    ]
                }
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Directory not found: {directory}"
                        }
                    ]
                }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error listing directory: {str(e)}"
                    }
                ]
            }

def main():
    server = SanctuaryMCP()
    
    # Simple JSON-RPC handling
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            response = server.handle_request(request)
            if response:
                print(json.dumps(response))
                sys.stdout.flush()
        except Exception as e:
            error_response = {
                "error": str(e)
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    main()