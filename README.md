# Modern Notepad App

A comprehensive, cross-platform note-taking application with advanced features including spell checking, rich text editing, and multiple export formats.

## 🌟 Features

### Core Features
- **Rich Text Editing**: Full-featured text editor with formatting support
- **Spell Checking**: Real-time spell checking with suggestions and custom dictionary
- **Multiple Export Formats**: Export notes in 16+ formats including PDF, HTML, Markdown, and programming languages
- **Categories & Organization**: Organize notes with categories and favorites
- **Search & Filter**: Powerful search and filtering capabilities
- **Auto-save & Backup**: Automatic saving and backup system
- **Themes**: Light and dark theme support
- **Templates**: Pre-built note templates for different use cases

### Advanced Features
- **Focus Mode**: Distraction-free writing environment
- **Keyboard Shortcuts**: Comprehensive keyboard shortcuts for productivity
- **Statistics**: Detailed statistics about your notes
- **Import/Export**: Import text files and export in multiple formats
- **Responsive Design**: Modern, responsive user interface

## 🚀 Quick Start

### Python Version (Recommended)

#### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

#### Installation

1. **Clone or download the repository**
   \`\`\`bash
   git clone <repository-url>
   cd modern-notepad-app
   \`\`\`

2. **Install Python dependencies**
   \`\`\`bash
   cd python
   pip install -r requirements.txt
   \`\`\`

3. **Run the application**
   \`\`\`bash
   python notepad_app.py
   \`\`\`

#### Alternative Installation Methods

**Using virtual environment (recommended):**
\`\`\`bash
# Create virtual environment
python -m venv notepad_env

# Activate virtual environment
# On Windows:
notepad_env\Scripts\activate
# On macOS/Linux:
source notepad_env/bin/activate

# Install dependencies
pip install -r python/requirements.txt

# Run the application
python python/notepad_app.py
\`\`\`

**Using conda:**
\`\`\`bash
# Create conda environment
conda create -n notepad python=3.9
conda activate notepad

# Install dependencies
pip install -r python/requirements.txt

# Run the application
python python/notepad_app.py
\`\`\`

### Web Version (Next.js)

#### Prerequisites
- Node.js 18 or higher
- npm or yarn

#### Installation

1. **Install dependencies**
   \`\`\`bash
   npm install
   # or
   yarn install
   \`\`\`

2. **Run the development server**
   \`\`\`bash
   npm run dev
   # or
   yarn dev
   \`\`\`

3. **Open your browser**
   Navigate to `http://localhost:3000`

## 📋 System Requirements

### Python Version
- **Operating System**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 512 MB minimum, 1 GB recommended
- **Storage**: 100 MB free space
- **Display**: 1024x768 minimum resolution

### Web Version
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **JavaScript**: Enabled
- **Local Storage**: 10 MB available

## 🎯 Usage Guide

### Getting Started

1. **Create Your First Note**
   - Click "New Note" or press `Ctrl+N`
   - Choose from available templates or start with a blank note
   - Enter a title and start writing

2. **Organize with Categories**
   - Add categories to organize your notes
   - Use the category filter to find related notes
   - Mark important notes as favorites with the ⭐ button

3. **Use Spell Checking**
   - Spell checking is enabled by default
   - Misspelled words are underlined in red
   - Click on misspelled words to see suggestions
   - Add words to your personal dictionary

### Keyboard Shortcuts

#### File Operations
- `Ctrl+N` - New Note
- `Ctrl+O` - Open File
- `Ctrl+S` - Save
- `Ctrl+E` - Export Note
- `Ctrl+P` - Print

#### Edit Operations
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo
- `Ctrl+X` - Cut
- `Ctrl+C` - Copy
- `Ctrl+V` - Paste
- `Ctrl+H` - Find & Replace

#### Formatting
- `Ctrl+B` - Bold
- `Ctrl+I` - Italic
- `Ctrl+U` - Underline

#### Spell Check
- `Ctrl+Shift+S` - Toggle Spell Check
- `F7` - Check Spelling Now

#### View
- `Ctrl+T` - Toggle Theme
- `F11` - Focus Mode
- `Ctrl+Shift+T` - Statistics

### Export Formats

The application supports exporting notes in multiple formats:

- **Text Formats**: Plain Text (.txt), Markdown (.md), Rich Text (.rtf)
- **Document Formats**: PDF (.pdf), HTML (.html), LaTeX (.tex)
- **Data Formats**: JSON (.json), XML (.xml), CSV (.csv), YAML (.yaml)
- **Programming Languages**: C (.c), Python (.py), JavaScript (.js), SQL (.sql)
- **Assembly Languages**: Assembly (.asm), NASM (.nasm)

### Spell Checking Features

- **Real-time Checking**: Words are checked as you type
- **Smart Suggestions**: Multiple suggestion algorithms including:
  - Edit distance (Levenshtein)
  - Phonetic matching (Soundex)
  - Keyboard layout awareness
- **Custom Dictionary**: Add your own words
- **Ignore Words**: Temporarily ignore specific words
- **Multiple Languages**: Support for different language dictionaries

## 🔧 Configuration

### Settings File Location

**Python Version:**
- Windows: `%USERPROFILE%\.notepad_app\settings.json`
- macOS: `~/.notepad_app/settings.json`
- Linux: `~/.notepad_app/settings.json`

**Web Version:**
- Browser Local Storage

### Available Settings

\`\`\`json
{
  "theme": "light",
  "font_family": "Arial",
  "font_size": 12,
  "auto_save_interval": 30,
  "word_wrap": true,
  "show_line_numbers": false,
  "backup_enabled": true,
  "backup_interval": 300,
  "spell_check_enabled": true,
  "auto_correct": false
}
\`\`\`

### Custom Dictionary

Add words to your personal dictionary:
- Right-click on misspelled words
- Select "Add to Dictionary"
- Words are saved in `custom_dictionary.json`

## 🗂️ File Structure

\`\`\`
modern-notepad-app/
├── python/                     # Python version
│   ├── notepad_app.py          # Main application
│   ├── enhanced_features.py    # Additional features
│   ├── requirements.txt        # Python dependencies
│   └── FEATURES.md            # Feature documentation
├── app/                        # Next.js web version
│   ├── page.tsx               # Main page
│   ├── layout.tsx             # App layout
│   └── globals.css            # Global styles
├── components/                 # React components
│   ├── rich-text-editor.tsx   # Rich text editor
│   ├── category-manager.tsx   # Category management
│   ├── spelling-suggestions.tsx # Spell check UI
│   └── ui/                    # UI components
├── lib/                       # Utilities
│   ├── spell-checker.ts       # Spell checking logic
│   └── export-utils.ts        # Export functionality
└── README.md                  # This file
\`\`\`

## 🔄 Data Management

### Backup System

**Automatic Backups:**
- Created every 5 minutes (configurable)
- Stored in `.notepad_app/backups/`
- Keeps last 10 backups automatically

**Manual Backup:**
- Use `Tools > Backup Notes` menu
- Or press `Ctrl+Shift+B`

### Data Storage

**Python Version:**
- Notes: `~/.notepad_app/notes.json`
- Settings: `~/.notepad_app/settings.json`
- Custom Dictionary: `~/.notepad_app/custom_dictionary.json`
- Backups: `~/.notepad_app/backups/`

**Web Version:**
- Browser Local Storage
- Export/Import for data portability

## 🐛 Troubleshooting

### Common Issues

**Python Version:**

1. **Import Error: No module named 'tkinter'**
   \`\`\`bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # CentOS/RHEL
   sudo yum install tkinter
   
   # macOS (if using Homebrew)
   brew install python-tk
   \`\`\`

2. **Font Issues on Linux**
   \`\`\`bash
   # Install additional fonts
   sudo apt-get install fonts-liberation fonts-dejavu
   \`\`\`

3. **Permission Errors**
   \`\`\`bash
   # Ensure user has write permissions to home directory
   chmod 755 ~/.notepad_app
   \`\`\`

**Web Version:**

1. **Build Errors**
   \`\`\`bash
   # Clear cache and reinstall
   rm -rf node_modules package-lock.json
   npm install
   \`\`\`

2. **Port Already in Use**
   \`\`\`bash
   # Use different port
   npm run dev -- --port 3001
   \`\`\`

### Performance Tips

1. **Large Notes**: For notes with 10,000+ words, consider disabling real-time spell checking
2. **Many Notes**: Use categories and search to organize large collections
3. **Slow Startup**: Check if backup directory has too many files

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**
   \`\`\`bash
   git checkout -b feature/amazing-feature
   \`\`\`
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Development Setup

\`\`\`bash
# Clone your fork
git clone https://github.com/yourusername/modern-notepad-app.git
cd modern-notepad-app

# Python development
cd python
pip install -r requirements.txt
python notepad_app.py

# Web development
npm install
npm run dev
\`\`\`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python Tkinter and Next.js
- Spell checking algorithms inspired by various open-source projects
- Icons and design inspired by modern note-taking applications
- Thanks to all contributors and testers

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/modern-notepad-app/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/modern-notepad-app/discussions)
- **Email**: support@notepad-app.com

---

**Happy Note Taking! 📝✨**
\`\`\`

```python file="python/requirements.txt"
# Core GUI framework
tkinter-tooltip>=2.0.0

# PDF generation
reportlab>=3.6.0

# Enhanced text processing
python-dateutil>=2.8.0

# File handling and utilities
pathlib2>=2.3.0; python_version &lt; '3.4'

# JSON handling (built-in, but listed for completeness)
# json - built-in module

# Regular expressions (built-in)
# re - built-in module

# Threading support (built-in)
# threading - built-in module

# Time utilities (built-in)
# time - built-in module

# Operating system interface (built-in)
# os - built-in module

# Data classes (built-in in Python 3.7+)
# dataclasses - built-in module

# Type hints (built-in in Python 3.5+)
# typing - built-in module

# Web browser control (built-in)
# webbrowser - built-in module

# Optional: Enhanced spell checking (if you want to use external libraries)
# pyspellchecker>=0.6.0
# enchant>=3.2.0

# Optional: Advanced PDF features
# PyPDF2>=2.0.0

# Optional: Enhanced file format support
# python-docx>=0.8.11
# openpyxl>=3.0.9

# Optional: Advanced text processing
# nltk>=3.7
# textstat>=0.7.0

# Development dependencies (optional)
# pytest>=6.0.0
# black>=21.0.0
# flake8>=4.0.0
