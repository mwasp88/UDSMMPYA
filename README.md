# Parking Management System

This repository contains a simple Flask application and a static front-end for managing vehicle entry and exit. The front-end (`index.html`) provides a user interface for uploading or capturing license plate images. The Flask backend (`app.py`) logs entries, handles serial communication and exposes a history download endpoint.

## Running the server

1. Install dependencies:
   ```bash
   pip install flask pyserial
   ```
2. Start the application:
   ```bash
   python app.py
   ```
   The server will run on `http://localhost:5000`.

The application writes scan history to `history.json` and attempts to communicate with the serial port specified in `app.py`.

