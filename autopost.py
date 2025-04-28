import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
import time

# Load API keys
load_dotenv()
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET_KEY")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

# Facebook Upload
def post_image_to_facebook(image_path, caption, retries=3):
    url = f"https://graph.facebook.com/v18.0/{FB_PAGE_ID}/photos"
    for attempt in range(retries):
        try:
            with open(image_path, 'rb') as img:
                files = {'source': img}
                payload = {'caption': caption, 'access_token': FB_TOKEN}
                response = requests.post(url, data=payload, files=files)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Facebook error {response.status_code}: {response.text}")
        except Exception as e:
            if attempt == retries - 1:
                raise e
            time.sleep(2)  # wait before retry

# Twitter (X) Upload
def upload_image_to_x(image_path, retries=3):
    auth = OAuth1(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET)
    upload_url = 'https://upload.twitter.com/1.1/media/upload.json'
    for attempt in range(retries):
        try:
            with open(image_path, 'rb') as file:
                files = {'media': file}
                response = requests.post(upload_url, auth=auth, files=files)
            if response.status_code == 200:
                return response.json()['media_id_string']
            else:
                raise Exception(f"X upload error {response.status_code}: {response.text}")
        except Exception as e:
            if attempt == retries - 1:
                raise e
            time.sleep(2)

def post_tweet(caption, media_id, retries=3):
    auth = OAuth1(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET)
    url = 'https://api.twitter.com/2/tweets'
    payload = {
        "text": caption,
        "media": {
            "media_ids": [media_id]
        }
    }
    for attempt in range(retries):
        try:
            response = requests.post(url, auth=auth, json=payload)
            if response.status_code in (200, 201):
                return True
            else:
                raise Exception(f"X tweet error {response.status_code}: {response.text}")
        except Exception as e:
            if attempt == retries - 1:
                raise e
            time.sleep(2)

# Compress Image Helper
def compress_image(image_path, output_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    img.save(output_path, 'JPEG', optimize=True, quality=85)

# GUI App
class SocialPosterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Earthquake Auto Poster 🌎 (Next Level)")
        self.root.geometry("600x800")
        self.root.configure(padx=20, pady=20)

        self.image_path = ""

        self.title_label = tk.Label(root, text="AutoPost Earthquake Data", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=10)

        self.text_label = tk.Label(root, text="Caption/Text:", font=("Helvetica", 14))
        self.text_label.pack(anchor="w")

        self.text_input = tk.Text(root, height=6, font=("Helvetica", 12))
        self.text_input.pack(fill="x", pady=5)

        self.image_button = ttk.Button(root, text="Choose Image 📷", command=self.select_image)
        self.image_button.pack(pady=10)

        self.image_preview = tk.Label(root)
        self.image_preview.pack(pady=10)

        self.post_button = ttk.Button(root, text="Post to Facebook and X 🚀", command=self.start_posting)
        self.post_button.pack(pady=20)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)
        self.progress["maximum"] = 2

        self.status_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.status_label.pack(pady=10)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
        if file_path:
            self.image_path = file_path
            img = Image.open(file_path)
            img.thumbnail((400, 400))
            img = ImageTk.PhotoImage(img)
            self.image_preview.configure(image=img)
            self.image_preview.image = img

    def start_posting(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image")
            return
        caption = self.text_input.get("1.0", tk.END).strip()
        if not caption:
            messagebox.showerror("Error", "Please enter a caption")
            return

        self.post_button.config(state="disabled")
        self.progress["value"] = 0
        self.status_label.config(text="Posting...")

        threading.Thread(target=self.post_to_platforms, args=(caption,)).start()

    def post_to_platforms(self, caption):
        errors = []

        compressed_path = "temp_compressed.jpg"
        compress_image(self.image_path, compressed_path)

        threads = []
        results = {"facebook": None, "x": None}

        t1 = threading.Thread(target=self.post_facebook, args=(self.image_path, caption, errors, results))
        t2 = threading.Thread(target=self.post_x, args=(compressed_path, caption, errors, results))

        threads.append(t1)
        threads.append(t2)

        t1.start()
        t2.start()

        for t in threads:
            t.join()

        if os.path.exists(compressed_path):
            os.remove(compressed_path)

        self.root.after(0, self.finish_posting, errors, results)

    def post_facebook(self, image_path, caption, errors, results):
        try:
            post_image_to_facebook(image_path, caption)
            results["facebook"] = "Success"
        except Exception as e:
            errors.append(f"Facebook Error: {e}")
            results["facebook"] = "Failed"
        finally:
            self.root.after(0, self.update_progress)

    def post_x(self, compressed_path, caption, errors, results):
        try:
            media_id = upload_image_to_x(compressed_path)
            post_tweet(caption, media_id)
            results["x"] = "Success"
        except Exception as e:
            errors.append(f"X Error: {e}")
            results["x"] = "Failed"
        finally:
            self.root.after(0, self.update_progress)

    def update_progress(self):
        self.progress["value"] += 1

    def finish_posting(self, errors, results):
        self.post_button.config(state="normal")
        if errors:
            summary = "\n".join(errors)
            messagebox.showerror("Post Result", f"Errors occurred:\n{summary}")
        else:
            messagebox.showinfo("Success", "✅ Successfully posted to Facebook and X!")

        self.status_label.config(text=f"Facebook: {results['facebook']} | X: {results['x']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SocialPosterApp(root)
    root.mainloop()
 