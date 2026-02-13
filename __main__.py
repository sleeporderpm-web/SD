# Create a working directory structure for Streamlit Cloud
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main app
if __name__ == "__main__":
    import streamlit
    streamlit.run("streamlit_app.py")
