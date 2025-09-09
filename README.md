PAR Reduction Training Module
This is a local coaching simulation powered by a large language model (LLM). The application is designed to help branch managers and team leads practice coaching their Customer Service Representatives (CSRs) on effective collections techniques to reduce their Portfolio at Risk (PAR).

The simulation runs entirely on a local server using Ollama, which means it does not require an internet connection or an external API key to function after the initial setup.

Prerequisites
Before you can run this application, you need to have the following installed on your machine:

Ollama: The local LLM server. You can download it from https://ollama.ai/download.

Llama3 Model: The language model used for the simulation. You must download it to your local Ollama library.

Python 3.9+

Pip: Python's package installer.

Setup and Installation
Follow these steps to get the application up and running.

1. Pull the LLM
The application requires the llama3 model. Open your terminal or Command Prompt and run the following command to download it:

ollama pull llama3

Note: If you get an error like "ollama is not recognized," it means the ollama.exe file is not in your system's PATH. You may need to specify the full path to the executable, for example: "C:\Users\<YourUsername>\AppData\Local\Programs\Ollama\ollama.exe" pull llama3.

2. Clone the Repository and Install Dependencies
First, download or clone this project's files to your local machine.

Next, open your terminal, navigate to the project directory, and install the required Python libraries using the requirements.txt file:

pip install -r requirements.txt

How to Run the Application
Once all the prerequisites are met, you can start the application.

Make sure the Ollama server is running. It typically runs automatically in the background after you install it.

Open your terminal in the project directory.

Run the following command:

streamlit run app.py

Your web browser will automatically open a new tab with the application.

Key Accomplishments
A Complete Conversational Simulation: The app creates a dynamic, multi-turn coaching scenario. It uses a few-shot prompting approach to provide the AI with examples of good and bad coaching, ensuring high-quality and relevant feedback.

Seamless, Local Deployment: The application runs entirely on a local Ollama server, which means it is completely self-contained after the initial setup. It does not require any internet connection or external API keys to function.

Dynamic, Data-Driven Outcomes: Beyond a simple chat, the simulation generates a concrete, actionable plan by feeding the entire conversation history back into the LLM. This shows how a simple chat can be used to produce tangible and valuable business output.
