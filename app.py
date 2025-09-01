import tkinter as tk
from textblob import TextBlob
import webbrowser
import urllib.parse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="ac1f0f3e5de946f0b480e2eda0395b4a",
    client_secret="741e754d6ee84d038a9b6026f9d3a86e"
))


def get_mood(text):
    analysis=TextBlob(text)
    polarity=analysis.sentiment.polarity
    if polarity > +0.3:
        return "happy"
    elif polarity < -0.3:
        return "sad"
    else:
        return "neutral"

root=tk.Tk()
root.title("Mood-Based Music Recommender")
root.geometry("520x360")

tk.Label(root, text="How are you feeling?", font=("Arial", 14)).pack(pady=(12, 6))
entry=tk.Entry(root,width=52,font=("Arial",11))
entry.pack(pady=(0,8))

button_frame = tk.Frame(root)
button_frame.pack()
result_label =tk.Label(root,text="Detected mood will appear here.",font=("Arial",11))
result_label.pack(pady=(10,6))

list_frame=tk.Frame(root)
list_frame.pack(pady=(6,12))
scrollbar=tk.Scrollbar(list_frame,orient=tk.VERTICAL)
songs_listbox=tk.Listbox(list_frame,width=60,height=8, yscrollcommand=scrollbar.set)
scrollbar.config(command=songs_listbox.yview)
songs_listbox.pack(side=tk.LEFT)
scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

def recommend_music():
    text = entry.get().strip()
    if not text:
        result_label.config(text="Please enter how you feel")
        return

    mood = get_mood(text)
    result_label.config(text=f"Detected mood: {mood.capitalize()}")

    songs_listbox.delete(0, tk.END)

    mood_map = {"happy": "pop", "sad": "acoustic", "neutral": "chill"}

    # Search for tracks instead of recommendations
    results = sp.search(q=mood_map[mood], type="track", limit=5)

    if not results["tracks"]["items"]:
        songs_listbox.insert(tk.END, "⚠️ No songs found, try again.")
        return

    for track in results["tracks"]["items"]:
        song_name = f"{track['name']} - {track['artists'][0]['name']}"
        url = track["external_urls"]["spotify"]
        songs_listbox.insert(tk.END, song_name + " | " + url)


       

def open_selected_song():
    sel=songs_listbox.curselection()
    if not sel:
        return
    song=songs_listbox.get(sel[0])
    if "|" in song:
        url = song.split("|")[-1].strip()
        webbrowser.open(url)

tk.Button(button_frame, text="Recommend", command=recommend_music, width=12).grid(row=0, column=0, padx=6)
tk.Button(button_frame, text="Open Selected", command=open_selected_song, width=12).grid(row=0, column=1, padx=6)

root.mainloop()




