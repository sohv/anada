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
        """Render a list of notes with enhanced styling."""
        if not notes:
            empty_panel = Panel.fit(
                "[dim]No notes found[/dim]\n\n"
                "[cyan]Get started:[/cyan]\n"
                "• Type [green]new \"my first note\"[/green] to create a note\n"
                "• Try [green]menu[/green] for interactive commands\n"
                "• Use [green]help[/green] to see all options",
                border_style="yellow",
                title="Notes"
            )
            self.console.print(empty_panel)
            return
        
        from rich.table import Table
        from rich import box
        
        table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan", title=f"Notes ({len(notes)} total)")
        table.add_column("Title", style="cyan", width=30)
        table.add_column("Modified", style="dim", width=20)
        table.add_column("Size", style="dim", width=10)
        
        for note in notes:
            modified_str = note['modified'].strftime('%Y-%m-%d %H:%M')
            size_str = f"{note['size']} B"
            
            table.add_row(
                note['title'][:28] + '...' if len(note['title']) > 28 else note['title'],
                modified_str, 
                size_str
            )
        
        self.console.print(table)
        self.console.print(f"\n[dim]Use [cyan]show <title>[/cyan] to view a note or [cyan]live-search[/cyan] for interactive search[/dim]")
    
    def render_search_results(self, results: list, query: str):
        """Render search results with enhanced styling."""
        if not results:
            no_results_panel = Panel.fit(
                f"[dim]No results found for '[cyan]{query}[/cyan]'[/dim]\n\n"
                "[cyan]Try:[/cyan]\n"
                "• Different keywords\n"
                "• [green]live-search[/green] for interactive search\n"
                "• [green]list[/green] to see all notes",
                border_style="yellow",
                title="Search Results"
            )
            self.console.print(no_results_panel)
            return
        
        from rich.table import Table
        from rich import box
        
        table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan", 
                     title=f"Search Results for '{query}' ({len(results)} found)")
        table.add_column("Note", style="cyan", width=25)
        table.add_column("Preview", style="dim", width=50)
        table.add_column("Matches", justify="center", style="green", width=8)
        
        for result in results:
            snippet = result['snippet'][:100] + '...' if len(result['snippet']) > 100 else result['snippet']
            # Highlight query in snippet
            highlighted_snippet = snippet.replace(query, f"[bold yellow]{query}[/bold yellow]")
            
            table.add_row(
                result['title'][:22] + '...' if len(result['title']) > 22 else result['title'], 
                highlighted_snippet, 
                str(result['matches'])
            )
        
        self.console.print(table)
        self.console.print(f"\n[dim]Use [cyan]show <title>[/cyan] to view a note or try [cyan]live-search[/cyan] for real-time results[/dim]")

