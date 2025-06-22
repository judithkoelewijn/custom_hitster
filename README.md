Hitster Card Generator

This project generates custom cards for the game Hitster, where each card contains:

The song title

The artist

The release year

A QR code linking directly to the song on Spotify

The songs are pulled from a public Spotify playlist using the Spotify Web API.

🔧 Setup Instructions

Please create a folder named images_output in the main project directory. This is where the generated card images will be saved when you run the script.



1. Clone or Download the Repository

Download the project files to your computer.

2. Create a .env File

In the project root, create a file named .env and add your Spotify API credentials.

🔒 Important: .env files are used to store sensitive information like API keys and passwords. This file is automatically hidden by many systems and should never be committed to version control (e.g., GitHub).

SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret

To get these credentials:

Visit the Spotify Developer Dashboard.

Log in with your Spotify account.

Click 'Create an App', give it a name and description.

After creating the app, you will find your Client ID and Client Secret.

Copy those into your .env file as shown above.

3. Install Dependencies

Make sure you have Python installed. Then open a terminal in the project folder (preferably in Visual Studio Code) and run:

pip install -r requirements.txt

This will install all the necessary packages like Spotipy, qrcode, Pillow, etc. I have listed them all in one requirements.txt file so that you can automatically install the correct versions in one go.

▶️ Running the Scripts

Generate Hitster Cards

This will fetch the songs from the hardcoded Spotify playlist and generate styled image cards:

python generate_cards.py

Each card will be saved as a PNG in the images_output folder.

💡 Make sure the playlist link used in the script is valid. To get the correct link, right-click a playlist in Spotify → Share → Copy link to playlist (not the embed code). Then update the playlist_link variable in generate_cards.py.

📝 Customisation

To change the playlist: edit the playlist_link in generate_cards.py

To adjust colours or layout: update the relevant lists and values at the top of generate_cards.py

Double-click the included font file (e.g., openSans.ttf) to install it on your system before running the script. If you prefer to use another font or if the file is missing, update the font_path variable in the script accordingly

📁 Output Example

Each generated card includes:

Title and artist (with auto-wrapping)

Release year

Custom-coloured QR code linking to the track

Cards are styled in batches of 20 with consistent colour themes.

✅ Dependencies

Listed in requirements.txt, including:

spotipy

python-dotenv

qrcode

Pillow

requests

📬 License & Attribution

This project was created by Judith Koelewijn. Feel free to reuse and adapt the code for personal or educational purposes.

If you share or publish any part of this project, please include appropriate credit. For example:

Original project by Judith Koelewijn
https://github.com/[your-repo-link-if-applicable]

No formal license is applied, so all rights are reserved unless stated otherwise. If you wish to use this project commercially or beyond personal use, please get in touch.

