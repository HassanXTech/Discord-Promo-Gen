# Discord Promo Gen V2

An automated tool for generating Epic Games accounts and obtaining Discord Nitro promotional links.

## 🚀 Features

- **Automated Account Creation**: Creates Epic Games accounts with random credentials
- **Discord Promo Generation**: Automatically obtains Discord Nitro promotional links
- **Email Verification**: Handles email verification using temporary email services
- **Browser Automation**: Uses nodriver for headless browser automation
- **Continuous Generation**: Runs in a loop to generate multiple accounts
- **File Management**: Saves promo links and account information to organized files
- **Error Handling**: Robust error handling with detailed logging

## 📋 Requirements

- Python 3.8+
- Chrome/Chromium browser
- Internet connection

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/HassanXTech/Discord-Promo-Gen.git
   cd Discord-Promo-Gen
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```
   
   Or on Windows, use the batch file:
   ```bash
   start.bat
   ```

## 📦 Dependencies

- `nodriver` - Browser automation
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `pystyle` - Terminal styling
- `colorama` - Cross-platform colored terminal text
- `raducord` - Logging utility
- `html2text` - HTML to text conversion

## 🎯 Usage

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **Select from the menu**:
   - `[1]` Generate EpicGames Account & Discord Promo
   - `[2]` Credits
   - `[3]` Exit

3. **Automated Process**:
   - Creates temporary email address
   - Navigates to Epic Games registration
   - Fills out registration form with random data
   - Handles email verification
   - Obtains Discord Nitro promo link
   - Saves results to output files

## 📁 Project Structure

```
Discord-Promo-Gen/
├── main.py                 # Main application file
├── start.bat              # Windows batch file to start the app
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── file_manager.py    # File operations and saving
│   ├── string_generator.py # Random string generation
│   └── url_extractor.py   # URL extraction from emails
├── output/                # Output directory
│   └── promo.txt         # Generated promo links
└── README.md             # This file
```

## 🔧 Configuration

The application uses a private email service for temporary email generation. The configuration is built into the `PrivateMailClient` class:

- **Domain**: `pixiboost.fun`
- **API Endpoint**: Custom email service
- **Email Format**: Random string + domain

## 📝 Output Files

- **`output/promo.txt`**: Contains generated Discord promo links
- **`accounts.txt`**: Stores account credentials (email and password)
- **`saved_emails.txt`**: Backup of email addresses and tokens

## ⚠️ Important Notes

- This tool is for educational purposes only
- Respect Discord's and Epic Games' Terms of Service
- Use responsibly and don't abuse the services
- The tool requires a stable internet connection
- Browser automation may be detected by anti-bot measures

## 🐛 Troubleshooting

### Common Issues:

1. **Browser not starting**:
   - Ensure Chrome/Chromium is installed
   - Check if browser is already running
   - Try running as administrator

2. **Email verification fails**:
   - Check internet connection
   - Email service might be temporarily down
   - Try restarting the application

3. **Element not found errors**:
   - Website layout might have changed
   - Try updating the application
   - Check if browser is fully loaded

## 🔄 Updates

The tool automatically handles:
- Dynamic element detection
- Retry mechanisms for failed operations
- Timeout handling for slow connections
- Error recovery and continuation

## 👨‍💻 Developer

- **Created by**: Hassan Tech
- **Discord**: anomus.ly
- **GitHub**: [HassanXTech](https://github.com/hassanxtech)
- **Discord Server**: [dreamlove](https://discord.gg/dreamlove)
- **Contact**: instagram.com/hsx.esticxs

## 📄 License

This project is for educational purposes. Please respect the terms of service of all platforms involved.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## ⭐ Support

If you find this project helpful, please give it a star on GitHub!

---

**Disclaimer**: This tool is provided as-is for educational purposes. Users are responsible for complying with all applicable terms of service and laws.
