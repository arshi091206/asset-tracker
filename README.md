# Asset Tracker

Asset Tracker is a Django-based web application that helps users monitor the prices of stocks, cryptocurrencies, gold, and forex in real time. Instead of manually checking prices throughout the day, users can set custom target prices and receive email notifications when their conditions are met.

---

## Features

- Track multiple asset classes
  - Stocks
  - Cryptocurrencies
  - Gold
  - Forex

- Custom Price Alerts
  - Notify when price goes above target
  - Notify when price goes below target

- Email Notifications
  - Automatic email alerts when conditions are met

- Historical Price Charts
  - Interactive graphs for asset price trends

- Company Search
  - Autocomplete for supported companies and tickers

- User Authentication
  - Secure registration and login
  - Personalized dashboard for each user

- Live Price Updates
  - Real-time market data fetched from Yahoo Finance

---

## Tech Stack

### Backend
- Python
- Django

### Database
- PostgreSQL

### APIs
- Yahoo Finance (yfinance)

### Scheduling
- APScheduler
- GitHub Actions (for periodic alert checking)

### Frontend
- HTML
- CSS
- JavaScript
- Django Templates

---

## 💻 Running Locally

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Configure the `.env` file
5. Run migrations
6. Start the server

```bash
python manage.py runserver
## Project Structure

```
---

asset-tracker/
│
├── accounts/
├── alerts/
├── dashboard/
├── asset_tracker/
├── static/
├── templates/
├── manage.py
├── requirements.txt
└── README.md
```

---

## Supported Assets

| Asset | Example |
|---------|---------|
| Stocks | AAPL, INFY |
| Crypto | BTC-USD, ETH-USD |
| Gold | Gold Futures |
| Forex | USDINR, EURUSD |

---

## How It Works

1. User creates an account.
2. User searches for an asset.
3. User selects:
   - Asset
   - Alert condition
   - Target price
4. Asset Tracker periodically checks live prices.
5. If the condition is met:
   - Email notification is sent.
   - Alert is marked as triggered.

---

## Future Improvements

- SMS notifications
- Push notifications
- Portfolio tracking
- Watchlists
- Mobile responsive redesign
- More financial data providers
- Price prediction and analytics
- Alert history

---

## Learning Outcomes

This project helped explore:

- Django Authentication
- PostgreSQL integration
- REST API consumption
- Scheduled background jobs
- Email automation
- Deployment
- GitHub Actions
- Interactive financial data visualization

---
---

## ⭐ If you found this project interesting, consider giving it a star!
