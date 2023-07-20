## Arbitrage Opportunities Finder

This repository contains a Python script that helps you find arbitrage opportunities in sports betting odds from various sportsbooks. The script uses the Selenium library to scrape odds data from the Action Network website and identifies potential arbitrage opportunities based on the provided odds.

### Prerequisites

To run the script, you need to have the following installed on your machine:

1. Python 3
2. Chrome web browser
3. ChromeDriver (automatically installed using `webdriver_manager`)

### Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/ismail-amouma/Arbitrage_Opportunities_Finder
```

2. Install the required Python libraries:

```bash
pip install pandas selenium webdriver_manager asyncio telegram
```

### Usage

1. Open a terminal or command prompt and navigate to the cloned repository's directory.

2. Execute the script:

```bash
python arbitrage_finder.py
```

The script will scrape odds data from the Action Network website for various sports and display potential arbitrage opportunities. If any arbitrage opportunities are found, it will also send a notification message to a Telegram group using the provided Telegram bot token and chat ID.

### Note

Please make sure to replace the `chat_id` and `token` variables in the script with your actual Telegram bot token and chat ID for the notification to work correctly.

### Disclaimer

Sports betting involves financial risk, and the script's results are for informational purposes only. The author is not responsible for any financial losses incurred while using the script or acting on the information provided.

Happy arbitrage hunting!
