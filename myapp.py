import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import streamlit as st

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Function to preprocess and tokenize the text
def preprocess_text(text):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Tokenize the sentences into words
    words = [word_tokenize(sentence) for sentence in sentences]
    
    # Remove stopwords and convert words to lowercase
    stop_words = set(stopwords.words('english'))
    words = [[word.lower() for word in sentence if word.lower() not in stop_words] for sentence in words]
    
    return words, sentences

# Function to generate a summary from the preprocessed text
def generate_summary(words, sentences, num_sentences=3):
    # Calculate the frequency of each word
    word_frequencies = {}
    for sentence in words:
        for word in sentence:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    
    # Assign scores to sentences based on word frequencies
    sentence_scores = {}
    for i, sentence in enumerate(words):
        for word in sentence:
            if word in word_frequencies:
                if i not in sentence_scores:
                    sentence_scores[i] = word_frequencies[word]
                else:
                    sentence_scores[i] += word_frequencies[word]
    
    # Get the top N sentences with the highest scores
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    
    # Join the top sentences to form the summary
    summary = ' '.join([sentences[i] for i in top_sentences])
    
    return summary

# Streamlit application
st.title('Text Summarization Tool')

# Text input
text = st.text_area('Enter Text')

# Generate summary
if st.button('Generate Summary') and text:
    # Preprocess the text
    words, sentences = preprocess_text(text)
    
    # Generate the summary
    summary = generate_summary(words, sentences)
    
    # Display the summary
    st.subheader('Summary')
    st.write(summary)
