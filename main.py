import tkinter as tk
from tkinter import messagebox
import threading
import sys
from data_collector import collect_reddit_data
from plot_sentiments import plot_sentiment_analysis

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)
        self.widget.config(state=tk.DISABLED)

    def flush(self):
        pass

def start_analysis(log_widget, start_button):
    print("Starting data collection...\n")
    log_widget.config(state=tk.NORMAL)
    log_widget.insert(tk.END, "Starting data collection...\n")
    log_widget.see(tk.END)
    log_widget.config(state=tk.DISABLED)

    posts_df, comments_df = collect_reddit_data()

    if posts_df.empty and comments_df.empty:
        print("⚠️ No posts or comments were found.")
        log_widget.config(state=tk.NORMAL)
        log_widget.insert(tk.END, "⚠️ No posts or comments were found.\n")
        log_widget.see(tk.END)
        log_widget.config(state=tk.DISABLED)
        messagebox.showwarning("No Data", "No posts or comments were found.")
    else:
        print("\nGenerating plots...")
        log_widget.config(state=tk.NORMAL)
        log_widget.insert(tk.END, "Generating plots...\n")
        log_widget.see(tk.END)
        log_widget.config(state=tk.DISABLED)

        plot_sentiment_analysis(posts_df, comments_df)

        print("Analysis completed!")
        log_widget.config(state=tk.NORMAL)
        log_widget.insert(tk.END, "Analysis completed!\n")
        log_widget.see(tk.END)
        log_widget.config(state=tk.DISABLED)

    start_button.config(state=tk.NORMAL)

def on_start_threaded(log_widget, start_button):
    start_button.config(state=tk.DISABLED)
    analysis_thread = threading.Thread(target=start_analysis, args=(log_widget, start_button), daemon=True)
    analysis_thread.start()

def show_main_window():
    window = tk.Tk()
    window.title("Reddit Sentiment Analysis")
    window.attributes('-fullscreen', True)
    window.config(bg="#2E2E2E")

    title_label = tk.Label(window, text="Reddit Sentiment Analysis", font=("Helvetica", 26, "bold"),
                           fg="#FFFFFF", bg="#2E2E2E")
    title_label.pack(pady=20)

    coop_label = tk.Label(window, text="The Cooper Union RPIE", font=("Helvetica", 16, "italic"),
                          fg="#FFD700", bg="#2E2E2E")
    coop_label.pack(pady=5)

    subreddits_label = tk.Label(window, text="Subreddits used for analysis:", font=("Helvetica", 14, "bold"),
                                fg="#FFFFFF", bg="#2E2E2E", anchor="w")
    subreddits_label.pack(fill="x", padx=40, pady=(20, 5))

    subreddits_text = tk.Label(window,
        text="mentalhealth, anxiety, depression, stress, bipolarreddit, CPTSD, schizophrenia",
        font=("Helvetica", 12), fg="#D3D3D3", bg="#2E2E2E", anchor="w", justify="left")
    subreddits_text.pack(fill="x", padx=40)

    log_label = tk.Label(window, text="System logs:", font=("Helvetica", 14, "bold"),
                         fg="#FFFFFF", bg="#2E2E2E", anchor="w")
    log_label.pack(fill="x", padx=40, pady=(25, 5))

    log_text = tk.Text(window, height=20, bg="#f4f4f4", font=("Courier", 10), wrap="word")
    log_text.pack(padx=40, pady=5, fill="both", expand=True)
    log_text.config(state=tk.DISABLED)

    sys.stdout = TextRedirector(log_text)
    sys.stderr = TextRedirector(log_text)

    start_button = tk.Button(window, text="Start Analysis", font=("Helvetica", 16),
                             bg="#4CAF50", fg="white", relief="raised", height=2, width=20,
                             command=lambda: on_start_threaded(log_text, start_button))
    start_button.pack(pady=20)

    close_button = tk.Button(window, text="✕", font=("Helvetica", 14, "bold"), fg="white", bg="#B22222",
                             activebackground="#8B0000", command=window.destroy)
    close_button.place(x=10, y=10, width=40, height=40)

    window.bind("<Escape>", lambda event: window.destroy())

    footer_label = tk.Label(window, text="© 2025 The Cooper Union RPIE - Luis Cunalema",
                            font=("Helvetica", 10), fg="#D3D3D3", bg="#2E2E2E")
    footer_label.pack(side="bottom", pady=10)

    window.mainloop()

if __name__ == "__main__":
    show_main_window()
