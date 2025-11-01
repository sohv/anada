"""Main CLI entry point for Anada."""

import sys
import click
from rich.console import Console

from anada.config import Config
from anada.note_manager import NoteManager
from anada.renderer import MarkdownRenderer
from anada.repl import REPL


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show version')
@click.pass_context
def cli(ctx, version):
    """Anada - Terminal-based Obsidian-like note-taking tool."""
    if version:
        from anada import __version__
        print(f"Anada v{__version__}")
        sys.exit(0)
    
    # If no subcommand, start REPL
    if ctx.invoked_subcommand is None:
        repl = REPL()
        repl.run()


@cli.command()
@click.argument('title')
def new(title):
    """Create a new note."""
    config = Config()
    manager = NoteManager(config.notes_dir)
    console = Console()
    
    try:
        path = manager.create(title)
        console.print(f"[green]Created: {path.name}[/green]")
        console.print(f"[dim]Saved to: {path}[/dim]")
    except FileExistsError as e:
        console.print(f"[yellow]{e}[/yellow]")
        sys.exit(1)


@cli.command()
@click.argument('title')
def show(title):
    """Show a note."""
    config = Config()
    manager = NoteManager(config.notes_dir)
    console = Console()
    renderer = MarkdownRenderer(config.get_theme_colors(), console)
    
    content = manager.read(title)
    if content is None:
        console.print(f"[red]Note not found: {title}[/red]")
        sys.exit(1)
    
    # Render content only - no automatic backlinks
    renderer.render_note(title, content)


@cli.command()
@click.argument('title')
@click.confirmation_option(prompt='Are you sure you want to delete this note?')
def delete(title):
    """Delete a note."""
    config = Config()
    manager = NoteManager(config.notes_dir)
    console = Console()
    
    if not manager.exists(title):
        console.print(f"[red]Note not found: {title}[/red]")
        sys.exit(1)
    
    manager.delete(title)
    console.print(f"[green]Deleted: {title}[/green]")


@cli.command()
def list():
    """List all notes."""
    config = Config()
    manager = NoteManager(config.notes_dir)
    console = Console()
    renderer = MarkdownRenderer(config.get_theme_colors(), console)
    
    notes = manager.list_all()
    renderer.render_list(notes)


@cli.command()
@click.argument('query')
def search(query):
    """Search notes by content."""
    config = Config()
    manager = NoteManager(config.notes_dir)
    console = Console()
    renderer = MarkdownRenderer(config.get_theme_colors(), console)
    
    results = manager.search(query)
    renderer.render_search_results(results, query)


@cli.command()
@click.argument('title')
def link(title):
    """Show links in a note."""
    config = Config()
    manager = NoteManager(config.notes_dir)
    console = Console()
    
    content = manager.read(title)
    if content is None:
        console.print(f"[red]Note not found: {title}[/red]")
        sys.exit(1)
    
    links = manager.find_links(content)
    if links:
        console.print(f"\n[bold cyan]Links in '{title}':[/bold cyan]\n")
        for link_title in links:
            # Use print() to avoid Rich markup interpretation
            print(f"  [[{link_title}]]")
    else:
        console.print(f"[dim]No links found in '{title}'[/dim]")


@cli.command()
@click.argument('title')
def backlinks(title):
    """Show backlinks to a note."""
    config = Config()
    manager = NoteManager(config.notes_dir)
    console = Console()
    
    backlinks = manager.get_backlinks(title)
    if backlinks:
        console.print(f"\n[bold cyan]Backlinks to '{title}':[/bold cyan]\n")
        for link in backlinks:
            # Use print() to avoid Rich markup interpretation
            print(f"  [[{link}]]")
    else:
        console.print(f"[dim]No backlinks found for '{title}'[/dim]")


@cli.command()
@click.argument('theme_name')
def theme(theme_name):
    """Change theme."""
    config = Config()
    console = Console()
    
    themes = config.get('themes', {})
    if theme_name in themes:
        config.set('theme', theme_name)
        console.print(f"[green]Theme changed to: {theme_name}[/green]")
    else:
        console.print(f"[red]Unknown theme: {theme_name}[/red]")
        console.print("[dim]Available themes: default, dark, nord[/dim]")
        sys.exit(1)


@cli.command()
@click.argument('editor_name', required=False)
def editor(editor_name):
    """Show or set the editor."""
    import shutil
    
    config = Config()
    console = Console()
    
    if not editor_name:
        # Show current editor
        current_editor = config.editor
        console.print(f"\n[bold cyan]Current Editor:[/bold cyan] [yellow]{current_editor}[/yellow]")
        
        if current_editor == 'vim':
            console.print("\n[dim]Using [cyan]Vim[/cyan] - Press 'i' to edit, ':wq' to save & exit[/dim]")
        elif current_editor == 'nano':
            console.print("\n[dim]Using [cyan]Nano[/cyan] - Ctrl+O to save, Ctrl+X to exit[/dim]")
        
        console.print(f"\n[dim]To change: [cyan]anada editor nano[/cyan] or [cyan]anada editor vim[/cyan][/dim]")
    else:
        # Set new editor
        if shutil.which(editor_name):
            config.set('editor', editor_name)
            console.print(f"[green]Editor changed to: {editor_name}[/green]")
            
            if editor_name == 'nano':
                console.print("[dim]Tip: Use Ctrl+O to save, Ctrl+X to exit[/dim]")
            elif editor_name == 'vim':
                console.print("[dim]Tip: Press 'i' to edit, ':wq' to save & exit[/dim]")
        else:
            console.print(f"[red]Editor '{editor_name}' not found[/red]")
            sys.exit(1)


@cli.command()
@click.argument('title')
def edit(title):
    """Edit a note in your default editor."""
    import subprocess
    
    config = Config()
    manager = NoteManager(config.notes_dir)
    console = Console()
    
    if not manager.exists(title):
        manager.create(title)
    
    path = manager._get_note_path(title)
    editor_cmd = config.editor
    
    # Show which editor is being used
    console.print(f"[dim]Opening in: [cyan]{editor_cmd}[/cyan][/dim]")
    if editor_cmd == 'vim':
        console.print("[dim]Vim commands: Press 'i' to edit, ':wq' to save & exit[/dim]")
    elif editor_cmd == 'nano':
        console.print("[dim]Nano commands: Ctrl+O to save, Ctrl+X to exit[/dim]")
    
    try:
        subprocess.run([editor_cmd, str(path)], check=True)
        console.print(f"[green]Note saved to: {path}[/green]")
    except Exception as e:
        console.print(f"[red]Failed to open editor: {e}[/red]")
        sys.exit(1)


if __name__ == '__main__':
    cli()

