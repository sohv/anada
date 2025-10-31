"""Interactive REPL command mode."""

import os
import subprocess
from typing import List, Optional
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.panel import Panel

from anada.config import Config
from anada.note_manager import NoteManager
from anada.renderer import MarkdownRenderer


class REPL:
    """Interactive REPL for Anada."""
    
    def __init__(self):
        self.config = Config()
        self.console = Console()
        self.note_manager = NoteManager(self.config.notes_dir)
        self.renderer = MarkdownRenderer(
            self.config.get_theme_colors(),
            self.console
        )
        self.session = None
        self.running = True
    
    def _setup_session(self):
        """Setup prompt session with history and autocompletion."""
        history_file = self.config.config_dir / '.anada_history'
        
        # Get note titles for autocompletion
        notes = self.note_manager.list_all()
        note_titles = [note['title'] for note in notes]
        
        commands = ['new', 'edit', 'open', 'show', 'delete', 'list', 'search', 
                   'link', 'backlinks', 'theme', 'editor', 'help', 'quit', 'exit', 'clear']
        completer = WordCompleter(commands + note_titles, ignore_case=True)
        
        self.session = PromptSession(
            history=FileHistory(str(history_file)),
            completer=completer,
            complete_while_typing=True,
        )
    
    def run(self):
        """Start the REPL."""
        self._setup_session()
        
        # Welcome message
        notes_path = self.config.notes_dir
        welcome = Panel.fit(
            f"[bold cyan]Anada[/bold cyan] - Terminal-based Obsidian-like notes\n"
            f"Notes directory: [dim]{notes_path}[/dim]\n"
            f"All notes are [green]persistent[/green] across sessions!\n\n"
            f"Type [dim]help[/dim] for commands or [dim]quit[/dim] to exit.",
            border_style="cyan"
        )
        self.console.print(welcome)
        self.console.print()
        
        while self.running:
            try:
                user_input = self.session.prompt("notes> ")
                if not user_input.strip():
                    continue
                
                self._process_command(user_input.strip())
            except KeyboardInterrupt:
                self.console.print("\n[dim]Press Ctrl+D to exit[/dim]")
            except EOFError:
                self.console.print("\n[dim]Goodbye![/dim]")
                break
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
    
    def _process_command(self, command: str):
        """Process a command."""
        parts = command.split(None, 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd == 'help':
            self._cmd_help()
        elif cmd == 'quit' or cmd == 'exit':
            self.running = False
        elif cmd == 'clear':
            os.system('clear' if os.name != 'nt' else 'cls')
        elif cmd == 'new':
            self._cmd_new(args)
        elif cmd == 'edit' or cmd == 'open':
            self._cmd_edit(args)
        elif cmd == 'show':
            self._cmd_show(args)
        elif cmd == 'delete':
            self._cmd_delete(args)
        elif cmd == 'list':
            self._cmd_list()
        elif cmd == 'search':
            self._cmd_search(args)
        elif cmd == 'link':
            self._cmd_link(args)
        elif cmd == 'backlinks':
            self._cmd_backlinks(args)
        elif cmd == 'theme':
            self._cmd_theme(args)
        elif cmd == 'editor':
            self._cmd_editor(args)
        else:
            # Try to show note if it's a note title
            if self.note_manager.exists(command):
                self._cmd_show(command)
            else:
                self.console.print(f"[red]Unknown command: {cmd}[/red]")
                self.console.print("[dim]Type 'help' for available commands[/dim]")
    
    def _cmd_help(self):
        """Show help message."""
        notes_path = self.config.notes_dir
        help_text = f"""
[bold cyan]Commands:[/bold cyan]

  [cyan]new <title>[/cyan]          Create a new note
  [cyan]edit <title>[/cyan]         Open note in editor
  [cyan]open <title>[/cyan]         Alias for edit
  [cyan]show <title>[/cyan]         Display note content
  [cyan]delete <title>[/cyan]       Delete a note
  [cyan]list[/cyan]                 List all notes
  [cyan]search <query>[/cyan]       Search notes by content
  [cyan]link <title>[/cyan]         Show links in a note
  [cyan]backlinks <title>[/cyan]    Show backlinks to a note
  [cyan]theme <name>[/cyan]         Change theme (default, dark, nord)
  [cyan]editor [name][/cyan]        Show or set editor (nano, vim, etc.)
  [cyan]clear[/cyan]                Clear screen
  [cyan]help[/cyan]                 Show this help
  [cyan]quit[/cyan]                 Exit Anada

[dim]Tip: Type a note title directly to view it[/dim]

[dim]Notes are saved to: {notes_path}[/dim]
[dim]All notes persist across terminal sessions![/dim]
"""
        self.console.print(help_text)
    
    def _cmd_new(self, title: str):
        """Create a new note."""
        if not title:
            self.console.print("[red]Usage: new <title>[/red]")
            return
        
        try:
            path = self.note_manager.create(title)
            self.console.print(f"[green]Created: {path.name}[/green]")
            self.console.print(f"[dim]Saved to: {path}[/dim]")
            # Ask if user wants to edit
            self.console.print("[dim]Note saved. Use 'edit' to open it.[/dim]")
        except FileExistsError as e:
            self.console.print(f"[yellow]{e}[/yellow]")
    
    def _cmd_edit(self, title: str):
        """Edit a note."""
        if not title:
            self.console.print("[red]Usage: edit <title>[/red]")
            return
        
        if not self.note_manager.exists(title):
            # Create if doesn't exist
            self.note_manager.create(title)
        
        path = self.note_manager._get_note_path(title)
        editor = self.config.editor
        
        # Show which editor is being used
        self.console.print(f"[dim]Opening in editor: [cyan]{editor}[/cyan][/dim]")
        if editor == 'vim':
            self.console.print("[dim]Using Vim - Press 'i' to edit, ':wq' to save & exit, ':q!' to exit without saving[/dim]")
        elif editor == 'nano':
            self.console.print("[dim]Using Nano - Ctrl+O to save, Ctrl+X to exit[/dim]")
        
        # Open in editor
        try:
            subprocess.run([editor, str(path)], check=True)
            # After editor closes, note is saved by the editor
            self.console.print(f"[green]Note saved to: {path}[/green]")
        except subprocess.CalledProcessError:
            self.console.print(f"[red]Failed to open editor: {editor}[/red]")
        except FileNotFoundError:
            self.console.print(f"[red]Editor not found: {editor}[/red]")
    
    def _cmd_show(self, title: str):
        """Show a note."""
        if not title:
            self.console.print("[red]Usage: show <title>[/red]")
            return
        
        content = self.note_manager.read(title)
        if content is None:
            self.console.print(f"[red]Note not found: {title}[/red]")
            return
        
        backlinks = self.note_manager.get_backlinks(title)
        
        # Print title
        self.console.print(f"\n[bold cyan]# {title}[/bold cyan]\n")
        
        # Render content
        self.renderer.render_note(title, content, backlinks)
        self.console.print()
    
    def _cmd_delete(self, title: str):
        """Delete a note."""
        if not title:
            self.console.print("[red]Usage: delete <title>[/red]")
            return
        
        if not self.note_manager.exists(title):
            self.console.print(f"[red]Note not found: {title}[/red]")
            return
        
        # Confirm
        confirm = self.session.prompt(f"Delete '{title}'? [y/N]: ")
        if confirm.lower() == 'y':
            self.note_manager.delete(title)
            self.console.print(f"[green]Deleted: {title}[/green]")
        else:
            self.console.print("[dim]Cancelled[/dim]")
    
    def _cmd_list(self):
        """List all notes."""
        notes = self.note_manager.list_all()
        if not notes:
            self.console.print("[dim]No notes found. Create one with 'new <title>'[/dim]")
            return
        
        self.renderer.render_list(notes)
    
    def _cmd_search(self, query: str):
        """Search notes."""
        if not query:
            self.console.print("[red]Usage: search <query>[/red]")
            return
        
        results = self.note_manager.search(query)
        self.renderer.render_search_results(results, query)
    
    def _cmd_link(self, title: str):
        """Show links in a note."""
        if not title:
            self.console.print("[red]Usage: link <title>[/red]")
            return
        
        content = self.note_manager.read(title)
        if content is None:
            self.console.print(f"[red]Note not found: {title}[/red]")
            return
        
        links = self.note_manager.find_links(content)
        if links:
            self.console.print(f"\n[bold cyan]Links in '{title}':[/bold cyan]\n")
            for link in links:
                self.console.print(f"  [[{link}]]")
        else:
            self.console.print(f"[dim]No links found in '{title}'[/dim]")
    
    def _cmd_backlinks(self, title: str):
        """Show backlinks to a note."""
        if not title:
            self.console.print("[red]Usage: backlinks <title>[/red]")
            return
        
        backlinks = self.note_manager.get_backlinks(title)
        if backlinks:
            self.console.print(f"\n[bold cyan]Backlinks to '{title}':[/bold cyan]\n")
            for link in backlinks:
                self.console.print(f"  [[{link}]]")
        else:
            self.console.print(f"[dim]No backlinks found for '{title}'[/dim]")
    
    def _cmd_theme(self, theme_name: str):
        """Change theme."""
        if not theme_name:
            self.console.print("[red]Usage: theme <name>[/red]")
            self.console.print("[dim]Available themes: default, dark, nord[/dim]")
            return
        
        themes = self.config.get('themes', {})
        if theme_name in themes:
            self.config.set('theme', theme_name)
            self.renderer = MarkdownRenderer(
                self.config.get_theme_colors(),
                self.console
            )
            self.console.print(f"[green]Theme changed to: {theme_name}[/green]")
        else:
            self.console.print(f"[red]Unknown theme: {theme_name}[/red]")
            self.console.print("[dim]Available themes: default, dark, nord[/dim]")
    
    def _cmd_editor(self, editor_name: str = None):
        """Show or set the editor."""
        if not editor_name:
            # Show current editor
            current_editor = self.config.editor
            self.console.print(f"\n[bold cyan]Current Editor:[/bold cyan] [yellow]{current_editor}[/yellow]")
            
            # Check if it's vim or nano and show helpful tips
            if current_editor == 'vim':
                self.console.print("\n[dim]You're using [cyan]Vim[/cyan]! Commands:[/dim]")
                self.console.print("  [dim]Press 'i' to enter insert mode[/dim]")
                self.console.print("  [dim]:wq  - Save and exit[/dim]")
                self.console.print("  [dim]:w   - Save without exiting[/dim]")
                self.console.print("  [dim]:q!  - Exit without saving[/dim]")
                self.console.print("  [dim]ESC  - Exit insert mode[/dim]")
            elif current_editor == 'nano':
                self.console.print("\n[dim]You're using [cyan]Nano[/cyan]! Commands:[/dim]")
                self.console.print("  [dim]Ctrl+O  - Save (write out)[/dim]")
                self.console.print("  [dim]Ctrl+X  - Exit[/dim]")
                self.console.print("  [dim]Ctrl+K  - Cut line[/dim]")
                self.console.print("  [dim]Ctrl+U  - Paste[/dim]")
            else:
                self.console.print(f"[dim]Unknown editor type. Make sure '{current_editor}' is installed.[/dim]")
            
            self.console.print(f"\n[dim]To change editor, run: [cyan]editor nano[/cyan] or [cyan]editor vim[/cyan][/dim]")
        else:
            # Set new editor
            # Check if editor exists
            import shutil
            if shutil.which(editor_name):
                self.config.set('editor', editor_name)
                self.console.print(f"[green]Editor changed to: {editor_name}[/green]")
                
                # Show helpful tips for the new editor
                if editor_name == 'nano':
                    self.console.print("[dim]Tip: Use Ctrl+O to save, Ctrl+X to exit[/dim]")
                elif editor_name == 'vim':
                    self.console.print("[dim]Tip: Press 'i' to edit, ':wq' to save & exit[/dim]")
            else:
                self.console.print(f"[red]Editor '{editor_name}' not found in PATH[/red]")
                self.console.print("[dim]Make sure the editor is installed and available in your PATH[/dim]")

