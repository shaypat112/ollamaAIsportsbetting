import streamlit as st
import ollama

st.title("Shivang Patel Ollama Project")
st.title("BY Shivang Patel Written in Python")
st.badge("New", color="blue")
st.badge("Old", color="red")

def load_model():
    """Initialize Ollama client with error handling"""
    host = "http://localhost:11434"
    try:
        client = ollama.Client(host=host)
        # Test connection with a simple request
        test = client.list()
        return client
    except Exception as e:
        st.error(f"Failed to connect to Ollama server at {host}")
        st.error(f"Error details: {str(e)}")
        st.info("Make sure Ollama is running. Check with: `ollama list` in terminal")
        return None

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize client
client = load_model()

if client:
    # Get available models
    try:
        models_response = client.list()
        
        # Handle the ListResponse object - access models attribute directly
        if hasattr(models_response, 'models'):
            model_list = models_response.models
            model_names = [model.model for model in model_list]  # Use .model attribute
        else:
            model_names = []
        
        if model_names:
            st.success(f"Found {len(model_names)} models!")
            selected_model = st.sidebar.selectbox("Select Model", model_names)
        else:
            st.warning("No models found. Pull a model with: `ollama pull llama2`")
            st.info("Run this in your terminal: `ollama pull llama2` or `ollama pull mistral`")
            selected_model = None
    except Exception as e:
        st.error(f"Error listing models: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        selected_model = None

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        if selected_model:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = client.chat(
                            model=selected_model,
                            messages=st.session_state.messages
                        )
                        assistant_response = response['message']['content']
                        st.write(assistant_response)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": assistant_response
                        })
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")
        else:
            st.warning("Please select a model first")

    # Clear chat button
    if st.sidebar.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()