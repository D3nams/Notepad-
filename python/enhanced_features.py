"""
Enhanced Features Module for Modern Notepad App
This module provides additional advanced features for the notepad application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import json
import re
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
import webbrowser
import subprocess
import sys

# Advanced spell checking and text analysis
class AdvancedTextAnalyzer:
    """Advanced text analysis and spell checking features"""
    
    def __init__(self):
        self.word_frequency = {}
        self.reading_level_cache = {}
        self.grammar_rules = self.load_grammar_rules()
    
    def load_grammar_rules(self):
        """Load basic grammar checking rules"""
        return {
            'double_spaces': r'  +',
            'sentence_spacing': r'[.!?]\s*[a-z]',
            'capitalization': r'^\s*[a-z]',
            'repeated_words': r'\b(\w+)\s+\1\b',
            'common_mistakes': {
                r'\bteh\b': 'the',
                r'\badn\b': 'and',
                r'\byuo\b': 'you',
                r'\btaht\b': 'that',
                r'\bwith\b': 'with',
                r'\bform\b': 'from',
                r'\bthier\b': 'their',
                r'\brecieve\b': 'receive',
                r'\boccur\b': 'occur',
                r'\bseperate\b': 'separate',
                r'\bdefinately\b': 'definitely',
                r'\bneccessary\b': 'necessary',
                r'\baccommodate\b': 'accommodate',
                r'\bbeginning\b': 'beginning',
                r'\bcommittee\b': 'committee',
                r'\bembarrass\b': 'embarrass',
                r'\bexistence\b': 'existence',
                r'\bgovernment\b': 'government',
                r'\bindependent\b': 'independent',
                r'\bmaintenance\b': 'maintenance',
                r'\boccasionally\b': 'occasionally',
                r'\bpersistence\b': 'persistence',
                r'\bprivilege\b': 'privilege',
                r'\brecommend\b': 'recommend',
                r'\bsimilar\b': 'similar',
                r'\btomorrow\b': 'tomorrow',
                r'\bunfortunately\b': 'unfortunately'
            }
        }
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Comprehensive text analysis"""
        if not text or not text.strip():
            return {
                'word_count': 0,
                'character_count': 0,
                'sentence_count': 0,
                'paragraph_count': 0,
                'reading_time': 0,
                'reading_level': 'N/A',
                'most_common_words': [],
                'grammar_issues': [],
                'spelling_errors': 0
            }
        
        # Basic counts
        words = re.findall(r'\b\w+\b', text.lower())
        sentences = re.split(r'[.!?]+', text)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Word frequency analysis
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        most_common = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Reading time (average 200 words per minute)
        reading_time = len(words) / 200
        
        # Grammar issues
        grammar_issues = self.check_grammar(text)
        
        return {
            'word_count': len(words),
            'character_count': len(text),
            'character_count_no_spaces': len(text.replace(' ', '')),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'paragraph_count': len(paragraphs),
            'reading_time': reading_time,
            'reading_level': self.calculate_reading_level(text),
            'most_common_words': most_common,
            'grammar_issues': grammar_issues,
            'average_words_per_sentence': len(words) / max(len([s for s in sentences if s.strip()]), 1),
            'average_sentence_length': sum(len(s.split()) for s in sentences if s.strip()) / max(len([s for s in sentences if s.strip()]), 1)
        }
    
    def check_grammar(self, text: str) -> List[Dict[str, Any]]:
        """Basic grammar checking"""
        issues = []
        
        # Check for double spaces
        for match in re.finditer(self.grammar_rules['double_spaces'], text):
            issues.append({
                'type': 'spacing',
                'message': 'Multiple consecutive spaces found',
                'position': match.start(),
                'suggestion': 'Use single space'
            })
        
        # Check for sentence capitalization
        sentences = re.split(r'[.!?]+', text)
        pos = 0
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and sentence[0].islower():
                issues.append({
                    'type': 'capitalization',
                    'message': 'Sentence should start with capital letter',
                    'position': pos,
                    'suggestion': f'Capitalize "{sentence[0]}"'
                })
            pos += len(sentence) + 1
        
        # Check for repeated words
        for match in re.finditer(self.grammar_rules['repeated_words'], text, re.IGNORECASE):
            issues.append({
                'type': 'repetition',
                'message': f'Repeated word: "{match.group(1)}"',
                'position': match.start(),
                'suggestion': 'Remove duplicate word'
            })
        
        # Check common mistakes
        for pattern, correction in self.grammar_rules['common_mistakes'].items():
            for match in re.finditer(pattern, text, re.IGNORECASE):
                issues.append({
                    'type': 'common_mistake',
                    'message': f'Possible misspelling: "{match.group()}"',
                    'position': match.start(),
                    'suggestion': f'Did you mean "{correction}"?'
                })
        
        return issues
    
    def calculate_reading_level(self, text: str) -> str:
        """Calculate approximate reading level using Flesch Reading Ease"""
        if not text.strip():
            return 'N/A'
        
        # Count sentences, words, and syllables
        sentences = len(re.split(r'[.!?]+', text))
        words = len(re.findall(r'\b\w+\b', text))
        
        if sentences == 0 or words == 0:
            return 'N/A'
        
        # Approximate syllable count
        syllables = 0
        for word in re.findall(r'\b\w+\b', text.lower()):
            syllable_count = max(1, len(re.findall(r'[aeiouy]+', word)))
            if word.endswith('e'):
                syllable_count -= 1
            syllables += max(1, syllable_count)
        
        # Flesch Reading Ease formula
        if sentences > 0 and words > 0:
            score = 206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables / words))
            
            if score >= 90:
                return 'Very Easy (5th grade)'
            elif score >= 80:
                return 'Easy (6th grade)'
            elif score >= 70:
                return 'Fairly Easy (7th grade)'
            elif score >= 60:
                return 'Standard (8th-9th grade)'
            elif score >= 50:
                return 'Fairly Difficult (10th-12th grade)'
            elif score >= 30:
                return 'Difficult (College level)'
            else:
                return 'Very Difficult (Graduate level)'
        
        return 'N/A'

class PluginManager:
    """Plugin system for extending functionality"""
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.plugins = {}
        self.plugin_dir = Path.home() / ".notepad_app" / "plugins"
        self.plugin_dir.mkdir(exist_ok=True)
        self.load_plugins()
    
    def load_plugins(self):
        """Load available plugins"""
        # This would scan for plugin files and load them
        # For now, we'll define some built-in plugins
        self.plugins = {
            'word_cloud': {
                'name': 'Word Cloud Generator',
                'description': 'Generate word clouds from note content',
                'enabled': True,
                'function': self.generate_word_cloud
            },
            'export_advanced': {
                'name': 'Advanced Export',
                'description': 'Export notes in additional formats',
                'enabled': True,
                'function': self.advanced_export
            },
            'note_templates': {
                'name': 'Template Manager',
                'description': 'Manage custom note templates',
                'enabled': True,
                'function': self.manage_templates
            },
            'collaboration': {
                'name': 'Collaboration Tools',
                'description': 'Share and collaborate on notes',
                'enabled': False,
                'function': self.collaboration_tools
            }
        }
    
    def generate_word_cloud(self):
        """Generate word cloud from current note"""
        if self.app.current_note_index is None:
            messagebox.showwarning("No Note", "Please select a note to generate word cloud.")
            return
        
        note = self.app.notes[self.app.current_note_index]
        
        # Simple word frequency analysis
        words = re.findall(r'\b\w+\b', note.content.lower())
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Skip short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        if not word_freq:
            messagebox.showinfo("Word Cloud", "Not enough words to generate word cloud.")
            return
        
        # Show top words in a dialog
        dialog = tk.Toplevel(self.app.root)
        dialog.title(f"Word Cloud - {note.title}")
        dialog.geometry("400x500")
        dialog.transient(self.app.root)
        
        ttk.Label(dialog, text="Most Frequent Words", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Create text widget to display words
        text_widget = tk.Text(dialog, wrap=tk.WORD, font=('Arial', 12))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sort words by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        for word, count in sorted_words[:50]:  # Top 50 words
            size = min(24, 8 + (count * 2))  # Scale font size by frequency
            text_widget.insert(tk.END, f"{word} ", f"size_{size}")
            text_widget.tag_configure(f"size_{size}", font=('Arial', size))
        
        text_widget.configure(state='disabled')
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
    
    def advanced_export(self):
        """Advanced export options"""
        if self.app.current_note_index is None:
            messagebox.showwarning("No Note", "Please select a note to export.")
            return
        
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Advanced Export")
        dialog.geometry("500x400")
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Advanced Export Options", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Export formats
        formats_frame = ttk.LabelFrame(dialog, text="Export Formats")
        formats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        export_vars = {}
        formats = [
            ('PDF with formatting', 'pdf_formatted'),
            ('Word document (.docx)', 'docx'),
            ('LaTeX document', 'latex'),
            ('EPUB e-book', 'epub'),
            ('XML structured', 'xml'),
            ('JSON with metadata', 'json_meta')
        ]
        
        for format_name, format_key in formats:
            var = tk.BooleanVar()
            ttk.Checkbutton(formats_frame, text=format_name, variable=var).pack(anchor=tk.W, padx=10, pady=2)
            export_vars[format_key] = var
        
        # Export options
        options_frame = ttk.LabelFrame(dialog, text="Export Options")
        options_frame.pack(fill=tk.X, padx=20, pady=10)
        
        include_metadata = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Include metadata", variable=include_metadata).pack(anchor=tk.W, padx=10, pady=2)
        
        include_categories = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Include categories", variable=include_categories).pack(anchor=tk.W, padx=10, pady=2)
        
        include_stats = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Include statistics", variable=include_stats).pack(anchor=tk.W, padx=10, pady=2)
        
        def perform_export():
            selected_formats = [key for key, var in export_vars.items() if var.get()]
            if not selected_formats:
                messagebox.showwarning("No Format", "Please select at least one export format.")
                return
            
            note = self.app.notes[self.app.current_note_index]
            
            for format_key in selected_formats:
                try:
                    if format_key == 'pdf_formatted':
                        self.export_pdf_formatted(note, include_metadata.get(), include_categories.get(), include_stats.get())
                    elif format_key == 'docx':
                        self.export_docx(note, include_metadata.get(), include_categories.get())
                    elif format_key == 'latex':
                        self.export_latex(note, include_metadata.get(), include_categories.get())
                    elif format_key == 'epub':
                        self.export_epub(note, include_metadata.get())
                    elif format_key == 'xml':
                        self.export_xml_structured(note, include_metadata.get(), include_categories.get())
                    elif format_key == 'json_meta':
                        self.export_json_metadata(note, include_stats.get())
                except Exception as e:
                    messagebox.showerror("Export Error", f"Failed to export as {format_key}:\n{str(e)}")
            
            dialog.destroy()
            messagebox.showinfo("Export Complete", f"Successfully exported in {len(selected_formats)} format(s).")
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Button(button_frame, text="Export", command=perform_export).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)
    
    def export_pdf_formatted(self, note, include_metadata, include_categories, include_stats):
        """Export as formatted PDF"""
        filename = filedialog.asksaveasfilename(
            title="Save PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if filename:
            # This would use a PDF library like reportlab
            messagebox.showinfo("PDF Export", f"PDF export functionality would create: {filename}")
    
    def export_docx(self, note, include_metadata, include_categories):
        """Export as Word document"""
        filename = filedialog.asksaveasfilename(
            title="Save Word Document",
            defaultextension=".docx",
            filetypes=[("Word documents", "*.docx")]
        )
        if filename:
            # This would use python-docx library
            messagebox.showinfo("DOCX Export", f"Word document export would create: {filename}")
    
    def export_latex(self, note, include_metadata, include_categories):
        """Export as LaTeX document"""
        filename = filedialog.asksaveasfilename(
            title="Save LaTeX Document",
            defaultextension=".tex",
            filetypes=[("LaTeX files", "*.tex")]
        )
        if filename:
            latex_content = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{geometry}}
\\geometry{{margin=1in}}

\\title{{{note.title}}}
\\author{{Modern Notepad}}
\\date{{{datetime.fromisoformat(note.created_at).strftime('%B %d, %Y')}}}

\\begin{{document}}
\\maketitle

{note.content}

"""
            if include_metadata:
                latex_content += f"""
\\section*{{Metadata}}
Created: {note.created_at}\\\\
Updated: {note.updated_at}\\\\
Word Count: {note.word_count}\\\\
Character Count: {note.char_count}\\\\
"""
            
            if include_categories and note.categories:
                latex_content += f"Categories: {', '.join(note.categories)}\\\\\n"
            
            latex_content += "\\end{document}"
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                messagebox.showinfo("LaTeX Export", f"LaTeX document saved: {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to save LaTeX file:\n{str(e)}")
    
    def export_epub(self, note, include_metadata):
        """Export as EPUB e-book"""
        filename = filedialog.asksaveasfilename(
            title="Save EPUB",
            defaultextension=".epub",
            filetypes=[("EPUB files", "*.epub")]
        )
        if filename:
            # This would use ebooklib or similar
            messagebox.showinfo("EPUB Export", f"EPUB export functionality would create: {filename}")
    
    def export_xml_structured(self, note, include_metadata, include_categories):
        """Export as structured XML"""
        filename = filedialog.asksaveasfilename(
            title="Save XML",
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml")]
        )
        if filename:
            xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<note>
    <id>{note.id}</id>
    <title><![CDATA[{note.title}]]></title>
    <content><![CDATA[{note.content}]]></content>
"""
            if include_categories:
                xml_content += "    <categories>\n"
                for category in note.categories:
                    xml_content += f"        <category>{category}</category>\n"
                xml_content += "    </categories>\n"
            
            if include_metadata:
                xml_content += f"""    <metadata>
        <created>{note.created_at}</created>
        <updated>{note.updated_at}</updated>
        <word_count>{note.word_count}</word_count>
        <char_count>{note.char_count}</char_count>
        <is_favorite>{str(note.is_favorite).lower()}</is_favorite>
    </metadata>
"""
            
            xml_content += "</note>"
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(xml_content)
                messagebox.showinfo("XML Export", f"XML document saved: {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to save XML file:\n{str(e)}")
    
    def export_json_metadata(self, note, include_stats):
        """Export as JSON with full metadata"""
        filename = filedialog.asksaveasfilename(
            title="Save JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if filename:
            data = {
                'note': {
                    'id': note.id,
                    'title': note.title,
                    'content': note.content,
                    'categories': note.categories,
                    'created_at': note.created_at,
                    'updated_at': note.updated_at,
                    'is_favorite': note.is_favorite,
                    'word_count': note.word_count,
                    'char_count': note.char_count
                },
                'export_info': {
                    'exported_at': datetime.now().isoformat(),
                    'exported_by': 'Modern Notepad Python Edition',
                    'version': '2.0.0'
                }
            }
            
            if include_stats:
                analyzer = AdvancedTextAnalyzer()
                stats = analyzer.analyze_text(note.content)
                data['statistics'] = stats
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("JSON Export", f"JSON document saved: {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to save JSON file:\n{str(e)}")
    
    def manage_templates(self):
        """Template management interface"""
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Template Manager")
        dialog.geometry("600x500")
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        # Template list
        list_frame = ttk.LabelFrame(dialog, text="Available Templates")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        template_listbox = tk.Listbox(list_frame)
        template_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load templates
        for template_name in self.app.note_templates.keys():
            template_listbox.insert(tk.END, template_name)
        
        # Template preview
        preview_frame = ttk.LabelFrame(dialog, text="Template Preview")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        preview_text = tk.Text(preview_frame, height=8, wrap=tk.WORD)
        preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def on_template_select(event):
            selection = template_listbox.curselection()
            if selection:
                template_name = template_listbox.get(selection[0])
                template_content = self.app.note_templates.get(template_name, "")
                preview_text.delete('1.0', tk.END)
                preview_text.insert('1.0', template_content)
        
        template_listbox.bind('<<ListboxSelect>>', on_template_select)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        def create_template():
            name = tk.simpledialog.askstring("Template Name", "Enter template name:")
            if name:
                content = preview_text.get('1.0', tk.END + '-1c')
                self.app.note_templates[name] = content
                template_listbox.insert(tk.END, name)
                messagebox.showinfo("Template Created", f"Template '{name}' created successfully.")
        
        def edit_template():
            selection = template_listbox.curselection()
            if selection:
                template_name = template_listbox.get(selection[0])
                content = preview_text.get('1.0', tk.END + '-1c')
                self.app.note_templates[template_name] = content
                messagebox.showinfo("Template Updated", f"Template '{template_name}' updated successfully.")
        
        def delete_template():
            selection = template_listbox.curselection()
            if selection:
                template_name = template_listbox.get(selection[0])
                if template_name != "Blank":  # Don't allow deleting the blank template
                    result = messagebox.askyesno("Delete Template", f"Delete template '{template_name}'?")
                    if result:
                        del self.app.note_templates[template_name]
                        template_listbox.delete(selection[0])
                        preview_text.delete('1.0', tk.END)
                        messagebox.showinfo("Template Deleted", f"Template '{template_name}' deleted.")
        
        ttk.Button(button_frame, text="New", command=create_template).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Edit", command=edit_template).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Delete", command=delete_template).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Close", command=dialog.destroy).pack(side=tk.RIGHT)
    
    def collaboration_tools(self):
        """Collaboration tools (placeholder)"""
        messagebox.showinfo("Collaboration Tools", 
                          "Collaboration features would include:\n\n"
                          "• Share notes via email or cloud\n"
                          "• Real-time collaborative editing\n"
                          "• Comment and review system\n"
                          "• Version history and conflict resolution\n"
                          "• Team workspaces\n\n"
                          "This feature is not yet implemented.")
    
    def get_plugin_menu_items(self):
        """Get menu items for plugins"""
        items = []
        for plugin_id, plugin_info in self.plugins.items():
            if plugin_info['enabled']:
                items.append({
                    'label': plugin_info['name'],
                    'command': plugin_info['function']
                })
        return items

class VoiceNoteRecorder:
    """Voice note recording functionality"""
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.is_recording = False
        self.audio_data = []
