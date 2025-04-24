import openai
import env
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox, QInputDialog
import pyttsx3  # Import pyttsx3 for TTS
import speech_recognition as sr

openai.api_key = env.OPENAI_API_KEY

# Initialize pyttsx3 TTS engine
tts_engine = pyttsx3.init()

# Function to read text out loud

def text_to_speech(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio,language= "en" )
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError:
            return "Speech Recognition service is unavailable."
        except Exception as e:
            return f"Error: {str(e)}"


# Existing functions
def new(ui):
    ui.textEdit.clear()
    ui.filename = None
    ui.statusbar.showMessage("A new file has been created. Make sure you save it.")
    ui.setWindowTitle("Untitled -- Abid Window")

def file_changed(filename, editor_text):
    with open(filename, 'r') as file:
        existing = file.read()
    return True if existing != editor_text else False

def send_to_openai(question):
    """
    Sends a user question to OpenAI and returns the AI's response.
    """
    try:
        # Make the API call to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the correct model
            #model="gemini-1.5-flash",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            max_tokens=2040,
        )

        # Extract the AI's response
        answer = response['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        print(f"Chatbot Error: {e}")
        return "An error occurred while fetching the response. Please try again."

def chatbot(ui):
    """
    Opens a dialog box to take a question from the user and displays the AI's response.
    """
    # Prompt the user for input
    question, ok = QInputDialog.getText(
        None, "Chat with AI", "Enter your question:"
    )

    if ok and question.strip():
        # Send the question to OpenAI
        answer = send_to_openai(question)

        # Display the AI's response
        QMessageBox.information(
            None,
            "AI Response",
            f"Q: {question}\n\nA: {answer}",
            QMessageBox.Ok
        )

def about_app():
    msg = QMessageBox()
    msg.setWindowTitle("About Abid Window")
    icon = QtGui.QIcon()
    icon.addPixmap(
        QtGui.QPixmap('./resources/imgs/_app_icon.ico'),
        QtGui.QIcon.Normal, QtGui.QIcon.Off
    )
    msg.setWindowIcon(icon)
    msg.setText(
        "<p><b>Abid Window</b> v1.0</p>"

        "This is an intelligent text editor built with Python.<br>"
        "<b>App Features</b>"
        "<ul>"
        "<li>Open, create and save new files.</li>"
        "<li>Export to PDF</li>"
        "<li>Print directly to a printer</li>"
        "<li>Save file before closing</li>"
        "<li>Text formatting.</li>"
        "<li>An interactive AI chat bot to assist you with your work</li>"
        "</ul>"
    )
    msg.exec_()
    
    

def about_me():
    msg = QMessageBox()
    msg.setWindowTitle("About Developer")
    icon = QtGui.QIcon()
    icon.addPixmap(
        QtGui.QPixmap('./resources/imgs/dev_info.png'),
        QtGui.QIcon.Normal, QtGui.QIcon.Off
    )
    msg.setWindowIcon(icon)
    msg.setText(
        "<p><b>Abid Window</b> v1.0</p>"

        "<b>About the developer</b>"

        "<p>"
        "This app was made by Abid"

        "Feel free to contact the developer for bug reports and feature suggestions.< br > "
        "<b>Developer Details</b><br>"
        "<b>Name:</b> Abid<br>"
        "<b>Email:</b> abid@mail.com"
        "</b><br><br>"

        "</p>"
    )
    msg.exec_()
