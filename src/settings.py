import fnmatch
import re

# Import necessary loader classes
from langchain.document_loaders import (
    CSVLoader,
    Docx2txtLoader,
    JSONLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredExcelLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredPowerPointLoader,
)

FILE_TYPE_MAPPINGS_LANGCHAIN = {
    re.compile(fnmatch.translate(pattern)): loader_class
    for pattern, loader_class in {
        "*.txt": TextLoader,
        "*.pdf": PyPDFLoader,
        "*.csv": CSVLoader,
        "*.docx": Docx2txtLoader,
        "*.xlss": UnstructuredExcelLoader,
        "*.xlsx": UnstructuredExcelLoader,
        "*.html": UnstructuredHTMLLoader,
        "*.pptx": UnstructuredPowerPointLoader,
        "*.ppt": UnstructuredPowerPointLoader,
        "*.md": UnstructuredMarkdownLoader,
        "*.json": JSONLoader,
    }.items()
}

MODEL_PREFIX_TO_ENCODING: dict[str, str] = {
    # chat
    "gpt-4-": "cl100k_base",  # e.g., gpt-4-0314, etc., plus gpt-4-32k
    "gpt-3.5-turbo-": "cl100k_base",  # e.g, gpt-3.5-turbo-0301, -0401, etc.
    "gpt-35-turbo-": "cl100k_base",  # Azure deployment name
    # fine-tuned
    "ft:gpt-4": "cl100k_base",
    "ft:gpt-3.5-turbo": "cl100k_base",
    "ft:davinci-002": "cl100k_base",
    "ft:babbage-002": "cl100k_base",
}

MODEL_TO_ENCODING: dict[str, str] = {
    # chat
    "gpt-4": "cl100k_base",
    "gpt-3.5-turbo": "cl100k_base",
    "gpt-35-turbo": "cl100k_base",  # Azure deployment name
    # base
    "davinci-002": "cl100k_base",
    "babbage-002": "cl100k_base",
    # embeddings
    "text-embedding-ada-002": "cl100k_base",
    # DEPRECATED MODELS
    # text (DEPRECATED)
    "text-davinci-003": "p50k_base",
    "text-davinci-002": "p50k_base",
    "text-davinci-001": "r50k_base",
    "text-curie-001": "r50k_base",
    "text-babbage-001": "r50k_base",
    "text-ada-001": "r50k_base",
    "davinci": "r50k_base",
    "curie": "r50k_base",
    "babbage": "r50k_base",
    "ada": "r50k_base",
    # code (DEPRECATED)
    "code-davinci-002": "p50k_base",
    "code-davinci-001": "p50k_base",
    "code-cushman-002": "p50k_base",
    "code-cushman-001": "p50k_base",
    "davinci-codex": "p50k_base",
    "cushman-codex": "p50k_base",
    # edit (DEPRECATED)
    "text-davinci-edit-001": "p50k_edit",
    "code-davinci-edit-001": "p50k_edit",
    # old embeddings (DEPRECATED)
    "text-similarity-davinci-001": "r50k_base",
    "text-similarity-curie-001": "r50k_base",
    "text-similarity-babbage-001": "r50k_base",
    "text-similarity-ada-001": "r50k_base",
    "text-search-davinci-doc-001": "r50k_base",
    "text-search-curie-doc-001": "r50k_base",
    "text-search-babbage-doc-001": "r50k_base",
    "text-search-ada-doc-001": "r50k_base",
    "code-search-babbage-code-001": "r50k_base",
    "code-search-ada-code-001": "r50k_base",
    # open source
    "gpt2": "gpt2",
}


def encoding_name_for_model(model_name: str) -> str:
    """Returns the name of the encoding used by a model.

    Raises a KeyError if the model name is not recognised.
    """
    encoding_name = None
    if model_name in MODEL_TO_ENCODING:
        encoding_name = MODEL_TO_ENCODING[model_name]
    else:
        # Check if the model matches a known prefix
        # Prefix matching avoids needing library updates for every model version release
        # Note that this can match on non-existent models (e.g., gpt-3.5-turbo-FAKE)
        for model_prefix, model_encoding_name in MODEL_PREFIX_TO_ENCODING.items():
            if model_name.startswith(model_prefix):
                return model_encoding_name

    if encoding_name is None:
        raise KeyError(
            f"Could not automatically map {model_name} to a tokeniser. "
            "Please use `tiktoken.get_encoding` to explicitly get the tokeniser you expect."
        ) from None

    return encoding_name
