# Re-running the enhanced lyrics extractor & analyzer UI after kernel reset

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from lyrics_extractor import SongLyrics
from textblob import TextBlob
from fpdf import FPDF
import webbrowser
from langdetect import detect

# API credentials (placeholders, replace with your own)
API_KEY = "AIzaSyAcZ6KgA7pCIa_uf8-bYdWR85vx6-dWqDg"
ENGINE_ID = "aa2313d6c88d1bf22"

# Sample suggestions
suggestions = {
    "happy": ["Happy - Pharrell Williams", "Can't Stop the Feeling - Justin Timberlake", "Best Day of My Life - American Authors"],
    "neutral": ["Let It Be - The Beatles", "Boulevard of Broken Dreams - Green Day", "Yellow - Coldplay"],
    "sad": ["Someone Like You - Adele", "Fix You - Coldplay", "Hurt - Johnny Cash"]
}

# GUI setup
window = tk.Tk()
window.title("🎶 AI Lyrics Extractor & Analyzer")
window.geometry("850x900")
window.configure(bg="#2c3e50")

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', background='#1abc9c', foreground='white', font=('Helvetica', 12, 'bold'), padding=10)
style.map('TButton', background=[('active', '#16a085')])

tk.Label(window, text="AI-Based Lyrics Extractor 🎤", font=('Helvetica', 24, 'bold'), bg='#2c3e50', fg='white').pack(pady=10)
frame = ttk.Frame(window, padding=20)
frame.pack(pady=10)

tk.Label(frame, text="Enter Song Name:", font=('Helvetica', 16, 'bold'), background='#2c3e50', foreground='white').pack(pady=10)
song_var = tk.StringVar()
entry = ttk.Entry(frame, textvariable=song_var, font=('Helvetica', 14), width=40)
entry.pack(pady=10)

lyrics_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=('Helvetica', 12), bg='#ecf0f1', fg='#2c3e50', width=85, height=20)
lyrics_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

mood_output = tk.Label(window, text="", font=('Helvetica', 14), bg='#2c3e50', fg='white')
mood_output.pack(pady=10)

suggestion_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=('Helvetica', 11), bg='#f0f8ff', fg='#2c3e50', width=85, height=5, state='disabled')
suggestion_box.pack(padx=20, pady=10)

def get_lyrics():
    song_name = song_var.get().strip()
    if not song_name:
        messagebox.showwarning("Input Error", "Please enter a song name.")
        return
    try:
        extractor = SongLyrics(API_KEY, ENGINE_ID)
        result = extractor.get_lyrics(song_name)
        lyrics = result.get("lyrics", "Lyrics not found.")
        lyrics_text.delete(1.0, tk.END)
        lyrics_text.insert(tk.END, lyrics)
        mood_output.config(text="")
        suggestion_box.config(state='normal')
        suggestion_box.delete(1.0, tk.END)
        suggestion_box.config(state='disabled')
    except Exception as e:
        lyrics_text.delete(1.0, tk.END)
        lyrics_text.insert(tk.END, f"Error occurred: {str(e)}")

def analyze_lyrics():
    lyrics = lyrics_text.get(1.0, tk.END).strip()
    if lyrics:
        analysis = TextBlob(lyrics)
        polarity = analysis.sentiment.polarity
        if polarity > 0.1:
            mood, key = "😊 Happy", "happy"
        elif polarity < -0.1:
            mood, key = "💔 Sad", "sad"
        else:
            mood, key = "😐 Neutral", "neutral"
        mood_output.config(text=f"Mood Detected: {mood} (Polarity Score: {polarity:.2f})")
        suggestion_box.config(state='normal')
        suggestion_box.delete(1.0, tk.END)
        suggestion_box.insert(tk.END, "🎧 Recommended Songs:\n\n")
        for song in suggestions[key]:
            suggestion_box.insert(tk.END, f"• {song}\n")
        suggestion_box.config(state='disabled')
    else:
        messagebox.showwarning("No Lyrics", "No lyrics to analyze.")

def save_lyrics():
    lyrics = lyrics_text.get(1.0, tk.END).strip()
    if lyrics:
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(lyrics)
            messagebox.showinfo("Saved", f"Lyrics saved to {filepath}")

def save_as_pdf():
    lyrics = lyrics_text.get(1.0, tk.END).strip()
    if lyrics:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in lyrics.split('\n'):
            pdf.cell(200, 10, txt=line, ln=True)
        filepath = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if filepath:
            pdf.output(filepath)
            messagebox.showinfo("Saved", f"PDF saved to {filepath}")

def open_in_browser():
    song_name = song_var.get().strip()
    if song_name:
        webbrowser.open(f"https://www.google.com/search?q={song_name.replace(' ', '+')}+lyrics")

def clear_all():
    entry.delete(0, tk.END)
    lyrics_text.delete(1.0, tk.END)
    mood_output.config(text="")
    suggestion_box.config(state='normal')
    suggestion_box.delete(1.0, tk.END)
    suggestion_box.config(state='disabled')

def about_project():
    messagebox.showinfo("About", "🎶 Python Mini Project - AI-Based Lyrics Extractor & Analyzer\n👨‍💻 Developer: MSH\n🔧 Tools: Python, Tkinter, TextBlob, Lyrics Extractor API\n📁 Features: Lyrics fetch, Mood analysis, Similar song suggestions, PDF export")

button_frame = ttk.Frame(window)
button_frame.pack(pady=10)
ttk.Button(button_frame, text="Get Lyrics", command=get_lyrics).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="Analyze Mood", command=analyze_lyrics).grid(row=0, column=1, padx=10)
ttk.Button(button_frame, text="Save as TXT", command=save_lyrics).grid(row=0, column=2, padx=10)
ttk.Button(button_frame, text="Save as PDF", command=save_as_pdf).grid(row=0, column=3, padx=10)
ttk.Button(button_frame, text="Search in Browser", command=open_in_browser).grid(row=0, column=4, padx=10)
ttk.Button(button_frame, text="Clear", command=clear_all).grid(row=1, column=1, pady=10)
ttk.Button(button_frame, text="About Project", command=about_project).grid(row=1, column=2, pady=10)

tk.Label(window, text="© 2025 Anurag University | MSH", font=('Helvetica', 10), bg='#2c3e50', fg='white').pack(side=tk.BOTTOM, pady=10)
window.mainloop()


def suggest_dynamic_songs(lyrics):
    # Analyze mood
    analysis = TextBlob(lyrics)
    polarity = analysis.sentiment.polarity
    mood = "happy" if polarity > 0.1 else "sad" if polarity < -0.1 else "neutral"

    # Detect language
    try:
        language_code = detect(lyrics)
    except Exception:
        language_code = "en"

    # Map language code to readable language name
    language_map = {
        "en": "English",
        "hi": "Hindi",
        "ta": "Tamil",
        "te": "Telugu",
        "bn": "Bengali",
        "kn": "Kannada",
        "ml": "Malayalam",
        "mr": "Marathi",
        "gu": "Gujarati",
        "pa": "Punjabi"
    }
    language = language_map.get(language_code, "English")

    # Create YouTube search query
    query = f"top {language} {mood} songs"
    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"

    # Open the suggestions in browser
    webbrowser.open(search_url)

    suggest_dynamic_songs(SongLyrics['lyrics'])
