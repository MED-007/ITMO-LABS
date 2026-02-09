import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO


def fetch_fox():
    try:
        # Get JSON from API
        response = requests.get("https://randomfox.ca/floof/")
        data = response.json()
        img_url = data['image']

        # Download the image
        img_response = requests.get(img_url)
        img_data = Image.open(BytesIO(img_response.content))

        # Resize image to fit window
        img_data = img_data.resize((400,400))

        # Convert to Tkinter image
        photo = ImageTk.PhotoImage(img_data)

        # Update label with new image
        label.config(image=photo)
        label.image = photo  # Keep reference to avoid garbage collection

    except Exception as e:
        print("Error fetching fox image:",e)




# Tkinter GUI setup
root = tk.Tk()
root.title("Random Fox Generator")

# Label for the image
label = tk.Label(root)
label.pack(pady=10)

# Button to fetch next fox
btn = tk.Button(root, text="Next Fox", command=fetch_fox)
btn.pack(pady=10)

# Fetch the first fox on startup
fetch_fox()

# Run the GUI loop
root.mainloop()
