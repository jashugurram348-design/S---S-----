# SignSpeak — Sign Language Translator

SignSpeak is a web application designed to help users explore sign-language translation, text translation, speech features, learning lessons, and sign-language dictionary entries through a modern glassmorphism interface.

## Features

- **Text Translation:** Translate text between supported languages.
- **Speech Support:** Speech-to-text and text-to-speech features.
- **Sign Detection Demo:** Webcam-based hand landmark detection.
- **Sign Dictionary:** Search sign entries and browse categories.
- **Learning Lessons:** Explore lessons by category and difficulty.
- **Translation History:** View and manage translation records.
- **SOS Requests:** Submit an emergency request within the application.
- **Database:** Store translation history, dictionary entries, lessons, and related records using SQLite and Flask-SQLAlchemy.
- **Glassmorphism UI:** A modern interface with translucent panels and a blue-themed design.

> **Note:** This project includes demonstration functionality. Hand landmark detection does not independently recognize full sign language. Dictionary entries and translations should be verified for the intended sign language. The SOS feature does not automatically contact emergency services.

## Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask
- Flask-CORS
- Flask-SQLAlchemy

### Additional Libraries
- Deep Translator
- SpeechRecognition
- pyttsx3
- OpenCV
- MediaPipe
- SQLite

## Project Structure

```text
SignSpeak/
├── index.html
├── style.css
├── main.js
├