"""app.py
Main GUI application — premium Netflix-inspired dark theme
Refactored for simplicity and beginner-friendly readability.
Uses clean layout managers, standard system fonts, and direct widget rendering.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import threading

from src.data_loader import DataLoader
from src.preprocessor import Preprocessor
from src.analyzer import Analyzer
from src.visualizer import Visualizer

# ── Force CustomTkinter Dark Mode ─────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Premium Dark Color Palette (Netflix-Inspired) ────────────────────────
BG_DARK     = "#0A0A0A"  # Deep black background
BG_PANEL    = "#141414"  # Dark gray sidebar panel
BG_CARD     = "#1E1E1E"  # Medium gray for cards and buttons
BG_HOVER    = "#282828"  # Gray highlight on hover
NETFLIX_RED = "#E50914"  # Classic Netflix brand red
RED_HOVER   = "#C2070F"  # Darker red for active hover
TEXT_WHITE  = "#FFFFFF"  # Primary white text
TEXT_GREY   = "#8A8A8A"  # Muted gray text
TEXT_LIGHT  = "#CCCCCC"  # Off-white body text
ACCENT_BLUE = "#3B82F6"  # Blue for movies stats
ACCENT_PURP = "#8B5CF6"  # Purple for TV shows stats
ACCENT_GRN  = "#22C55E"  # Green for genres stats
BORDER      = "#2A2A2A"  # Accent divider line color

# ── Universal Fonts ──────────────────────────────────────────────────────
# Switched to standard system fonts to ensure 100% out-of-the-box compatibility
F_DISPLAY = "Segoe UI"
F_MAIN    = "Segoe UI"
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class NetflixAnalyzerApp:
    """The main GUI for the Netflix Data Analyzer — premium beginner-friendly edition."""

    def __init__(self, root):
        """Initialize the main window, data state, and build the user interface."""
        self.root = root
        self.root.title("Netflix Data Analyzer")
        self.root.geometry("1280x780")
        self.root.minsize(1100, 680)
        self.root.configure(bg=BG_DARK)

        # Data State Variables (initially empty)
        self._clean_df   = None
        self._analyzer   = None
        self._visualizer = None
        self.chart_canvas = None

        # Build Sidebar and Main Content areas
        self._setup_ui()

    # ══════════════════════════════════════════════════════════════
    #   UI LAYOUT CONSTRUCTION
    # ══════════════════════════════════════════════════════════════

    def _setup_ui(self):
        """Assemble the layout: Left sidebar + Right content area."""
        self._build_sidebar()
        self._build_main_area()

    def _build_sidebar(self):
        """Create the left control sidebar containing the logo, dropdowns, and buttons."""
        self._sidebar = tk.Frame(self.root, bg=BG_PANEL, width=280)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)  # Force sidebar to keep its explicit width

        # ── Logo Header ──────────────────────────────────────────
        header = tk.Frame(self._sidebar, bg=BG_DARK, height=120)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Try to load the Netflix PNG logo; fallback to a styled letter "N" if missing
        logo_path = os.path.join(_BASE_DIR, "assets", "netflix_logo.png")
        try:
            from PIL import Image, ImageTk
            img = Image.open(logo_path).resize((52, 52), Image.Resampling.LANCZOS)
            self._logo_img = ImageTk.PhotoImage(img)
            tk.Label(header, image=self._logo_img, bg=BG_DARK).pack(pady=(18, 2))
        except Exception:
            tk.Label(header, text="N", bg=BG_DARK, fg=NETFLIX_RED,
                     font=(F_DISPLAY, 46, "bold")).pack(pady=(12, 0))

        tk.Label(header, text="Netflix Analyzer", bg=BG_DARK,
                 fg=TEXT_GREY, font=(F_MAIN, 10)).pack()

        # Premium solid red accent separator line below header
        tk.Frame(self._sidebar, bg=NETFLIX_RED, height=2).pack(fill="x")

        # ── DATA SECTION ─────────────────────────────────────────
        self._section_label("DATA")
        self._btn_load = self._make_btn("  ⬆   Load Dataset", self._load_dataset, accent=True)

        # ── VISUALIZATION SECTION ────────────────────────────────
        self._section_label("VISUALIZE")
        self._chart_options = [
            "🥧  Content Type Pie",
            "🌍  Top Countries",
            "📈  Yearly Trend",
            "⭐  Ratings",
            "🎬  Top Genres",
            "📅  Release Year Histogram",
            "🔥  Country × Genre Heatmap",
        ]
        
        # CTkOptionMenu replaces standard Tkinter comboboxes with premium, themed menus
        self._combo = ctk.CTkOptionMenu(
            self._sidebar,
            values=self._chart_options,
            fg_color=BG_CARD,
            button_color=NETFLIX_RED,
            button_hover_color=RED_HOVER,
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color=BG_HOVER,
            text_color=TEXT_WHITE,
            font=(F_MAIN, 12),
            width=240, height=38,
            corner_radius=8,
        )
        self._combo.pack(padx=20, pady=(6, 8))
        self._combo.set(self._chart_options[0])

        self._btn_chart = self._make_btn("  ▶   Show Chart", self._show_chart)

        # ── TOOLS SECTION ────────────────────────────────────────
        self._section_label("TOOLS")
        self._btn_stats  = self._make_btn("  📊  Statistics",  self._show_statistics)
        self._btn_raw    = self._make_btn("  🗃   Raw Data",    self._show_raw_data)
        self._btn_export = self._make_btn("  💾  Export CSV",   self._export_csv)

        # Disable analytical buttons initially (activated after a dataset is successfully loaded)
        for btn in [self._btn_chart, self._btn_stats, self._btn_raw, self._btn_export]:
            btn.configure(state="disabled")

        # Footer Label
        tk.Label(self._sidebar, text="PFAI Semester Project",
                 bg=BG_PANEL, fg="#3D3D3D",
                 font=(F_MAIN, 8)).pack(side="bottom", pady=10)

    def _section_label(self, text):
        """Create a small uppercase header label in the sidebar to organize categories."""
        tk.Label(self._sidebar, text=text,
                 bg=BG_PANEL, fg=TEXT_GREY,
                 font=(F_MAIN, 8, "bold")).pack(anchor="w", padx=24, pady=(18, 4))

    def _make_btn(self, text, cmd, accent=False):
        """Create a uniform, beautifully-styled CustomTkinter button."""
        btn = ctk.CTkButton(
            self._sidebar,
            text=text,
            command=cmd,
            fg_color=NETFLIX_RED if accent else BG_CARD,
            hover_color=RED_HOVER if accent else BG_HOVER,
            text_color=TEXT_WHITE,
            font=(F_MAIN, 13, "bold"),
            width=240, height=44,
            corner_radius=10,
            anchor="w",
        )
        btn.pack(padx=20, pady=4)
        return btn

    def _build_main_area(self):
        """Create the right side display panel including a top bar and a contents frame."""
        self._main = tk.Frame(self.root, bg=BG_DARK)
        self._main.pack(side="right", fill="both", expand=True)

        # Top Bar frame
        topbar = tk.Frame(self._main, bg=BG_DARK, height=70)
        topbar.pack(fill="x", padx=36, pady=(24, 0))
        topbar.pack_propagate(False)

        # Main Page Title (e.g. Dashboard, Statistics, etc.)
        self._page_title = tk.Label(
            topbar, text="Dashboard",
            bg=BG_DARK, fg=TEXT_WHITE,
            font=(F_DISPLAY, 30, "bold")
        )
        self._page_title.pack(side="left", anchor="w")

        # Small status label on the right side of the top bar
        self._status_label = tk.Label(
            topbar, text="No dataset loaded",
            bg=BG_DARK, fg=TEXT_GREY,
            font=(F_MAIN, 12)
        )
        self._status_label.pack(side="right", anchor="e")

        # Thin divider line separating the top bar from actual page contents
        tk.Frame(self._main, bg=BORDER, height=1).pack(fill="x", padx=36, pady=(10, 0))

        # Main dynamic container frame where screens are rendered
        self._content = tk.Frame(self._main, bg=BG_DARK)
        self._content.pack(fill="both", expand=True, padx=36, pady=24)

        # Render the welcome screen on startup
        self._show_welcome()

    # ══════════════════════════════════════════════════════════════
    #   SCREEN RENDERING FUNCTIONS
    # ══════════════════════════════════════════════════════════════

    def _clear_content(self):
        """Remove all active widgets from the dynamic content container to load a new screen."""
        for widget in self._content.winfo_children():
            widget.destroy()
        self.chart_canvas = None

    def _set_page_title(self, text):
        """Quickly update the top bar header title."""
        self._page_title.configure(text=text)

    def _show_welcome(self):
        """Render the initial welcome card that prompts the user to load a dataset."""
        self._clear_content()
        self._set_page_title("Dashboard")

        # Centered visual card
        card = tk.Frame(self._content, bg=BG_CARD, padx=70, pady=56)
        card.place(relx=0.5, rely=0.46, anchor="center")

        # Netflix brand red text letter
        n_label = tk.Label(card, text="N", bg=BG_CARD, fg=NETFLIX_RED,
                           font=(F_DISPLAY, 86, "bold"))
        n_label.pack()

        tk.Label(card, text="NETFLIX DATA ANALYZER",
                 bg=BG_CARD, fg=TEXT_WHITE,
                 font=(F_DISPLAY, 22, "bold")).pack(pady=(0, 6))

        tk.Label(card,
                 text="Load your netflix_titles.csv to explore insights,\ntrends, and beautiful visualisations.",
                 bg=BG_CARD, fg=TEXT_GREY,
                 font=(F_MAIN, 12), justify="center").pack()

        tk.Frame(card, bg=NETFLIX_RED, height=2, width=280).pack(pady=22)

        tk.Label(card, text="← Click  \"Load Dataset\"  to begin",
                 bg=BG_CARD, fg=TEXT_GREY,
                 font=(F_MAIN, 11, "italic")).pack()

    def _show_loading_screen(self):
        """Display a professional progress screen while processing data in the background."""
        self._clear_content()
        self._set_page_title("Loading...")

        center = tk.Frame(self._content, bg=BG_DARK)
        center.place(relx=0.5, rely=0.42, anchor="center")

        tk.Label(center, text="Processing Dataset",
                 bg=BG_DARK, fg=TEXT_WHITE,
                 font=(F_DISPLAY, 22, "bold")).pack(pady=(0, 8))

        # Replaced complex, slow timer animations with standard, high-performance CTk Indeterminate progress bars
        self._loading_label = tk.Label(center, text="Pre-processing titles, removing duplicates...",
                                       bg=BG_DARK, fg=TEXT_GREY,
                                       font=(F_MAIN, 13))
        self._loading_label.pack()

        # Create a looping indeterminate progress bar
        bar = ctk.CTkProgressBar(center, width=360, height=6,
                                  fg_color=BG_CARD,
                                  progress_color=NETFLIX_RED,
                                  corner_radius=3)
        bar.pack(pady=18)
        bar.configure(mode="indeterminate")
        bar.start()  # Instantly animates automatically inside CustomTkinter

    def _show_quick_stats(self):
        """Render high-level metadata stat cards on the dashboard once data is loaded."""
        self._clear_content()
        self._set_page_title("Dashboard")

        # Gather dataset aggregates
        counts = self._clean_df['type'].value_counts()
        movies = counts.get('Movie', 0)
        shows  = counts.get('TV Show', 0)
        total  = len(self._clean_df)
        genres = self._clean_df['primary_genre'].nunique()

        tk.Label(self._content, text="OVERVIEW",
                 bg=BG_DARK, fg=TEXT_GREY,
                 font=(F_MAIN, 9, "bold")).pack(anchor="w", pady=(0, 10))

        # Horizontal layout container
        row = tk.Frame(self._content, bg=BG_DARK)
        row.pack(fill="x", pady=(0, 24))

        # Render each stat card directly (removes high-complexity staggered timer delays)
        stats_to_display = [
            ("Total Titles",  total,  NETFLIX_RED),
            ("Movies",        movies, ACCENT_BLUE),
            ("TV Shows",      shows,  ACCENT_PURP),
            ("Unique Genres", genres, ACCENT_GRN),
        ]

        for label, value, color in stats_to_display:
            self._stat_card(row, label, value, color)

        # Footer guide box
        strip = tk.Frame(self._content, bg=BG_CARD, padx=22, pady=16)
        strip.pack(fill="x")
        tk.Label(strip,
                 text="✨  Use the left-hand sidebar options to explore interactive charts, statistics, and raw data.",
                 bg=BG_CARD, fg=TEXT_LIGHT,
                 font=(F_MAIN, 12)).pack(anchor="w")

    def _stat_card(self, parent, label, value, accent_color):
        """Create a direct, styled dashboard card to show a single statistical total."""
        card = tk.Frame(parent, bg=BG_CARD, padx=26, pady=20)
        card.pack(side="left", padx=(0, 14))

        # Left thin brand border strip
        tk.Frame(card, bg=accent_color, width=4, height=56).pack(side="left", padx=(0, 14))

        inner = tk.Frame(card, bg=BG_CARD)
        inner.pack(side="left")

        # Direct values displayed instantly (removes complex incremental timer recursion)
        val_lbl = tk.Label(inner, text=f"{value:,}", bg=BG_CARD, fg=TEXT_WHITE,
                           font=(F_DISPLAY, 34, "bold"))
        val_lbl.pack(anchor="w")

        tk.Label(inner, text=label, bg=BG_CARD, fg=TEXT_GREY,
                 font=(F_MAIN, 11)).pack(anchor="w")

    # ══════════════════════════════════════════════════════════════
    #   CORE FUNCTIONAL ACTION HANDLERS
    # ══════════════════════════════════════════════════════════════

    def _load_dataset(self):
        """Open a standard OS dialog to load, clean, and preprocess the Netflix titles CSV."""
        filepath = filedialog.askopenfilename(
            title="Select netflix_titles.csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not filepath:
            return  # User clicked cancel

        # Display indeterminate progress bar immediately
        self._show_loading_screen()

        # Inner helper routine run on a background thread so the GUI remains fluid
        def do_load():
            try:
                # 1. Load data
                loader = DataLoader(filepath)
                loader.load()
                
                # 2. Preprocess data
                preprocessor = Preprocessor(loader.get_dataframe())
                clean = preprocessor.process()
                
                # 3. Safely update UI state on main thread
                self.root.after(0, lambda: self._on_load_success(clean))
            except Exception as e:
                # 3. Safely alert about failures on main thread
                self.root.after(0, lambda: self._on_load_error(str(e)))

        # Fire off loading on a separate thread to prevent "App Not Responding" crashes
        threading.Thread(target=do_load, daemon=True).start()

    def _on_load_success(self, clean_df):
        """Action handler when data processes successfully."""
        self._clean_df   = clean_df
        self._analyzer   = Analyzer(self._clean_df)
        self._visualizer = Visualizer(self._clean_df, self._analyzer)

        # Unlock all navigation and data viewing buttons in sidebar
        for btn in [self._btn_chart, self._btn_stats, self._btn_raw, self._btn_export]:
            btn.configure(state="normal")

        # Update green success header text
        self._status_label.configure(
            text=f"✅  {len(self._clean_df):,} titles loaded", fg=ACCENT_GRN
        )
        self._show_quick_stats()

    def _on_load_error(self, msg):
        """Action handler if file parsing or processing runs into an error."""
        self._show_welcome()
        messagebox.showerror("Load Error", f"Failed to load dataset:\n{msg}")

    def _show_chart(self):
        """Parse dropdown selection, retrieve Matplotlib figure, and embed it into the UI."""
        try:
            selected_option = self._combo.get()
            
            # Map selected option to corresponding visualizer function
            mapping = {
                self._chart_options[0]: self._visualizer.plot_content_type_pie,
                self._chart_options[1]: self._visualizer.plot_top_countries_bar,
                self._chart_options[2]: self._visualizer.plot_yearly_trend_line,
                self._chart_options[3]: self._visualizer.plot_rating_bar,
                self._chart_options[4]: self._visualizer.plot_genre_bar,
                self._chart_options[5]: self._visualizer.plot_release_year_histogram,
                self._chart_options[6]: self._visualizer.plot_country_genre_heatmap,
            }
            
            fig = mapping[selected_option]()

            self._clear_content()
            title_text = selected_option.split("  ", 1)[-1]
            self._set_page_title(title_text)

            tk.Label(self._content, text=title_text,
                     bg=BG_DARK, fg=TEXT_WHITE,
                     font=(F_DISPLAY, 20, "bold")).pack(anchor="w", pady=(0, 10))

            # Embed Matplotlib canvas container in Tkinter Frame
            self.chart_canvas = FigureCanvasTkAgg(fig, master=self._content)
            widget = self.chart_canvas.get_tk_widget()
            widget.configure(bg=BG_DARK, highlightthickness=0)
            widget.pack(fill="both", expand=True)
            self.chart_canvas.draw()

        except Exception as e:
            messagebox.showerror("Chart Error", f"Could not render chart:\n{e}")

    def _show_statistics(self):
        """Fetch computed numerical aggregates from Analyzer class and display in a card."""
        try:
            self._clear_content()
            self._set_page_title("Statistics")

            tk.Label(self._content, text="Statistics Summary",
                     bg=BG_DARK, fg=TEXT_WHITE,
                     font=(F_DISPLAY, 22, "bold")).pack(anchor="w", pady=(0, 14))

            # CTkScrollableFrame allows easy scrolling if content height exceeds window size
            frame = ctk.CTkScrollableFrame(self._content, fg_color=BG_DARK)
            frame.pack(fill="both", expand=True)

            # Compile multiple analytical text reports
            full_text = (
                self._analyzer.get_basic_stats() + "\n"
                + self._analyzer.get_duration_stats() + "\n"
                + "--- Top 5 Countries ---\n"
                + "\n".join(f"  {country}: {count}" for country, count in self._analyzer.get_top_countries(5).items())
                + "\n\n--- Top 5 Genres ---\n"
                + "\n".join(f"  {genre}: {count}" for genre, count in self._analyzer.get_genre_counts(5).items())
            )

            card = tk.Frame(frame, bg=BG_CARD, padx=30, pady=26)
            card.pack(fill="both", expand=True, pady=4)

            tk.Label(card, text=full_text,
                     bg=BG_CARD, fg=TEXT_WHITE,
                     font=(F_MAIN, 13),
                     justify="left", anchor="w").pack(anchor="w")

        except Exception as e:
            messagebox.showerror("Stats Error", f"Could not display statistics:\n{e}")

    def _show_raw_data(self):
        """Render first 50 rows of the processed DataFrame in a styled dark Treeview grid."""
        try:
            self._clear_content()
            self._set_page_title("Raw Data")

            tk.Label(self._content, text="Raw Data (First 50 Rows)",
                     bg=BG_DARK, fg=TEXT_WHITE,
                     font=(F_DISPLAY, 22, "bold")).pack(anchor="w", pady=(0, 12))

            columns_to_show = ['type', 'title', 'director', 'country',
                               'release_year', 'rating', 'primary_genre', 'year_added']
            display_data = self._clean_df[columns_to_show].head(50)

            # Configure dark theme styling for Tkinter Treeview table grid
            style = ttk.Style()
            style.theme_use("default")
            style.configure("Dark.Treeview",
                background=BG_CARD, foreground=TEXT_WHITE,
                rowheight=30, fieldbackground=BG_CARD,
                font=(F_MAIN, 11))
            style.configure("Dark.Treeview.Heading",
                background=NETFLIX_RED, foreground=TEXT_WHITE,
                font=(F_MAIN, 11, "bold"), relief="flat")
            style.map("Dark.Treeview", background=[("selected", "#3A3A3A")])

            wrap = tk.Frame(self._content, bg=BG_DARK)
            wrap.pack(fill="both", expand=True)

            # Scrollbars
            yscroll = ttk.Scrollbar(wrap, orient="vertical")
            yscroll.pack(side="right", fill="y")
            xscroll = ttk.Scrollbar(wrap, orient="horizontal")
            xscroll.pack(side="bottom", fill="x")

            # Initialize Treeview
            tree = ttk.Treeview(wrap, columns=columns_to_show, show="headings",
                                style="Dark.Treeview",
                                yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
            yscroll.config(command=tree.yview)
            xscroll.config(command=tree.xview)

            # Define headers and column layouts
            for col in columns_to_show:
                tree.heading(col, text=col.replace("_", " ").title())
                tree.column(col, width=140, minwidth=100)

            tree.pack(side="left", fill="both", expand=True)

            # Replaced complex staggered row animation insertion with a standard, simple python loop
            for _, row in display_data.iterrows():
                tree.insert("", "end", values=[str(x) for x in row])

        except Exception as e:
            messagebox.showerror("Raw Data Error", f"Could not display data:\n{e}")

    def _export_csv(self):
        """Open file dialog and save the complete processed DataFrame to disk as a CSV file."""
        try:
            path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")]
            )
            if path:
                self._clean_df.to_csv(path, index=False, encoding="utf-8-sig")
                messagebox.showinfo("Exported ✅", f"Successfully saved cleaned dataset to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not save dataset file:\n{e}")
