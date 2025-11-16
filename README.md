# 📦 Project Name

> Add Youtube videos to playlist

---

## 📚 Table of Contents

- [📦 Project Name](#-project-name)
  - [📚 Table of Contents](#-table-of-contents)
  - [📝 About](#-about)
  - [✨ Features](#-features)
  - [🚀 Getting Started](#-getting-started)
    - [Prerequisites](#prerequisites)
    - [Source](#source)
    - [Usage](#usage)
- [Run](#run)
    - [Reference](#reference)

---

## 📝 About

> App to add videos of 1 channel to personal playlist.

---

## ✨ Features

- ✅ Access channel Youtube
- ✅ Add videos of that channel to personal playlist
- ✅ Save info of added videos to cache to avoid duplicate 

---

## 🚀 Getting Started

### Prerequisites

- List software dependencies or system requirements here:
  - Python
  - Google cloud (Youtube Data API)

### Source

- *.py: main app
- *.json: data

### Usage

- Access https://console.cloud.google.com/
- Create project
- **APIs & Services → Library,** Enable **YouTube Data API v3**
- Config OAuth consent screen
  - User type: **External**
  - App name
  - Developer contact email
  - Save & Continue
- Add test users (your email)
- **APIs & Services → Credentials**; **Create Credential;** select **OAuth client ID**
  - Application type: **Desktop App**    
- **Download JSON** and rename to **client_secret.json**
- pip install google-api-python-client google-auth google-auth-oauthlib

# Run

- Put json in same place with main.py
- Run **python main.py**
- Enter url of channel, e.g. ***https://www.youtube.com/c/KI%E1%BA%BENTH%E1%BB%A8CTH%C3%9AV%E1%BB%8A***
- Enter ID playlist, e.g. *https://www.youtube.com/playlist?list=**PLnLNse3s5NStQmalyduXAU5W4_9RRAggD***
- Verify on web browser

### Reference

- 