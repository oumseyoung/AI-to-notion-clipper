# AI-to-Notion Clipper

Save AI conversations from ChatGPT, Claude, and Gemini to Notion instantly with a single shortcut.

macOS automation tool for clipping AI conversations directly into Notion without copy-paste.

macOS only.

---

# ✨ Why This Tool?

When working with AI tools, useful insights often get buried in long conversations.  
Manually copying and organizing them into Notion is repetitive and time-consuming.

**AI-to-Notion Clipper automates this workflow.**

Press a shortcut → The conversation is parsed → Sent to Notion automatically.

---

# 🚀 Features

### ⚡ One-Shortcut Clipping
Save the current AI conversation to Notion instantly using a macOS shortcut.

### 🤖 AI Conversation Parsing
Automatically extracts visible text from ChatGPT, Claude, Gemini, and formats it for Notion.

### 🧩 GUI Setup Wizard
Includes a native **macOS Setup.app** that automatically:

- creates Python virtual environment
- installs dependencies
- configures environment variables

No terminal knowledge required.

### 📦 Dynamic Script Path Detection
Even if the project folder is moved, the script automatically detects the correct path and runs properly.

---

# 🛠 Requirements

Before installation, prepare the following:

### 1. Notion API Token
Create a private integration at:

https://www.notion.so/my-integrations

Example format:

```
ntn_xxxxxxxxxxxxxxxxx
```

### 2. Notion Page ID

The **32-character ID** at the end of the target Notion page URL.

Example:

```
https://www.notion.so/workspace/AI-Clips-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Important:

You must **share the Notion page with the integration**  
via **"Add Connections"** in the page menu.

---

# ⚡ Quick Start

### 1. Download Installer

Go to **Releases** and download:

```
Setup.app.zip
```

Unzip the file.

---

### 2. Run Setup

Double click:

```
Setup.app
```
---

### 3. Enter Notion Credentials

The installer will ask for:

- Notion API Token
- Notion Page ID

The setup will automatically configure the environment.

---

### 4. Install Shortcut

A browser window will open automatically.

Click:

```
Add Shortcut
```

to install the macOS automation shortcut.

---

# 🧠 Usage

1. Open ChatGPT / Claude / Gemini / etc.
2. Navigate to the conversation you want to save
3. Run the macOS shortcut

The conversation will be automatically added to your **Notion page** as text blocks.

---

# 🧯 Troubleshooting

### Shortcut does not run

Open **macOS Shortcuts** and verify permissions:

- screen reading access
- script execution permission

---

### Data not appearing in Notion

Check that your Notion page has been shared with the **integration**.

```
Page Menu → Add Connections → Select your Integration
```

---

# 📌 Tech Stack

- Python
- Notion API
- AppleScript
- macOS Shortcuts
- Python Virtual Environment (venv)

---

# 📄 License

MIT License

---

# 👋 Author

Built by **[Seyoung Oum](https://github.com/oumseyoung)**
