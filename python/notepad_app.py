import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog, colorchooser
import json
import os
import re
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
import webbrowser
from pathlib import Path
import threading
import time

@dataclass
class Note:
    id: str
    title: str
    content: str
    categories: List[str]
    created_at: str
    updated_at: str
    is_favorite: bool = False
    word_count: int = 0
    char_count: int = 0

@dataclass
class Category:
    id: str
    name: str
    color: str

@dataclass
class AppSettings:
    theme: str = "light"
    font_family: str = "Arial"
    font_size: int = 12
    auto_save_interval: int = 30  # seconds
    word_wrap: bool = True
    show_line_numbers: bool = False
    backup_enabled: bool = True
    backup_interval: int = 300  # 5 minutes
    spell_check_enabled: bool = True
    auto_correct: bool = False

class SpellChecker:
    """Enhanced spell checker with suggestions and corrections"""
    
    def __init__(self):
        # Load dictionary
        self.dictionary = self.load_dictionary()
        self.custom_words = self.load_custom_dictionary()
        self.suggestions_cache = {}
        
    def load_dictionary(self):
        """Load the main dictionary"""
        # Common English words - in a real implementation, this would be loaded from a file
        common_words = {
            "the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by",
            "from", "up", "about", "into", "through", "during", "before", "after", "above",
            "below", "between", "among", "under", "over", "inside", "outside", "within",
            "without", "against", "toward", "upon", "across", "behind", "beneath", "beside",
            "beyond", "except", "since", "until", "while", "where", "when", "why", "how",
            "what", "which", "who", "whom", "whose", "this", "that", "these", "those",
            "here", "there", "now", "then", "today", "tomorrow", "yesterday", "always",
            "never", "sometimes", "often", "usually", "rarely", "seldom", "frequently",
            "occasionally", "constantly", "immediately", "suddenly", "quickly", "slowly",
            "carefully", "easily", "hardly", "nearly", "almost", "quite", "very", "too",
            "enough", "more", "most", "less", "least", "much", "many", "few", "little",
            "some", "any", "all", "both", "each", "every", "either", "neither", "other",
            "another", "same", "different", "similar", "such", "like", "unlike", "as",
            "than", "so", "because", "since", "although", "though", "however", "therefore",
            "thus", "hence", "moreover", "furthermore", "nevertheless", "nonetheless",
            "meanwhile", "otherwise", "instead", "besides", "also", "too", "either",
            "neither", "both", "not", "only", "just", "even", "still", "yet", "already",
            "again", "once", "twice", "first", "second", "third", "last", "next", "previous",
            "following", "final", "initial", "original", "new", "old", "young", "ancient",
            "modern", "recent", "current", "past", "future", "present", "early", "late",
            "good", "bad", "great", "small", "large", "big", "little", "huge", "tiny",
            "enormous", "massive", "gigantic", "microscopic", "beautiful", "ugly", "pretty",
            "handsome", "attractive", "gorgeous", "stunning", "hideous", "lovely", "cute",
            "adorable", "charming", "elegant", "graceful", "stylish", "fashionable",
            "trendy", "modern", "classic", "traditional", "conventional", "unusual",
            "strange", "weird", "odd", "peculiar", "bizarre", "normal", "ordinary",
            "common", "rare", "unique", "special", "particular", "specific", "general",
            "universal", "global", "local", "national", "international", "personal",
            "private", "public", "official", "formal", "informal", "casual", "serious",
            "funny", "amusing", "entertaining", "boring", "interesting", "exciting",
            "thrilling", "amazing", "incredible", "fantastic", "wonderful", "excellent",
            "perfect", "terrible", "awful", "horrible", "disgusting", "pleasant",
            "enjoyable", "delightful", "satisfying", "disappointing", "frustrating",
            "annoying", "irritating", "disturbing", "shocking", "surprising", "expected",
            "unexpected", "predictable", "unpredictable", "certain", "uncertain", "sure",
            "unsure", "confident", "doubtful", "hopeful", "hopeless", "optimistic",
            "pessimistic", "positive", "negative", "happy", "sad", "joyful", "miserable",
            "cheerful", "gloomy", "excited", "calm", "peaceful", "angry", "furious",
            "mad", "upset", "worried", "anxious", "nervous", "relaxed", "comfortable",
            "uncomfortable", "tired", "exhausted", "energetic", "lazy", "busy", "free",
            "available", "occupied", "empty", "full", "complete", "incomplete", "finished",
            "unfinished", "ready", "prepared", "unprepared", "organized", "disorganized",
            "clean", "dirty", "neat", "messy", "tidy", "untidy", "clear", "unclear",
            "obvious", "hidden", "visible", "invisible", "bright", "dark", "light",
            "heavy", "easy", "difficult", "hard", "soft", "rough", "smooth", "sharp",
            "dull", "hot", "cold", "warm", "cool", "wet", "dry", "solid", "liquid",
            "gas", "frozen", "melted", "cooked", "raw", "fresh", "stale", "ripe",
            "unripe", "sweet", "sour", "bitter", "salty", "spicy", "mild", "strong",
            "weak", "powerful", "gentle", "violent", "peaceful", "dangerous", "safe",
            "secure", "risky", "careful", "careless", "cautious", "reckless", "brave",
            "cowardly", "bold", "shy", "outgoing", "friendly", "unfriendly", "kind",
            "cruel", "generous", "selfish", "honest", "dishonest", "truthful", "lying",
            "loyal", "disloyal", "faithful", "unfaithful", "reliable", "unreliable",
            "responsible", "irresponsible", "mature", "immature", "wise", "foolish",
            "smart", "stupid", "intelligent", "ignorant", "educated", "uneducated",
            "experienced", "inexperienced", "skilled", "unskilled", "talented", "untalented",
            "creative", "uncreative", "artistic", "scientific", "technical", "practical",
            "theoretical", "logical", "illogical", "reasonable", "unreasonable", "sensible",
            "nonsensical", "rational", "irrational", "realistic", "unrealistic", "possible",
            "impossible", "probable", "improbable", "likely", "unlikely", "necessary",
            "unnecessary", "important", "unimportant", "significant", "insignificant",
            "relevant", "irrelevant", "useful", "useless", "helpful", "unhelpful",
            "beneficial", "harmful", "advantageous", "disadvantageous", "profitable",
            "unprofitable", "successful", "unsuccessful", "effective", "ineffective",
            "efficient", "inefficient", "productive", "unproductive", "active", "inactive",
            "busy", "idle", "working", "resting", "moving", "stationary", "fast", "slow",
            "quick", "gradual", "sudden", "immediate", "instant", "delayed", "prompt",
            "late", "early", "timely", "untimely", "temporary", "permanent", "brief",
            "lengthy", "short", "long", "narrow", "wide", "thin", "thick", "slim",
            "fat", "skinny", "chubby", "tall", "short", "high", "low", "deep", "shallow",
            "close", "far", "near", "distant", "inside", "outside", "upstairs", "downstairs",
            "indoor", "outdoor", "public", "private", "open", "closed", "locked", "unlocked",
            "available", "unavailable", "present", "absent", "here", "there", "everywhere",
            "nowhere", "somewhere", "anywhere", "home", "away", "back", "forward", "ahead",
            "behind", "left", "right", "straight", "curved", "round", "square", "circular",
            "rectangular", "triangular", "oval", "flat", "steep", "level", "uneven",
            "smooth", "bumpy", "straight", "crooked", "bent", "twisted", "broken", "fixed",
            "damaged", "repaired", "new", "used", "fresh", "old", "ancient", "modern",
            "recent", "current", "latest", "previous", "former", "original", "copy",
            "duplicate", "similar", "different", "same", "other",
            "another", "extra", "additional", "more", "less", "enough", "insufficient",
            "adequate", "inadequate", "plenty", "scarce", "abundant", "limited", "unlimited",
            "finite", "infinite", "maximum", "minimum", "average", "normal", "standard",
            "regular", "irregular", "usual", "unusual", "typical", "atypical", "common",
            "uncommon", "ordinary", "extraordinary", "special", "general", "specific",
            "particular", "individual", "collective", "single", "multiple", "several",
            "various", "diverse", "uniform", "mixed", "pure", "impure", "clean", "dirty",
            "clear", "cloudy", "transparent", "opaque", "visible", "invisible", "obvious",
            "hidden", "secret", "public", "known", "unknown", "familiar", "unfamiliar",
            "strange", "normal", "weird", "ordinary", "regular", "irregular", "consistent",
            "inconsistent", "constant", "variable", "stable", "unstable", "steady", "unsteady",
            "firm", "loose", "tight", "slack", "tense", "relaxed", "rigid", "flexible",
            "hard", "soft", "solid", "hollow", "dense", "sparse", "thick", "thin",
            "heavy", "light", "strong", "weak", "powerful", "powerless", "mighty", "feeble"
        }
        return common_words
    
    def load_custom_dictionary(self):
        """Load user's custom dictionary"""
        try:
            custom_dict_file = Path.home() / ".notepad_app" / "custom_dictionary.json"
            if custom_dict_file.exists():
                with open(custom_dict_file, 'r', encoding='utf-8') as f:
                    return set(json.load(f))
        except Exception:
            pass
        return set()
    
    def save_custom_dictionary(self):
        """Save user's custom dictionary"""
        try:
            data_dir = Path.home() / ".notepad_app"
            data_dir.mkdir(exist_ok=True)
            custom_dict_file = data_dir / "custom_dictionary.json"
            with open(custom_dict_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.custom_words), f, indent=2)
        except Exception as e:
            print(f"Error saving custom dictionary: {e}")
    
    def is_word_correct(self, word):
        """Check if a word is spelled correctly"""
        if not word or not word.isalpha():
            return True
        
        word_lower = word.lower()
        return (word_lower in self.dictionary or 
                word_lower in self.custom_words or
                word.isupper() or  # Acronyms
                word.isdigit())    # Numbers
    
    def get_suggestions(self, word, max_suggestions=5):
        """Get spelling suggestions for a misspelled word"""
        if word in self.suggestions_cache:
            return self.suggestions_cache[word]
        
        word_lower = word.lower()
        suggestions = []
        
        # Combine dictionary and custom words
        all_words = self.dictionary.union(self.custom_words)
        
        # Find suggestions using different methods
        suggestions.extend(self._get_edit_distance_suggestions(word_lower, all_words))
        suggestions.extend(self._get_phonetic_suggestions(word_lower, all_words))
        suggestions.extend(self._get_keyboard_suggestions(word_lower, all_words))
        
        # Remove duplicates and sort by relevance
        unique_suggestions = list(dict.fromkeys(suggestions))
        
        # Score suggestions based on similarity
        scored_suggestions = []
        for suggestion in unique_suggestions:
            score = self._calculate_similarity_score(word_lower, suggestion)
            scored_suggestions.append((suggestion, score))
        
        # Sort by score and return top suggestions
        scored_suggestions.sort(key=lambda x: x[1], reverse=True)
        final_suggestions = [s[0] for s in scored_suggestions[:max_suggestions]]
        
        # Cache the result
        self.suggestions_cache[word] = final_suggestions
        return final_suggestions
    
    def _get_edit_distance_suggestions(self, word, dictionary):
        """Get suggestions based on edit distance"""
        suggestions = []
        for dict_word in dictionary:
            if abs(len(word) - len(dict_word)) <= 2:  # Reasonable length difference
                distance = self._levenshtein_distance(word, dict_word)
                if distance <= 2:  # Allow up to 2 character differences
                    suggestions.append(dict_word)
        return suggestions
    
    def _get_phonetic_suggestions(self, word, dictionary):
        """Get suggestions based on phonetic similarity"""
        suggestions = []
        word_soundex = self._soundex(word)
        for dict_word in dictionary:
            if self._soundex(dict_word) == word_soundex:
                suggestions.append(dict_word)
        return suggestions
    
    def _get_keyboard_suggestions(self, word, dictionary):
        """Get suggestions based on keyboard layout (common typos)"""
        keyboard_map = {
            'q': 'wa', 'w': 'qes', 'e': 'wrd', 'r': 'etf', 't': 'ryg',
            'y': 'tuh', 'u': 'yij', 'i': 'uok', 'o': 'ipl', 'p': 'ol',
            'a': 'qsz', 's': 'awdx', 'd': 'sefc', 'f': 'drgv', 'g': 'fthb',
            'h': 'gynj', 'j': 'hukm', 'k': 'jilm', 'l': 'kop',
            'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn',
            'n': 'bhjm', 'm': 'njk'
        }
        
        suggestions = []
        for i, char in enumerate(word):
            if char in keyboard_map:
                for replacement in keyboard_map[char]:
                    candidate = word[:i] + replacement + word[i+1:]
                    if candidate in dictionary:
                        suggestions.append(candidate)
        return suggestions
    
    def _levenshtein_distance(self, s1, s2):
        """Calculate Levenshtein distance between two strings"""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _soundex(self, word):
        """Generate Soundex code for phonetic matching"""
        if not word:
            return "0000"
        
        word = word.upper()
        soundex = word[0]
        
        # Soundex mapping
        mapping = {
            'BFPV': '1', 'CGJKQSXZ': '2', 'DT': '3',
            'L': '4', 'MN': '5', 'R': '6'
        }
        
        for char in word[1:]:
            for key, value in mapping.items():
                if char in key:
                    if soundex[-1] != value:  # Avoid consecutive duplicates
                        soundex += value
                    break
        
        # Pad with zeros and truncate to 4 characters
        soundex = (soundex + "0000")[:4]
        return soundex
    
    def _calculate_similarity_score(self, word1, word2):
        """Calculate similarity score between two words"""
        # Combine multiple factors for scoring
        length_diff = abs(len(word1) - len(word2))
        edit_distance = self._levenshtein_distance(word1, word2)
        
        # Prefer words with similar length and fewer edits
        score = 100 - (length_diff * 5) - (edit_distance * 10)
        
        # Bonus for common prefixes/suffixes
        if word1.startswith(word2[:2]) or word2.startswith(word1[:2]):
            score += 10
        
        return max(0, score)
    
    def add_to_dictionary(self, word):
        """Add a word to the custom dictionary"""
        if word and word.isalpha():
            self.custom_words.add(word.lower())
            self.save_custom_dictionary()
            # Clear cache to include new word
            self.suggestions_cache.clear()

class ModernNotepadApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Modern Notepad - Python Edition")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Data
        self.notes: List[Note] = []
        self.categories: List[Category] = []
        self.current_note_index: Optional[int] = None
        self.data_dir = Path.home() / ".notepad_app"
        self.data_dir.mkdir(exist_ok=True)
        self.settings = AppSettings()
        
        # Spell checker
        self.spell_checker = SpellChecker()
        self.misspelled_words = {}  # Store positions of misspelled words
        self.suggestions_window = None
        
        # Variables
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_changed)
        
        self.title_var = tk.StringVar()
        self.title_var.trace('w', self.on_title_changed)
        
        self.current_theme = "light"
        self.is_focus_mode = False
        self.auto_save_timer = None
        self.backup_timer = None
        self.spell_check_timer = None
        
        # Templates
        self.note_templates = {
            "Blank": "",
            "Meeting Notes": """# Meeting Notes - {date}

## Attendees
- 

## Agenda
1. 

## Discussion Points
- 

## Action Items
- [ ] 

## Next Steps
- 
""",
            "Daily Journal": """# Daily Journal - {date}

## Today's Highlights
- 

## Thoughts & Reflections
- 

## Goals for Tomorrow
- 

## Gratitude
- 
""",
            "Project Plan": """# Project: {title}

## Overview
Brief description of the project.

## Objectives
- 

## Timeline
- **Phase 1**: 
- **Phase 2**: 
- **Phase 3**: 

## Resources Needed
- 

## Success Metrics
- 
""",
            "Book Notes": """# Book Notes: {title}

## Author
- 

## Key Concepts
- 

## Important Quotes
> 

## Personal Thoughts
- 

## Rating
⭐⭐⭐⭐⭐ (5/5)
""",
            "Recipe": """# Recipe: {title}

## Ingredients
- 

## Instructions
1. 

## Prep Time
- 

## Cook Time
- 

## Serves
- 

## Notes
- 
"""
        }
        
        # Setup UI
        self.setup_styles()
        self.setup_ui()
        self.setup_menus()
        self.setup_bindings()
        
        # Load data
        self.load_settings()
        self.load_data()
        self.update_notes_list()
        self.update_category_combo()
        
        if self.notes:
            self.select_note(0)
        
        # Start auto-save and backup timers
        self.start_auto_save()
        self.start_backup_timer()
        
        # Configure spell check tags
        self.setup_spell_check_tags()
    
    def setup_spell_check_tags(self):
        """Setup text tags for spell checking"""
        if hasattr(self, 'content_text'):
            # Configure misspelled word tag
            self.content_text.tag_configure("misspelled", 
                                          underline=True, 
                                          underlinefg="red",
                                          selectbackground="#ffcccc")
            
            # Bind click event for suggestions
            self.content_text.tag_bind("misspelled", "<Button-1>", self.on_misspelled_word_click)
            self.content_text.tag_bind("misspelled", "<Button-3>", self.on_misspelled_word_right_click)
    
    def setup_styles(self):
        """Configure modern styling"""
        self.style = ttk.Style()
        self.apply_theme()
    
    def apply_theme(self):
        """Apply the current theme"""
        if self.current_theme == "dark":
            self.style.theme_use('clam')
            
            # Dark theme colors
            bg_color = "#2d3748"
            fg_color = "#e2e8f0"
            select_color = "#4a5568"
            accent_color = "#3182ce"
            
            self.root.configure(bg=bg_color)
            
            self.style.configure('Title.TLabel', 
                               font=('Arial', 18, 'bold'),
                               background=bg_color,
                               foreground=fg_color)
            
            self.style.configure('Sidebar.TFrame', background=bg_color)
            self.style.configure('Main.TFrame', background=bg_color)
            
            # Configure text widgets
            if hasattr(self, 'content_text'):
                self.content_text.configure(
                    bg=select_color,
                    fg=fg_color,
                    insertbackground=fg_color,
                    selectbackground=accent_color
                )
            
            if hasattr(self, 'notes_listbox'):
                self.notes_listbox.configure(
                    bg=select_color,
                    fg=fg_color,
                    selectbackground=accent_color
                )
        else:
            self.style.theme_use('clam')
            
            # Light theme colors
            bg_color = "#f8fafc"
            fg_color = "#1a202c"
            select_color = "#ffffff"
            accent_color = "#3182ce"
            
            self.root.configure(bg=bg_color)
            
            self.style.configure('Title.TLabel', 
                               font=('Arial', 18, 'bold'),
                               background=bg_color,
                               foreground=fg_color)
            
            self.style.configure('Sidebar.TFrame', background=bg_color)
            self.style.configure('Main.TFrame', background=select_color)
            
            # Configure text widgets
            if hasattr(self, 'content_text'):
                self.content_text.configure(
                    bg=select_color,
                    fg=fg_color,
                    insertbackground=fg_color,
                    selectbackground=accent_color
                )
            
            if hasattr(self, 'notes_listbox'):
                self.notes_listbox.configure(
                    bg=select_color,
                    fg=fg_color,
                    selectbackground=accent_color
                )
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create paned window for resizable layout
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Left sidebar
        self.setup_sidebar(paned)
        
        # Right editor
        self.setup_editor(paned)
        
        # Status bar
        self.setup_status_bar()
    
    def setup_sidebar(self, parent):
        """Setup the left sidebar"""
        sidebar = ttk.Frame(parent, style='Sidebar.TFrame')
        sidebar.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(sidebar)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, text="📝 Notes", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Theme toggle button
        theme_btn = ttk.Button(header_frame, text="🌙", command=self.toggle_theme, width=3)
        theme_btn.pack(side=tk.RIGHT)
        
        # Search
        search_frame = ttk.Frame(sidebar)
        search_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Label(search_frame, text="🔍").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.search_entry.insert(0, "Search notes...")
        self.search_entry.bind('<FocusIn>', self.on_search_focus_in)
        self.search_entry.bind('<FocusOut>', self.on_search_focus_out)
        
        # Advanced search button
        search_btn = ttk.Button(search_frame, text="⚙", command=self.show_advanced_search, width=3)
        search_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # New note button with template dropdown
        btn_frame = ttk.Frame(sidebar)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        new_btn = ttk.Button(btn_frame, text="+ New Note", command=self.show_template_dialog)
        new_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        fav_btn = ttk.Button(btn_frame, text="⭐", command=self.toggle_favorite, width=3)
        fav_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Notes list with context menu
        list_frame = ttk.Frame(sidebar)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Scrollable listbox
        list_scroll = ttk.Scrollbar(list_frame)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.notes_listbox = tk.Listbox(
            list_frame, 
            yscrollcommand=list_scroll.set,
            font=(self.settings.font_family, 10),
            selectmode=tk.SINGLE,
            activestyle='none'
        )
        self.notes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scroll.config(command=self.notes_listbox.yview)
        
        self.notes_listbox.bind('<<ListboxSelect>>', self.on_note_selected)
        self.notes_listbox.bind('<Button-3>', self.show_note_context_menu)
        
        # Category management
        category_frame = ttk.Frame(sidebar)
        category_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Label(category_frame, text="Categories:").pack(anchor=tk.W)
        
        cat_control_frame = ttk.Frame(category_frame)
        cat_control_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.category_combo = ttk.Combobox(cat_control_frame, state="readonly")
        self.category_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.category_combo.bind('<<ComboboxSelected>>', self.on_category_filter_changed)
        
        add_cat_btn = ttk.Button(cat_control_frame, text="Add", command=self.add_category)
        add_cat_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        manage_cat_btn = ttk.Button(cat_control_frame, text="⚙", command=self.manage_categories, width=3)
        manage_cat_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        parent.add(sidebar, weight=1)
    
    def setup_editor(self, parent):
        """Setup the right editor panel"""
        editor_frame = ttk.Frame(parent, style='Main.TFrame')
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title editor
        title_frame = ttk.Frame(editor_frame)
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.title_entry = ttk.Entry(
            title_frame, 
            textvariable=self.title_var,
            font=(self.settings.font_family, 18, 'bold')
        )
        self.title_entry.pack(fill=tk.X)
        self.title_entry.insert(0, "Note title...")
        self.title_entry.bind('<FocusIn>', self.on_title_focus_in)
        self.title_entry.bind('<FocusOut>', self.on_title_focus_out)
        
        # Toolbar
        toolbar_frame = ttk.Frame(editor_frame)
        toolbar_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Formatting buttons
        ttk.Button(toolbar_frame, text="B", command=self.format_bold, width=3).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(toolbar_frame, text="I", command=self.format_italic, width=3).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(toolbar_frame, text="U", command=self.format_underline, width=3).pack(side=tk.LEFT, padx=(0, 5))
        
        # Spell check toggle
        self.spell_check_var = tk.BooleanVar(value=self.settings.spell_check_enabled)
        spell_check_btn = ttk.Checkbutton(toolbar_frame, text="ABC", variable=self.spell_check_var, 
                                        command=self.toggle_spell_check)
        spell_check_btn.pack(side=tk.LEFT, padx=(5, 5))
        
        # Font size
        ttk.Label(toolbar_frame, text="Size:").pack(side=tk.LEFT, padx=(5, 2))
        self.font_size_var = tk.StringVar(value=str(self.settings.font_size))
        font_size_combo = ttk.Combobox(toolbar_frame, textvariable=self.font_size_var, 
                                     values=[8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32], 
                                     width=5, state="readonly")
        font_size_combo.pack(side=tk.LEFT, padx=(0, 5))
        font_size_combo.bind('<<ComboboxSelected>>', self.on_font_size_changed)
        
        # Word wrap toggle
        self.word_wrap_var = tk.BooleanVar(value=self.settings.word_wrap)
        wrap_check = ttk.Checkbutton(toolbar_frame, text="Wrap", variable=self.word_wrap_var, 
                                   command=self.toggle_word_wrap)
        wrap_check.pack(side=tk.LEFT, padx=(5, 0))
        
        # Right side buttons
        ttk.Button(toolbar_frame, text="Focus", command=self.toggle_focus_mode).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(toolbar_frame, text="Export", command=self.export_note).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(toolbar_frame, text="Delete", command=self.delete_note).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Content editor
        content_frame = ttk.Frame(editor_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Text widget with scrollbar
        text_scroll = ttk.Scrollbar(content_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.content_text = tk.Text(
            content_frame,
            yscrollcommand=text_scroll.set,
            font=(self.settings.font_family, self.settings.font_size),
            wrap=tk.WORD if self.settings.word_wrap else tk.NONE,
            padx=15,
            pady=15,
            undo=True,
            maxundo=50
        )
        self.content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scroll.config(command=self.content_text.yview)
        
        self.content_text.bind('<KeyRelease>', self.on_content_changed)
        self.content_text.bind('<Button-3>', self.show_editor_context_menu)
        self.content_text.insert('1.0', "Start writing your note...")
        self.content_text.bind('<FocusIn>', self.on_content_focus_in)
        
        # Setup spell check tags after text widget is created
        self.setup_spell_check_tags()
        
        # Metadata frame
        meta_frame = ttk.Frame(editor_frame)
        meta_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.meta_label = ttk.Label(meta_frame, text="", font=(self.settings.font_family, 9))
        self.meta_label.pack(anchor=tk.W)
        
        parent.add(editor_frame, weight=3)
    
    def setup_status_bar(self):
        """Setup status bar"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_bar = ttk.Label(
            status_frame, 
            text="Ready", 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Auto-save indicator
        self.auto_save_label = ttk.Label(status_frame, text="Auto-save: ON", relief=tk.SUNKEN)
        self.auto_save_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Spell check indicator
        self.spell_check_label = ttk.Label(status_frame, text="Spell Check: ON", relief=tk.SUNKEN)
        self.spell_check_label.pack(side=tk.RIGHT, padx=(5, 0))
    
    def setup_menus(self):
        """Setup application menus"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Note", command=self.show_template_dialog, accelerator="Ctrl+N")
        file_menu.add_command(label="Open File...", command=self.import_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.manual_save, accelerator="Ctrl+S")
        file_menu.add_command(label="Export Note", command=self.export_note, accelerator="Ctrl+E")
        file_menu.add_command(label="Print", command=self.print_note, accelerator="Ctrl+P")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Find & Replace", command=self.show_find_replace, accelerator="Ctrl+H")
        edit_menu.add_command(label="Go to Line", command=self.go_to_line, accelerator="Ctrl+G")
        
        # Format menu
        format_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Format", menu=format_menu)
        format_menu.add_command(label="Bold", command=self.format_bold, accelerator="Ctrl+B")
        format_menu.add_command(label="Italic", command=self.format_italic, accelerator="Ctrl+I")
        format_menu.add_command(label="Underline", command=self.format_underline, accelerator="Ctrl+U")
        format_menu.add_separator()
        format_menu.add_command(label="Font...", command=self.choose_font)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Toggle Spell Check", command=self.toggle_spell_check, accelerator="Ctrl+Shift+S")
        tools_menu.add_command(label="Check Spelling Now", command=self.check_spelling_now, accelerator="F7")
        tools_menu.add_separator()
        tools_menu.add_command(label="Backup Notes", command=self.manual_backup)
        tools_menu.add_command(label="Restore from Backup", command=self.restore_backup)
        tools_menu.add_separator()
        tools_menu.add_command(label="Settings", command=self.show_settings, accelerator="Ctrl+,")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme, accelerator="Ctrl+T")
        view_menu.add_command(label="Focus Mode", command=self.toggle_focus_mode, accelerator="F11")
        view_menu.add_separator()
        view_menu.add_command(label="Statistics", command=self.show_statistics, accelerator="Ctrl+Shift+T")
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts, accelerator="F1")
        help_menu.add_command(label="About", command=self.show_about)
    
    def setup_bindings(self):
        """Setup keyboard bindings"""
        # File operations
        self.root.bind('<Control-n>', lambda e: self.show_template_dialog())
        self.root.bind('<Control-o>', lambda e: self.import_file())
        self.root.bind('<Control-s>', lambda e: self.manual_save())
        self.root.bind('<Control-e>', lambda e: self.export_note())
        self.root.bind('<Control-p>', lambda e: self.print_note())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        
        # Edit operations
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-y>', lambda e: self.redo())
        self.root.bind('<Control-x>', lambda e: self.cut_text())
        self.root.bind('<Control-c>', lambda e: self.copy_text())
        self.root.bind('<Control-v>', lambda e: self.paste_text())
        self.root.bind('<Control-h>', lambda e: self.show_find_replace())
        self.root.bind('<Control-g>', lambda e: self.go_to_line())
        
        # Format operations
        self.root.bind('<Control-b>', lambda e: self.format_bold())
        self.root.bind('<Control-i>', lambda e: self.format_italic())
        self.root.bind('<Control-u>', lambda e: self.format_underline())
        
        # Spell check operations
        self.root.bind('<Control-Shift-S>', lambda e: self.toggle_spell_check())
        self.root.bind('<F7>', lambda e: self.check_spelling_now())
        
        # View operations
        self.root.bind('<Control-t>', lambda e: self.toggle_theme())
        self.root.bind('<F11>', lambda e: self.toggle_focus_mode())
        self.root.bind('<Control-Shift-T>', lambda e: self.show_statistics())
        
        # Navigation
        self.root.bind('<Control-f>', lambda e: self.search_entry.focus())
        self.root.bind('<Delete>', lambda e: self.delete_note())
        self.root.bind('<Control-Up>', lambda e: self.navigate_notes(-1))
        self.root.bind('<Control-Down>', lambda e: self.navigate_notes(1))
        
        # Tools
        self.root.bind('<Control-comma>', lambda e: self.show_settings())
        self.root.bind('<F1>', lambda e: self.show_shortcuts())
        
        # Close suggestions on Escape
        self.root.bind('<Escape>', lambda e: self.close_suggestions())
    
    # Spell checking methods
    def toggle_spell_check(self):
        """Toggle spell checking on/off"""
        self.settings.spell_check_enabled = self.spell_check_var.get()
        
        if self.settings.spell_check_enabled:
            self.spell_check_label.config(text="Spell Check: ON")
            self.check_spelling_now()
            self.start_spell_check_timer()
        else:
            self.spell_check_label.config(text="Spell Check: OFF")
            self.clear_spell_check_highlights()
            self.stop_spell_check_timer()
        
        self.save_settings()
    
    def check_spelling_now(self):
        """Check spelling of current content immediately"""
        if not self.settings.spell_check_enabled:
            return
        
        # Clear existing highlights
        self.clear_spell_check_highlights()
        
        # Get current content
        content = self.content_text.get('1.0', tk.END + '-1c')
        if not content or content == "Start writing your note...":
            return
        
        # Find all words and their positions
        words_with_positions = []
        for match in re.finditer(r'\b[a-zA-Z]+\b', content):
            word = match.group()
            start_pos = match.start()
            end_pos = match.end()
            words_with_positions.append((word, start_pos, end_pos))
        
        # Check each word
        for word, start_pos, end_pos in words_with_positions:
            if not self.spell_checker.is_word_correct(word):
                # Convert string positions to Tkinter text positions
                start_line = content[:start_pos].count('\n') + 1
                start_col = start_pos - content.rfind('\n', 0, start_pos) - 1
                end_line = content[:end_pos].count('\n') + 1
                end_col = end_pos - content.rfind('\n', 0, end_pos) - 1
                
                start_index = f"{start_line}.{start_col}"
                end_index = f"{end_line}.{end_col}"
                
                # Highlight misspelled word
                self.content_text.tag_add("misspelled", start_index, end_index)
                
                # Store word position for suggestions
                self.misspelled_words[start_index] = {
                    'word': word,
                    'start': start_index,
                    'end': end_index
                }
    
    def clear_spell_check_highlights(self):
        """Clear all spell check highlights"""
        self.content_text.tag_remove("misspelled", '1.0', tk.END)
        self.misspelled_words.clear()
    
    def start_spell_check_timer(self):
        """Start timer for automatic spell checking"""
        if self.spell_check_timer:
            self.root.after_cancel(self.spell_check_timer)
        
        def delayed_spell_check():
            if self.settings.spell_check_enabled:
                self.check_spelling_now()
            self.spell_check_timer = self.root.after(2000, delayed_spell_check)  # Check every 2 seconds
        
        self.spell_check_timer = self.root.after(2000, delayed_spell_check)
    
    def stop_spell_check_timer(self):
        """Stop automatic spell checking timer"""
        if self.spell_check_timer:
            self.root.after_cancel(self.spell_check_timer)
            self.spell_check_timer = None
    
    def on_misspelled_word_click(self, event):
        """Handle click on misspelled word"""
        # Get the position where clicked
        index = self.content_text.index(f"@{event.x},{event.y}")
        
        # Find the misspelled word at this position
        for pos, word_info in self.misspelled_words.items():
            if self.content_text.compare(index, ">=", word_info['start']) and \
               self.content_text.compare(index, "<=", word_info['end']):
                self.show_spelling_suggestions(word_info, event.x_root, event.y_root)
                break
    
    def on_misspelled_word_right_click(self, event):
        """Handle right-click on misspelled word"""
        self.on_misspelled_word_click(event)
    
    def show_spelling_suggestions(self, word_info, x, y):
        """Show spelling suggestions popup"""
        if self.suggestions_window:
            self.suggestions_window.destroy()
        
        word = word_info['word']
        suggestions = self.spell_checker.get_suggestions(word)
        
        # Create suggestions window
        self.suggestions_window = tk.Toplevel(self.root)
        self.suggestions_window.title("Spelling Suggestions")
        self.suggestions_window.geometry(f"+{x}+{y}")
        self.suggestions_window.transient(self.root)
        self.suggestions_window.grab_set()
        self.suggestions_window.resizable(False, False)
        
        # Configure window
        self.suggestions_window.configure(bg='white', relief='solid', bd=1)
        
        # Header
        header_frame = tk.Frame(self.suggestions_window, bg='#f0f0f0')
        header_frame.pack(fill=tk.X, padx=1, pady=1)
        
        tk.Label(header_frame, text=f"Suggestions for: '{word}'", 
                font=('Arial', 10, 'bold'), bg='#f0f0f0').pack(pady=5)
        
        # Suggestions list
        if suggestions:
            for suggestion in suggestions:
                btn = tk.Button(
                    self.suggestions_window,
                    text=suggestion,
                    font=('Arial', 10),
                    bg='white',
                    relief='flat',
                    anchor='w',
                    padx=10,
                    pady=3,
                    command=lambda s=suggestion, wi=word_info: self.apply_suggestion(s, wi)
                )
                btn.pack(fill=tk.X, padx=1)
                
                # Hover effects
                def on_enter(e, button=btn):
                    button.configure(bg='#e6f3ff')
                def on_leave(e, button=btn):
                    button.configure(bg='white')
                
                btn.bind('<Enter>', on_enter)
                btn.bind('<Leave>', on_leave)
        else:
            tk.Label(self.suggestions_window, text="No suggestions found", 
                    font=('Arial', 10), fg='gray', bg='white').pack(pady=10)
        
        # Separator
        tk.Frame(self.suggestions_window, height=1, bg='#d0d0d0').pack(fill=tk.X, pady=2)
        
        # Action buttons
        action_frame = tk.Frame(self.suggestions_window, bg='white')
        action_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Add to dictionary button
        add_btn = tk.Button(
            action_frame,
            text="Add to Dictionary",
            font=('Arial', 9),
            bg='#4CAF50',
            fg='white',
            relief='flat',
            padx=10,
            pady=2,
            command=lambda: self.add_word_to_dictionary(word, word_info)
        )
        add_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Ignore button
        ignore_btn = tk.Button(
            action_frame,
            text="Ignore",
            font=('Arial', 9),
            bg='#ff9800',
            fg='white',
            relief='flat',
            padx=10,
            pady=2,
            command=lambda: self.ignore_word(word_info)
        )
        ignore_btn.pack(side=tk.LEFT)
        
        # Close button
        close_btn = tk.Button(
            action_frame,
            text="Close",
            font=('Arial', 9),
            bg='#f44336',
            fg='white',
            relief='flat',
            padx=10,
            pady=2,
            command=self.close_suggestions
        )
        close_btn.pack(side=tk.RIGHT)
        
        # Bind escape key to close
        self.suggestions_window.bind('<Escape>', lambda e: self.close_suggestions())
        
        # Focus the window
        self.suggestions_window.focus_set()
    
    def apply_suggestion(self, suggestion, word_info):
        """Apply a spelling suggestion"""
        # Replace the misspelled word with the suggestion
        self.content_text.delete(word_info['start'], word_info['end'])
        self.content_text.insert(word_info['start'], suggestion)
        
        # Close suggestions window
        self.close_suggestions()
        
        # Update spell checking
        self.root.after(100, self.check_spelling_now)  # Delay to allow text update
        
        # Update note content
        self.on_content_changed(None)
    
    def add_word_to_dictionary(self, word, word_info):
        """Add word to custom dictionary"""
        self.spell_checker.add_to_dictionary(word)
        
        # Remove highlight for this word
        self.content_text.tag_remove("misspelled", word_info['start'], word_info['end'])
        if word_info['start'] in self.misspelled_words:
            del self.misspelled_words[word_info['start']]
        
        # Close suggestions window
        self.close_suggestions()
        
        # Show confirmation
        self.status_bar.config(text=f"Added '{word}' to dictionary")
        self.root.after(3000, lambda: self.status_bar.config(text="Ready"))
    
    def ignore_word(self, word_info):
        """Ignore the misspelled word (remove highlight)"""
        # Remove highlight for this word
        self.content_text.tag_remove("misspelled", word_info['start'], word_info['end'])
        if word_info['start'] in self.misspelled_words:
            del self.misspelled_words[word_info['start']]
        
        # Close suggestions window
        self.close_suggestions()
    
    def close_suggestions(self):
        """Close the suggestions window"""
        if self.suggestions_window:
            self.suggestions_window.destroy()
            self.suggestions_window = None
    
    # Event handlers
    def on_search_focus_in(self, event):
        if self.search_entry.get() == "Search notes...":
            self.search_entry.delete(0, tk.END)
    
    def on_search_focus_out(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search notes...")
    
    def on_title_focus_in(self, event):
        if self.title_entry.get() == "Note title...":
            self.title_entry.delete(0, tk.END)
    
    def on_title_focus_out(self, event):
        if not self.title_entry.get():
            self.title_entry.insert(0, "Note title...")
    
    def on_content_focus_in(self, event):
        content = self.content_text.get('1.0', tk.END + '-1c')
        if content == "Start writing your note...":
            self.content_text.delete('1.0', tk.END)
    
    def on_font_size_changed(self, event):
        new_size = int(self.font_size_var.get())
        self.settings.font_size = new_size
        self.content_text.configure(font=(self.settings.font_family, new_size))
        self.save_settings()
    
    def toggle_word_wrap(self):
        self.settings.word_wrap = self.word_wrap_var.get()
        wrap_mode = tk.WORD if self.settings.word_wrap else tk.NONE
        self.content_text.configure(wrap=wrap_mode)
        self.save_settings()
    
    def on_category_filter_changed(self, event):
        self.filter_notes_by_category()
    
    # Core functionality
    def show_template_dialog(self):
        """Show template selection dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Choose Template")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        ttk.Label(dialog, text="Select a template for your new note:", font=('Arial', 12)).pack(pady=10)
        
        # Template listbox
        template_frame = ttk.Frame(dialog)
        template_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        template_scroll = ttk.Scrollbar(template_frame)
        template_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        template_listbox = tk.Listbox(template_frame, yscrollcommand=template_scroll.set)
        template_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        template_scroll.config(command=template_listbox.yview)
        
        for template_name in self.note_templates.keys():
            template_listbox.insert(tk.END, template_name)
        
        template_listbox.selection_set(0)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        def create_note():
            selection = template_listbox.curselection()
            if selection:
                template_name = template_listbox.get(selection[0])
                self.new_note_from_template(template_name)
            dialog.destroy()
        
        ttk.Button(button_frame, text="Create", command=create_note).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)
        
        template_listbox.bind('<Double-Button-1>', lambda e: create_note())
        template_listbox.focus()
    
    def new_note_from_template(self, template_name):
        """Create a new note from template"""
        template_content = self.note_templates.get(template_name, "")
        
        # Replace placeholders
        current_date = datetime.now().strftime("%Y-%m-%d")
        template_content = template_content.replace("{date}", current_date)
        template_content = template_content.replace("{title}", "New Note")
        
        note = Note(
            id=str(int(datetime.now().timestamp() * 1000)),
            title="Untitled Note",
            content=template_content,
            categories=[],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            word_count=len(template_content.split()),
            char_count=len(template_content)
        )
        
        self.notes.insert(0, note)
        self.update_notes_list()
        self.select_note(0)
        self.title_entry.focus()
        self.title_entry.select_range(0, tk.END)
        self.save_data()
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.settings.theme = self.current_theme
        self.apply_theme()
        self.save_settings()
        
        # Update theme button
        theme_text = "☀️" if self.current_theme == "dark" else "🌙"
        # Find and update theme button (this is a simplified approach)
        self.status_bar.config(text=f"Theme switched to {self.current_theme}")
    
    def toggle_focus_mode(self):
        """Toggle focus mode (hide sidebar)"""
        self.is_focus_mode = not self.is_focus_mode
        # Implementation would hide/show sidebar
        self.status_bar.config(text=f"Focus mode: {'ON' if self.is_focus_mode else 'OFF'}")
    
    def toggle_favorite(self):
        """Toggle favorite status of current note"""
        if self.current_note_index is not None:
            note = self.notes[self.current_note_index]
            note.is_favorite = not note.is_favorite
            self.update_notes_list()
            self.save_data()
    
    def show_advanced_search(self):
        """Show advanced search dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Advanced Search")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Search options
        ttk.Label(dialog, text="Search Options", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Search term
        search_frame = ttk.Frame(dialog)
        search_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(search_frame, text="Search for:").pack(anchor=tk.W)
        search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=search_var).pack(fill=tk.X, pady=2)
        
        # Options
        options_frame = ttk.Frame(dialog)
        options_frame.pack(fill=tk.X, padx=20, pady=10)
        
        case_sensitive = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Case sensitive", variable=case_sensitive).pack(anchor=tk.W)
        
        whole_words = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Whole words only", variable=whole_words).pack(anchor=tk.W)
        
        search_content = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Search in content", variable=search_content).pack(anchor=tk.W)
        
        search_titles = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Search in titles", variable=search_titles).pack(anchor=tk.W)
        
        # Results
        ttk.Label(dialog, text="Results", font=('Arial', 12, 'bold')).pack(pady=(20, 5))
        
        results_frame = ttk.Frame(dialog)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        results_scroll = ttk.Scrollbar(results_frame)
        results_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        results_listbox = tk.Listbox(results_frame, yscrollcommand=results_scroll.set)
        results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scroll.config(command=results_listbox.yview)
        
        def perform_search():
            results_listbox.delete(0, tk.END)
            search_term = search_var.get()
            if not search_term:
                return
            
            # Perform search based on options
            for i, note in enumerate(self.notes):
                match_found = False
                
                if search_titles.get():
                    title_text = note.title if case_sensitive.get() else note.title.lower()
                    search_text = search_term if case_sensitive.get() else search_term.lower()
                    
                    if whole_words.get():
                        if re.search(r'\b' + re.escape(search_text) + r'\b', title_text):
                            match_found = True
                    else:
                        if search_text in title_text:
                            match_found = True
                
                if search_content.get() and not match_found:
                    content_text = note.content if case_sensitive.get() else note.content.lower()
                    search_text = search_term if case_sensitive.get() else search_term.lower()
                    
                    if whole_words.get():
                        if re.search(r'\b' + re.escape(search_text) + r'\b', content_text):
                            match_found = True
                    else:
                        if search_text in content_text:
                            match_found = True
                
                if match_found:
                    results_listbox.insert(tk.END, f"{note.title} ({note.created_at[:10]})")
        
        def on_result_select(event):
            selection = results_listbox.curselection()
            if selection:
                index = selection[0]
                # Find the actual note index
                search_term = search_var.get()
                if search_term:
                    matching_notes = []
                    for i, note in enumerate(self.notes):
                        # Simplified matching logic
                        if (search_term.lower() in note.title.lower() or 
                            search_term.lower() in note.content.lower()):
                            matching_notes.append(i)
                    
                    if index < len(matching_notes):
                        self.select_note(matching_notes[index])
                        dialog.destroy()
        
        results_listbox.bind('<<ListboxSelect>>', on_result_select)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(button_frame, text="Search", command=perform_search).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Close", command=dialog.destroy).pack(side=tk.RIGHT)
        
        # Bind Enter to search
        search_var.trace('w', lambda *args: perform_search())
    
    def on_search_changed(self, *args):
        """Handle search text changes"""
        search_term = self.search_var.get()
        if search_term and search_term != "Search notes...":
            self.filter_notes_by_search(search_term)
        else:
            self.update_notes_list()
    
    def filter_notes_by_search(self, search_term):
        """Filter notes by search term"""
        self.notes_listbox.delete(0, tk.END)
        
        for i, note in enumerate(self.notes):
            if (search_term.lower() in note.title.lower() or 
                search_term.lower() in note.content.lower() or
                any(search_term.lower() in cat.lower() for cat in note.categories)):
                
                display_text = f"{'⭐ ' if note.is_favorite else ''}{note.title}"
                if note.categories:
                    display_text += f" [{', '.join(note.categories)}]"
                
                self.notes_listbox.insert(tk.END, display_text)
    
    def filter_notes_by_category(self):
        """Filter notes by selected category"""
        selected_category = self.category_combo.get()
        if not selected_category or selected_category == "All Categories":
            self.update_notes_list()
            return
        
        self.notes_listbox.delete(0, tk.END)
        
        for note in self.notes:
            if selected_category in note.categories:
                display_text = f"{'⭐ ' if note.is_favorite else ''}{note.title}"
                if note.categories:
                    display_text += f" [{', '.join(note.categories)}]"
                
                self.notes_listbox.insert(tk.END, display_text)
    
    def on_note_selected(self, event):
        """Handle note selection"""
        selection = self.notes_listbox.curselection()
        if selection:
            # Find the actual note index based on current filter
            selected_index = selection[0]
            
            # If we're filtering, we need to find the real index
            search_term = self.search_var.get()
            selected_category = self.category_combo.get()
            
            if search_term and search_term != "Search notes...":
                # Find matching notes
                matching_indices = []
                for i, note in enumerate(self.notes):
                    if (search_term.lower() in note.title.lower() or 
                        search_term.lower() in note.content.lower() or
                        any(search_term.lower() in cat.lower() for cat in note.categories)):
                        matching_indices.append(i)
                
                if selected_index < len(matching_indices):
                    self.select_note(matching_indices[selected_index])
            
            elif selected_category and selected_category != "All Categories":
                # Find notes in category
                matching_indices = []
                for i, note in enumerate(self.notes):
                    if selected_category in note.categories:
                        matching_indices.append(i)
                
                if selected_index < len(matching_indices):
                    self.select_note(matching_indices[selected_index])
            
            else:
                # No filter, direct selection
                self.select_note(selected_index)
    
    def select_note(self, index):
        """Select and display a note"""
        if 0 <= index < len(self.notes):
            self.save_current_note()  # Save any changes to current note
            
            self.current_note_index = index
            note = self.notes[index]
            
            # Update UI
            self.title_var.set(note.title)
            self.content_text.delete('1.0', tk.END)
            self.content_text.insert('1.0', note.content)
            
            # Update metadata
            self.update_metadata_display(note)
            
            # Update listbox selection
            self.notes_listbox.selection_clear(0, tk.END)
            
            # Check spelling if enabled
            if self.settings.spell_check_enabled:
                self.root.after(500, self.check_spelling_now)  # Delay to allow text to render
    
    def update_metadata_display(self, note):
        """Update the metadata display"""
        created = datetime.fromisoformat(note.created_at).strftime("%Y-%m-%d %H:%M")
        updated = datetime.fromisoformat(note.updated_at).strftime("%Y-%m-%d %H:%M")
        
        metadata_text = f"Created: {created} | Updated: {updated} | Words: {note.word_count} | Characters: {note.char_count}"
        if note.categories:
            metadata_text += f" | Categories: {', '.join(note.categories)}"
        
        self.meta_label.config(text=metadata_text)
    
    def on_title_changed(self, *args):
        """Handle title changes"""
        if self.current_note_index is not None:
            new_title = self.title_var.get()
            if new_title and new_title != "Note title...":
                self.notes[self.current_note_index].title = new_title
                self.notes[self.current_note_index].updated_at = datetime.now().isoformat()
                self.update_notes_list()
    
    def on_content_changed(self, event):
        """Handle content changes"""
        if self.current_note_index is not None:
            content = self.content_text.get('1.0', tk.END + '-1c')
            if content != "Start writing your note...":
                note = self.notes[self.current_note_index]
                note.content = content
                note.updated_at = datetime.now().isoformat()
                
                # Update word and character counts
                note.word_count = len(content.split()) if content.strip() else 0
                note.char_count = len(content)
                
                self.update_metadata_display(note)
                
                # Trigger spell check if enabled
                if self.settings.spell_check_enabled:
                    if self.spell_check_timer:
                        self.root.after_cancel(self.spell_check_timer)
                    self.spell_check_timer = self.root.after(1000, self.check_spelling_now)
    
    def save_current_note(self):
        """Save the currently selected note"""
        if self.current_note_index is not None:
            note = self.notes[self.current_note_index]
            
            title = self.title_var.get()
            if title and title != "Note title...":
                note.title = title
            
            content = self.content_text.get('1.0', tk.END + '-1c')
            if content != "Start writing your note...":
                note.content = content
                note.word_count = len(content.split()) if content.strip() else 0
                note.char_count = len(content)
            
            note.updated_at = datetime.now().isoformat()
    
    def update_notes_list(self):
        """Update the notes list display"""
        self.notes_listbox.delete(0, tk.END)
        
        for note in self.notes:
            display_text = f"{'⭐ ' if note.is_favorite else ''}{note.title}"
            if note.categories:
                display_text += f" [{', '.join(note.categories)}]"
            
            self.notes_listbox.insert(tk.END, display_text)
    
    def update_category_combo(self):
        """Update category combobox"""
        all_categories = set()
        for note in self.notes:
            all_categories.update(note.categories)
        
        categories = ["All Categories"] + sorted(list(all_categories))
        self.category_combo['values'] = categories
        if not self.category_combo.get():
            self.category_combo.set("All Categories")
    
    def delete_note(self):
        """Delete the current note"""
        if self.current_note_index is not None:
            note = self.notes[self.current_note_index]
            
            result = messagebox.askyesno(
                "Delete Note",
                f"Are you sure you want to delete '{note.title}'?\n\nThis action cannot be undone."
            )
            
            if result:
                del self.notes[self.current_note_index]
                self.current_note_index = None
                
                # Clear editor
                self.title_var.set("Note title...")
                self.content_text.delete('1.0', tk.END)
                self.content_text.insert('1.0', "Start writing your note...")
                self.meta_label.config(text="")
                
                self.update_notes_list()
                self.save_data()
                
                # Select first note if available
                if self.notes:
                    self.select_note(0)
    
    # Additional methods would continue here...
    # (The rest of the methods like export_note, import_file, etc. would follow)
    
    def export_note(self):
        """Export current note"""
        if self.current_note_index is None:
            messagebox.showwarning("No Note", "Please select a note to export.")
            return
        
        note = self.notes[self.current_note_index]
        
        # Ask for export format
        formats = [
            ("Text files", "*.txt"),
            ("Markdown files", "*.md"),
            ("HTML files", "*.html"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.asksaveasfilename(
            title="Export Note",
            defaultextension=".txt",
            filetypes=formats,
            initialvalue=f"{note.title}.txt"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    if filename.endswith('.md'):
                        f.write(f"# {note.title}\n\n{note.content}\n\n---\n")
                        f.write(f"*Created: {note.created_at}*\n")
                        f.write(f"*Updated: {note.updated_at}*\n")
                    elif filename.endswith('.html'):
                        f.write(f"<html><head><title>{note.title}</title></head><body>")
                        f.write(f"<h1>{note.title}</h1>")
                        f.write(f"<pre>{note.content}</pre>")
                        f.write(f"<hr><p><em>Created: {note.created_at}</em></p>")
                        f.write(f"<p><em>Updated: {note.updated_at}</em></p>")
                        f.write("</body></html>")
                    else:
                        f.write(f"{note.title}\n")
                        f.write("=" * len(note.title) + "\n\n")
                        f.write(f"{note.content}\n\n")
                        f.write(f"Created: {note.created_at}\n")
                        f.write(f"Updated: {note.updated_at}\n")
                
                self.status_bar.config(text=f"Note exported to {filename}")
                self.root.after(3000, lambda: self.status_bar.config(text="Ready"))
                
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export note:\n{str(e)}")
    
    def import_file(self):
        """Import a file as a new note"""
        filename = filedialog.askopenfilename(
            title="Import File",
            filetypes=[
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Create new note
                title = Path(filename).stem
                note = Note(
                    id=str(int(datetime.now().timestamp() * 1000)),
                    title=title,
                    content=content,
                    categories=[],
                    created_at=datetime.now().isoformat(),
                    updated_at=datetime.now().isoformat(),
                    word_count=len(content.split()) if content.strip() else 0,
                    char_count=len(content)
                )
                
                self.notes.insert(0, note)
                self.update_notes_list()
                self.select_note(0)
                self.save_data()
                
                self.status_bar.config(text=f"File imported: {filename}")
                self.root.after(3000, lambda: self.status_bar.config(text="Ready"))
                
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import file:\n{str(e)}")
    
    def manual_save(self):
        """Manual save operation"""
        self.save_current_note()
        self.save_data()
        self.status_bar.config(text="Notes saved")
        self.root.after(2000, lambda: self.status_bar.config(text="Ready"))
    
    def print_note(self):
        """Print current note"""
        if self.current_note_index is None:
            messagebox.showwarning("No Note", "Please select a note to print.")
            return
        
        # This would typically open a print dialog
        # For now, we'll show a message
        messagebox.showinfo("Print", "Print functionality would be implemented here.")
    
    # Text editing operations
    def undo(self):
        try:
            self.content_text.edit_undo()
        except tk.TclError:
            pass
    
    def redo(self):
        try:
            self.content_text.edit_redo()
        except tk.TclError:
            pass
    
    def cut_text(self):
        try:
            self.content_text.event_generate("<<Cut>>")
        except tk.TclError:
            pass
    
    def copy_text(self):
        try:
            self.content_text.event_generate("<<Copy>>")
        except tk.TclError:
            pass
    
    def paste_text(self):
        try:
            self.content_text.event_generate("<<Paste>>")
        except tk.TclError:
            pass
    
    def format_bold(self):
        """Apply bold formatting (placeholder)"""
        self.status_bar.config(text="Bold formatting applied")
        self.root.after(2000, lambda: self.status_bar.config(text="Ready"))
    
    def format_italic(self):
        """Apply italic formatting (placeholder)"""
        self.status_bar.config(text="Italic formatting applied")
        self.root.after(2000, lambda: self.status_bar.config(text="Ready"))
    
    def format_underline(self):
        """Apply underline formatting (placeholder)"""
        self.status_bar.config(text="Underline formatting applied")
        self.root.after(2000, lambda: self.status_bar.config(text="Ready"))
    
    def choose_font(self):
        """Choose font (placeholder)"""
        messagebox.showinfo("Font", "Font selection dialog would be implemented here.")
    
    def show_find_replace(self):
        """Show find and replace dialog"""
        messagebox.showinfo("Find & Replace", "Find & Replace dialog would be implemented here.")
    
    def go_to_line(self):
        """Go to specific line"""
        line_num = simpledialog.askinteger("Go to Line", "Enter line number:")
        if line_num:
            self.content_text.mark_set(tk.INSERT, f"{line_num}.0")
            self.content_text.see(tk.INSERT)
    
    def navigate_notes(self, direction):
        """Navigate between notes"""
        if not self.notes:
            return
        
        if self.current_note_index is None:
            self.select_note(0)
        else:
            new_index = self.current_note_index + direction
            if 0 <= new_index < len(self.notes):
                self.select_note(new_index)
    
    def add_category(self):
        """Add a new category"""
        category_name = simpledialog.askstring("New Category", "Enter category name:")
        if category_name and self.current_note_index is not None:
            note = self.notes[self.current_note_index]
            if category_name not in note.categories:
                note.categories.append(category_name)
                note.updated_at = datetime.now().isoformat()
                self.update_notes_list()
                self.update_category_combo()
                self.update_metadata_display(note)
                self.save_data()
    
    def manage_categories(self):
        """Manage categories dialog"""
        messagebox.showinfo("Manage Categories", "Category management dialog would be implemented here.")
    
    def show_note_context_menu(self, event):
        """Show context menu for notes list"""
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Open", command=lambda: self.on_note_selected(event))
        context_menu.add_command(label="Duplicate", command=self.duplicate_note)
        context_menu.add_command(label="Export", command=self.export_note)
        context_menu.add_separator()
        context_menu.add_command(label="Delete", command=self.delete_note)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def show_editor_context_menu(self, event):
        """Show context menu for editor"""
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Cut", command=self.cut_text)
        context_menu.add_command(label="Copy", command=self.copy_text)
        context_menu.add_command(label="Paste", command=self.paste_text)
        context_menu.add_separator()
        context_menu.add_command(label="Select All", command=lambda: self.content_text.tag_add(tk.SEL, "1.0", tk.END))
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def duplicate_note(self):
        """Duplicate current note"""
        if self.current_note_index is not None:
            original = self.notes[self.current_note_index]
            
            duplicate = Note(
                id=str(int(datetime.now().timestamp() * 1000)),
                title=f"{original.title} (Copy)",
                content=original.content,
                categories=original.categories.copy(),
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat(),
                word_count=original.word_count,
                char_count=original.char_count
            )
            
            self.notes.insert(self.current_note_index + 1, duplicate)
            self.update_notes_list()
            self.select_note(self.current_note_index + 1)
            self.save_data()
    
    def show_statistics(self):
        """Show note statistics"""
        if not self.notes:
            messagebox.showinfo("Statistics", "No notes available.")
            return
        
        total_notes = len(self.notes)
        total_words = sum(note.word_count for note in self.notes)
        total_chars = sum(note.char_count for note in self.notes)
        favorites = sum(1 for note in self.notes if note.is_favorite)
        
        all_categories = set()
        for note in self.notes:
            all_categories.update(note.categories)
        
        stats_text = f"""📊 Note Statistics

Total Notes: {total_notes}
Favorite Notes: {favorites}
Total Words: {total_words:,}
Total Characters: {total_chars:,}
Categories: {len(all_categories)}

Average words per note: {total_words // total_notes if total_notes > 0 else 0}
Average characters per note: {total_chars // total_notes if total_notes > 0 else 0}
"""
        
        messagebox.showinfo("Statistics", stats_text)
    
    def show_settings(self):
        """Show settings dialog"""
        messagebox.showinfo("Settings", "Settings dialog would be implemented here.")
    
    def show_shortcuts(self):
        """Show keyboard shortcuts"""
        shortcuts_text = """⌨️ Keyboard Shortcuts

File Operations:
Ctrl+N - New Note
Ctrl+O - Import File
Ctrl+S - Save
Ctrl+E - Export Note
Ctrl+P - Print
Ctrl+Q - Quit

Edit Operations:
Ctrl+Z - Undo
Ctrl+Y - Redo
Ctrl+X - Cut
Ctrl+C - Copy
Ctrl+V - Paste
Ctrl+H - Find & Replace
Ctrl+G - Go to Line

Format Operations:
Ctrl+B - Bold
Ctrl+I - Italic
Ctrl+U - Underline

Spell Check:
Ctrl+Shift+S - Toggle Spell Check
F7 - Check Spelling Now

View Operations:
Ctrl+T - Toggle Theme
F11 - Focus Mode
Ctrl+Shift+T - Statistics

Navigation:
Ctrl+F - Focus Search
Ctrl+Up/Down - Navigate Notes
Delete - Delete Note
F1 - Show Shortcuts
"""
        
        messagebox.showinfo("Keyboard Shortcuts", shortcuts_text)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """📝 Modern Notepad - Python Edition

Version 2.0.0
Built with Python & Tkinter

Features:
✅ Rich text editing
✅ Advanced spell checking with suggestions
✅ Category management
✅ Search and filtering
✅ Multiple export formats
✅ Auto-save functionality
✅ Dark/Light themes
✅ Keyboard shortcuts
✅ Note templates

Created with ❤️ for productivity enthusiasts
"""
        
        messagebox.showinfo("About Modern Notepad", about_text)
    
    # Auto-save and backup functionality
    def start_auto_save(self):
        """Start auto-save timer"""
        def auto_save():
            self.save_current_note()
            self.save_data()
            self.auto_save_timer = self.root.after(self.settings.auto_save_interval * 1000, auto_save)
        
        if self.settings.auto_save_interval > 0:
            self.auto_save_timer = self.root.after(self.settings.auto_save_interval * 1000, auto_save)
    
    def start_backup_timer(self):
        """Start backup timer"""
        def create_backup():
            if self.settings.backup_enabled:
                self.create_backup()
            self.backup_timer = self.root.after(self.settings.backup_interval * 1000, create_backup)
        
        if self.settings.backup_enabled and self.settings.backup_interval > 0:
            self.backup_timer = self.root.after(self.settings.backup_interval * 1000, create_backup)
    
    def create_backup(self):
        """Create backup of notes"""
        try:
            backup_dir = self.data_dir / "backups"
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"notes_backup_{timestamp}.json"
            
            backup_data = {
                'notes': [asdict(note) for note in self.notes],
                'categories': [asdict(cat) for cat in self.categories],
                'settings': asdict(self.settings),
                'backup_timestamp': datetime.now().isoformat()
            }
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            # Keep only last 10 backups
            backup_files = sorted(backup_dir.glob("notes_backup_*.json"))
            if len(backup_files) > 10:
                for old_backup in backup_files[:-10]:
                    old_backup.unlink()
            
        except Exception as e:
            print(f"Backup failed: {e}")
    
    def manual_backup(self):
        """Manual backup operation"""
        self.create_backup()
        self.status_bar.config(text="Backup created")
        self.root.after(2000, lambda: self.status_bar.config(text="Ready"))
    
    def restore_backup(self):
        """Restore from backup"""
        backup_dir = self.data_dir / "backups"
        if not backup_dir.exists():
            messagebox.showwarning("No Backups", "No backup files found.")
            return
        
        backup_files = sorted(backup_dir.glob("notes_backup_*.json"), reverse=True)
        if not backup_files:
            messagebox.showwarning("No Backups", "No backup files found.")
            return
        
        # Show backup selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Restore from Backup")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select backup to restore:", font=('Arial', 12)).pack(pady=10)
        
        backup_listbox = tk.Listbox(dialog)
        backup_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        for backup_file in backup_files:
            # Extract timestamp from filename
            timestamp_str = backup_file.stem.replace("notes_backup_", "")
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                display_name = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                backup_listbox.insert(tk.END, display_name)
            except ValueError:
                backup_listbox.insert(tk.END, backup_file.name)
        
        def restore_selected():
            selection = backup_listbox.curselection()
            if selection:
                backup_file = backup_files[selection[0]]
                
                result = messagebox.askyesno(
                    "Confirm Restore",
                    "This will replace all current notes with the backup data.\n\nAre you sure you want to continue?"
                )
                
                if result:
                    try:
                        with open(backup_file, 'r', encoding='utf-8') as f:
                            backup_data = json.load(f)
                        
                        # Restore notes
                        self.notes = [Note(**note_data) for note_data in backup_data['notes']]
                        
                        # Restore categories if available
                        if 'categories' in backup_data:
                            self.categories = [Category(**cat_data) for cat_data in backup_data['categories']]
                        
                        # Update UI
                        self.current_note_index = None
                        self.update_notes_list()
                        self.update_category_combo()
                        
                        # Clear editor
                        self.title_var.set("Note title...")
                        self.content_text.delete('1.0', tk.END)
                        self.content_text.insert('1.0', "Start writing your note...")
                        self.meta_label.config(text="")
                        
                        # Select first note if available
                        if self.notes:
                            self.select_note(0)
                        
                        self.save_data()
                        dialog.destroy()
                        
                        messagebox.showinfo("Restore Complete", "Notes restored successfully from backup.")
                        
                    except Exception as e:
                        messagebox.showerror("Restore Error", f"Failed to restore backup:\n{str(e)}")
            
            dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(button_frame, text="Restore", command=restore_selected).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)
    
    # Data persistence
    def load_data(self):
        """Load notes and categories from file"""
        try:
            data_file = self.data_dir / "notes.json"
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.notes = [Note(**note_data) for note_data in data.get('notes', [])]
                self.categories = [Category(**cat_data) for cat_data in data.get('categories', [])]
        
        except Exception as e:
            print(f"Error loading data: {e}")
            self.notes = []
            self.categories = []
    
    def save_data(self):
        """Save notes and categories to file"""
        try:
            data = {
                'notes': [asdict(note) for note in self.notes],
                'categories': [asdict(cat) for cat in self.categories],
                'last_saved': datetime.now().isoformat()
            }
            
            data_file = self.data_dir / "notes.json"
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_settings(self):
        """Load application settings"""
        try:
            settings_file = self.data_dir / "settings.json"
            if settings_file.exists():
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings_data = json.load(f)
                
                self.settings = AppSettings(**settings_data)
        
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.settings = AppSettings()
    
    def save_settings(self):
        """Save application settings"""
        try:
            settings_file = self.data_dir / "settings.json"
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.settings), f, indent=2)
        
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def run(self):
        """Start the application"""
        # Handle window closing
        def on_closing():
            self.save_current_note()
            self.save_data()
            self.save_settings()
            
            # Cancel timers
            if self.auto_save_timer:
                self.root.after_cancel(self.auto_save_timer)
            if self.backup_timer:
                self.root.after_cancel(self.backup_timer)
            if self.spell_check_timer:
                self.root.after_cancel(self.spell_check_timer)
            
            self.root.destroy()
        
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Start the main loop
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernNotepadApp()
    app.run()
