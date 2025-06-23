import os
from tinyllama import Llama, LlamaConfig

# Path to your TinyLlama model files
MODEL_PATH = os.getenv('TINYLLAMA_MODEL_PATH', './models/llama-7B')

# Initialize once at import time
def _load_model():
    config = LlamaConfig(
        path=MODEL_PATH,
        # tweak these settings as needed
        max_seq_len=512,
        dtype="fp16",
        gpu=True
    )
    return Llama(config)

_llm = _load_model()


def llama_generate(prompt: str, **kwargs) -> str:
    """
    Generate text using TinyLlama local model.

    :param prompt: The input prompt string.
    :param kwargs: Additional generation parameters.
    :return: Generated text.
    """
    # Default generation settings
    settings = {
        'max_length': kwargs.get('max_length', 128),
        'temperature': kwargs.get('temperature', 0.7),
        'top_k': kwargs.get('top_k', 40),
    }
    output = _llm.generate([prompt], **settings)
    # output[0] contains the generated continuation
    return output[0]