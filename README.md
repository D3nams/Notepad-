# Modern Notepad - Multi-Platform

A beautiful, feature-rich notepad application built in three different technologies: C++ (Qt), Python (Tkinter), and Flutter.

## Features

### Core Features
- ✨ **Modern, beautiful UI** with clean design
- 📝 **Rich text editing** with formatting options
- 🔍 **Search functionality** across all notes
- 📁 **Category management** with color coding
- 💾 **Multiple export formats** (TXT, MD, HTML, PDF, JSON, etc.)
- ⌨️ **Keyboard shortcuts** for power users
- 🌙 **Dark/Light theme** support
- 💾 **Auto-save** functionality
- 📱 **Responsive design**

### Export Formats
- Plain Text (.txt)
- Markdown (.md)
- HTML (.html)
- PDF (.pdf)
- JSON (.json)
- XML (.xml)
- RTF (.rtf)
- CSV (.csv)
- Assembly (.asm)
- NASM (.nasm)
- C Source (.c)
- Python (.py)
- JavaScript (.js)
- LaTeX (.tex)
- YAML (.yaml)
- SQL (.sql)

## Platforms

### C++ Version (Qt)
**Requirements:**
- Qt 6.0 or higher
- CMake 3.16 or higher
- C++17 compatible compiler

**Build Instructions:**
\`\`\`bash
cd cpp
mkdir build
cd build
cmake ..
make
./ModernNotepad
\`\`\`

**Features:**
- Native desktop performance
- System integration
- Print support
- Professional UI with Qt styling

### Python Version (Tkinter)
**Requirements:**
- Python 3.8 or higher
- tkinter (usually included with Python)

**Run Instructions:**
\`\`\`bash
cd python
python notepad_app.py
\`\`\`

**Features:**
- Cross-platform compatibility
- No external dependencies
- Easy to modify and extend
- Lightweight and fast

### Flutter Version
**Requirements:**
- Flutter SDK 3.10 or higher
- Dart 3.0 or higher

**Build Instructions:**
\`\`\`bash
cd flutter
flutter pub get
flutter run
\`\`\`

**Features:**
- Cross-platform (Windows, macOS, Linux, iOS, Android)
- Modern Material Design 3
- Smooth animations
- Mobile-optimized UI

## Keyboard Shortcuts

### Universal Shortcuts
- `Ctrl+N` - Create new note
- `Ctrl+S` - Save as TXT (default)
- `Ctrl+Shift+S` - Save As... (show all formats)
- `Ctrl+F` - Focus search
- `Ctrl+D` - Delete current note
- `Ctrl+E` - Export current note
- `Ctrl+/` - Show keyboard shortcuts

### Formatting Shortcuts
- `Ctrl+B` - Bold text
- `Ctrl+I` - Italic text
- `Ctrl+U` - Underline text (C++/Python)
- `Ctrl+Z` - Undo
- `Ctrl+Shift+Z` - Redo

## Data Storage

### C++ Version
- Uses JSON files in system's AppData directory
- Cross-platform file locations
- Automatic backup on save

### Python Version
- Stores data in `~/.notepad_app/` directory
- JSON format for easy portability
- Human-readable data files

### Flutter Version
- Uses platform-specific document directories
- Automatic data persistence
- Cross-platform compatibility

## Architecture

Each version follows clean architecture principles:

### C++ (Qt)
- **Model**: Note and Category structs
- **View**: Qt widgets with modern styling
- **Controller**: Main application class with signal/slot connections
- **Storage**: JSON-based file system storage

### Python (Tkinter)
- **Models**: Dataclasses for Note and Category
- **Views**: Tkinter widgets with custom styling
- **Controllers**: Event-driven architecture
- **Storage**: JSON file-based persistence

### Flutter
- **Models**: Dart classes with JSON serialization
- **Views**: Material Design 3 widgets
- **Services**: Storage service for data persistence
- **State Management**: StatefulWidget with setState

## Customization

### Themes
All versions support customizable themes:
- Light and dark modes
- Customizable color schemes
- Modern, clean aesthetics

### Categories
- Create custom categories
- Color-coded organization
- Filter notes by category

### Export Templates
Easy to add new export formats by extending the export utilities in each version.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test across all platforms
5. Submit a pull request

## License

MIT License - feel free to use and modify for your projects.

## Screenshots

### C++ Version
- Native Qt interface
- Professional desktop appearance
- System-integrated menus and toolbars

### Python Version
- Clean Tkinter interface
- Cross-platform consistency
- Lightweight and responsive

### Flutter Version
- Modern Material Design
- Smooth animations
- Mobile-friendly interface

## Performance

### C++ Version
- **Startup**: < 1 second
- **Memory**: ~50MB
- **File I/O**: Native performance

### Python Version
- **Startup**: < 2 seconds
- **Memory**: ~30MB
- **File I/O**: Good performance

### Flutter Version
- **Startup**: < 3 seconds
- **Memory**: ~80MB
- **File I/O**: Excellent performance

## Future Enhancements

- [ ] Cloud synchronization
- [ ] Collaborative editing
- [ ] Plugin system
- [ ] Advanced search with regex
- [ ] Note linking and references
- [ ] Markdown preview
- [ ] Voice notes
- [ ] OCR for images
- [ ] Advanced formatting tools
- [ ] Note templates

Choose the version that best fits your needs and platform requirements!
