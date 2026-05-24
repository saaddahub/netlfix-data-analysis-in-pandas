"""app.py
Main GUI application — premium Netflix-inspired dark theme
with Inter ExtraBold font, smooth animations, and Netflix logo.
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

# ── Force dark mode ───────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Colour palette ────────────────────────────────────────────────
BG_DARK     = "#0A0A0A"
BG_PANEL    = "#141414"
BG_CARD     = "#1E1E1E"
BG_HOVER    = "#282828"
NETFLIX_RED = "#E50914"
RED_HOVER   = "#C2070F"
TEXT_WHITE  = "#FFFFFF"
TEXT_GREY   = "#8A8A8A"
TEXT_LIGHT  = "#CCCCCC"
ACCENT_BLUE = "#3B82F6"
ACCENT_PURP = "#8B5CF6"
ACCENT_GRN  = "#22C55E"
BORDER      = "#2A2A2A"


# Inter fonts are installed to Windows user fonts directory at startup
# Font families — Inter is now a proper system font
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F_DISPLAY = "Inter Display"
F_MAIN    = "Inter"


class NetflixAnalyzerApp:
    """The main GUI for the Netflix Data Analyzer — premium edition."""

    def __init__(self, root):
        """Initialize the window, variables, and build the UI."""
        self.root = root
        self.root.title("Netflix Data Analyzer")
        self.root.geometry("1280x780")
        self.root.minsize(1100, 680)
        self.root.configure(bg=BG_DARK)

        # Data state
        self._clean_df   = None
        self._analyzer   = None
        self._visualizer = None
        self.chart_canvas = None

        # Animation handles
        self._anim_after = None

        self._setup_ui()

    # ══════════════════════════════════════════════════════════════
    #   UI CONSTRUCTION
    # ══════════════════════════════════════════════════════════════

    def _setup_ui(self):
        """Build sidebar + main content layout."""
        self._build_sidebar()
        self._build_main_area()

    def _build_sidebar(self):
        """Create the left control panel with logo, sections, and buttons."""
        self._sidebar = tk.Frame(self.root, bg=BG_PANEL, width=280)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)

        # ── Logo header ───────────────────────────────────────────
        header = tk.Frame(self._sidebar, bg=BG_DARK, height=120)
        header.pack(fill="x")
        header.pack_propagate(False)

        logo_path = os.path.join(_BASE_DIR, "assets", "netflix_logo.png")
        try:
            from PIL import Image, ImageTk
            img = Image.open(logo_path).resize((52, 52), Image.LANCZOS)
            self._logo_img = ImageTk.PhotoImage(img)
            tk.Label(header, image=self._logo_img, bg=BG_DARK).pack(pady=(18, 2))
        except Exception:
            tk.Label(header, text="N", bg=BG_DARK, fg=NETFLIX_RED,
                     font=(F_DISPLAY, 46, "bold")).pack(pady=(12, 0))

        tk.Label(header, text="Netflix Analyzer", bg=BG_DARK,
                 fg=TEXT_GREY, font=(F_MAIN, 10)).pack()

        # Red accent bar below header
        tk.Frame(self._sidebar, bg=NETFLIX_RED, height=2).pack(fill="x")

        # ── Buttons ───────────────────────────────────────────────
        self._section_label("DATA")
        self._btn_load = self._make_btn("  ⬆   Load Dataset", self._load_dataset, accent=True)

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

        self._btn_chart  = self._make_btn("  ▶   Show Chart",    self._show_chart)

        self._section_label("TOOLS")
        self._btn_stats  = self._make_btn("  📊  Statistics",     self._show_statistics)
        self._btn_raw    = self._make_btn("  🗃    Raw Data",       self._show_raw_data)
        self._btn_export = self._make_btn("  💾  Export CSV",     self._export_csv)

        for b in [self._btn_chart, self._btn_stats, self._btn_raw, self._btn_export]:
            b.configure(state="disabled")

        tk.Label(self._sidebar, text="PFAI Semester Project",
                 bg=BG_PANEL, fg="#3D3D3D",
                 font=(F_MAIN, 8)).pack(side="bottom", pady=10)

    def _section_label(self, text):
        """Small uppercase section divider label in the sidebar."""
        tk.Label(self._sidebar, text=text,
                 bg=BG_PANEL, fg=TEXT_GREY,
                 font=(F_MAIN, 8, "bold")).pack(anchor="w", padx=24, pady=(18, 4))

    def _make_btn(self, text, cmd, accent=False):
        """Create and return a styled sidebar button."""
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
        """Build the right-side area with top bar and content frame."""
        self._main = tk.Frame(self.root, bg=BG_DARK)
        self._main.pack(side="right", fill="both", expand=True)

        # Top bar
        topbar = tk.Frame(self._main, bg=BG_DARK, height=70)
        topbar.pack(fill="x", padx=36, pady=(24, 0))
        topbar.pack_propagate(False)

        self._page_title = tk.Label(
            topbar, text="Dashboard",
            bg=BG_DARK, fg=TEXT_WHITE,
            font=(F_DISPLAY, 30, "bold")
        )
        self._page_title.pack(side="left", anchor="w")

        self._status_label = tk.Label(
            topbar, text="No dataset loaded",
            bg=BG_DARK, fg=TEXT_GREY,
            font=(F_MAIN, 12)
        )
        self._status_label.pack(side="right", anchor="e")

        tk.Frame(self._main, bg=BORDER, height=1).pack(fill="x", padx=36, pady=(10, 0))

        self._content = tk.Frame(self._main, bg=BG_DARK)
        self._content.pack(fill="both", expand=True, padx=36, pady=24)

        self._show_welcome()

    # ══════════════════════════════════════════════════════════════
    #   ANIMATION HELPERS
    # ══════════════════════════════════════════════════════════════

    def _stop_animation(self):
        """Cancel any running after() loop."""
        if self._anim_after:
            self.root.after_cancel(self._anim_after)
            self._anim_after = None

    def _animate_dots(self, label, base_text, dots=0):
        """Animate loading dots — stops silently if the label is destroyed."""
        try:
            symbols = ["   ", ".  ", ".. ", "..."]
            label.configure(text=base_text + symbols[dots % 4])
            self._anim_after = self.root.after(
                380, self._animate_dots, label, base_text, dots + 1
            )
        except tk.TclError:
            self._anim_after = None

    def _animate_progress(self, bar, step=0):
        """Animate progress bar — stops silently if the bar is destroyed."""
        try:
            bar.set(step / 100)
            if step < 95:
                speed = 28 if step < 55 else 55
                self._anim_after = self.root.after(
                    speed, self._animate_progress, bar, step + 2
                )
        except tk.TclError:
            self._anim_after = None

    def _fade_in_label(self, label, colors, step=0):
        """Cycle a label's fg colour through a list for a fade-in effect."""
        if step < len(colors):
            label.configure(fg=colors[step])
            self.root.after(45, self._fade_in_label, label, colors, step + 1)

    def _slide_in(self, widget, target_y, current_y):
        """Slide a widget upward into its target position."""
        if current_y > target_y:
            widget.place(relx=0.5, y=current_y, anchor="n")
            self.root.after(8, self._slide_in, widget, target_y, current_y - 7)
        else:
            widget.place(relx=0.5, y=target_y, anchor="n")

    def _count_up(self, label, target, current):
        """Animate a number counting up to target."""
        step = max(1, target // 28)
        if current < target:
            label.configure(text=f"{min(current + step, target):,}")
            self.root.after(28, self._count_up, label, target, current + step)
        else:
            label.configure(text=f"{target:,}")

    # ══════════════════════════════════════════════════════════════
    #   SCREENS
    # ══════════════════════════════════════════════════════════════

    def _clear_content(self):
        """Remove all widgets from the content frame."""
        for w in self._content.winfo_children():
            w.destroy()
        self.chart_canvas = None
        self._stop_animation()

    def _set_page_title(self, text):
        """Update the top-bar page title text."""
        self._page_title.configure(text=text)

    def _show_welcome(self):
        """Render the animated welcome landing card."""
        self._clear_content()
        self._set_page_title("Dashboard")

        card = tk.Frame(self._content, bg=BG_CARD, padx=70, pady=56)
        card.place(relx=0.5, rely=0.46, anchor="center")

        n_label = tk.Label(card, text="N", bg=BG_CARD, fg=NETFLIX_RED,
                           font=(F_DISPLAY, 86, "bold"))
        n_label.pack()
        self._fade_in_label(n_label, ["#3D0000","#6B0000","#990000","#C2070F","#E50914"])

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

        self._slide_in(card, target_y=60, current_y=220)

    def _show_loading_screen(self):
        """Show an animated loading screen while data processes."""
        self._clear_content()
        self._set_page_title("Loading...")

        center = tk.Frame(self._content, bg=BG_DARK)
        center.place(relx=0.5, rely=0.42, anchor="center")

        tk.Label(center, text="Processing Dataset",
                 bg=BG_DARK, fg=TEXT_WHITE,
                 font=(F_DISPLAY, 22, "bold")).pack(pady=(0, 8))

        self._loading_label = tk.Label(center, text="Loading   ",
                                        bg=BG_DARK, fg=TEXT_GREY,
                                        font=(F_MAIN, 13))
        self._loading_label.pack()

        bar = ctk.CTkProgressBar(center, width=360, height=5,
                                  fg_color=BG_CARD,
                                  progress_color=NETFLIX_RED,
                                  corner_radius=3)
        bar.pack(pady=18)
        bar.set(0)

        self._animate_progress(bar)
        self._animate_dots(self._loading_label, "Loading")

    def _show_quick_stats(self):
        """Show overview stat cards after data loads."""
        self._clear_content()
        self._set_page_title("Dashboard")

        counts = self._clean_df['type'].value_counts()
        movies = counts.get('Movie', 0)
        shows  = counts.get('TV Show', 0)
        total  = len(self._clean_df)
        genres = self._clean_df['primary_genre'].nunique()

        tk.Label(self._content, text="OVERVIEW",
                 bg=BG_DARK, fg=TEXT_GREY,
                 font=(F_MAIN, 9, "bold")).pack(anchor="w", pady=(0, 10))

        row = tk.Frame(self._content, bg=BG_DARK)
        row.pack(fill="x", pady=(0, 24))

        for i, (label, value, color) in enumerate([
            ("Total Titles",  total,  NETFLIX_RED),
            ("Movies",        movies, ACCENT_BLUE),
            ("TV Shows",      shows,  ACCENT_PURP),
            ("Unique Genres", genres, ACCENT_GRN),
        ]):
            self._stat_card(row, label, value, color, delay=i * 110)

        strip = tk.Frame(self._content, bg=BG_CARD, padx=22, pady=16)
        strip.pack(fill="x")
        tk.Label(strip,
                 text="✨  Use the sidebar to explore charts, statistics, and raw data.",
                 bg=BG_CARD, fg=TEXT_LIGHT,
                 font=(F_MAIN, 12)).pack(anchor="w")

    def _stat_card(self, parent, label, value, accent, delay=0):
        """Render a single animated stat card."""
        card = tk.Frame(parent, bg=BG_CARD, padx=26, pady=20)

        def place():
            card.pack(side="left", padx=(0, 14))
            tk.Frame(card, bg=accent, width=4, height=56).pack(side="left", padx=(0, 14))
            inner = tk.Frame(card, bg=BG_CARD)
            inner.pack(side="left")
            val_lbl = tk.Label(inner, text="0", bg=BG_CARD, fg=TEXT_WHITE,
                               font=(F_DISPLAY, 34, "bold"))
            val_lbl.pack(anchor="w")
            tk.Label(inner, text=label, bg=BG_CARD, fg=TEXT_GREY,
                     font=(F_MAIN, 11)).pack(anchor="w")
            self._count_up(val_lbl, value, 0)

        self.root.after(delay, place)

    # ══════════════════════════════════════════════════════════════
    #   CORE ACTIONS
    # ══════════════════════════════════════════════════════════════

    def _load_dataset(self):
        """Open file dialog and load/preprocess CSV on a background thread."""
        filepath = filedialog.askopenfilename(
            title="Select netflix_titles.csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not filepath:
            return

        self._show_loading_screen()

        def do_load():
            try:
                loader = DataLoader(filepath)
                loader.load()
                preprocessor = Preprocessor(loader.get_dataframe())
                clean = preprocessor.process()
                self.root.after(0, self._on_load_success, clean)
            except Exception as e:
                self.root.after(0, self._on_load_error, str(e))

        threading.Thread(target=do_load, daemon=True).start()

    def _on_load_success(self, clean_df):
        """Called on the main thread once data has loaded successfully."""
        self._stop_animation()
        self._clean_df   = clean_df
        self._analyzer   = Analyzer(self._clean_df)
        self._visualizer = Visualizer(self._clean_df, self._analyzer)

        for b in [self._btn_chart, self._btn_stats, self._btn_raw, self._btn_export]:
            b.configure(state="normal")

        self._status_label.configure(
            text=f"✅  {len(self._clean_df):,} titles loaded", fg=ACCENT_GRN
        )
        self._show_quick_stats()

    def _on_load_error(self, msg):
        """Called on the main thread if loading fails."""
        self._stop_animation()
        self._show_welcome()
        messagebox.showerror("Load Error", msg)

    def _show_chart(self):
        """Generate and embed the selected chart."""
        try:
            sel = self._combo.get()
            mapping = {
                self._chart_options[0]: self._visualizer.plot_content_type_pie,
                self._chart_options[1]: self._visualizer.plot_top_countries_bar,
                self._chart_options[2]: self._visualizer.plot_yearly_trend_line,
                self._chart_options[3]: self._visualizer.plot_rating_bar,
                self._chart_options[4]: self._visualizer.plot_genre_bar,
                self._chart_options[5]: self._visualizer.plot_release_year_histogram,
                self._chart_options[6]: self._visualizer.plot_country_genre_heatmap,
            }
            fig = mapping[sel]()

            self._clear_content()
            title_text = sel.split("  ", 1)[-1]
            self._set_page_title(title_text)

            tk.Label(self._content, text=title_text,
                     bg=BG_DARK, fg=TEXT_WHITE,
                     font=(F_DISPLAY, 20, "bold")).pack(anchor="w", pady=(0, 10))

            self.chart_canvas = FigureCanvasTkAgg(fig, master=self._content)
            widget = self.chart_canvas.get_tk_widget()
            widget.configure(bg=BG_DARK, highlightthickness=0)
            widget.pack(fill="both", expand=True)
            self.chart_canvas.draw()

        except Exception as e:
            messagebox.showerror("Chart Error", f"Could not render chart:\n{e}")

    def _show_statistics(self):
        """Display stats in a bold text card."""
        try:
            self._clear_content()
            self._set_page_title("Statistics")

            tk.Label(self._content, text="Statistics",
                     bg=BG_DARK, fg=TEXT_WHITE,
                     font=(F_DISPLAY, 22, "bold")).pack(anchor="w", pady=(0, 14))

            frame = ctk.CTkScrollableFrame(self._content, fg_color=BG_DARK)
            frame.pack(fill="both", expand=True)

            full_text = (
                self._analyzer.get_basic_stats() + "\n"
                + self._analyzer.get_duration_stats() + "\n"
                + "--- Top 5 Countries ---\n"
                + "\n".join(f"  {k}: {v}" for k, v in self._analyzer.get_top_countries(5).items())
                + "\n\n--- Top 5 Genres ---\n"
                + "\n".join(f"  {k}: {v}" for k, v in self._analyzer.get_genre_counts(5).items())
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
        """Display first 50 rows in a dark styled Treeview."""
        try:
            self._clear_content()
            self._set_page_title("Raw Data")

            tk.Label(self._content, text="Raw Data  (first 50 rows)",
                     bg=BG_DARK, fg=TEXT_WHITE,
                     font=(F_DISPLAY, 22, "bold")).pack(anchor="w", pady=(0, 12))

            columns = ['type', 'title', 'director', 'country',
                       'release_year', 'rating', 'primary_genre', 'year_added']
            display = self._clean_df[columns].head(50)

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

            ys = ttk.Scrollbar(wrap, orient="vertical")
            ys.pack(side="right", fill="y")
            xs = ttk.Scrollbar(wrap, orient="horizontal")
            xs.pack(side="bottom", fill="x")

            tree = ttk.Treeview(wrap, columns=columns, show="headings",
                                style="Dark.Treeview",
                                yscrollcommand=ys.set, xscrollcommand=xs.set)
            ys.config(command=tree.yview)
            xs.config(command=tree.xview)

            for col in columns:
                tree.heading(col, text=col.replace("_", " ").title())
                tree.column(col, width=140, minwidth=100)

            tree.pack(side="left", fill="both", expand=True)

            rows = [list(r) for _, r in display.iterrows()]
            self._insert_rows_animated(tree, rows, 0)

        except Exception as e:
            messagebox.showerror("Raw Data Error", f"Could not display data:\n{e}")

    def _insert_rows_animated(self, tree, rows, index):
        """Insert Treeview rows one by one for a smooth appearance."""
        if index < len(rows):
            tree.insert("", "end", values=[str(x) for x in rows[index]])
            self.root.after(16, self._insert_rows_animated, tree, rows, index + 1)

    def _export_csv(self):
        """Save the cleaned DataFrame to a user-chosen CSV path."""
        try:
            path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")]
            )
            if path:
                self._clean_df.to_csv(path, index=False, encoding="utf-8-sig")
                messagebox.showinfo("Exported ✅", f"File saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not save:\n{e}")
