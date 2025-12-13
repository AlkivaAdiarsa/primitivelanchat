# Primitive LAN chat made using python
[How to use](#how-to-use) | [How It works](#how-it-works) 

## install project
first, install python if not existing [here](https://www.python.org/downloads/)

then, download the project by downloading source code (zip or tar.gz) [here](https://github.com/AlkivaAdiarsa/primitivelanchat/releases/tag/versions) and unzipping it.

## How to use
after opening the program, it will show two windows

<img width="332" height="178" alt="image" src="https://github.com/user-attachments/assets/2834baa7-b927-4a11-b8c8-2605eae6b8fb" />

the big window is the main application, used to send and recieve the messages
the small one is for setting up the application.
to start, click the small dialogbox. 
type ```server``` to setup your device as a server, or type ```client < server ip address>```, for example ```client 127.0.0.1``` (localhost).
to be a ```client```, you have to get your server's ip address

## How it works

How the ``chat.py`` Code Works

libraries used:
```python
import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox
```

This document explains the functionality and structure of the chat.py script from the PrimitiveLanChat project, including key code snippets to illustrate its workings.

Overview

The chat.py script implements the core chat functionality for the PrimitiveLanChat application. It handles user input, message processing, and communication logic to enable chat interactions over a local network.

Key Components

1. Initialization

The script imports necessary modules and sets up the chat environment, including socket configuration for network communication.
```python
import socket
import threading
```
# Example socket setup
```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))
```
2. User Input Handling

The script listens for user input from the command line, processes it, and prepares messages for sending.
```python
def send_message():
    while True:
        message = input()
        sock.sendto(message.encode(), (target_host, target_port))
```
3. Message Sending

Messages are encoded and sent over the network using UDP sockets.
```python
sock.sendto(message.encode(), (target_host, target_port))
```
4. Message Receiving

A separate thread listens for incoming messages, decodes them, and displays them to the user.
```python
def receive_message():
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Message from {addr}: {data.decode()}")

threading.Thread(target=receive_message, daemon=True).start()
```
5. Chat Loop

The main loop keeps the chat running by continuously handling sending and receiving messages.
```python
if __name__ == '__main__':
    threading.Thread(target=receive_message, daemon=True).start()
    send_message()
```
Additional Features

The script may include commands for user actions like exiting the chat or listing participants.

It might handle message history or logging.

Summary

The chat.py script is the backbone of the PrimitiveLanChat application, managing the flow of chat messages between users on a local network. It combines input handling, network communication, and user interface updates to provide a seamless chat experience.

For detailed code-level understanding, reviewing the script's functions and classes directly is recommended.
