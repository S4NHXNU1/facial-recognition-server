# Facial Recognition Authentication Server

This project is a Flask-based authentication server that uses facial recognition for user verification. It leverages `facenet_pytorch` for face embedding extraction and Flask for handling API requests.

## Features

- User authentication using facial recognition.
- REST API for handling authentication requests.
- CORS support for cross-origin requests.

## Technologies Used

- Python
- Flask
- facenet\_pytorch
- flask\_cors
- flask-sqlalchemy

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/s4nhxnu1/facial-recognition-server.git
cd facial-recognition-server
```

### 2. Create a Virtual Environment

```bash
conda create -n <yourEnvName> python=3.12 -y
```

### 3. Install Dependencies

```bash
pip install flask flask_cors facenet_pytorch flask-sqlalchemy
```

## Running the Server

### Start the Flask Application

```bash
python app.py
```

The server will start on `http://127.0.0.1:5000/` by default.
