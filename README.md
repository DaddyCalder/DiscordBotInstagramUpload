### 📸 Discord to Instagram Auto Uploader Bot

This bot monitors a designated Discord channel for video uploads, queues them for review, and posts them to Instagram after receiving moderator approval via reactions.

---

### ⚙️ Features

- Detects video attachments in a target channel
- Sends a notification message for approval with ✅ / ❌ reactions
- Uploads approved videos directly to Instagram
- Deletes temporary files after processing
- Uses `instagrapi` for reliable Instagram uploads

---

### 🚀 Getting Started

#### 🧱 Requirements

- Python 3.8+
- A Discord bot with **Message Content Intent** enabled
- An Instagram account (preferably a business/test account)

---

### 🔐 Environment Variables

Create a `.env` file in the project directory with the following keys:

```
DISCORD_TOKEN=your_discord_bot_token
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
TARGET_CHANNEL_ID=your_video_channel
NOTIFICATION_CHANNEL_ID=your_admin_channel
```

| Key | Description |
|-----|-------------|
| `DISCORD_TOKEN` | Your Discord bot token |
| `INSTAGRAM_USERNAME` / `INSTAGRAM_PASSWORD` | Instagram credentials for the uploader |
| `TARGET_CHANNEL_ID` | Discord channel to monitor for video uploads |
| `NOTIFICATION_CHANNEL_ID` | Channel where approvals are requested |

---

### 📂 Installation

1. Clone the repo
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set your `.env` file as explained above.

5. Run the bot:
   ```bash
   python contentbro.py
   ```

---

### 📦 Dependencies

- `discord.py`
- `instagrapi`
- `moviepy`
- `python-dotenv`

Install them all with:

```bash
pip install discord.py instagrapi moviepy python-dotenv
```

---

### ✅ How it Works

1. A user uploads a video in `TARGET_CHANNEL_ID`.
2. The bot saves the video and sends a message in `NOTIFICATION_CHANNEL_ID` with a link to the original message.
3. Moderators react with:
   - ✅ to approve and post to Instagram.
   - ❌ to deny and skip the video.
4. The bot handles cleanup and continues processing the next item in the queue.

---

### 🔐 Notes

- **Instagram may limit certain accounts** from posting videos via third-party tools—use at your own risk.
- Avoid storing real credentials in plaintext or public repos.
- Make sure the `Message Content Intent` is enabled for your bot [in the developer portal](https://discord.com/developers/applications).

---

### 👥 Contributing

Pull requests are welcome. Feel free to open issues for bugs or feature requests.
