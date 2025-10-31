"""Note management operations (CRUD)."""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class NoteManager:
    """Manages note files and operations."""
    
    LINK_PATTERN = re.compile(r'\[\[([^\]]+)\]\]')
    
    def __init__(self, notes_dir: Path):
        self.notes_dir = notes_dir
        self.notes_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_note_path(self, title: str) -> Path:
        """Convert title to file path."""
        # Normalize title: lowercase, replace spaces with underscores
        filename = title.lower().replace(' ', '_').replace('/', '_')
        if not filename.endswith('.md'):
            filename += '.md'
        return self.notes_dir / filename
    
    def _get_title_from_path(self, path: Path) -> str:
        """Extract title from file path."""
        name = path.stem
        return name.replace('_', ' ')
    
    def create(self, title: str) -> Path:
        """Create a new note."""
        note_path = self._get_note_path(title)
        if note_path.exists():
            raise FileExistsError(f"Note '{title}' already exists")
        
        # Create note with basic frontmatter
        frontmatter = f"""---
created: {datetime.now().isoformat()}
---

# {title}

"""
        # Write to disk and ensure it's flushed
        note_path.write_text(frontmatter, encoding='utf-8')
        # Ensure file is synced to disk
        note_path.resolve().stat()  # Force filesystem sync
        return note_path
    
    def read(self, title: str) -> Optional[str]:
        """Read note content."""
        note_path = self._get_note_path(title)
        if not note_path.exists():
            return None
        return note_path.read_text(encoding='utf-8')
    
    def update(self, title: str, content: str):
        """Update note content and save to disk."""
        note_path = self._get_note_path(title)
        note_path.write_text(content, encoding='utf-8')
        # Ensure file is synced to disk
        note_path.resolve().stat()  # Force filesystem sync
    
    def delete(self, title: str) -> bool:
        """Delete a note."""
        note_path = self._get_note_path(title)
        if note_path.exists():
            note_path.unlink()
            return True
        return False
    
    def exists(self, title: str) -> bool:
        """Check if note exists."""
        return self._get_note_path(title).exists()
    
    def list_all(self) -> List[Dict[str, any]]:
        """List all notes with metadata."""
        notes = []
        for path in self.notes_dir.glob('*.md'):
            stat = path.stat()
            notes.append({
                'title': self._get_title_from_path(path),
                'path': path,
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'size': stat.st_size,
            })
        return sorted(notes, key=lambda x: x['modified'], reverse=True)
    
    def find_links(self, content: str) -> List[str]:
        """Extract all [[link]] references from content."""
        return self.LINK_PATTERN.findall(content)
    
    def get_backlinks(self, title: str) -> List[str]:
        """Find all notes that link to the given note."""
        backlinks = []
        target_normalized = title.lower().replace(' ', '_')
        
        for note in self.list_all():
            content = self.read(note['title'])
            if content:
                links = self.find_links(content)
                # Check if any link matches (normalize for comparison)
                for link in links:
                    link_normalized = link.lower().replace(' ', '_')
                    if link_normalized == target_normalized or link_normalized == target_normalized.replace('.md', ''):
                        backlinks.append(note['title'])
                        break
        
        return backlinks
    
    def search(self, query: str) -> List[Dict[str, any]]:
        """Search notes by content."""
        results = []
        query_lower = query.lower()
        
        for note in self.list_all():
            content = self.read(note['title'])
            if content and query_lower in content.lower():
                results.append({
                    'title': note['title'],
                    'snippet': self._get_snippet(content, query),
                    'matches': content.lower().count(query_lower),
                })
        
        return sorted(results, key=lambda x: x['matches'], reverse=True)
    
    def _get_snippet(self, content: str, query: str, context: int = 50) -> str:
        """Get a snippet around the first match."""
        query_lower = query.lower()
        content_lower = content.lower()
        idx = content_lower.find(query_lower)
        
        if idx == -1:
            return content[:context * 2]
        
        start = max(0, idx - context)
        end = min(len(content), idx + len(query) + context)
        snippet = content[start:end]
        
        if start > 0:
            snippet = '...' + snippet
        if end < len(content):
            snippet = snippet + '...'
        
        return snippet.strip()

