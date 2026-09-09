import tkinter as tk
from tkinter import font, messagebox
from enum import Enum

class GameState(Enum):
    HOME = 1
    CASE_SELECTION = 2
    CASE_ACTIVE = 3
    WORD_VAULT = 4
    CASE_CLOSED = 5

# Vocabulary Crime Cases Database
CASES = [
    {
        "id": 1,
        "sentence": "The tiny elephant filled the entire room.",
        "suspicious_word": "tiny",
        "clue": "Size Clue",
        "options": ["enormous", "sleepy", "colourful", "quiet"],
        "correct": "enormous",
        "definition": "Enormous means extremely large or huge.",
        "example": "The enormous building could be seen from miles away.",
    },
    {
        "id": 2,
        "sentence": "She felt brave when she heard the sad news.",
        "suspicious_word": "brave",
        "clue": "Emotion Clue",
        "options": ["happy", "sad", "angry", "nervous"],
        "correct": "sad",
        "definition": "Sad means feeling unhappy or sorrowful.",
        "example": "I felt sad when my best friend moved away.",
    },
    {
        "id": 3,
        "sentence": "The bright night made it hard to see the stars.",
        "suspicious_word": "bright",
        "clue": "Light Clue",
        "options": ["dark", "cloudy", "clear", "cold"],
        "correct": "dark",
        "definition": "Dark means having little or no light.",
        "example": "The dark cave was so dark we needed flashlights.",
    },
    {
        "id": 4,
        "sentence": "The generous student refused to share her lunch.",
        "suspicious_word": "generous",
        "clue": "Character Clue",
        "options": ["selfish", "hungry", "tired", "quiet"],
        "correct": "selfish",
        "definition": "Selfish means thinking only of yourself, not others.",
        "example": "It was selfish of him to take all the cookies.",
    },
    {
        "id": 5,
        "sentence": "The ancient civilisation was just built last year.",
        "suspicious_word": "ancient",
        "clue": "Time Clue",
        "options": ["modern", "old", "strange", "famous"],
        "correct": "modern",
        "definition": "Modern means new or from recent times.",
        "example": "Modern phones are much faster than old ones.",
    },
    {
        "id": 6,
        "sentence": "The silent classroom was filled with loud noise.",
        "suspicious_word": "silent",
        "clue": "Sound Clue",
        "options": ["noisy", "quiet", "empty", "boring"],
        "correct": "noisy",
        "definition": "Noisy means making a lot of sound.",
        "example": "The noisy traffic made it hard to hear.",
    },
    {
        "id": 7,
        "sentence": "He was disappointed when he won first prize.",
        "suspicious_word": "disappointed",
        "clue": "Feeling Clue",
        "options": ["thrilled", "sad", "tired", "confused"],
        "correct": "thrilled",
        "definition": "Thrilled means very excited or happy.",
        "example": "She was thrilled to receive the surprise gift.",
    },
    {
        "id": 8,
        "sentence": "The fragrant flower smelled absolutely terrible.",
        "suspicious_word": "fragrant",
        "clue": "Scent Clue",
        "options": ["stinky", "fresh", "pretty", "small"],
        "correct": "stinky",
        "definition": "Stinky means having a bad or unpleasant smell.",
        "example": "The stinky garbage needed to be taken out.",
    },
]

class VocabularyCrimeScene:
    def __init__(self, root):
        self.root = root
        self.root.title("🔎 VOCABULARY CRIME SCENE")
        self.root.geometry("900x700")
        self.root.config(bg="#1a1a2e")
        
        # Game state
        self.state = GameState.HOME
        self.current_case_index = 0
        self.detective_points = 0
        self.evidence_collected = []
        self.words_learned = {}
        self.wrong_attempts = {}
        
        # Create fonts
        self.title_font = font.Font(family="Arial", size=28, weight="bold")
        self.subtitle_font = font.Font(family="Arial", size=14)
        self.heading_font = font.Font(family="Arial", size=18, weight="bold")
        self.normal_font = font.Font(family="Arial", size=12)
        self.small_font = font.Font(family="Arial", size=10)
        
        # Main container
        self.main_frame = tk.Frame(root, bg="#1a1a2e")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.show_home_screen()
    
    def clear_frame(self):
        """Clear all widgets from main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def create_button(self, parent, text, command, bg="#ff6b6b", fg="white", width=25, height=2):
        """Create a styled button"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            font=self.normal_font,
            width=width,
            height=height,
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            activebackground="#ff5252",
            activeforeground="white"
        )
        btn.pack(pady=10)
        
        # Hover effect
        def on_enter(event):
            btn.config(bg="#ff5252", relief=tk.SUNKEN)
        
        def on_leave(event):
            btn.config(bg=bg, relief=tk.RAISED)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def show_home_screen(self):
        """Display home screen"""
        self.state = GameState.HOME
        self.clear_frame()
        
        # Title
        title = tk.Label(
            self.main_frame,
            text="🔎 VOCABULARY CRIME SCENE",
            font=self.title_font,
            fg="#ff6b6b",
            bg="#1a1a2e"
        )
        title.pack(pady=20)
        
        # Subtitle
        subtitle = tk.Label(
            self.main_frame,
            text='"Every wrong word leaves a clue!"',
            font=self.subtitle_font,
            fg="#a8e6cf",
            bg="#1a1a2e"
        )
        subtitle.pack(pady=10)
        
        # Decorative line
        line = tk.Frame(self.main_frame, height=2, bg="#ff6b6b")
        line.pack(fill=tk.X, pady=20)
        
        # Info text
        info = tk.Label(
            self.main_frame,
            text="Welcome, Detective!\n\nYour mission: Solve 8 vocabulary crimes by finding\nthe wrong word in each sentence and replacing it\nwith the correct one.\n\nCollect evidence. Earn detective points.\nLearn new vocabulary.",
            font=self.normal_font,
            fg="#ffffff",
            bg="#1a1a2e",
            justify=tk.CENTER
        )
        info.pack(pady=30)
        
        # Buttons container
        button_frame = tk.Frame(self.main_frame, bg="#1a1a2e")
        button_frame.pack(pady=30)
        
        self.create_button(button_frame, "🚀 START INVESTIGATION", self.start_investigation, bg="#4ecdc4")
        self.create_button(button_frame, "📚 WORD VAULT", self.show_word_vault, bg="#95e1d3")
    
    def start_investigation(self):
        """Start the game"""
        self.current_case_index = 0
        self.detective_points = 0
        self.evidence_collected = []
        self.words_learned = {}
        self.wrong_attempts = {}
        self.show_case_screen()
    
    def show_case_screen(self):
        """Display active case"""
        self.state = GameState.CASE_ACTIVE
        self.clear_frame()
        
        case = CASES[self.current_case_index]
        case_num = self.current_case_index + 1
        
        # Header with progress
        header_frame = tk.Frame(self.main_frame, bg="#1a1a2e")
        header_frame.pack(fill=tk.X, pady=10)
        
        progress = tk.Label(
            header_frame,
            text=f"CASE {case_num} / {len(CASES)}",
            font=self.heading_font,
            fg="#ff6b6b",
            bg="#1a1a2e"
        )
        progress.pack()
        
        # Progress bar
        progress_width = int((case_num / len(CASES)) * 40)
        progress_bar = tk.Label(
            header_frame,
            text="█" * progress_width + "░" * (40 - progress_width),
            font=font.Font(family="Arial", size=10),
            fg="#4ecdc4",
            bg="#1a1a2e"
        )
        progress_bar.pack()
        
        # Detective points
        points = tk.Label(
            header_frame,
            text=f"🔍 Detective Points: {self.detective_points}",
            font=self.normal_font,
            fg="#a8e6cf",
            bg="#1a1a2e"
        )
        points.pack()
        
        # Case panel
        panel = tk.Frame(self.main_frame, bg="#2d2d44", relief=tk.RAISED, bd=3)
        panel.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Case instruction
        instruction = tk.Label(
            panel,
            text="🚨 SUSPICIOUS WORD DETECTED! 🚨",
            font=self.heading_font,
            fg="#ff6b6b",
            bg="#2d2d44"
        )
        instruction.pack(pady=15)
        
        # Sentence display
        sentence_label = tk.Label(
            panel,
            text="Click the SUSPICIOUS word in this sentence:",
            font=self.normal_font,
            fg="#ffffff",
            bg="#2d2d44"
        )
        sentence_label.pack(pady=5)
        
        # Sentence as clickable words
        sentence_frame = tk.Frame(panel, bg="#2d2d44")
        sentence_frame.pack(pady=15)
        
        words = case["sentence"].rstrip(".").split()
        for word in words:
            word_clean = word.rstrip(".")
            if word_clean.lower() == case["suspicious_word"].lower():
                word_btn = tk.Label(
                    sentence_frame,
                    text=word,
                    font=font.Font(family="Arial", size=14, weight="bold"),
                    fg="#ff6b6b",
                    bg="#2d2d44",
                    relief=tk.RAISED,
                    bd=2,
                    padx=8,
                    pady=5,
                    cursor="hand2"
                )
                word_btn.pack(side=tk.LEFT, padx=5)
                word_btn.bind("<Button-1>", lambda e: self.word_clicked(case["suspicious_word"]))
            else:
                word_label = tk.Label(
                    sentence_frame,
                    text=word,
                    font=font.Font(family="Arial", size=14),
                    fg="#a8e6cf",
                    bg="#2d2d44",
                    padx=5
                )
                word_label.pack(side=tk.LEFT, padx=5)
        
        # Message label for feedback
        self.feedback_label = tk.Label(
            panel,
            text="",
            font=self.normal_font,
            fg="#ffffff",
            bg="#2d2d44"
        )
        self.feedback_label.pack(pady=15)
        
        # Options frame
        self.options_frame = tk.Frame(panel, bg="#2d2d44")
        self.options_frame.pack(pady=20)
        
        self.show_options(case)
    
    def word_clicked(self, word):
        """Handle word click"""
        case = CASES[self.current_case_index]
        if word.lower() == case["suspicious_word"].lower():
            self.feedback_label.config(text="✓ Correct word selected!", fg="#a8e6cf")
            self.show_replacement_options()
        else:
            self.feedback_label.config(text="✗ Wrong word! Try again.", fg="#ff6b6b")
    
    def show_options(self, case):
        """Show replacement word options"""
        # Clear previous options
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        title = tk.Label(
            self.options_frame,
            text="What would be a better word?",
            font=self.normal_font,
            fg="#ffffff",
            bg="#2d2d44"
        )
        title.pack(pady=10)
        
        self.show_replacement_options()
    
    def show_replacement_options(self):
        """Display replacement word buttons"""
        case = CASES[self.current_case_index]
        
        # Clear options
        for widget in self.options_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
        
        for option in case["options"]:
            btn = tk.Button(
                self.options_frame,
                text=option,
                command=lambda opt=option: self.check_answer(opt),
                bg="#4ecdc4",
                fg="white",
                font=self.normal_font,
                width=20,
                height=2,
                relief=tk.RAISED,
                bd=2,
                cursor="hand2",
                activebackground="#3db8ad"
            )
            btn.pack(pady=8)
            
            def on_enter(event, button=btn):
                button.config(bg="#3db8ad", relief=tk.SUNKEN)
            
            def on_leave(event, button=btn):
                button.config(bg="#4ecdc4", relief=tk.RAISED)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
    
    def check_answer(self, selected_word):
        """Check if answer is correct"""
        case = CASES[self.current_case_index]
        case_id = case["id"]
        
        if selected_word == case["correct"]:
            # Correct answer
            self.detective_points += 10
            self.evidence_collected.append(case["clue"])
            self.words_learned[case["correct"]] = {
                "definition": case["definition"],
                "example": case["example"]
            }
            
            # Show success screen
            self.show_case_success(case)
        else:
            # Wrong answer
            if case_id not in self.wrong_attempts:
                self.wrong_attempts[case_id] = 0
            self.wrong_attempts[case_id] += 1
            
            self.feedback_label.config(
                text=f"❌ Not quite! Try again. (Attempt {self.wrong_attempts[case_id]})",
                fg="#ff6b6b"
            )
            self.root.after(2000, self.show_replacement_options)
    
    def show_case_success(self, case):
        """Show case solved screen"""
        self.clear_frame()
        
        # Success message
        success = tk.Label(
            self.main_frame,
            text="✅ CASE CRACKED! ✅",
            font=self.title_font,
            fg="#a8e6cf",
            bg="#1a1a2e"
        )
        success.pack(pady=20)
        
        # Points earned
        points = tk.Label(
            self.main_frame,
            text=f"📍 +10 Detective Points!\nTotal: {self.detective_points}",
            font=self.heading_font,
            fg="#4ecdc4",
            bg="#1a1a2e"
        )
        points.pack(pady=15)
        
        # Evidence
        evidence = tk.Label(
            self.main_frame,
            text=f"🔎 Evidence Collected: {case['clue']}",
            font=self.normal_font,
            fg="#ff6b6b",
            bg="#1a1a2e"
        )
        evidence.pack(pady=10)
        
        # Word panel
        word_panel = tk.Frame(self.main_frame, bg="#2d2d44", relief=tk.RAISED, bd=3)
        word_panel.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)
        
        word_title = tk.Label(
            word_panel,
            text=f"📚 Word Learned: {case['correct'].upper()}",
            font=self.heading_font,
            fg="#a8e6cf",
            bg="#2d2d44"
        )
        word_title.pack(pady=15)
        
        definition = tk.Label(
            word_panel,
            text=case["definition"],
            font=self.normal_font,
            fg="#ffffff",
            bg="#2d2d44",
            wraplength=600,
            justify=tk.CENTER
        )
        definition.pack(pady=10)
        
        example = tk.Label(
            word_panel,
            text=f'Example: "{case["example"]}"',
            font=self.small_font,
            fg="#95e1d3",
            bg="#2d2d44",
            wraplength=600,
            justify=tk.CENTER,
            slant="italic"
        )
        example.pack(pady=10)
        
        # Next button
        button_frame = tk.Frame(self.main_frame, bg="#1a1a2e")
        button_frame.pack(pady=20)
        
        if self.current_case_index < len(CASES) - 1:
            self.create_button(
                button_frame,
                "➡️ NEXT CASE",
                self.next_case,
                bg="#ff6b6b",
                width=20
            )
        else:
            self.create_button(
                button_frame,
                "🏁 CASE CLOSED!",
                self.show_final_screen,
                bg="#a8e6cf",
                width=20
            )
    
    def next_case(self):
        """Move to next case"""
        self.current_case_index += 1
        self.show_case_screen()
    
    def show_final_screen(self):
        """Show game completion screen"""
        self.state = GameState.CASE_CLOSED
        self.clear_frame()
        
        # Title
        title = tk.Label(
            self.main_frame,
            text="🔎 CASE CLOSED! 🔎",
            font=self.title_font,
            fg="#a8e6cf",
            bg="#1a1a2e"
        )
        title.pack(pady=20)
        
        # Subtitle
        subtitle = tk.Label(
            self.main_frame,
            text='"You solved every vocabulary crime!"',
            font=self.subtitle_font,
            fg="#4ecdc4",
            bg="#1a1a2e"
        )
        subtitle.pack(pady=10)
        
        # Stats panel
        stats_panel = tk.Frame(self.main_frame, bg="#2d2d44", relief=tk.RAISED, bd=3)
        stats_panel.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)
        
        # Stats
        stats_text = f"""
📊 INVESTIGATION COMPLETE 📊

Cases Solved: {len(CASES)} / {len(CASES)}
🔍 Detective Points: {self.detective_points}
📚 Words Learned: {len(self.words_learned)}
🔎 Evidence Items: {len(self.evidence_collected)}

Evidence Collected:
"""
        for i, evidence in enumerate(self.evidence_collected, 1):
            stats_text += f"\n  {i}. {evidence}"
        
        stats_label = tk.Label(
            stats_panel,
            text=stats_text,
            font=self.normal_font,
            fg="#ffffff",
            bg="#2d2d44",
            justify=tk.LEFT
        )
        stats_label.pack(pady=20, padx=20)
        
        # Buttons
        button_frame = tk.Frame(self.main_frame, bg="#1a1a2e")
        button_frame.pack(pady=20)
        
        self.create_button(button_frame, "🔄 PLAY AGAIN", self.start_investigation, bg="#ff6b6b")
        self.create_button(button_frame, "📚 WORD VAULT", self.show_word_vault, bg="#4ecdc4")
        self.create_button(button_frame, "🏠 HOME", self.show_home_screen, bg="#95e1d3")
    
    def show_word_vault(self):
        """Show learned words"""
        self.state = GameState.WORD_VAULT
        self.clear_frame()
        
        # Title
        title = tk.Label(
            self.main_frame,
            text="📚 WORD VAULT 📚",
            font=self.title_font,
            fg="#4ecdc4",
            bg="#1a1a2e"
        )
        title.pack(pady=20)
        
        if not self.words_learned:
            empty = tk.Label(
                self.main_frame,
                text="No words learned yet!\nStart the investigation to learn new vocabulary.",
                font=self.normal_font,
                fg="#a8e6cf",
                bg="#1a1a2e"
            )
            empty.pack(pady=30)
        else:
            # Create scrollable area
            canvas = tk.Canvas(self.main_frame, bg="#1a1a2e", highlightthickness=0)
            scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#1a1a2e")
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Add words
            for word, data in self.words_learned.items():
                word_card = tk.Frame(scrollable_frame, bg="#2d2d44", relief=tk.RAISED, bd=2)
                word_card.pack(fill=tk.X, pady=10, padx=10)
                
                word_label = tk.Label(
                    word_card,
                    text=word.upper(),
                    font=self.heading_font,
                    fg="#a8e6cf",
                    bg="#2d2d44"
                )
                word_label.pack(pady=10)
                
                def_label = tk.Label(
                    word_card,
                    text=data["definition"],
                    font=self.normal_font,
                    fg="#ffffff",
                    bg="#2d2d44",
                    wraplength=600,
                    justify=tk.LEFT
                )
                def_label.pack(pady=5, padx=10)
                
                example_label = tk.Label(
                    word_card,
                    text=f'Example: "{data["example"]}"',
                    font=self.small_font,
                    fg="#95e1d3",
                    bg="#2d2d44",
                    wraplength=600,
                    justify=tk.LEFT
                )
                example_label.pack(pady=5, padx=10)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Back button
        button_frame = tk.Frame(self.main_frame, bg="#1a1a2e")
        button_frame.pack(pady=20)
        
        self.create_button(button_frame, "🔙 BACK", self.show_home_screen, bg="#95e1d3")

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyCrimeScene(root)
    root.mainloop()
