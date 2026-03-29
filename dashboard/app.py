import streamlit as st
import requests

API_URL = "https://ai-recommendation-system-fastapi.onrender.com"
st.set_page_config(page_title="Movie Recommender", page_icon="🎬",layout="wide")
st.title("🎬 AI Movie Recommender")
st.markdown("Find similar movies instantly using AI")

#Search Box
query = st.text_input("Search Movie")
#Auto Suggestion
if query:
    res = requests.get(f"{API_URL}/search",params={"query":query})
    suggestions = res.json()
    selected_movie = st.selectbox("Suggestions",suggestions)
    if st.button("Recommend"):
        response = requests.post(
            f"{API_URL}/recommend",
            json={"title":selected_movie}
        )
        data = response.json()
        st.subheader(f"Recommendations for {data['input_movie']}")
        st.divider()
        movies = data.get("recommendations",[])
        #Display Cards
        if not movies:
            st.warning("!!!No recommendations found")
        else:
            #Grid layout 3 column
            cols = st.columns(3)
            for i, movie in enumerate(movies):
                with cols[i%3]:
                    if movie.get('poster'):
                        st.image(movie['poster'])
                    st.markdown(f"###{movie['title'].title()}")
                    st.write(f"⭐ Score: {movie['score']}")
                    
st.divider()
st.caption("Have a good day to you <3")
