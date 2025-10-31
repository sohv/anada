set -e

echo " Installing Anada..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo " Error: Python 3 is required but not found"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo " Error: Python 3.8+ is required (found $python_version)"
    exit 1
fi

echo " Python $python_version detected"

# Install dependencies and package
echo " Installing dependencies..."
pip3 install -e . --user

# Verify installation
if command -v anada &> /dev/null; then
    echo " Anada installed successfully!"
    echo ""
    echo "Usage:"
    echo "  anada              # Start interactive mode"
    echo "  anada new \"title\"  # Create a new note"
    echo "  anada list         # List all notes"
    echo ""
    echo "Notes are stored in: ~/.notes/notes/"
else
    echo " Installation completed, but 'anada' command not found in PATH"
    echo "   You may need to add Python user bin to your PATH:"
    echo "   export PATH=\$PATH:\$(python3 -m site --user-base)/bin"
fi

