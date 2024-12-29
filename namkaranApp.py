import streamlit as st
import requests

# GitHub raw URL of the text file
GITHUB_URL = "https://raw.githubusercontent.com/Rigava/JobMaker/main/names.txt"

def load_names(url):
    """Fetches the content of a text file from the provided URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        names = response.text.splitlines()
        return names
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the file: {e}")
        return []

# Load the names from the GitHub repo
names = load_names(GITHUB_URL)

# Streamlit App UI
st.title("Name Selector")

if names:
    # Allow the user to input words to search for in the names
    search_words = st.text_input("Enter words to search for (comma-separated):", "")

    if search_words:
        # Process the input words
        words = [word.strip().lower() for word in search_words.split(",")]

        # Filter names that contain any of the selected words
        matching_names = [name for name in names if any(word in name.lower() for word in words)]

        if matching_names:
            st.write("### Matching Names:")
            st.write(matching_names)
        else:
            st.write("No matching names found.")
    else:
        st.write("Please enter words to search for.")
else:
    st.write("Could not load names from the GitHub repository. Please check the URL.")
