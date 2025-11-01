# Anada

A lightweight, terminal-first note-taking tool with Markdown support and bi-directional linking. 

<!--
Anada is Obsidian distilled for the terminal: fast, lightweight, scriptable, and distraction-free — perfect for developers and terminal lovers who want a Markdown-based PKM without leaving the CLI.-->

[![PyPI version](https://badge.fury.io/py/anada.svg)](https://pypi.org/project/anada/) 
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


>NOTE: A detailed documentation is under development and will be available soon.

## Why Anada?

- **Terminal-first & Lightweight** – Fast, distraction-free, runs entirely in the terminal.
- **Plain Markdown Notes** – Fully persistent `.md` files accessible with any editor.
- **Interactive CLI & REPL** – Create, edit, search, and link notes from the command line.
- **Bi-directional Linking** – [[note]] style links with automatic backlinks.
- **Customizable Themes & Editor** – Pick your favorite terminal theme and editor.
- **Developer-friendly** – Scriptable, works with Git, perfect for terminal workflows.

## Installation

### Install from PyPI

```bash
pip install anada
```

After installation, use `anada` command:

```bash
anada  # Start interactive mode
anada new "my note"  # Create a note
anada list  # List all notes
```

### Install from GitHub

```bash
pip install git+https://github.com/sohv/anada.git
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/sohv/anada.git
cd anada

# Install dependencies and package
pip install -e .

# Or install normally
pip install .
```

### Development Installation

```bash
git clone https://github.com/sohv/anada.git
cd anada
pip install -r requirements.txt
pip install -e .
```

For deployment instructions, see [deployment](deploy.md).

# Features

- **CRUD Operations** - Create, read, update, and delete Markdown notes
- **Persistent Storage** - All notes saved to disk (`~/.notes/notes/`) and persist across sessions
- **Bi-directional Links** - `[[note]]` style links with automatic backlinks
- **Full-text Search** - Search notes by content
- **Interactive REPL** - Command mode with autocompletion and history
- **Theming** - Multiple color themes (default, dark, nord)
- **Lightweight** - Minimal dependencies, runs everywhere

## Usage

### Interactive Mode

```bash
python main.py
# or
./main.py
```

This starts an interactive REPL where you can use commands:

```bash
notes> new "project ideas"
notes> edit "project ideas"
notes> list
notes> search "obsidian"
notes> theme dark
notes> help
```

### Command Mode

You can also use Anada as a CLI tool:

```bash
# Create a new note
python main.py new "my note"

# Edit a note
python main.py edit "my note"

# Show a note
python main.py show "my note"

# List all notes
python main.py list

# Search notes
python main.py search "keyword"

# Show links in a note
python main.py link "my note"

# Show backlinks
python main.py backlinks "my note"

# Change theme
python main.py theme nord
```

## Commands

| Command | Description |
|---------|-------------|
| `new <title>` | Create a new note |
| `edit <title>` | Open note in your default editor (`$EDITOR`) |
| `show <title>` | Display note content with backlinks |
| `delete <title>` | Delete a note |
| `list` | List all notes with metadata |
| `search <query>` | Search notes by content |
| `link <title>` | Show all `[[links]]` in a note |
| `backlinks <title>` | Show notes that link to this note |
| `theme <name>` | Change theme (default, dark, nord) |
| `editor [name]` | Show or set editor (nano, vim, etc.) |
| `help` | Show help message |
| `quit` | Exit Anada |

## Editing Notes

When you use `edit <title>` or `open <title>`, Anada opens the note in your default editor. The editor is determined by:

1. The `editor` setting in `~/.notes/config.yml`
2. The `$EDITOR` environment variable
3. Defaults to `vim` if neither is set

### Setting Up Your Editor

**Check or Change Editor:**

```bash
# In interactive mode
notes> editor          # Show current editor
notes> editor nano     # Change to nano
notes> editor vim      # Change to vim

# Or via command line
anada editor          # Show current editor
anada editor nano     # Change to nano
```

**Set Editor via Environment Variable:**

```bash
# For current session
export EDITOR=nano

# Permanently (add to ~/.bashrc or ~/.zshrc)
echo 'export EDITOR=nano' >> ~/.zshrc  # or ~/.bashrc
```

**Editor Commands Reference:**

For comprehensive editor commands (nano and vim), see [commands.md](commands.md):

- Nano commands: Save, exit, navigation, etc.
- Vim commands: Navigation, editing, save/exit, etc.

## Configuration

Configuration is stored in `~/.notes/config.yml`. You can customize:

- `notes_dir`: Directory where notes are stored (default: `~/.notes/notes`)
- `editor`: Editor command (default: `$EDITOR` or `vim`)
- `theme`: Current theme name (default: `default`)

Themes are defined in the config file and can be customized.

## Linking Notes

Anada uses Obsidian-style links:

```markdown
# My Note

This is related to [[another note]].
```

When you view a note, Anada automatically shows:
- All links in the note
- All notes that link back to this note (backlinks)

## Directory Structure

```
~/.notes/
├── notes/                    # All your notes are stored here
│   ├── my_note.md           # Each note is a .md file
│   ├── project_ideas.md     # Notes persist across sessions!
├── config.yml               # Configuration file
└── .anada_history            # Command history
```

**Important:** All notes are saved to `~/.notes/notes/` directory on your filesystem. This means:
- Notes persist across terminal sessions
- Notes are saved immediately when created/edited
- You can access notes even after closing and reopening the terminal
- Notes are plain Markdown files - you can edit them with any text editor

## Tech Stack

- **Python 3.8+** - Core language
- **Rich** - Beautiful terminal output
- **prompt-toolkit** - Interactive REPL with autocompletion
- **Click** - CLI framework
- **PyYAML** - Configuration management

## Examples

### Creating and Linking Notes

```bash
notes> new "project ideas"
Created: project_ideas.md

notes> new "terminal tools"
Created: terminal_tools.md

notes> edit "project ideas"
# Opens in your editor - add: "See [[terminal tools]] for inspiration"

notes> show "terminal tools"
# Shows note with backlinks showing it's linked from "project ideas"
```

### Searching

```bash
notes> search "project"
# Shows all notes containing "project"
```

### Theming

```bash
notes> theme nord
Theme changed to: nord
```

## Future Enhancements

- Graph visualization (ASCII or web export)
- Tag support (`#tag` parsing)
- Sync/export to Obsidian folder
- Plugin hooks for extensibility
- Enhanced Markdown rendering with syntax highlighting

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

