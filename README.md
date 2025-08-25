# AI CEO: Your Personalized AI Assistant

**AI CEO** is a versatile, voice-activated AI assistant designed to help you manage tasks, brainstorm ideas, fetch information, and stay productive. Whether you need help with task management, weather updates, email automation, or creative brainstorming, AI CEO has got you covered.

---

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Supported Commands](#supported-commands)
6. [Contributing](#contributing)
7. [License](#license)

---

## Features

AI CEO offers a wide range of features to enhance productivity and simplify daily tasks:

- **Task Management**: Add, remove, mark as done, and view tasks on your to-do list.
- **Voice Activation**: Use voice commands to interact with the AI seamlessly.
- **Weather Forecasts**: Get real-time weather updates for any city.
- **Email Automation**: Send automated emails directly through voice commands.
- **PDF Reader**: Extract and read content from PDF files.
- **Mathematical Calculations**: Perform calculations using natural language.
- **Internet Search**: Fetch quick answers from DuckDuckGo.
- **Code Generation**: Generate Python code snippets for various tasks.
- **Collaborative Brainstorming**: Generate, organize, and prioritize ideas for creative projects.
- **Motivational Quotes**: Start your day with inspiring quotes.
- **Customizable Personality**: Tailor the AI's tone to match your preferences (e.g., professional, friendly).
- **Offline Mode**: Perform tasks like reading PDFs or managing tasks without an internet connection.

---

## Prerequisites

Before running the AI CEO system, ensure you have the following:

1. **Python 3.8+**: The system is built using Python. Install it from [python.org](https://www.python.org/).
2. **Required APIs**:
   - **Cohere API Key**: For generating responses. Sign up at [cohere.com](https://cohere.com).
   - **OpenWeatherMap API Key**: For weather forecasts. Sign up at [openweathermap.org](https://openweathermap.org).
   - **Gmail Account**: For sending emails (optional).
3. **Dependencies**: Install the required libraries using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/ai-ceo.git
   cd ai-ceo
   ```

2. **Set Up API Keys**:
   - Create a `.env` file in the root directory and add your API keys:
     ```
     COHERE_API_KEY=your_cohere_api_key
     WEATHERAPI_API_KEY=your_weatherapi_key
     GMAIL_EMAIL=your_email@gmail.com
     GMAIL_PASSWORD=your_gmail_password
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Program**:
   ```bash
   python main.py
   ```

---

## Usage

### Voice Commands
- Speak clearly into your microphone to issue commands.
- Example: "Add 'Prepare presentation' to my to-do list."

### Text-Based Interaction
- If you prefer typing, you can modify the program to accept text input instead of voice.

### Exiting the Program
- Say "Exit" or "That's enough for now" to terminate the AI CEO.

---

## Supported Commands

Here’s a list of commands you can use with AI CEO:

| Command Type                     | Example Command                                      |
|----------------------------------|------------------------------------------------------|
| Task Management                  | "Add 'Send emails' to my to-do list."                |
|                                  | "Mark 'Prepare report' as done."                     |
|                                  | "Remove 'Buy groceries' from my to-do list."         |
| Weather Forecast                 | "What's the weather in New York?"                    |
| Email Automation                 | "Send an email to john.doe@example.com."             |
| Mathematical Calculations        | "Calculate 5 * (3 + 2)."                             |
| Internet Search                  | "Search for the best AI tools."                      |
| Code Generation                  | "Generate Python code for a Fibonacci sequence."    |
| Collaborative Brainstorming      | "Brainstorm ideas for marketing strategies."         |
| Motivational Quotes              | "Give me a motivational quote."                      |
| Read PDF                         | "Read PDF file."                                     |

---
