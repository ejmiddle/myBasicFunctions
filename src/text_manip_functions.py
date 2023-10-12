import openai
import tiktoken


def translate_text(text, source_language, target_language):
    prompt = f"Translate the following text from '{source_language}' to '{target_language}': {text}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates text."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.01,
    )

    translation = response.choices[0].message.content.strip()
    return translation


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(string))
    return num_tokens


def split_text(text, chunk_size=4900, overlap=100):
    """
    Split the text into overlapping chunks.

    Parameters:
    text (str): The text to be split
    chunk_size (int): The maximum size of each chunk
    overlap (int): The number of overlapping characters between each chunk
    
    Returns:
    list: A list of strings representing each chunk
    """
    
    chunks = []
    text_length = len(text)
    
    for i in range(0, text_length, chunk_size-overlap):
        # If it's the last chunk and it's smaller than the overlap
        if i + chunk_size > text_length:
            chunks.append(text[i:])
        else:
            chunks.append(text[i:i+chunk_size])
            
    return chunks
