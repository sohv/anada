"""Interactive REPL command mode."""

import os
import subprocess
from typing import List, Optional
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import radiolist_dialog, input_dialog
from prompt_toolkit.formatted_text import HTML
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich.table import Table
from rich import box

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
        self.interactive_mode = False
        self.status_info = {
            'total_notes': 0,
            'last_modified': 'Never',
            'current_theme': self.config.theme
        }
    
    def _setup_session(self):
        """Setup prompt session with history and autocompletion."""
        history_file = self.config.config_dir / '.anada_history'
        
        # Get note titles for autocompletion
        notes = self.note_manager.list_all()
        note_titles = [note['title'] for note in notes]
        
        commands = ['new', 'edit', 'open', 'show', 'delete', 'list', 'search', 
                   'link', 'backlinks', 'theme', 'editor', 'help', 'quit', 'exit', 'clear',
                   'menu', 'live-search', 'status', 'interactive', 'user']
        completer = WordCompleter(commands + note_titles, ignore_case=True)
        
        self.session = PromptSession(
            history=FileHistory(str(history_file)),
            completer=completer,
            complete_while_typing=True,
        )
        
        # Update status info
        self._update_status_info()
    
    def run(self):
        """Start the REPL."""
        self._setup_session()
        
        # Get or prompt for user name
        user_name = self.config.prompt_for_user_name()
        
        # Welcome message
        notes_path = self.config.notes_dir
        if user_name:
            greeting = f"Welcome back, {user_name}!"
        else:
            greeting = "Welcome to Anada!"
            
        welcome = Panel.fit(
            f"[bold cyan]Anada[/bold cyan] - Terminal-based Obsidian-like notes\n"
            f"{greeting}\n"
            f"Notes directory: [dim]{notes_path}[/dim]\n"
            f"All notes are [green]persistent[/green] across sessions!\n\n"
            f"[bold yellow]Interactive Features:[/bold yellow]\n"
            f"• [green]menu[/green] - Interactive command menu\n"
            f"• [green]live-search[/green] - Real-time search with preview\n"
            f"• [green]status[/green] - Live dashboard\n\n"
            f"Type [dim]help[/dim] for all commands or [dim]quit[/dim] to exit.",
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
        elif cmd == 'menu':
            self._cmd_interactive_menu()
        elif cmd == 'live-search':
            self._cmd_live_search()
        elif cmd == 'status':
            self._cmd_show_status()
        elif cmd == 'interactive':
            self._cmd_toggle_interactive()
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
        elif cmd == 'user':
            self._cmd_user(args)
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
  [cyan]theme <name>[/cyan]         Change theme (default, dark, nord, cyan, brown, grey)
  [cyan]editor [name][/cyan]        Show or set editor (nano, vim, etc.)
  [cyan]user [name][/cyan]          Show or set user name
  [cyan]clear[/cyan]                Clear screen
  [cyan]help[/cyan]                 Show this help
  [cyan]quit[/cyan]                 Exit Anada

[bold green]Interactive Features:[/bold green]

  [green]menu[/green]                   Interactive command menu
  [green]live-search[/green]            Real-time search with preview
  [green]status[/green]                Show live statistics
  [green]interactive[/green]           Toggle interactive mode

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
        
        # Add simple footer with quick commands
        self.console.print(f"[dim]edit {title} | link {title} | delete {title}[/dim]")
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
            self.console.print("[dim]Available themes: default, dark, nord, cyan, brown, grey[/dim]")
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
            self.console.print("[dim]Available themes: default, dark, nord, cyan, brown, grey[/dim]")
    
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
    
    def _cmd_user(self, user_name: str = None):
        """Show or set the user name."""
        if not user_name:
            # Show current user
            current_user = self.config.user_name
            if current_user:
                self.console.print(f"\n[bold cyan]Current User:[/bold cyan] [yellow]{current_user}[/yellow]")
            else:
                self.console.print("\n[dim]No user name set[/dim]")
            self.console.print(f"\n[dim]To change: [cyan]user \"Your Name\"[/cyan][/dim]")
        else:
            # Set new user name
            self.config.set_user_name(user_name)
            self.console.print(f"[green]User name set to: {user_name}[/green]")
            self.console.print("[dim]You'll see a personalized welcome message next time![/dim]")
    
    def _update_status_info(self):
        """Update status information."""
        notes = self.note_manager.list_all()
        self.status_info['total_notes'] = len(notes)
        if notes:
            latest = max(notes, key=lambda x: x['modified'])
            self.status_info['last_modified'] = latest['modified'].strftime('%Y-%m-%d %H:%M')
        else:
            self.status_info['last_modified'] = 'Never'
        self.status_info['current_theme'] = self.config.theme
    
    def _cmd_interactive_menu(self):
        """Show interactive command menu."""
        try:
            # Create menu options
            choices = [
                ('new', 'Create a new note'),
                ('list', 'List all notes'),
                ('search', 'Search notes'),
                ('live-search', 'Interactive search with preview'),
                ('theme_menu', 'Change theme'),
                ('editor_menu', 'Configure editor'),
                ('status', 'Show status information'),
                ('help', 'Show help'),
                ('quit', 'Exit Anada')
            ]
            
            result = radiolist_dialog(
                title="Anada Interactive Menu",
                text="Select an action:",
                values=choices,
                style="class:radiolist"
            ).run()
            
            if result:
                if result == 'new':
                    title = input_dialog(
                        title="Create New Note",
                        text="Enter note title:"
                    ).run()
                    if title:
                        self._cmd_new(title)
                elif result == 'search':
                    query = input_dialog(
                        title="Search Notes",
                        text="Enter search query:"
                    ).run()
                    if query:
                        self._cmd_search(query)
                elif result == 'theme_menu':
                    self._show_theme_menu()
                elif result == 'editor_menu':
                    self._show_editor_menu()
                else:
                    # Execute the command directly
                    self._process_command(result)
        except Exception as e:
            self.console.print(f"[yellow]Interactive menu not available: {e}[/yellow]")
            self.console.print("[dim]Try using individual commands instead[/dim]")
    
    def _show_theme_menu(self):
        """Show theme selection menu."""
        try:
            themes = list(self.config.get('themes', {}).keys())
            choices = [(theme, f"Switch to {theme} theme") for theme in themes]
            
            result = radiolist_dialog(
                title="Select Theme",
                text=f"Current theme: {self.config.theme}",
                values=choices
            ).run()
            
            if result:
                self._cmd_theme(result)
        except Exception as e:
            self.console.print(f"[yellow]Theme menu not available: {e}[/yellow]")
            self.console.print("[dim]Use 'theme <name>' command instead[/dim]")
    
    def _show_editor_menu(self):
        """Show editor selection menu."""
        try:
            editors = [
                ('nano', 'Nano - Simple and beginner-friendly'),
                ('vim', 'Vim - Powerful text editor'),
                ('code', 'VS Code - Modern editor'),
                ('emacs', 'Emacs - Extensible editor'),
                ('micro', 'Micro - Modern terminal editor')
            ]
            
            result = radiolist_dialog(
                title="Select Editor",
                text=f"Current editor: {self.config.editor}",
                values=editors
            ).run()
            
            if result:
                self._cmd_editor(result)
        except Exception as e:
            self.console.print(f"[yellow]Editor menu not available: {e}[/yellow]")
            self.console.print("[dim]Use 'editor <name>' command instead[/dim]")
    
    def _cmd_live_search(self):
        """Interactive live search with note preview."""
        self.console.print("[bold cyan]🔍 Live Search Mode[/bold cyan]")
        self.console.print("[dim]Type to search, press Enter to view note, Ctrl+C to exit[/dim]\n")
        
        try:
            query = ""
            while True:
                try:
                    if query:
                        # Show search prompt with current query
                        user_input = self.session.prompt(f"search ({query})> ")
                    else:
                        user_input = self.session.prompt("search> ")
                    
                    if not user_input.strip():
                        if query:
                            # Show current results
                            results = self.note_manager.search(query)
                            self._show_live_preview(results, query)
                        continue
                    
                    # Check if it's a command to select a note
                    if user_input.startswith('show '):
                        title = user_input[5:].strip()
                        if self.note_manager.exists(title):
                            self._cmd_show(title)
                        else:
                            self.console.print(f"[red]Note not found: {title}[/red]")
                            self.console.print("[dim]Available notes can be seen in the search results above[/dim]")
                        continue
                    elif user_input == 'exit' or user_input == 'quit':
                        break
                    elif user_input == 'clear':
                        query = ""
                        os.system('clear' if os.name != 'nt' else 'cls')
                        self.console.print("[bold cyan]🔍 Live Search Mode[/bold cyan]")
                        continue
                    
                    # Update search query
                    query = user_input
                    results = self.note_manager.search(query)
                    self._show_live_preview(results, query)
                    
                except KeyboardInterrupt:
                    break
                    
        except Exception as e:
            self.console.print(f"[red]Live search error: {e}[/red]")
        
        self.console.print("\n[dim]Exited live search mode[/dim]")
    
    def _show_live_preview(self, results, query):
        """Show live search results with preview."""
        if not results:
            self.console.print(f"[dim]No results for '{query}'[/dim]")
            return
        
        # Create a table for results
        table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
        table.add_column("Note", style="cyan", width=25)
        table.add_column("Preview", style="dim", width=50)
        table.add_column("Matches", justify="center", style="green", width=8)
        
        for i, result in enumerate(results[:5]):  # Show top 5 results
            preview = result['snippet'][:80] + '...' if len(result['snippet']) > 80 else result['snippet']
            # Highlight the query in preview
            preview = preview.replace(query, f"[bold yellow]{query}[/bold yellow]")
            table.add_row(
                result['title'][:25] + '...' if len(result['title']) > 25 else result['title'],
                preview,
                str(result['matches'])
            )
        
        self.console.print(table)
        if len(results) > 5:
            self.console.print(f"[dim]... and {len(results) - 5} more results[/dim]")
        
        self.console.print(f"\n[dim]Type 'show <note_title>' to view a note, 'clear' to reset, or Ctrl+C to exit[/dim]")
    
    def _cmd_show_status(self):
        """Show live status information."""
        self._update_status_info()
        
        # Create status panel
        layout = Layout()
        
        # Status table
        status_table = Table(box=box.ROUNDED, show_header=False, title="Anada Status")
        status_table.add_column("Metric", style="cyan", width=20)
        status_table.add_column("Value", style="bright_white", width=30)
        
        status_table.add_row("Total Notes", str(self.status_info['total_notes']))
        status_table.add_row("Last Modified", self.status_info['last_modified'])
        status_table.add_row("Current Theme", self.status_info['current_theme'])
        status_table.add_row("Editor", self.config.editor)
        status_table.add_row("Notes Directory", str(self.config.notes_dir))
        
        # Recent notes table
        notes = self.note_manager.list_all()
        recent_table = Table(box=box.ROUNDED, show_header=True, title="Recent Notes")
        recent_table.add_column("Note", style="cyan", width=25)
        recent_table.add_column("Modified", style="dim", width=20)
        recent_table.add_column("Size", style="dim", width=10)
        
        for note in notes[:5]:  # Show 5 most recent
            recent_table.add_row(
                note['title'][:22] + '...' if len(note['title']) > 22 else note['title'],
                note['modified'].strftime('%m-%d %H:%M'),
                f"{note['size']} B"
            )
        
        # Display both tables
        self.console.print(status_table)
        self.console.print()
        if notes:
            self.console.print(recent_table)
        else:
            self.console.print("[dim]No notes created yet. Use 'new <title>' to create your first note![/dim]")
    
    def _cmd_toggle_interactive(self):
        """Toggle interactive mode features."""
        self.interactive_mode = not self.interactive_mode
        if self.interactive_mode:
            self.console.print("[bold green]Interactive mode enabled![/bold green]")
            self.console.print("[dim]Enhanced features are now active. Try 'menu', 'live-search', or 'status'[/dim]")
        else:
            self.console.print("[dim]Interactive mode disabled[/dim]")
    
    def _cmd_live_search(self):
        """Interactive live search with note preview."""
        self.console.print("[bold cyan]Live Search Mode[/bold cyan]")
        self.console.print("[dim]Type to search, press Enter to view note, Ctrl+C to exit[/dim]\n")

