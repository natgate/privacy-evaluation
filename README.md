
# Encrypted Dot Product Server-Client Application

This application performs encrypted dot product computations using a server-client model. The server processes encrypted batches of data and returns encrypted results, enabling secure computations without exposing sensitive data.

---

## Features

- **Encrypted Computation**: Securely compute dot products on encrypted data.
- **Client-Server Architecture**: The server performs computations, and the client sends encrypted data and receives results.

---

## Requirements

To run this project, ensure you have the following installed:

- Python 3.8 or later
- Required Python libraries (see below)

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install the required Python libraries:
   ```bash
   pip install numpy tenseal
   ```

3. Verify the installation:
   ```bash
   python --version
   pip list
   ```

---

## Usage

This application requires you to run the `server.py` script first, followed by `client.py`. Each script should be executed in a separate terminal.

### Step 1: Start the Server
Run the server script:
```bash
python server.py
```

The server will listen for incoming client connections and perform encrypted computations.

### Step 2: Run the Client
In a separate terminal, run the client script:
```bash
python client.py
```

The client will send encrypted data to the server, retrieve the results, and display them.

---

## Project Structure

- **`server.py`**: Handles encrypted computations on batches of data.
- **`client.py`**: Sends encrypted data to the server and retrieves results.
- **`client-server.py`**: Contains baseline interaction for testing
- **`README.md`**: This file.

---
