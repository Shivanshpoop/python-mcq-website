# QuizLab — Python MCQ Website

A responsive multiple-choice quiz website powered by a small Python HTTP server. This repository contains a runnable reference implementation using **only Python's standard library**—no Flask, Django, database, or third-party packages are required.

## Features
- Responsive quiz interface
- Questions loaded from a JSON file
- Server-side answer evaluation and score calculation
- Explanations shown after submission
- Easy-to-edit question bank
- No external dependencies

## Run locally
1. Install Python 3.9 or newer.
2. Clone this repository.
3. From the project folder, run:

   ```bash
   python app.py
   ```

4. Open **http://127.0.0.1:8000** in your browser.
5. Select an answer for every question and submit.

Stop the server with `Ctrl+C`.

## Project structure
```
python-mcq-website/
├── app.py
├── questions.json
├── index.html
├── style.css
├── script.js
└── README.md
```

## Add your own questions
Edit `questions.json`. Each question has an integer `id`, a `category`, question text, four `options`, a zero-based `answer` index, and an `explanation`.

Example:
```json
{
  "id": 9,
  "category": "Python",
  "question": "What is Python?",
  "options": ["A programming language", "An operating system", "A database", "A browser"],
  "answer": 0,
  "explanation": "Python is a general-purpose programming language."
}
```

## Notes
This is a clean, working starter implementation created for the public portfolio repository. It is not represented as a copy of any earlier private/unavailable source code or as a deployment of the user's original website.

## License
MIT
