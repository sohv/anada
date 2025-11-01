"""Configuration management for Anada."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Manages configuration for Anada."""
    
    DEFAULT_CONFIG = {
        'notes_dir': '~/.notes/notes',
        'config_dir': '~/.notes',
        'editor': os.environ.get('EDITOR', 'vim'),
        'theme': 'default',
        'themes': {
            'default': {
                'header': 'cyan',
                'bold': 'bright_white',
                'link': 'blue',
                'code': 'yellow',
                'italic': 'white',
                'blockquote': 'dim white',
            },
            'dark': {
                'header': 'bright_cyan',
                'bold': 'white',
                'link': 'bright_blue',
                'code': 'bright_yellow',
                'italic': 'dim white',
                'blockquote': 'dim white',
            },
            'nord': {
                'header': '#88C0D0',
                'bold': '#ECEFF4',
                'link': '#5E81AC',
                'code': '#EBCB8B',
                'italic': '#D8DEE9',
                'blockquote': '#4C566A',
            }
        }
    }
    
    def __init__(self):
        self.config_dir = Path(self.DEFAULT_CONFIG['config_dir']).expanduser()
        self.config_file = self.config_dir / 'config.yml'
        self.notes_dir = Path(self.DEFAULT_CONFIG['notes_dir']).expanduser()
        self._config = self.DEFAULT_CONFIG.copy()
        self.load()
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure config and notes directories exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.notes_dir.mkdir(parents=True, exist_ok=True)
    
    def load(self):
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded = yaml.safe_load(f) or {}
                    self._config.update(loaded)
            except Exception as e:
                print(f"Warning: Could not load config: {e}")
        
        # Update paths after loading
        if 'notes_dir' in self._config:
            self.notes_dir = Path(self._config['notes_dir']).expanduser()
        if 'config_dir' in self._config:
            self.config_dir = Path(self._config['config_dir']).expanduser()
    
    def save(self):
        """Save current configuration to file."""
        self._ensure_directories()
        with open(self.config_file, 'w') as f:
            yaml.dump(self._config, f, default_flow_style=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a config value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a config value."""
        self._config[key] = value
        self.save()
    
    @property
    def editor(self) -> str:
        """Get the configured editor."""
        return self._config.get('editor', os.environ.get('EDITOR', 'vim'))
    
    @property
    def theme(self) -> str:
        """Get current theme name."""
        return self._config.get('theme', 'default')
    
    def get_theme_colors(self) -> Dict[str, str]:
        """Get color scheme for current theme."""
        theme_name = self.theme
        themes = self._config.get('themes', {})
        return themes.get(theme_name, themes.get('default', {}))
    
    @property
    def user_name(self) -> Optional[str]:
        """Get the configured user name."""
        return self._config.get('user_name')
    
    def set_user_name(self, name: str):
        """Set the user name."""
        self._config['user_name'] = name
        self.save()
    
    def prompt_for_user_name(self) -> str:
        """Prompt user for their name if not set."""
        if not self.user_name:
            print("\nWelcome to Anada! Let's personalize your experience.")
            name = input("What's your name? ").strip()
            if name:
                self.set_user_name(name)
                print(f"Nice to meet you, {name}!")
                return name
        return self.user_name

