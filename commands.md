# Editor Commands Reference

This guide provides comprehensive commands for the text editors used in Anada.

## Using Nano Editor

If you're using **nano** (or want to use it), here are the essential commands:

### Basic Nano Commands

**Essential Commands for Editing Notes:**

- **Save and Exit**:
  1. Press `Ctrl + O` (Write Out)
  2. Press `Enter` to confirm filename
  3. Press `Ctrl + X` to exit
  > 💡 **Quick tip**: The bottom of nano shows available commands - `^O` means `Ctrl+O`

- **Exit without saving**: Press `Ctrl + X`, then press `N` when asked to save
- **Save without exiting**: Press `Ctrl + O`, then press `Enter`
- **Cut entire line**: `Ctrl + K`
- **Paste**: `Ctrl + U`
- **Search**: `Ctrl + W`
- **Search and replace**: `Ctrl + \`

**Editing Workflow in Nano:**

```bash
notes> edit "my note"
# Nano opens - bottom bar shows commands:
# ^O Write Out  ^X Exit  ^W Where Is  etc.

# Edit your note...
# When done:

# Option 1: Save and exit
Ctrl+O → Enter → Ctrl+X

# Option 2: Just exit (if no changes)
Ctrl+X → N (if asked to save)
```

### Setting Nano as Default Editor

You can set nano as your default editor:

```bash
# Set for current session
export EDITOR=nano

# Set permanently (add to ~/.bashrc or ~/.zshrc)
echo 'export EDITOR=nano' >> ~/.zshrc  # or ~/.bashrc

# Or configure in Anada
anada editor nano
# Or manually edit ~/.notes/config.yml and set:
# editor: nano
```

## Using Vim Editor

For **vim** users, here's a comprehensive guide:

### Basic Vim Commands

**Save and Exit:**
- `:wq` - Write (save) and quit
- `:x` or `ZZ` - Save and exit (shorthand)
- `:wqa` - Save all and quit (if multiple files)

**Exit without saving:**
- `:q!` - Quit without saving (force quit)
- `:q` - Quit (only if no changes)

**Save without exiting:**
- `:w` - Write (save) without exiting
- `:w <filename>` - Save as new file

**Modes:**
- `i` - Enter **insert mode** (start typing/editing)
- `a` - Enter insert mode after cursor
- `o` - Insert new line below and enter insert mode
- `O` - Insert new line above and enter insert mode
- `Esc` - Exit insert mode (return to **normal mode**)

### Navigation Commands (Normal Mode)

**Basic Movement:**
- `h` - Move left ←
- `j` - Move down ↓
- `k` - Move up ↑
- `l` - Move right →
- `0` - Move to beginning of line
- `$` - Move to end of line
- `^` - Move to first non-blank character of line

**Word Movement:**
- `w` - Move forward to start of next word
- `b` - Move backward to start of previous word
- `e` - Move to end of current word
- `W`, `B`, `E` - Same as above but ignore punctuation

**Line Movement:**
- `gg` - Move to beginning of file (top)
- `G` - Move to end of file (bottom)
- `:<number>` then `Enter` - Jump to line number (e.g., `:15` goes to line 15)
- `{` - Move to previous paragraph/block
- `}` - Move to next paragraph/block

**Screen Movement:**
- `Ctrl + f` - Move forward one screen (page down)
- `Ctrl + b` - Move backward one screen (page up)
- `Ctrl + d` - Move down half screen
- `Ctrl + u` - Move up half screen
- `H` - Move to top of screen (High)
- `M` - Move to middle of screen (Middle)
- `L` - Move to bottom of screen (Low)

### Editing Commands

**Deletion:**
- `x` - Delete character under cursor
- `X` - Delete character before cursor
- `dd` - Delete entire line
- `dw` - Delete word
- `d$` or `D` - Delete from cursor to end of line
- `d0` - Delete from cursor to beginning of line
- `dG` - Delete from cursor to end of file
- `dgg` - Delete from cursor to beginning of file

**Copy & Paste:**
- `yy` - Yank (copy) entire line
- `yw` - Yank word
- `y$` - Yank from cursor to end of line
- `p` - Paste after cursor
- `P` - Paste before cursor

**Undo/Redo:**
- `u` - Undo last change
- `Ctrl + r` - Redo (undo the undo)

**Find & Replace:**
- `/pattern` - Search forward for pattern (press `Enter` to search)
- `?pattern` - Search backward for pattern
- `n` - Find next match
- `N` - Find previous match
- `:%s/old/new/g` - Replace all occurrences of "old" with "new"
- `:%s/old/new/gc` - Replace with confirmation (interactive)

### Editing Workflow in Vim

```bash
notes> edit "my note"
# Vim opens - you're in normal mode

# Step 1: Navigate to where you want to edit
# Use h, j, k, l or arrow keys to move around
# Use /pattern to search for text

# Step 2: Enter insert mode
Press 'i' to start editing

# Step 3: Type your content
# Edit your note...

# Step 4: Exit insert mode
Press Esc to return to normal mode

# Step 5: Save and exit
Type :wq and press Enter
# Or just :x or ZZ

# Alternative: Exit without saving
Type :q! and press Enter
```

**Quick Reference:**

```text
Normal Mode → Press 'i' → Insert Mode → Press Esc → Normal Mode → :wq → Exit
```

**Common Patterns:**
- `i` → edit → `Esc` → `:wq` → Save & exit
- `i` → edit → `Esc` → `:q!` → Exit without saving
- `dd` → Delete line → `p` → Paste it back
- `/word` → `Enter` → Find word → `n` → Find next
- `gg` → Go to top → `G` → Go to bottom

### Setting Vim as Default Editor

```bash
# Set for current session
export EDITOR=vim

# Set permanently (add to ~/.bashrc or ~/.zshrc)
echo 'export EDITOR=vim' >> ~/.zshrc  # or ~/.bashrc

# Or configure in Anada
anada editor vim
# Or manually edit ~/.notes/config.yml and set:
# editor: vim
```

