import customtkinter as ctk
from tkinter import messagebox
import threading
import time
import fake_news_model  


ctk.set_appearance_mode("light")   
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("🌟 Fake News Detector - Chat UI")
app.geometry("900x700")
app.resizable(False, False)


header = ctk.CTkFrame(app, fg_color="#e6f2ff", corner_radius=0)
header.pack(fill="x")
title = ctk.CTkLabel(header, text="🧠 Fake News Detection Chat", font=ctk.CTkFont(size=22, weight="bold"), text_color="#173f5f")
title.pack(padx=20, pady=14, anchor="w")

subtitle = ctk.CTkLabel(header, text="Type a headline/article and press Analyze (or Enter). Type 'exit'/'bye' to close.", 
                        font=ctk.CTkFont(size=11), text_color="#3a5a72")
subtitle.pack(padx=20, pady=(0,12), anchor="w")


chat_frame = ctk.CTkFrame(app, fg_color="#f8fafc", corner_radius=12)
chat_frame.pack(padx=20, pady=(10,5), fill="both", expand=False)

# Scrollable area for bubbles
scrollable = ctk.CTkScrollableFrame(chat_frame, width=840, height=360, fg_color="#f8fafc", corner_radius=10)
scrollable.pack(padx=10, pady=10)

# helper to add chat bubbles
def add_bubble(text, sender="bot", color=None):
    bubble_frame = ctk.CTkFrame(scrollable, fg_color="#f8fafc", corner_radius=8)
    bubble_frame.pack(fill="x", pady=6, padx=8)

    if sender == "user":
        inner = ctk.CTkLabel(bubble_frame, text=text, width=520, wraplength=520, 
                             corner_radius=12, anchor="e",
                             font=ctk.CTkFont(size=12, weight="bold"),
                             fg_color="#d1f0e0", text_color="#045d5d")
        inner.pack(anchor="e", padx=6, pady=4)
    else:
        bg = "#f0f4ff" if color is None else color
        txt_color = "#173f5f" if color is None else "white"
        inner = ctk.CTkLabel(bubble_frame, text=text, width=520, wraplength=520, 
                             corner_radius=12, anchor="w",
                             font=ctk.CTkFont(size=12),
                             fg_color=bg, text_color=txt_color)
        inner.pack(anchor="w", padx=6, pady=4)

    # ---------------- SCROLL TO BOTTOM ----------------
    scrollable.update_idletasks()
    scrollable._scrollbar.set(1.0, 1.0)  # force scrollbar to bottom

    return inner


# ---------------- Input area ----------------
input_frame = ctk.CTkFrame(app, fg_color="#ffffff", corner_radius=12)
input_frame.pack(padx=20, pady=(6,10), fill="x")

input_label = ctk.CTkLabel(input_frame, text="Enter news text:", font=ctk.CTkFont(size=12), text_color="#234e52")
input_label.pack(anchor="w", padx=12, pady=(10,0))

text_box = ctk.CTkTextbox(input_frame, width=760, height=110, corner_radius=8, border_width=1, border_color="#cfe9ff")
text_box.pack(padx=12, pady=(8,10), anchor="center")

# bottom controls: analyze button + progress + mode toggle
controls = ctk.CTkFrame(input_frame, fg_color="#ffffff", corner_radius=8)
controls.pack(fill="x", padx=12, pady=(0,12))

# Confidence progress bar and label
conf_label = ctk.CTkLabel(controls, text="Confidence:", font=ctk.CTkFont(size=11), text_color="#234e52")
conf_label.pack(side="left", padx=(4,8))
confidence_bar = ctk.CTkProgressBar(controls, width=300, height=15, progress_color="#00b894")
confidence_bar.set(0.0)
confidence_bar.pack(side="left", padx=(0,12))

# Analyze button (explicit)
def on_analyze_click(event=None):
    analyze_news()

analyze_btn = ctk.CTkButton(controls, text="🚀 Analyze News", width=180, height=36, 
                            fg_color="#0984e3", hover_color="#0664b0", 
                            command=on_analyze_click)
analyze_btn.pack(side="right", padx=8)

# Light/Dark mode switch for user preference (keeps light by default)
def toggle_mode():
    if mode_switch.get():
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light")

mode_switch = ctk.CTkSwitch(controls, text="Dark Mode", command=toggle_mode)
mode_switch.pack(side="right", padx=12)

# Bind Enter key to analyze (Shift+Enter still allows new lines)
def handle_enter(event):
    if event.state & 0x0001:  # Shift pressed -> insert newline
        return
    on_analyze_click()
    return "break"

text_box.bind("<Return>", handle_enter)

# ---------------- Analysis logic with chat bubble animation ----------------
EXIT_WORDS = {"exit", "bye", "goodbye", "quit", "close"}

def analyze_news():
    raw_text = text_box.get("1.0", "end").strip()
    if not raw_text:
        messagebox.showwarning("Input Missing", "Please enter a news headline or article to analyze.")
        return

    # show user bubble (right-aligned)
    add_bubble(raw_text, sender="user")
    text_box.delete("1.0", "end")

    lower_text = raw_text.strip().lower()
    if lower_text in EXIT_WORDS:
        # friendly message then close
        add_bubble("Goodbye! Thanks for using Fake News Detector. Stay safe and informed. 👋", sender="bot", color="#a6e3a1")
        app.after(1200, lambda: (messagebox.showinfo("Goodbye 👋", "Thank you for using the Fake News Detector!\nStay informed and safe."), app.destroy()))
        return

    # create a typing bubble (bot) that we can update
    typing_label = add_bubble("Bot is typing", sender="bot", color="#051c5a")

    # run model in background thread so UI remains responsive
    def worker():
        # Typing animation: "Bot is typing.", "Bot is typing..", "Bot is typing..."
        for _ in range(3):
            for dots in [".", "..", "..."]:
                try:
                    typing_label.configure(text=f"Bot is typing{dots}")
                except:
                    pass
                time.sleep(0.4)

        # small simulated processing progress update to confidence bar
        for i in range(6):
            confidence_bar.set(i/6.0)
            time.sleep(0.08)

        # call real model (ensure model returns label and float confidence 0..1)
        try:
            prediction, confidence = fake_news_model.predict_fake_news(raw_text)
            # ensure numeric confidence
            if isinstance(confidence, (int, float)):
                confidence_val = float(confidence)
                # sometimes model might return 0..100 scale -> normalize if >1
                if confidence_val > 1:
                    confidence_val = confidence_val / 100.0
                confidence_val = max(0.0, min(1.0, confidence_val))
            else:
                confidence_val = 0.0
        except Exception as e:
            prediction = "Error"
            confidence_val = 0.0
            print("Model error:", e)

        # update confidence bar fully to model value
        confidence_bar.set(confidence_val)

        # create result bubble and replace typing bubble
        if prediction.lower() == "fake":
            color = "#ffd6d6"  # light red
            text_color = "#9b1c1c"
            emoji = "❌"
        elif prediction.lower() == "real":
            color = "#e6ffe6"  # light green
            text_color = "#116530"
            emoji = "✅"
        elif prediction.lower() == "uncertain":
            color = "#fff7d1"  # light yellow
            text_color = "#725b00"
            emoji = "⚠️"
        elif prediction.lower() == "error":
            color = "#ffe6e6"
            text_color = "#9b1c1c"
            emoji = "⚠️"
        else:
            color = "#f0f4ff"
            text_color = "#173f5f"
            emoji = "💡"

        conf_pct = int(confidence_val * 100)
        result_text = f"{emoji} Predicted: {str(prediction).upper()}  —  Confidence: {conf_pct}%"
        try:
            typing_label.configure(text=result_text, fg_color=color, text_color=text_color)
        except:
            pass

        # final small flourish: ensure bar shows confidence
        confidence_bar.set(confidence_val)
        # auto-scroll bottom
        scrollable.yview_moveto(1.0)

    threading.Thread(target=worker, daemon=True).start()

# ---------------- Start with a welcome bot bubble ----------------
add_bubble("Hello! 👋 I'm your Fake News Detector. Paste a headline or article and click Analyze. (Type 'bye' or 'exit' to quit)", sender="bot", color="#f0f8ff")
confidence_bar.set(0.0)

# ---------------- Run app ----------------
app.mainloop()
