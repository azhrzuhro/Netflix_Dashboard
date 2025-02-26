import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import urllib.request
from urllib.error import HTTPError, URLError

# Reading the CSV file
data = 'data/cleaned_data.csv'

try:
    df = pd.read_csv(data)
except HTTPError as e:
    st.error(f'HTTP Error: {e.code} - {e.reason}')
    st.stop()
except URLError as e:
    st.error(f'URL Error: {e.reason}')
    st.stop()
except Exception as e:
    st.error(f'An unexpected error occurred: {e}')
    st.stop()

# Ensure all genre values are in lowercase
df['genre'] = df['genre'].str.lower()

# Dashboard title
st.title("Netflix Streaming Dashboard")

# Netflix logo
try:
    img = Image.open('image/Netflix Logo.png')
    st.sidebar.image(img)
except FileNotFoundError:
    st.sidebar.warning("Netflix Logo.png not found. Please ensure the file is in the directory.")
    
# Sidebar for page selection
page = st.sidebar.selectbox("Choose The Page", ["Genre Distribution", "The Most Top Show of Netflix", "Descriptive Statistics"])

if page == "Genre Distribution":
    # List all unique genres
    all_genres = df['genre'].str.split(',').explode().str.strip().unique()
    all_genres = sorted(set(all_genres))  # Sort and remove duplicates
    
    # Dropdown for selecting a genre
    selected_genre = st.sidebar.selectbox("Select Genre", all_genres)
    
    # Filter the DataFrame based on the selected genre
    filtered_df = df[df['genre'].str.contains(selected_genre, case=False, na=False)]

    # Remove duplicate titles
    filtered_df = filtered_df.drop_duplicates(subset='title')
    
    # Displaying genre distribution for the selected genre
    st.subheader(f"Top 10 Shows in {selected_genre.capitalize()} Genre")

    # Get the top 10 shows based on votes
    top_10_shows = filtered_df.sort_values(by='votes', ascending=False).head(10)

    # Visualization of top 10 shows
    fig = px.bar(
        top_10_shows,
        x='votes',
        y='title',
        color='votes',
        color_continuous_scale='reds',
        title=f'Top 10 Shows in {selected_genre.capitalize()} Genre',
        labels={'votes': 'Votes', 'title': 'Show Title'},
        text='votes'
    )
    fig.update_layout(
        yaxis_title='Show Title',
        xaxis_title='Votes',
        yaxis=dict(
            tickmode='array',
            tickvals=top_10_shows['title'],
            ticktext=[t if len(t) <= 50 else t[:47] + '...' for t in top_10_shows['title']],
            autorange='reversed'
        ),
        xaxis=dict(tickformat=',')
    )
    
    # Adjusting y-axis to rotate labels
    fig.update_yaxes(tickangle=-45)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Displaying the top 10 shows table
    st.table(top_10_shows[['title', 'year', 'rating', 'votes']].reset_index(drop=True))

elif page == "The Most Top Show of Netflix":
    # Most Streamed visualization options
    statistic_option = st.sidebar.selectbox(
        "Choose The Statistics",
        ["Top 10 Most Streamed", "Top 10 Most Popular"]
    )

    if statistic_option == "Top 10 Most Streamed":
        # Remove duplicate titles
        df_no_duplicates = df.drop_duplicates(subset='title')
        
        # Sort by 'votes' and get the top 10 shows
        top_10_streamed = df_no_duplicates.sort_values(by='votes', ascending=False).head(10)

        st.subheader("Top 10 Most Streamed Netflix Shows")
        
        # Visualization of the top 10 streamed shows
        fig = px.bar(
            top_10_streamed,
            x='votes',
            y='title',
            color='votes',
            color_continuous_scale='reds',
            title='Top 10 Most Streamed Netflix Shows',
            labels={'votes': 'Votes', 'title': 'Show Title'},
            text='votes'
        )
        fig.update_layout(
            yaxis_title='Show Title',
            xaxis_title='Votes',
            yaxis=dict(
                tickmode='array',
                tickvals=top_10_streamed['title'],
                ticktext=[t if len(t) <= 50 else t[:47] + '...' for t in top_10_streamed['title']],
                autorange='reversed'
            ),
            xaxis=dict(tickformat=',')
        )
    
        # Adjusting y-axis to rotate labels
        fig.update_yaxes(tickangle=-45)
    
        st.plotly_chart(fig, use_container_width=True)
        
        # Displaying the top 10 shows table
        st.table(top_10_streamed[['title', 'genre', 'year', 'votes']].reset_index(drop=True))

    elif statistic_option == "Top 10 Most Popular":
        # Remove duplicate titles
        df_no_duplicates = df.drop_duplicates(subset='title')
        
        # Sort by 'rating' and get the top 10 shows
        top_10_popular = df_no_duplicates.sort_values(by='rating', ascending=False).head(10)

        st.subheader("Top 10 Most Popular Netflix Shows")
    
        # Visualization of the top 10 popular shows
        fig = px.bar(
            top_10_popular,
            x='rating',
            y='title',
            color='rating',
            color_continuous_scale='reds',
            title='Top 10 Most Popular Netflix Shows',
            labels={'rating': 'Rating', 'title': 'Show Title'},
            text='rating'
        )
        fig.update_layout(
            xaxis_title='Rating',
            yaxis_title='Show Title',
            yaxis=dict(autorange='reversed')  # Reversing the y-axis to maintain order
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Displaying the top 10 shows table
        st.table(top_10_popular[['title', 'genre', 'year', 'rating']].reset_index(drop=True))

elif page == "Descriptive Statistics":
    st.subheader("Descriptive Statistics")

    # Calculating descriptive statistics
    descriptive_stats = df[['rating', 'votes']].describe().transpose()
    
    # Displaying descriptive statistics
    st.write(descriptive_stats)

    # Displaying histogram distribution of 'votes' and 'rating'
    st.subheader("Distribution of Votes")
    fig_votes = px.histogram(df, x='votes', nbins=30, title='Distribution of Votes', color_discrete_sequence=['#800000'])  # Maroon
    st.plotly_chart(fig_votes, use_container_width=True)

    st.subheader("Distribution of Ratings")
    fig_ratings = px.histogram(df, x='rating', nbins=30, title='Distribution of Ratings', color_discrete_sequence=['#800000'])  # Maroon
    st.plotly_chart(fig_ratings, use_container_width=True)
