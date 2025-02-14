import streamlit as st
from google.cloud import texttospeech_v1 as tts
import io
import base64
import re
import os


def text_to_speech(text, voice_name="en-US-Neural2-J", speaking_rate=1.0, pitch=0.0, file_name="output", file_extension=".wav"):
    """Converts text to speech, handling long texts, displaying progress, and returning audio chunks."""
    try:
        client = tts.TextToSpeechClient()
        voice = tts.VoiceSelectionParams(
            language_code="en-US",
            name=voice_name
        )
        audio_config = tts.AudioConfig(
            audio_encoding=tts.AudioEncoding.LINEAR16,
            speaking_rate=speaking_rate,
            pitch=pitch
        )

        chunks = split_text(text)
        audio_chunks = []

        for i, chunk in enumerate(chunks):
            synthesis_input = tts.SynthesisInput(text=chunk)
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            audio_chunk = io.BytesIO(response.audio_content)
            audio_chunk.seek(0)
            audio_chunks.append(audio_chunk)

            # Display progress and audio player *immediately* after processing each chunk
            with st.expander(f"Processed chunk {i+1} of {len(chunks)}"): # Use st.expander
                st.write(chunk)  # Show full chunk text inside expander

            # Use f-string for dynamic filename
            download_filename = f"{file_name}_Part{i+1:03}{file_extension.replace('txt', 'wav')}"
            st.subheader(download_filename) # Display the filename
            st.audio(audio_chunk, format="audio/wav")  # Display audio player

            # Create download link
            b64 = base64.b64encode(audio_chunk.getvalue()).decode()
            href = f'<a download="{download_filename}" href="data:audio/wav;base64,{b64}">Download {download_filename}</a>'
            st.markdown(href, unsafe_allow_html=True)

        return audio_chunks

    except Exception as e:
        st.error(f"Text-to-Speech Error: {e}")
        return None

def split_text(text, max_bytes=4500):
    """Splits text into chunks, same as before."""
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(?=[A-Z]|\s)', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len((current_chunk + sentence).encode('utf-8')) < max_bytes:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())

    if not chunks:
        words = text.split()
        current_chunk = ""
        for word in words:
            if len((current_chunk + word).encode('utf-8')) < max_bytes:
                current_chunk += word + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = word + " "
        if current_chunk:
            chunks.append(current_chunk.strip())
    return chunks



def main():
    st.title("Text to Speech")
    uploaded_file = st.file_uploader("Choose a text file", type="txt")

    if uploaded_file is not None:
        # Get filename and extension
        file_name, file_extension = os.path.splitext(uploaded_file.name)

        text = uploaded_file.read().decode("utf-8", errors="replace")

        st.header("Original Text (First 500 Characters):")
        st.write(text[:500] + ("..." if len(text) > 500 else ""))

        with st.expander("Advanced Options"):
            voice_name = st.selectbox("Voice", options=[
                "en-US-Neural2-J", "en-US-Neural2-C", "en-US-Neural2-D", "en-US-Neural2-F",
                "en-GB-Neural2-A", "en-GB-Neural2-B", "en-GB-Neural2-C", "en-GB-Neural2-D", "en-GB-Neural2-F",
                "fr-FR-Neural2-A", "fr-FR-Neural2-B", "fr-FR-Neural2-C", "fr-FR-Neural2-D", "fr-FR-Neural2-E",
                "es-ES-Neural2-A", "es-ES-Neural2-B", "es-ES-Neural2-C", "es-ES-Neural2-D", "es-ES-Neural2-F",
            ], index=0)
            speaking_rate = st.slider("Speaking Rate", 0.25, 4.0, 1.0)
            pitch = st.slider("Pitch", -20.0, 20.0, 0.0)

        if st.button("Generate Audio"):
            if not text:
                st.warning("Please upload a text file first.")
            else:
                with st.spinner("Generating Audio..."):
                    # Pass file_name and file_extension to text_to_speech
                    audio_chunks = text_to_speech(text, voice_name, speaking_rate, pitch, file_name, file_extension)

                if audio_chunks:
                    # No longer need to loop here, as everything's handled inside text_to_speech.
                    pass  # Or remove this if block entirely, as it's now empty
                else:
                    st.error("Audio generation failed.")

        # Cost warning in red
        st.markdown("<p style='color:red;'>**Important:** Using the Text-to-Speech API incurs costs. See <a href='https://cloud.google.com/text-to-speech/pricing'>pricing</a>.</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    **Important Notes:**

    *   **Google Cloud Project:** You need a Google Cloud project with the Text-to-Speech API enabled.  Make sure billing is enabled.
    *   **Authentication:** This app expects Application Default Credentials (ADC).  Run `gcloud auth application-default login`. For deployment, use a service account key (see below).
    *   **Service Account Key (for deployment):** Create a service account, grant "Cloud Text-to-Speech API Admin" role, and create a JSON key.  In Streamlit secrets, add a secret named `GOOGLE_APPLICATION_CREDENTIALS` and paste the JSON key's contents.
    *   **Large Files**: Generating audio for large files can be slow and expensive. Chunking is implemented to handle this.
    *   **Encoding**: Assumes UTF-8.
    """)

if __name__ == "__main__":
    main()
