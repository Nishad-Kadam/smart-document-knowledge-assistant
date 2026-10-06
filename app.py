import streamlit as st
import fitz
from google import genai
import math

if "messages" not in st.session_state:
    st.session_state.messages = []

# Gemini setup

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Split text into chunks

def split_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

# Create embedding

def get_embedding(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return result.embeddings[0].values

# Calculate similarity

def cosine_similarity(a, b):

    dot_product = sum(
        x * y for x, y in zip(a, b)
    )

    magnitude_a = math.sqrt(
        sum(x * x for x in a)
    )

    magnitude_b = math.sqrt(
        sum(x * x for x in b)
    )

    return dot_product / (
        magnitude_a * magnitude_b
    )

# Streamlit UI

st.title("📚 Smart Document Knowledge Assistant")
st.caption("Upload a document and ask questions based on its content.")

uploaded_file = st.file_uploader(
    "Upload your document",
    type=["pdf", "txt"],
    help="Supported formats: PDF and TXT"
)

if uploaded_file is not None:

    # Extract text

    text = ""

    if uploaded_file.type == "application/pdf":
        pdf = fitz.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        )

        for page in pdf:
            text += page.get_text()

    else:
        text = uploaded_file.read().decode("utf-8")

    # Split into chunks

    chunks = split_text(text)

    st.success(f"Document loaded successfully — {len(chunks)} chunks created.")

    # Create embeddings

    @st.cache_data
    def create_chunk_embeddings(chunks):

        embeddings = []

        for chunk in chunks:
            embedding = get_embedding(chunk)
            embeddings.append(embedding)

        return embeddings


    with st.spinner("Creating document embeddings..."):

        chunk_embeddings = create_chunk_embeddings(chunks)

    st.success("Document is ready! You can now ask questions.")
    
    # Ask a question

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

            if message["role"] == "assistant" and message["sources"]:

                st.write("**Referenced Document Chunks**")

                for source in message["sources"]:

                    st.write(
                        f"Chunk {source['index'] + 1}"
                    )

                    st.write(
                        f"Similarity score: {source['score']:.4f}"
                    )

                    st.write(
                        source["text"]
                    )

    question = st.chat_input(
        "Ask a question about your document..."
    )

    if question:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.write(question)

        # Create question embedding

        question_embedding = get_embedding(question)

        # Compare question with chunks

        results = []

        for i, chunk_embedding in enumerate(
            chunk_embeddings
        ):

            score = cosine_similarity(
                question_embedding,
                chunk_embedding
            )

            results.append(
                (score, i)
            )

        results.sort(
            reverse=True
        )

        # Take top 3 chunks

        top_results = results[:3]

        # Prepare context

        context = ""

        for rank, (score, index) in enumerate(
            top_results,
            start=1
        ):

            context += f"\nDocument Chunk {rank}:\n"
            context += chunks[index]
            context += "\n"

        # Ask Gemini

        prompt = f"""
        You are a document knowledge assistant.

        Answer the user's question using only the information
        provided in the document chunks below.

        Give a clear and helpful answer based on the document.
        Include the relevant details from the document instead of
        giving only a short one-line answer.

        Do not use information that is not present in the document.

        If the answer cannot be found in the provided document
        chunks, say exactly:
        "I could not find the answer in the uploaded document."

        Document chunks:
        {context}

        User question:
        {question}

        Answer:
        """        

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        # Display answer and sources

        answer = response.text

        if "I could not find the answer" in answer:
            sources = []
        else:
            sources = [
                {
                    "index": index,
                    "score": score,
                    "text": chunks[index]
                }
                for score, index in top_results
            ]

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources
            }
        )

        with st.chat_message("assistant"):
            st.write(answer)

        if sources:

            st.write("**Referenced Document Chunks**")

            for source in sources:

                st.write(
                    f"**Chunk {source['index'] + 1}** "
                    f"(Similarity: {source['score']:.4f})"
                )

                st.write(source["text"])

                st.divider()
