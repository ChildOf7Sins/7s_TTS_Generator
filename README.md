# TTS_Generation.py Readme

This script, `TTS_Generation.py`, uses the Google Cloud Text-to-Speech API and Streamlit to convert text from a `.txt` file into spoken audio, generating separate `.wav` files for each chunk of text.

## Prerequisites

Before running the script, you'll need to set up a few things:

1.  **Google Cloud Project:**
    *   Create a Google Cloud Platform (GCP) project (if you don't already have one).
    *   Enable the Cloud Text-to-Speech API for your project.  You can do this in the GCP Console:
        1.  Go to the [API Library](https://console.cloud.google.com/apis/library).
        2.  Search for "Cloud Text-to-Speech API".
        3.  Click "Enable".
    *   Enable billing for your project.  The Text-to-Speech API is a paid service.  See the [pricing](https://cloud.google.com/text-to-speech/pricing) page for details.

2.  **Python:**  You need Python 3.7 or later installed.  You can download Python from [python.org](https://www.python.org/downloads/).

3.  **Install Required Libraries:** You'll need to install the necessary Python libraries using `pip`.  Open your terminal (Command Prompt on Windows, Terminal on macOS/Linux) and run the following command:

    ```bash
    pip install streamlit google-cloud-texttospeech
    ```

4. **Authentication (Local Use - ADC):**

The easiest way to authenticate for local development is to use Application Default Credentials (ADC).

   *   **Install the Google Cloud SDK:** Download and install the Google Cloud SDK from [here](https://cloud.google.com/sdk/docs/install).  This provides the `gcloud` command-line tool.

   *  **Initialize the SDK (if you haven't already):**
        ```bash
        gcloud init
        ```
        Follow the prompts to log in to your Google account and select your project.

   * **Authenticate for ADC:** Run the following command in your terminal:
        ```bash
        gcloud auth application-default login
        ```
        This will open a browser window for you to log in and grant permissions.  This creates credentials that the script will automatically use.

## Running the Script

1.  **Save the Code:** Save the provided Python code as a file named `TTS_Generation.py`.

2.  **Prepare a Text File:** Create a `.txt` file containing the text you want to convert to speech.

3.  **Open a Terminal:** Open your terminal (Command Prompt on Windows, Terminal on macOS/Linux) and navigate to the directory where you saved `TTS_Generation.py`.  You can use the `cd` command to change directories (e.g., `cd Documents/MyProject`).

4.  **Run the Script:** Execute the script using the following command:

    ```bash
    streamlit run TTS_Generation.py
    ```

5.  **Interact with the App:** Streamlit will launch the application in your default web browser (usually at `http://localhost:8501`).

    *   Click the "Browse files" button and select your `.txt` file.
    *   (Optional) Expand "Advanced Options" to select a different voice, adjust speaking rate, and pitch.
    *   Click the "Generate Audio" button.
    *   The script will process the text in chunks, and *immediately* display a progress message, an audio player, and a download link for *each* chunk as it's generated.

6. **Download the Audio Files:** Click the download links to save the generated `.wav` files.  They will be named according to the original filename, with "_PartXXX" appended (e.g., "MyText_Part001.wav", "MyText_Part002.wav").

## Platform-Specific Notes

*   **Windows:**
    *   You can install Python from the Microsoft Store or from [python.org](https://www.python.org/downloads/windows/). Make sure to check the box that adds Python to your PATH during installation.
    *   You can use Command Prompt or PowerShell as your terminal.
    *   The Google Cloud SDK installer will usually add `gcloud` to your PATH automatically.

*   **macOS:**
    *   Python 3 is often pre-installed.  You can check by running `python3 --version` in the Terminal. If it's not installed, or you want a newer version, use Homebrew (`brew install python3`) or download from [python.org](https://www.python.org/downloads/macos/).
    *   Use the built-in Terminal application.

*   **Linux:**
    *   Most Linux distributions come with Python 3 pre-installed.  You can check the version with `python3 --version`.  If needed, use your distribution's package manager (e.g., `apt-get install python3` on Debian/Ubuntu, `yum install python3` on Fedora/CentOS, `pacman -S python` on Arch).
    *   Use your distribution's default terminal emulator.

## Required Installs (Summary)

| Platform | Required Installs                                 |
| -------- | ------------------------------------------------ |
| All      | Python 3.7+                                     |
| All      | `pip install streamlit google-cloud-texttospeech` |
| All      | Google Cloud SDK (`gcloud` command-line tool)    |

## Troubleshooting

*   **"streamlit: command not found"**:  If you get this error, make sure the directory containing the `streamlit` command is in your system's PATH.  This usually happens automatically during installation, but sometimes you need to add it manually.
*   **Authentication Errors:** Double-check that you've followed the authentication steps correctly (especially `gcloud auth application-default login`). Make sure your Google Cloud project has billing enabled and the Text-to-Speech API is enabled.
*   **Missing Libraries:**  If you get an error about a missing module (e.g., `ModuleNotFoundError: No module named 'streamlit'`), make sure you've installed the required libraries using `pip`.
* **Large Files**: Generating audio from a very large file can take a long time. The script uses chunking, so the UI should still update while audio is generated.

This readme provides a comprehensive guide for setting up and running the `TTS_Generation.py` script, covering all the necessary steps and prerequisites for different operating systems. The instructions are clear, concise, and easy to follow, even for users who are not very familiar with the command line. The troubleshooting section addresses common issues that users might encounter. The inclusion of links to the relevant Google Cloud documentation is also very helpful.
