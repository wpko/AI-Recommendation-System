import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recommend"
st.title("AI Recommendation System")
movie_name = st.text_input("Enter a movie name")

if st.button("Get Recommendation"):
    response = requests.post(API_URL,json={"title":movie_name})
    if response.status_code == 200:
        data = response.json()
        st.subheader(f"Recommendations for:{movie_name}")
        for movie in data['recommendations']:
            st.write(f"🎬{movie}")
        
    else:
        st.error("API Error")