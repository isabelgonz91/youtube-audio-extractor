import os
import streamlit as st
from langchain_community.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import OpenAIWhisperParser
from dotenv import load_dotenv
import base64
import tempfile

# Cargar variables de entorno desde un archivo .env
load_dotenv()

# Configurar la API de OpenAI utilizando las variables de entorno
openai_api_key = os.getenv("OPENAI_API_KEY")

# Clase para depuración que extiende YoutubeAudioLoader
class DebugYoutubeAudioLoader(YoutubeAudioLoader):
    def yield_blobs(self):
        for blob in super().yield_blobs():
            print(f"Audio file downloaded: {blob}")
            yield blob

# Función principal para la interfaz de Streamlit
def main():
    st.title("Transcripción de Audio de YouTube")

    api_key = st.text_input("Clave de API de OpenAI", type="password")
    video_url = st.text_input("URL del video de YouTube")
    language = st.selectbox("Selecciona el idioma del audio", ["en", "es", "fr", "de", "it", "pt", "nl", "ru", "zh"])

    if st.button("Transcribir"):
        if not api_key or not video_url:
            st.error("Por favor, proporciona la clave de API de OpenAI y la URL del video.")
            return

        # Mostrar el video de YouTube
        video_id = video_url.split("v=")[-1].split("&")[0]
        st.video(f"https://www.youtube.com/embed/{video_id}")

        # Crear una instancia del cargador genérico utilizando la clase DebugYoutubeAudioLoader y el parser OpenAIWhisperParser
        loader = GenericLoader(DebugYoutubeAudioLoader([video_url], tempfile.gettempdir()), OpenAIWhisperParser(api_key=api_key))

        try:
            # Cargar los documentos (transcripciones de audio)
            docs = loader.load()

            if docs:
                for doc in docs:
                    # Obtener el nombre del archivo de audio desde los metadatos del documento
                    audio_filename = doc.metadata["source"]
                    # Crear el nombre del archivo de texto reemplazando la extensión del archivo de audio por .txt
                    text_filename = os.path.splitext(audio_filename)[0] + ".txt"
                    # Guardar la transcripción en un archivo de texto
                    with open(text_filename, "w", encoding="utf-8") as text_file:
                        text_file.write(doc.page_content)
                    st.success(f"Transcription saved to {text_filename}")
                    st.text_area("Transcripción", doc.page_content, height=300)

                    # Crear un enlace de descarga para la transcripción
                    b64 = base64.b64encode(doc.page_content.encode()).decode()
                    href = f'<a href="data:text/plain;base64,{b64}" download="{text_filename}">Descargar Transcripción</a>'
                    st.markdown(href, unsafe_allow_html=True)
            else:
                st.error("No se cargaron documentos.")
        except Exception as e:
            st.error(f"Ocurrió un error durante la transcripción: {e}")

if __name__ == "__main__":
    main()
