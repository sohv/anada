"""Markdown renderer for terminal output."""

import re
from typing import Dict
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text


class MarkdownRenderer:
    """Renders Markdown with theme colors."""
    
    # Patterns for Markdown elements
    HEADER_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    BOLD_PATTERN = re.compile(r'\*\*([^*]+)\*\*')
    ITALIC_PATTERN = re.compile(r'\*([^*]+)\*')
    CODE_PATTERN = re.compile(r'`([^`]+)`')
    LINK_PATTERN = re.compile(r'\[\[([^\]]+)\]\]')
    BLOCKQUOTE_PATTERN = re.compile(r'^>\s+(.+)$', re.MULTILINE)
    
    def __init__(self, theme_colors: Dict[str, str], console: Console):
        self.theme_colors = theme_colors
        self.console = console
    
    def render(self, content: str) -> Text:
        """Render Markdown content with theme colors."""
        text = Text(content)
        
        # Apply colors based on theme
        # This is a simplified renderer - rich.Markdown is better but harder to theme
        
        # Headers
        for match in self.HEADER_PATTERN.finditer(content):
            level = len(match.group(1))
            header_text = match.group(2)
            color = self.theme_colors.get('header', 'cyan')
            # Rich will handle this better, but we'll use console.print with Markdown
        
        return text
    
    def render_note(self, title: str, content: str, backlinks: list = None):
        """Render a complete note with title, content, and backlinks."""
        # Use rich's Markdown renderer
        markdown = Markdown(content)
        
        # Create panel with title
        panel_content = []
        
        if backlinks:
            backlinks_text = "\n\n**Backlinks:**\n"
            for link in backlinks:
                backlinks_text += f"- [[{link}]]\n"
            markdown = Markdown(content + backlinks_text)
        
        # For now, use rich's built-in Markdown which handles most cases
        # We'll enhance with custom theming if needed
        self.console.print(markdown)
    
    def render_list(self, notes: list):
        """Render a list of notes."""
        from rich.table import Table
        from rich import box
        
        table = Table(box=box.SIMPLE, show_header=True, header_style="bold cyan")
        table.add_column("Title", style="cyan")
        table.add_column("Modified", style="dim")
        table.add_column("Size", style="dim")
        
        for note in notes:
            modified_str = note['modified'].strftime('%Y-%m-%d %H:%M')
            size_str = f"{note['size']} bytes"
            table.add_row(note['title'], modified_str, size_str)
        
        self.console.print(table)
    
    def render_search_results(self, results: list, query: str):
        """Render search results."""
        from rich.table import Table
        from rich import box
        
        if not results:
            self.console.print(f"[dim]No results found for '{query}'[/dim]")
            return
        
        table = Table(box=box.SIMPLE, show_header=True, header_style="bold cyan")
        table.add_column("Title", style="cyan")
        table.add_column("Snippet", style="dim")
        table.add_column("Matches", justify="right", style="dim")
        
        for result in results:
            snippet = result['snippet'][:100] + '...' if len(result['snippet']) > 100 else result['snippet']
            table.add_row(result['title'], snippet, str(result['matches']))
        
        self.console.print(table)

