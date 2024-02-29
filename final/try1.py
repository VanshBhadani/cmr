import streamlit as st
from PIL import Image
from datetime import date
from gtts import gTTS, lang
from googletrans import Translator
import PyPDF2

# Constants for file names
USER_DETECT_AUDIO_FILE = "user_detect.mp3"
USER_TRANS_AUDIO_FILE = "user_trans.mp3"
TRANSLATED_PDF_AUDIO_FILE = "translated_pdf.mp3"

def get_key(val):
    for key, value in lang.tts_langs().items():
        if val == value:
            return key

def convert_to_audio(text, lang, file_name):
    audio = gTTS(text=text, lang=lang, slow=False)
    audio.save(file_name)
    with open(file_name, "rb") as file:
        return file.read()

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def translate_pdf_text(pdf_text, dest_lang):
    translator = Translator()
    translation = translator.translate(pdf_text, dest=dest_lang)
    return translation.text

def main():
    trans = Translator()
    langs = lang.tts_langs()

    st.set_page_config(page_title="test1", page_icon="🎯")
    st.header("Translate your thoughts.")
    st.write(f"Date: {date.today()}")

    input_text = st.text_input("Enter whatever")
    lang_choice = st.selectbox(
        "Language to translate: ", list(langs.values())
    )

    if st.button("Translate"):
        if input_text == "":
            st.write("Please Enter text to translate")
        else:
            detect_expander = st.expander("Detected Language")
            with detect_expander:
                detect = trans.detect([input_text])[0]
                detect_text = f"Detected Language: {langs[detect.lang]}"
                st.success(detect_text)
                detect_audio_bytes = convert_to_audio(input_text, detect.lang, USER_DETECT_AUDIO_FILE)
                st.audio(detect_audio_bytes, format="audio/mpeg", start_time=0)

            trans_expander = st.expander("Translated Text")
            with trans_expander:
                translation = trans.translate(input_text, dest=get_key(lang_choice))
                translation_text = f"Translated Text: {translation.text}"
                st.success(translation_text)
                translated_audio_bytes = convert_to_audio(translation.text, get_key(lang_choice), USER_TRANS_AUDIO_FILE)
                st.audio(translated_audio_bytes, format="audio/mpeg", start_time=0)

                with open(USER_TRANS_AUDIO_FILE, "rb") as file:
                    st.download_button(
                        label="Download",
                        data=file,
                        file_name="trans.mp3",
                        mime="audio/mpeg",
                    )

    uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])

    if uploaded_file is not None:        
        pdf_text = read_pdf(uploaded_file)
        st.subheader("PDF Text:")
        st.write(pdf_text)

        lang_choice_pdf = st.selectbox(
            "Language to translate PDF text: ", list(langs.values())
        )

        if st.button("Translate PDF Text"):
            if not pdf_text:
                st.warning("The PDF does not contain any text.")
            else:
                translated_pdf_text = translate_pdf_text(pdf_text, get_key(lang_choice_pdf))
                st.subheader("Translated PDF Text:")
                st.success(translated_pdf_text)

                translated_pdf_audio_bytes = convert_to_audio(translated_pdf_text, get_key(lang_choice_pdf), TRANSLATED_PDF_AUDIO_FILE)
                st.audio(translated_pdf_audio_bytes, format="audio/mpeg", start_time=0)

                with open(TRANSLATED_PDF_AUDIO_FILE, "rb") as file_pdf:
                    st.download_button(
                        label="Download Translated PDF",
                        data=file_pdf,
                        file_name="translated_pdf.mp3",
                        mime="audio/mpeg",
                    )

if __name__ == "__main__":
    main()
