import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import qrcode  # Import qrcode library for generating QR code
from PIL import Image, ImageDraw, ImageFont  # Import libraries for image manipulation
import textwrap
import re

load_dotenv()

# Replace with client id and client secret (import from dotenv)
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def generate_spotify_qr(text, fill_color, back_color):
    """Generates a QR code for the provided Spotify link with specified colors."""
    qr = qrcode.QRCode(
        version=1,  # Adjust version for larger QR code (optional)
        error_correction=qrcode.constants.ERROR_CORRECT_L,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)  # Default colors
    return img

# Function to handle text wrapping
def draw_wrapped_text(draw, text, x, y, max_width, font_path, font_size, fill_color):
    words = text.split()
    current_line = ""
    for word in words:
        line_width = draw.textlength(current_line + " " + word, font=ImageFont.truetype(font_path, font_size))
        if line_width <= max_width:
            current_line += " " + word
        else:
            draw.text((x, y), current_line, font=ImageFont.truetype(font_path, font_size), fill=fill_color)
            y += font_size + 10  # Adjust spacing between lines
            current_line = word
    if current_line:
        draw.text((x, y), current_line, font=ImageFont.truetype(font_path, font_size), fill=fill_color)

# Authentication - use to authenticate without user
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Playlist link and URI to retrieve playlist and loop through songs
playlist_link = "https://open.spotify.com/playlist/1C5fSB8nHRnHzb1BzOJWLs?si=03b140bbc18e4faf"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]

# Create a folder to store the generated images
output_folder = "images_output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define background colors, title colors, artist colors, and QR colors for each batch
background_colors = ["#BDE6FF", "#E2BDFF", "#BDFFC4", "#FFC5BD", "#FFF59E"]
title_colors = ["#206B98", "#4D1D9B", "#2B8614", "#8E1515", "#D3A11F"]
artist_colors = ["#206B98", "#4D1D9B", "#2B8614", "#8E1515", "#D3A11F"]
qr_colors = ["#206B98", "#4D1D9B", "#2B8614", "#8E1515", "#D3A11F"]

# Loop to go through each song in the defined playlist
for track_index, track in enumerate(sp.playlist_tracks(playlist_URI)["items"]):
    # Determine the batch number based on the track index
    batch_number = track_index // 20  # Each batch contains 20 images

    # Background color for the current batch
    background_color = background_colors[min(batch_number, len(background_colors) - 1)]
    # Title color for the current batch
    title_color = title_colors[min(batch_number, len(title_colors) - 1)]
    # Artist color for the current batch
    artist_color = artist_colors[min(batch_number, len(artist_colors) - 1)]
    # QR color for the current batch
    qr_color = qr_colors[min(batch_number, len(qr_colors) - 1)]

    # Track information
    track_uri = track["track"]["uri"]
    track_name = track["track"]["name"]
    # Remove specified substring from the title
    track_name = re.sub(r'\(Orchestral Version\) \[Live at Abbey Road\]', '', track_name).strip()
    # Remove everything after the hyphen in the title
    track_name = track_name.split(' - ')[0].strip()
    # Remove unwanted parts from title
    track_name = re.sub(r'\bOriginal Single Version\b|\bRemaster\b|\bVersion\b|\bPts\. 1-5\b|\bSingle Version\b|\[Live at Abbey Road\]\b|\b- ed \d+\b|\bed \d+\b|\bed\b|\b\d{4}\b', '', track_name).strip()

    # Artist information
    artist_name = track["track"]["artists"][0]["name"]
    # Move artist name to next line if it's too long
    artist_lines = textwrap.wrap(artist_name, width=17)

    # Release year
    release_date = track["track"]["album"]["release_date"][:4]  # Only extract the year from the release information

    # Combine information for QR code
    info_to_encode = f"Track: {track_name}\nArtist: {artist_name}\nYear: {release_date}\nListen on Spotify: {track_uri}"

    # Generate QR code
    qr_img = generate_spotify_qr(track_uri, fill_color=qr_color, back_color=background_color)

    # Additional code for adding title, artist, year to card
    font_path = "./openSans.ttf"  # Replace with the path to your desired font file
    font_size = 35  # Adjust font size as needed

    # Create a new image for the card with the background color
    card_width = 400  # Increased width
    card_height = 800  # Increased height
    card_img = Image.new('RGB', (card_width, card_height), color=background_color)
    draw = ImageDraw.Draw(card_img)

    # Draw text on the card
    text_x = 40  # Adjust text position horizontally, moved one space to the left
    text_y = 50  # Adjust text position vertically, increased for moving text down

    # Draw title with wrapping
    draw_wrapped_text(draw, track_name, text_x - 10, text_y, card_width - text_x - 20, font_path, font_size, title_color)  # Subtract margins

    # Adjust y position if title takes two lines
    title_lines = textwrap.wrap(track_name, width=17)
    if len(title_lines) > 1:
        text_y += (len(title_lines) - 1) * (font_size + 10)

    # Draw artist
    artist_y = text_y + font_size + 20
    for line in artist_lines:
        draw.text((text_x, artist_y), line, font=ImageFont.truetype(font_path, font_size), fill=artist_color)
        artist_y += font_size + 10

    # Draw year with slight adjustment down
    year_y = artist_y + 5
    draw.text((text_x, year_y), f"{release_date}", font=ImageFont.truetype(font_path, font_size), fill=artist_color)

    # Calculate position for QR code placement
    qr_x = 20  # Adjust the value to move the QR code to the left
    qr_y = (card_height - qr_img.height) // 2 + 200  # Keep QR code position unchanged

    # Paste QR code onto card image
    card_img.paste(qr_img, (qr_x, qr_y))

    # Create unique filename for each combined image
    combined_filename = os.path.join(output_folder, f"{track_index}_{track_name}_card.png")  # Example filename format

    # Save the combined image with unique filename
    card_img.save(combined_filename)

print('QR codes generated successfully and stored in the folder:', output_folder)
