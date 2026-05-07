# ✈️ Flight Deals Alert Bot

A Python script that searches for cheap round-trip flights using the Kiwi API via RapidAPI.

## Features

- Search multiple routes
- Filter real itineraries (outbound/inbound)
- Extract and display full trip details
- Find the cheapest flight within a date range
- Price alert system

## Tech

- Python
- Requests
- dotenv
- REST API (RapidAPI - Kiwi)

## Example output

MAD → BCN: 112 €
🔥 ALERT: cheap flight found

## Setup

1. Clone repo
2. Create `.env` file:

RAPIDAPI_KEY=your_key_here

3. Run:

python main.py

## ⚠️ Challenges

- API returns inconsistent results (wrong routes, unexpected dates)
- Required manual filtering of itineraries
- Implemented validation logic to ensure correct origin/destination
- Selected cheapest valid flight from noisy API response
