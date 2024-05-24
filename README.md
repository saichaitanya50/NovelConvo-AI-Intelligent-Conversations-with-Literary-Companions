# NovelConvo AI-Intelligent-Conversations-with-Literary-Companions

**NovelConvo AI - A Literary Chat Experience**

**Overview:**
NovelConvo AI is an innovative Q/A and chat system tailored for classic book enthusiasts. It features ten iconic novels, including "The Adventures of Sherlock Holmes," sourced from Project Gutenberg. Powered by Chatterbot and advanced language models, the system intelligently engages users in literary conversations, even deducing the novel in question. The core is a Q/A bot utilizing Information Retrieval and RAG generative models. Exception handling ensures a smooth user experience, while the user-friendly web app offers detailed chat analytics and visualizations.


## Architecture Overview
![Architecture](artifacts/architecture.png?raw=true "Architecture")

**Methodology:**
- **Novel Collection and Processing:**
  - Curated a diverse dataset from Project Gutenberg, applying text cleaning, tokenization, lemmatization, and metadata extraction.
  - Created a structured data format for efficient processing and content filtering.
- **Language Model Integration:**
  - Integrated Chatterbot, enhancing its capabilities with diverse datasets for natural and contextually relevant dialogues.
- **Novel and Prompt Classification:**
  - Utilized DeBERTa-v3-large-mnli-fever-anli-ling-wanli to classify novels and prompts, streamlining user interactions.
- **Information Retrieval System:**
  - Inverted Index using Linked Lists and Flask in Python. It allows for efficient Boolean queries using a Document-at-a-time (DAAT) strategy, ideal for understanding Information Retrieval concepts.
- **Q/A Bot Configuration:**
  - Implemented an Information Retrieval System and RAG generative model for coherent and context-aware answers.
- **Exception Handling:**
  - Routed unresolved queries to the RAG Large Language Model for comprehensive responses.
  - Prompted users to refine queries or change filters for novel-related questions.
- **User Interface Design:**
  - Developed a user-friendly ReactJS web app, allowing asynchronous API calls for seamless interaction.

**Testing and Iteration:**
Rigorous testing and user feedback shaped iterative improvements, ensuring a robust and user-friendly system.

**Conclusion:**
NovelConvo AI blends classic literature with cutting-edge technology, providing precise answers and engaging conversations. The platform intelligently identifies novels and handles complex inquiries, promising an enriched reading experience. The user-friendly system is poised for growth, driven by team dedication and user feedback, offering exciting possibilities at the intersection of books and technology.

**References:**
- [Chatbot Designer Free Course](https://www.chatbot.com/academy/chatbot-designer-free-course/error-messages/)
- [Python Documentation on Errors](https://docs.python.org/3/tutorial/errors.html)
- [Chatterbot Documentation](https://chatterbot.readthedocs.io/en/stable/)
- [Chit-chat Dataset](https://github.com/BYU-PCCL/chitchat-dataset)
- [Project Gutenberg](https://www.gutenberg.org/)
- [Hugging Face](https://huggingface.co)
- [ReactJS Documentation](https://legacy.reactjs.org/docs/getting-started.html)

