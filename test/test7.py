import streamlit as st
from datetime import date
from gtts import gTTS, lang
from googletrans import Translator
import PyPDF2

# setting app's title, icon & layout
st.set_page_config(page_title="test7", page_icon="🎯")

def get_key(val):
    """function to find the key of the given value in the dict object

    Args:
        val (str): value to find key

    Returns:
        key(str): key for the given value
    """
    for key, value in lang.tts_langs().items():
        if val == value:
            return key

def read_pdf(file):
    """Reads a PDF file and extracts text from it.

    Args:
        file (BytesIO): BytesIO object representing the uploaded PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def translate_pdf_text(pdf_text, dest_lang):
    """Translates text extracted from a PDF to the specified destination language.

    Args:
        pdf_text (str): Text extracted from the PDF.
        dest_lang (str): Destination language for translation.

    Returns:
        str: Translated text.
    """
    translator = Translator()

    # Split the text into paragraphs
    paragraphs = pdf_text.split("\n\n")

    # Translate each paragraph and combine the results
    translated_paragraphs = []
    for paragraph in paragraphs:
        # Split the paragraph into chunks of 100 characters
        chunk_size = 100
        chunks = [paragraph[i:i+chunk_size] for i in range(0, len(paragraph), chunk_size)]

        # Translate each chunk and combine the results
        translated_text_chunks = []
        for chunk in chunks:
            translation = translator.translate(chunk, dest=dest_lang)
            translated_text_chunks.append(translation.text)

        # Combine the translated chunks
        translated_paragraph = " ".join(translated_text_chunks)
        translated_paragraphs.append(translated_paragraph)

    # Combine the translated paragraphs
    translated_text = "\n\n".join(translated_paragraphs)

    return translated_text

def main():
    # instance of Translator()
    trans = Translator()

    # gets gtts supported languages as dict
    langs = lang.tts_langs()  # Corrected variable name

    # display current date & header
    st.header("Translate your thoughts.")
    st.write(f"Date : {date.today()}")

    input_text = st.text_input("Enter whatever")  # gets text to translate
    lang_choice = st.selectbox(
        "Language to translate: ", list(langs.values())
    )  # shows the supported languages list as selectbox options

    if st.button("Translate"):
        if input_text == "":
            # if the user input is empty
            st.write("Please Enter text to translate")
        else:
            detect_expander = st.expander("Detected Language")
            with detect_expander:
                detect = trans.detect([input_text])[
                    0
                ]  # detect the user given text language
                detect_text = f"Detected Language : {langs[detect.lang]}"
                st.success(detect_text)  # displays the detected language

                # convert the detected text to audio file
                detect_audio = gTTS(text=input_text, lang=detect.lang, slow=False)
                detect_audio.save("user_detect.mp3")
                audio_file = open("user_detect.mp3", "rb")
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/ogg", start_time=0)

            trans_expander = st.expander("Translated Text")
            with trans_expander:
                translation = trans.translate(
                    input_text, dest=get_key(lang_choice)
                )  # translates user given text to target language
                translation_text = f"Translated Text : {translation.text}"
                st.success(translation_text)  # displays the translated text

                # convert the translated text to audio file
                translated_audio = gTTS(
                    text=translation.text, lang=get_key(lang_choice), slow=False
                )
                translated_audio.save("user_trans.mp3")
                audio_file = open("user_trans.mp3", "rb")
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/ogg", start_time=0)

                # download button to download translated audio file
                with open("user_trans.mp3", "rb") as file:
                    st.download_button(
                        label="Download",
                        data=file,
                        file_name="trans.mp3",
                        mime="audio/ogg",
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

                # Convert the translated PDF text to audio file
                translated_pdf_audio = gTTS(
                    text=translated_pdf_text,
                    lang=get_key(lang_choice_pdf),
                    slow=False
                )
                translated_pdf_audio.save("translated_pdf.mp3")
                audio_file_pdf = open("translated_pdf.mp3", "rb")
                audio_bytes_pdf = audio_file_pdf.read()
                st.audio(audio_bytes_pdf, format="audio/ogg", start_time=0)

                # Download button to download translated audio file
                with open("translated_pdf.mp3", "rb") as file:
                    st.download_button(
                        label="Download",
                        data=file,
                        file_name="translated_pdf.mp3",
                        mime="audio/ogg",
                    )

if __name__ == "__main__":
    main()
