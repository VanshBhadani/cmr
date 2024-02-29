import streamlit as st
from datetime import date
from gtts import gTTS, lang
from translate import Translator  # Install using: pip install translate
import PyPDF2

st.set_page_config(page_title="test2", page_icon="🎯")

def get_key(val):
    for key, value in lang.tts_langs().items():
        if val == value:
            return key

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def translate_text(text, dest_lang):
    translator = Translator(to_lang=dest_lang)
    translation = translator.translate(text)
    return translation

def main():
    langs = lang.tts_langs()

    st.header("Translate your thoughts.")
    st.write(f"Date: {date.today()}")

    input_text = st.text_input("Enter text to translate")
    lang_choice = st.selectbox("Language to translate:", list(langs.values()))

    uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])

    if uploaded_file is not None:
        pdf_text = read_pdf(uploaded_file)
        st.subheader("PDF Text:")
        st.write(pdf_text)

        lang_choice_pdf = st.selectbox(
            "Language to translate PDF text:", list(langs.values())
        )

        if st.button("Translate PDF Text"):
            if not pdf_text:
                st.warning("The PDF does not contain any text.")
            else:
                translated_pdf_text = translate_text(pdf_text, get_key(lang_choice_pdf))
                st.subheader("Translated PDF Text:")
                st.success(translated_pdf_text)

                translated_pdf_audio = gTTS(
                    text=translated_pdf_text, lang=get_key(lang_choice_pdf), slow=False
                )
                translated_pdf_audio.save("translated_pdf.mp3")
                audio_file_pdf = open("translated_pdf.mp3", "rb")
                audio_bytes_pdf = audio_file_pdf.read()
                st.audio(audio_bytes_pdf, format="audio/ogg", start_time=0)

                with open("translated_pdf.mp3", "rb") as file_pdf:
                    st.download_button(
                        label="Download Translated PDF",
                        data=file_pdf,
                        file_name="translated_pdf.mp3",
                        mime="audio/ogg",
                    )

if __name__ == "__main__":
    main()
