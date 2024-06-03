# -*- coding: utf-8 -*-
"""Survey Data Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Gr_RwxdK7WksZZraCxQmHQvTKIjZh3Ls
"""

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import io

def main():
    st.title("Survey Data Dashboard")

    # File upload widget
    uploaded_file = st.file_uploader("Upload CSV", type="csv")

    if uploaded_file is not None:
        # Read the uploaded CSV file
        data = pd.read_csv(uploaded_file)

        # Convert the timestamp to datetime and extract the date
        data['date'] = pd.to_datetime(data['timestamp'], format='%m/%d/%y %H:%M').dt.date

        # Define game days
        game_day_1 = pd.to_datetime('2024-05-14').date()
        game_day_2 = pd.to_datetime('2024-05-17').date()

        # Categorize the responses based on the date
        def categorize_date(date):
            if date > game_day_1 and date < game_day_2:
                return '2024-05-14'
            elif date >= game_day_2:
                return '2024-05-17'
            else:
                return None

        data['game_day'] = data['date'].apply(categorize_date)

        # Filter out rows with None game_day
        data = data.dropna(subset=['game_day'])

        # Convert rating column to integers
        data['choice_text'] = data['choice_text'].astype(int)

        # Create a dropdown for selecting a game day
        game_day = st.selectbox("Select Game Day", data['game_day'].unique())

        # Plot graphs and cumulative tables based on selected game day
        plot_data(data, game_day)

def plot_data(data, game_day):
    st.write(f"Game Day: {game_day}")

    filtered_data = data[data['game_day'] == game_day]
    questions = filtered_data['question'].unique()

    for question in questions:
        st.subheader(f'Question: {question}')
        question_data = filtered_data[filtered_data['question'] == question]

        # Generate bar chart using Matplotlib
        fig, ax = plt.subplots()
        question_data.groupby('choice_text').size().sort_index().plot(kind='bar', ax=ax)
        plt.title(f'Question: {question}')
        plt.xlabel('Choices')
        plt.ylabel('Frequency')

        # Display bar chart in Streamlit
        st.pyplot(fig)
        
        # Display cumulative table
        st.table(question_data['choice_text'].value_counts().cumsum())

if __name__ == "__main__":
    main()
