# Victoria BC Transit Bus Tracker 🚌

A real-time bus tracker for **Victoria, BC**, using open transit data provided by **BC Transit**.

The application displays live bus locations on an interactive map and updates vehicle positions in real time.

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/amm-ar03/realtime-bustracker.git
cd realtime-bustracker
```

### 2. Start the real-time data process

In one terminal:

```bash
python3 realtime_data.py
```

### 3. Start the Flask application

Open a **separate terminal** and run:

```bash
python3 live.py
```

Then open the local address shown in the terminal to view the bus tracker.

## Data

This project uses open transit data provided by **BC Transit**.
