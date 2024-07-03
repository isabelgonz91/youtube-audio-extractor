# YouTube Audio Transcription App

This Streamlit application transcribes audio from YouTube videos using the OpenAI Whisper API. Users can input a YouTube video URL and their OpenAI API key to get the audio transcribed in their desired language. The transcribed text can then be viewed and downloaded directly from the application.

## Features

- Input YouTube video URL and OpenAI API key
- Select the language of the audio
- View YouTube video within the app
- Display transcribed text
- Download transcribed text

## Requirements

- Python 3.7+
- Streamlit
- dotenv
- langchain_community

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Install dependencies:**

    ```bash
    pip install streamlit python-dotenv langchain_community
    ```

3. **Create a `.env` file in the project directory and add your OpenAI API key:**

    ```
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

1. **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

2. **Open your web browser and go to `http://localhost:8501`.**

3. **Input your OpenAI API key and the YouTube video URL.**

4. **Select the language of the audio.**

5. **Click on the "Transcribir" button to start the transcription process.**

6. **View the YouTube video and the transcribed text in the app.**

7. **Download the transcribed text if needed.**

## Code Overview

- **Loading environment variables:**

    ```python
    from dotenv import load_dotenv
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    ```

- **Streamlit UI:**

    ```python
    st.title("Transcripción de Audio de YouTube")
    api_key = st.text_input("Clave de API de OpenAI", type="password")
    video_url = st.text_input("URL del video de YouTube")
    language = st.selectbox("Selecciona el idioma del audio", ["en", "es", "fr", "de", "it", "pt", "nl", "ru", "zh"])
    ```

- **YouTube video embedding and transcription:**

    ```python
    video_id = video_url.split("v=")[-1].split("&")[0]
    st.video(f"https://www.youtube.com/embed/{video_id}")
    ```

- **Downloading audio and transcribing:**

    ```python
    loader = GenericLoader(DebugYoutubeAudioLoader([video_url], tempfile.gettempdir()), OpenAIWhisperParser(api_key=api_key))
    docs = loader.load()
    ```

- **Displaying and downloading the transcription:**

    ```python
    st.text_area("Transcripción", doc.page_content, height=300)
    b64 = base64.b64encode(doc.page_content.encode()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="{text_filename}">Descargar Transcripción</a>'
    st.markdown(href, unsafe_allow_html=True)
    ```

## Error Handling

If an error occurs during the transcription process, it will be displayed in the Streamlit app:

```python
except Exception as e:
    st.error(f"Ocurrió un error durante la transcripción: {e}")
