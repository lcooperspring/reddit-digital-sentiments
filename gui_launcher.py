import tkinter as tk
from tkinter import messagebox
import sys
import threading
from data_collector import collect_reddit_data
from plot_sentiments import plot_sentiment_analysis

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)

    def flush(self):
        pass

def start_analysis(log_widget):
    print("Starting data collection...\n")
    posts_df, comments_df = collect_reddit_data()

    if posts_df.empty and comments_df.empty:
        print("⚠️ No posts or comments found.")
        messagebox.showwarning("No Data", "No posts or comments were found.")
    else:
        print("\nGenerating plots...")
        plot_sentiment_analysis(posts_df, comments_df)

def on_start_threaded(log_widget):
    analysis_thread = threading.Thread(target=start_analysis, args=(log_widget,))
    analysis_thread.start()

def show_main_window():
    window = tk.Tk()
    window.title("Reddit Sentiment Analysis")
    window.geometry("700x600")

    label = tk.Label(window, text="Subreddits to analyze:\nmentalhealth, anxiety, depression, stress, etc.",
                     wraplength=600, justify="center", font=("Arial", 12))
    label.pack(pady=10)

    start_button = tk.Button(window, text="Start Analysis", font=("Arial", 14), bg="green", fg="white")
    start_button.pack(pady=10)

    log_label = tk.Label(window, text="System Logs:", font=("Arial", 11))
    log_label.pack(pady=(10, 0))

    log_text = tk.Text(window, height=20, width=80, bg="#f4f4f4", font=("Courier", 9))
    log_text.pack(padx=10, pady=5)

    sys.stdout = TextRedirector(log_text)
    sys.stderr = TextRedirector(log_text)

    start_button.config(command=lambda: on_start_threaded(log_text))

    window.mainloop()
