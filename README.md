# Zen

LangChain-Powered AI Assistant with Streamlit
This is a Streamlit-powered AI assistant that utilizes LangChain and OpenAI’s API to process user queries intelligently. The app classifies input into three categories:
- Text-based questions handled via OpenAI’s language model.
- Image-related requests, generating creative descriptions.
- Code-related inquiries, providing helpful coding suggestions.
Users can interact through a sleek Streamlit UI, making it easy to query the AI assistant in real-time. Perfect for chatbots, AI-powered Q&A apps, or educational tools! 🚀
Features
✅ Natural language processing via LangChain
✅ Smart input classification (text, image, or code)
✅ Streamlit-based UI for seamless interaction
✅ Live query handling using OpenAI’s API

How to Run
1. Clone the repository:
```bash
git clone <your-repo-url>
cd <repo-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

# Project Structure
your-project/
├── main_app.py          # Main Streamlit app (what Streamlit Cloud runs)
├── chains/
│   ├── __init__.py
│   ├── factual_chain.py    # Low temp factual responses
│   ├── engagement_chain.py # High temp engagement
│   └── psycho_analysis.py  # Future psycholinguistic analysis
├── prompts/
│   ├── __init__.py
│   └── sen_prompts.py      # All your prompt templates
└── requirements.txt
