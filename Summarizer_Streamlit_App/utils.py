def sliding_window(text, window_size=512, overlap=128):
    chunks = []
    for i in range(0, len(text), window_size - overlap):
        chunks.append(text[i:i + window_size])
    return chunks