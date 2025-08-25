import logging
import speech_recognition as sr
from duckduckgo_search import DDGS
from sympy import sympify
import cohere
from langchain_community.llms import OpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_experimental.tools import PythonREPLTool
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import PyPDF2  # For reading PDF files
import tkinter as tk
from tkinter import filedialog  # For file browsing
import requests  # For making HTTP requests to OpenWeatherMap API
import json
import os

# File to store tasks
TASKS_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Add a task
def add_task(task_description, tasks):
    tasks.append({"description": task_description, "status": "pending"})
    save_tasks(tasks)
    return f"Added '{task_description}' to your to-do list."

# Mark a task as done
def mark_task_as_done(task_description, tasks):
    for task in tasks:
        if task["description"].lower() == task_description.lower():
            task["status"] = "done"
            save_tasks(tasks)
            return f"Marked '{task_description}' as done."
    return f"Task '{task_description}' not found."

# Remove a task
def remove_task(task_description, tasks):
    for task in tasks:
        if task["description"].lower() == task_description.lower():
            tasks.remove(task)
            save_tasks(tasks)
            return f"Removed '{task_description}' from your to-do list."
    return f"Task '{task_description}' not found."

# Show all tasks
def show_tasks(tasks):
    if not tasks:
        return "Your to-do list is empty."
    response = "Your to-do list:\n"
    for task in tasks:
        response += f"- {task['description']} [{task['status']}]\n"
    return response.strip()

# Process task-related commands
def process_task_command(command, tasks):
    command = command.lower()
    if "add" in command:
        task_description = command.replace("add", "").replace("to my to-do list", "").strip()
        return add_task(task_description, tasks)
    elif "mark" in command and "as done" in command:
        task_description = command.replace("mark", "").replace("as done", "").strip()
        return mark_task_as_done(task_description, tasks)
    elif "remove" in command or "delete" in command:
        task_description = command.replace("remove", "").replace("delete", "").replace("from my to-do list", "").strip()
        return remove_task(task_description, tasks)
    elif "show" in command and "to-do list" in command:
        return show_tasks(tasks)
    else:
        return "I'm sorry, I didn't understand that task command."

# Function to send an email
def send_email(to_email, subject, body):
    sender_email = "kajisadmansakib@gmail.com"  # Replace with your Gmail address
    sender_password = "youtubeSucks100"      # Replace with your Gmail app password

    # Create the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
        return "Email sent successfully!"
    except Exception as e:
        return f"Error sending email: {e}"

# Function to read PDF file
def read_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            return text
    except Exception as e:
        logging.error(f"Error reading PDF file: {e}")
        return f"Error reading PDF file: {e}"

# Function to browse and select a PDF file
def browse_pdf():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF Files", "*.pdf")]  # Only allow PDF files
    )
    return file_path

# Function to get weather forecast
def get_weather(city_name):
    WEATHERAPI_API_KEY = "e6502c9dd9bf45a7970132533251304"  # Replace with your actual API key
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHERAPI_API_KEY}&q={city_name}&aqi=no"
    try:
        response = requests.get(url)
        data = response.json()
        if "error" in data:
            return f"Error fetching weather data: {data['error']['message']}"
        weather_description = data["current"]["condition"]["text"]
        temperature = data["current"]["temp_c"]
        humidity = data["current"]["humidity"]
        wind_speed = data["current"]["wind_kph"]
        return (
            f"Weather in {city_name}:\n"
            f"Description: {weather_description}\n"
            f"Temperature: {temperature}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} km/h"
        )
    except Exception as e:
        logging.error(f"Error fetching weather data: {e}")
        return "An unexpected error occurred while fetching weather data."

# Function to generate response using Cohere
def generate_response(prompt):
    try:
        response = cohere_client.chat(
            model='command-xlarge-nightly',
            message=prompt,
            max_tokens=100,
            temperature=0.7
        )
        logging.info(f"Cohere API response: {response.text.strip()}")
        return response.text.strip()
    except cohere.errors.BadRequestError as e:
        logging.error(f"Bad request to Cohere API: {e}")
        return "Sorry, there was an issue generating a response. Please try again later."
    except Exception as e:
        logging.error(f"Unexpected error with Cohere API: {e}")
        return "An unexpected error occurred. Please try again later."

# Process voice command
def process_command(command, tasks):
    command = command.lower()
    
    if "calculate" in command:
        try:
            expression = command.replace("calculate", "").strip()
            result = sympify(expression)
            return f"The result is {result}."
        except Exception as e:
            return f"Error calculating: {e}"
    
    elif "search" in command:
        query = command.replace("search", "").strip()
        try:
            search_results = DDGS().text(query, max_results=3)
            if search_results:
                return "\n".join([f"{result['title']} - {result['href']}" for result in search_results])
            else:
                return "Sorry, no results found."
        except Exception as e:
            logging.error(f"Error with DuckDuckGo search: {e}")
            return "Sorry, I couldn't fetch search results."
    
    elif "write" in command or "create" in command:
        prompt = command.replace("write", "").replace("create", "").strip()
        return f"Here's what I wrote: {generate_response(prompt)}"
    
    elif "code" in command:
        try:
            code_prompt = command.replace("code", "").strip()
            generated_code = agent.run(f"Generate Python code for: {code_prompt}")
            return f"Generated Python code:\n\n{generated_code}"
        except Exception as e:
            return f"Error generating code: {e}"
        
    elif "send an email" in command:
        try:
            # Extract recipient, subject, and body from the command
            parts = command.split(" to ")
            if len(parts) > 1:
                to_email = parts[1].strip()
            else:
                to_email = "xyz@gmail.com"  # Default recipient
            
            subject = "Automated Email"
            body = "This is an automated email sent by AI CEO."
            
            result = send_email(to_email, subject, body)
            return result
        except Exception as e:
            return f"Error sending email: {e}"
    
    elif "read pdf" in command:
        try:
            # Open file browser to select a PDF file
            file_path = browse_pdf()
            if not file_path:
                return "No PDF file selected."
            pdf_content = read_pdf(file_path)
            return f"PDF Content:\n{pdf_content}"
        except Exception as e:
            return f"Error reading PDF: {e}"
    
    elif "weather" in command:
        try:
            # Extract city name from the command
            parts = command.split("in")
            if len(parts) > 1:
                city_name = parts[1].strip()
            else:
                return "Please specify a city name (e.g., 'What's the weather in New York?')."
            weather_info = get_weather(city_name)
            return weather_info
        except Exception as e:
            return f"Error fetching weather: {e}"
    
    elif "to-do list" in command or "task" in command:
        return process_task_command(command, tasks)
    
    else:
        return generate_response(command)

# Listen for commands
def listen_for_command():
    print("Listening for your command...")
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio)
        logging.info(f"Recognized command: {command}")
        return command
    except sr.UnknownValueError:
        logging.error("Speech recognition could not understand audio.")
        return "Sorry, I couldn't understand the command."
    except sr.RequestError as e:
        logging.error(f"Could not request results from Google Speech Recognition service: {e}")
        return f"Error with speech recognition: {e}"

# Main execution
def main():
    print("Welcome to AI CEO!")
    logging.info("AI CEO Activated.")

    authenticated = authenticate_voice()
    if not authenticated:
        print("Authentication failed. Exiting...")
        return
    
    print("Authentication successful. Listening for commands...")
    
    # Load tasks
    tasks = load_tasks()
    
    try:
        while True:
            command = listen_for_command()
            
            # Check for exit phrases
            if "exit" in command.lower() or "that's enough for now" in command.lower():
                print("Exiting AI CEO. Goodbye!")
                break
            
            if command:
                result = process_command(command, tasks)
                print(f"AI CEO: {result}")
    except KeyboardInterrupt:
        print("\nExiting AI CEO. Goodbye!")

if __name__ == "__main__":
    main()