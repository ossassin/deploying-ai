I created OpenCoach as a personal career coach. His name is Eames and he helps with all your career questions!

1. Feature 1: N/A 
2. Feature 2: I used a RAG with embeddings of an MIT article on "How to Create a Career Plan". This is what I used for my semantic search requirement
3. Feature 3: N/A

Instructions:
1. You will need to use my chroma.sqlite3 file to import the embeddings into your docker at http://localhost:8000. Or you may create the embeddings again using the embedder.py file
2. Run the app.py file in your terminal.
3. Use the link generated in the terminal to use the chat in your browser.

Other important notes:
- I was able to create chat history within Gradio!
- Users can also like or dislike the LLM output which can be used for fine-tuning later

Guardrails:
- I created a detailed system prompt stopping the user from changing the system prompt or talking about the forbidden topic
- I kept the prompt in the main, separate from the app.py. I'm not sure if that helps sandboxing the prompt a little bit.