# ✈️ Flight Deals Alert Bot

A Python-based flight deal alert system that queries a real-world API and handles inconsistent responses to extract valid itineraries.

---

## Features

- Search multiple routes
- Filter real itineraries (outbound/inbound)
- Extract and display full trip details
- Find the cheapest flight within a date range
- Price alert system

--- 

## Tech

- Python
- Requests
- Python-dotenv
- REST API (RapidAPI - Kiwi)

---

## Example output

MAD → BCN: 112 €
🔥 ALERT: cheap flight found

---

## Setup

1. Clone repo

```bash
git clone <repo_url>
cd flight-deal-alert
```

2. Create `.env` file:

```env
RAPIDAPI_KEY=your_key_here
```

3. Run:

```bash
python main.py
```
---

## ⚠️ Challenges

- API returns inconsistent results (wrong routes, unexpected dates)
- Required manual filtering of itineraries
- Implemented validation logic to ensure correct origin/destination
- Selected cheapest valid flight from noisy API response
