import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

du_lieu = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/movies.csv")
du_lieu.info()
du_lieu.duplicated()
du_lieu.count()
du_lieu.dropna()

danh_sach_nam = du_lieu['year'].unique().tolist()
diem_danh_gia = du_lieu['score'].unique().tolist()
danh_sach_the_loai = du_lieu['genre'].unique().tolist()
chon_cot = du_lieu.loc[:, ["name", "genre", "year"]]

st.set_page_config(page_title = "Streamlit",layout = 'wide')
st.header("Interactive Dashboard")
st.subheader("Interact with this dashboard using the widgets on the sidebar")

with st.sidebar:
    st.write('Select a range on the slider (it represents movie score) to view the total number of movies in a genre that falls within that range')
    khoang_diem = st.slider(label='Choose a value:',min_value=1.00,max_value=10.00,value= (3.00, 4.00))

    st.write('Select your preferred genre(s) and year to view the movies released that year and on that genre')
    chon_the_loai = st.multiselect('Choose Genre:',danh_sach_the_loai, default = ['Animation', 'Horror', 'Fantasy', 'Romance'])

    chon_nam = st.selectbox('Choose a Year:', danh_sach_nam, 0)

neu_diem = (du_lieu['score'].between(*khoang_diem))

chon_nam = [chon_nam]

the_loai_nam = (du_lieu['genre'].isin(chon_the_loai)) & (du_lieu['year'].isin(chon_nam))


movies_columns, score_columns = st.columns([2, 3])
with movies_columns:
    st.write("#### Lists of movies filtered by year and Genre ")
    dataframe_genre_year = du_lieu[the_loai_nam].groupby(['name', 'genre'])['year'].sum()
    dataframe_genre_year = dataframe_genre_year.reset_index()
    st.dataframe(dataframe_genre_year, width=400)

with score_columns:
    st.write("#### User score of movies and their genre ")
    rating_count_year = du_lieu[neu_diem].groupby('genre')['score'].count()
    rating_count_year = rating_count_year.reset_index()
    figpx = px.line(rating_count_year, x = 'genre', y = 'score')
    st.plotly_chart(figpx)

st.write("Average Movie Budget, Grouped by Genre")
avg_budget = du_lieu.groupby('genre')['budget'].mean().round()
avg_budget = avg_budget.reset_index()
genre = avg_budget['genre']
avg_bud = avg_budget['budget']
fig = plt.figure(figsize = (19, 10))
plt.bar(genre, avg_bud, color = 'maroon')
plt.xlabel('genre')
plt.ylabel('budget')
plt.title('Matplotlib Bar Chart Showing The Average Budget of Movies in Each Genre')
st.pyplot(fig)
hide_st_style = """
            <style>
            #github-link {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
