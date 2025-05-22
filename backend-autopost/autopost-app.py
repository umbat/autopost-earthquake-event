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
from imagekitio import ImageKit

# Load environment variables
load_dotenv()

# Facebook Config
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")

# Twitter (X) Config
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET_KEY")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

# Instagram Business Config
IG_USER_ID = os.getenv("IG_USER_ID")
IG_TOKEN = os.getenv("IG_ACCESS_TOKEN")

# ImageKit Config
IK_PUBLIC_KEY = os.getenv("IMAGEKIT_PUBLIC_KEY")
IK_PRIVATE_KEY = os.getenv("IMAGEKIT_PRIVATE_KEY")
IK_URL_ENDPOINT = os.getenv("IMAGEKIT_URL_ENDPOINT")
imagekit = ImageKit(private_key=IK_PRIVATE_KEY, public_key=IK_PUBLIC_KEY, url_endpoint=IK_URL_ENDPOINT)

# Helper Functions

def compress_image(image_path, output_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    img.save(output_path, 'JPEG', optimize=True, quality=85)
    
def upload_to_imagekit(image_path):
    imagekit = ImageKit(
        public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
        private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
        url_endpoint=os.getenv("IMAGEKIT_URL_ENDPOINT")
    )

    with open(image_path, "rb") as file:
        upload_response = imagekit.upload_file(
            file=file,
            file_name=os.path.basename(image_path),
            options={"is_private_file": False}
        )

    if upload_response and hasattr(upload_response, 'url') and upload_response.url:
        return upload_response.url
    else:
        raise Exception(f"ImageKit upload failed: {vars(upload_response)}")

def post_to_facebook(image_path, caption):
    with open(image_path, 'rb') as img:
        files = {'source': img}
        payload = {'caption': caption, 'access_token': FB_TOKEN}
        url = f"https://graph.facebook.com/v18.0/{FB_PAGE_ID}/photos"
        r = requests.post(url, data=payload, files=files)
        r.raise_for_status()


def upload_image_to_x(image_path):
    auth = OAuth1(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET)
    with open(image_path, 'rb') as file:
        r = requests.post('https://upload.twitter.com/1.1/media/upload.json', auth=auth, files={'media': file})
        r.raise_for_status()
    return r.json()['media_id_string']

def post_tweet(caption, media_id):
    auth = OAuth1(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET)
    payload = {"text": caption, "media": {"media_ids": [media_id]}}
    r = requests.post('https://api.twitter.com/2/tweets', auth=auth, json=payload)
    r.raise_for_status()


def post_to_instagram(image_url, caption):
    container_url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media"
    publish_url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media_publish"

    container_payload = {
        'image_url': image_url,
        'caption': caption,
        'access_token': IG_TOKEN
    }
    container_res = requests.post(container_url, data=container_payload)
    container_res.raise_for_status()

    container_id = container_res.json()['id']

    publish_payload = {
        'creation_id': container_id,
        'access_token': IG_TOKEN
    }
    publish_res = requests.post(publish_url, data=publish_payload)
    publish_res.raise_for_status()

# GUI Class
class SocialPosterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Earthquake Auto Poster 🌎 (Final Version)")
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

        self.post_button = ttk.Button(root, text="Post to All Platforms 🚀", command=self.start_posting)
        self.post_button.pack(pady=20)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)
        self.progress["maximum"] = 3

        self.status_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.status_label.pack(pady=10)

    def select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
        if path:
            self.image_path = path
            img = Image.open(path)
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

        threading.Thread(target=self.post_all, args=(caption,)).start()

    def post_all(self, caption):
        errors = []
        compressed_path = "temp_compressed.jpg"
        compress_image(self.image_path, compressed_path)

        try:
            imagekit_url = upload_to_imagekit(compressed_path)
        except Exception as e:
            errors.append(f"ImageKit: {e}")
            imagekit_url = None

        def post_facebook():
            try:
                post_to_facebook(self.image_path, caption)
            except Exception as e:
                errors.append(f"Facebook: {e}")
            self.root.after(0, self.update_progress)

        def post_x():
            try:
                media_id = upload_image_to_x(compressed_path)
                post_tweet(caption, media_id)
            except Exception as e:
                errors.append(f"X: {e}")
            self.root.after(0, self.update_progress)

        def post_instagram():
            try:
                if imagekit_url:
                    post_to_instagram(imagekit_url, caption)
            except Exception as e:
                errors.append(f"Instagram: {e}")
            self.root.after(0, self.update_progress)

        for func in [post_facebook, post_x, post_instagram]:
            threading.Thread(target=func).start()

        while self.progress["value"] < 3:
            time.sleep(0.1)

        os.remove(compressed_path)
        self.root.after(0, self.finish_posting, errors)

    def update_progress(self):
        self.progress["value"] += 1

    def finish_posting(self, errors):
        self.post_button.config(state="normal")
        if errors:
            messagebox.showerror("Post Result", "Errors:\n" + "\n".join(errors))
        else:
            messagebox.showinfo("Success", "✅ Successfully posted to all platforms!")
        self.status_label.config(text="Done.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SocialPosterApp(root)
    root.mainloop()
