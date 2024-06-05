# -*- coding: utf-8 -*-
"""Survey Data Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Gr_RwxdK7WksZZraCxQmHQvTKIjZh3Ls
"""

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def main():
    st.title("Survey Data Dashboard")

    # Path to the CSV file
    file_path = "Feedback-Responses-2024-05-17_updated.csv"

    # Read the CSV file
    try:
        data = pd.read_csv(file_path)

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
        try:
            data['choice_text'] = pd.to_numeric(data['choice_text'], errors='raise').astype(int)
        except ValueError:
            st.error("Error: Some values in 'choice_text' column are not numeric.")
            return

        # Create a dropdown for selecting a game day
        game_day = st.selectbox("Select Game Day", sorted(data['game_day'].unique()))

        # Plot graphs and count tables based on selected game day
        plot_data(data, game_day)

    except FileNotFoundError:
        st.error(f"Error: File '{file_path}' not found.")
    except pd.errors.ParserError:
        st.error("Error: Could not parse the CSV file. Please check the file format.")

def plot_data(data, game_day):
    st.write(f"Game Day: {game_day}")

    filtered_data = data[data['game_day'] == game_day]
    questions = sorted(filtered_data['question'].unique())  # Sort questions

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
        
        # Display count table
        st.table(question_data['choice_text'].value_counts().sort_index())

if __name__ == "__main__":
    main()
