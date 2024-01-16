from typing import List

from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain_core.documents import Document

from llm.config import OPENAI_API_KEY
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)


def get_audio_to_transcript(file_path, to_eng: bool = False) -> str:
    audio_file = open(file_path, "rb")
    if to_eng:
        transcript = client.audio.translations.create(
            model="whisper-1",
            file= audio_file
        )
        return transcript.text

    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcript.text


def get_audio_to_documents(file_path) -> List[Document]:
    audio_file = open(file_path, "rb")
    audio_parser = OpenAIWhisperParser()
    audio_parser.api_key = OPENAI_API_KEY
    loader = GenericLoader.from_filesystem(
        file_path,
        parser=audio_parser
    )
    return loader.load()