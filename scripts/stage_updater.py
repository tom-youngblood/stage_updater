import pandas as pd
import webbrowser
import pyautogui
import time
import tkinter as tk

# Load CSV with LinkedIn URLs
df = pd.read_csv("../data/non_outreached.csv")
df = df[:3] # Testing: first three
df["organic_social_outreached"] = ""
df["outreach_note"] = ""

# Initialize current index
current_index = 0

# Function to open LinkedIn profile (closes previous tab first)
def open_linkedin_profile(url):
    close_browser_tab()
    webbrowser.open(url)

# Function to close the current browser tab
def close_browser_tab():
    pyautogui.hotkey("ctrl", "w")

# Function to handle user decision and move forward
def user_decision(decision, note_entry, root):
    """Stores decision, saves outreach note, and moves to the next profile."""
    global current_index
    df.at[current_index, "organic_social_outreached"] = decision
    df.at[current_index, "outreach_note"] = note_entry.get()  # Save note

    root.destroy()
    current_index += 1
    next_profile()

# Function to go back
def go_back(root):
    """Moves back to the previous profile."""
    global current_index
    if current_index > 0:
        current_index -= 1  # Move back
        root.destroy()
        next_profile()
    else:
        print("Already at the first profile!")

# Function to display UI for decision-making
def show_ui(url):
    global current_index

    # Create UI window
    root = tk.Tk()
    root.title("Outreach Decision")
    root.geometry("400x250+0+0")

    # Header
    first_name = df.iloc[current_index]["firstname"]
    last_name = df.iloc[current_index]["lastname"]
    post_name = df.iloc[current_index]["post_name"]
    label = tk.Label(root, text=f"Outreach to {first_name} {last_name}? (from: {post_name})", font=("Arial", 12))
    label.pack(pady=10)

    # Note entry box
    note_label = tk.Label(root, text="Add a note:")
    note_label.pack()
    note_entry = tk.Entry(root, width=40)
    note_entry.pack(pady=5)

    # Decision buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    yes_button = tk.Button(button_frame, text="Yes", command=lambda: user_decision("Yes", note_entry, root), width=10)
    no_button = tk.Button(button_frame, text="No", command=lambda: user_decision("No", note_entry, root), width=10)

    yes_button.grid(row=0, column=0, padx=5)
    no_button.grid(row=0, column=1, padx=5)

    # Navigation button (Back)
    back_button = tk.Button(root, text="Back", command=lambda: go_back(root), width=10)
    back_button.pack(pady=10)

    root.mainloop()

# Function to iterate through LinkedIn profiles
def next_profile():
    global current_index
    if current_index < len(df):
        url = df.iloc[current_index]["hs_linkedin_url"]
        open_linkedin_profile(url)
        show_ui(url)
    else:
        print("All profiles reviewed!")
        outreach_df = df[["vid", "firstname", "lastname", "organic_social_outreached", "outreach_note"]]
        outreach_df.to_csv("../data/linkedin_outreach_results.csv", index=False)

# Start Process
next_profile()
