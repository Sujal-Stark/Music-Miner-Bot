# 🎶 Music Miner Bot

A **Song Scraping Bot** is a powerful Python-based application designed to simplify your music search and download experience. With just a few user inputs like **Song Title**, **Singer's Name**, and **Album or Movie name**, the bot filters the best matches across multiple websites and downloads your desired songs seamlessly. 

---

## 🚀 Features

- 🌟 **Effortless Music Search**  
  Input **Song Name**, **Artist**, or **Album**, and let the bot do the rest!  

- 🔍 **Smart Filtering**  
  Filters search results to find the most accurate match for you.

- 🌐 **Multi-Site Scraping**  
  Searches across various websites to ensure you get the best results.

- 📥 **Flexible Download Mechanism**  
  - Uses **HTTP requests** to download when possible.  
  - Falls back on **Selenium automation** when requests are blocked.

- 🎧 **Audio Conversion**  
  - Converts and processes downloaded audio files using **pydub** for an optimal experience.  

---

## 🛠️ Tech Stack

- **Python**  
  The backbone of the project.

- **Selenium**  
  For web automation when HTTP requests fail.

- **Beautiful Soup (bs4)**  
  For parsing and scraping web content efficiently.

- **Requests**  
  For sending HTTP requests and handling responses.

- **Pydub**  
  To process and convert audio files as needed.

---

## 💡 How It Works

1. **User Input**  
   Provide the **song name**, **artist**, or **album** via the input prompt.  

2. **Search and Match**  
   The bot crawls multiple music websites, filtering results to find the most relevant option.  

3. **Download**  
   - Attempts to download using **HTTP requests** first.  
   - If blocked, switches to **Selenium automation** to bypass restrictions.

4. **Audio Processing**  
   Processes and converts the downloaded file (if required) using **pydub**.
