import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import requests
import tweepy
from dotenv import load_dotenv

load_dotenv()

# === Load API credentials ===
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_TOKEN = os.getenv("FB_ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")
IG_TOKEN = os.getenv("IG_ACCESS_TOKEN")
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.getenv("X_ACCESS_SECRET")
IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")

# === Upload image to Imgur ===
def upload_to_imgur(image_path, client_id):
    headers = {'Authorization': f'Client-ID {client_id}'}
    with open(image_path, 'rb') as img:
        response = requests.post("https://api.imgur.com/3/upload", headers=headers, files={"image": img})
    return response.json()["data"]["link"]

# === Facebook image post ===
def post_image_to_facebook(image_path, message):
    url = f"https://graph.facebook.com/{FB_PAGE_ID}/photos"
    with open(image_path, 'rb') as img:
        files = {'source': img}
        payload = {'caption': message, 'access_token': FB_TOKEN}
        response = requests.post(url, data=payload, files=files)
    return response.json()

# === Instagram post (via hosted image URL) ===
def post_to_instagram(image_url, caption):
    create_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    publish_url = "https://graph.facebook.com/v19.0/{}/"

    media_res = requests.post(create_url, data={
        "image_url": image_url,
        "caption": caption,
        "access_token": IG_TOKEN
    })
    creation_id = media_res.json().get("id")
    if not creation_id:
        return media_res.json()

    publish_res = requests.post(publish_url.format(creation_id), data={"access_token": IG_TOKEN})
    return publish_res.json()

# === X (Twitter) post ===
def post_image_to_x(image_path, message):
    auth = tweepy.OAuth1UserHandler(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET)
    api = tweepy.API(auth)
    media = api.media_upload(image_path)
    tweet = api.update_status(status=message, media_ids=[media.media_id])
    return tweet.id

# === GUI App ===
class SocialPosterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Earthquake Auto Poster")
        self.root.geometry("500x600")

        self.image_path = ""

        self.text_label = tk.Label(root, text="Enter Caption/Text:")
        self.text_label.pack()

        self.text_input = tk.Text(root, height=5)
        self.text_input.pack(pady=5)

        self.image_button = tk.Button(root, text="Choose Image", command=self.select_image)
        self.image_button.pack()

        self.image_preview = tk.Label(root)
        self.image_preview.pack(pady=5)

        self.post_button = tk.Button(root, text="Post to All Platforms", command=self.post_to_all)
        self.post_button.pack(pady=10)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.image_path = file_path
            img = Image.open(file_path)
            img.thumbnail((400, 400))
            img = ImageTk.PhotoImage(img)
            self.image_preview.configure(image=img)
            self.image_preview.image = img

    def post_to_all(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image")
            return
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Please enter a caption")
            return

        try:
            # Upload image to Imgur
            image_url = upload_to_imgur(self.image_path, IMGUR_CLIENT_ID)

            # Post to Facebook
            fb_res = post_image_to_facebook(self.image_path, text)

            # Post to Instagram
            insta_res = post_to_instagram(image_url, text)

            # Post to X
            x_res = post_image_to_x(self.image_path, text)

            messagebox.showinfo("Success", "Posted successfully to all platforms!")
        except Exception as e:
            messagebox.showerror("Post Failed", str(e))


if __name__ == '__main__':
    root = tk.Tk()
    app = SocialPosterApp(root)
    root.mainloop()
