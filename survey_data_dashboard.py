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

    # File upload widget
    file_path = "Feedback-Responses-2024-05-17_updated.csv"

    if file_path is not None:
        # Read the uploaded CSV file
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

        # Create tabs
        tab1, tab2 = st.tabs(["Cumulative Data by Question (over specified dates)", "Single Question Comparison by Date"])

        with tab1:
            st.header("Multi-Question by Date")
            # Create a multiselect for selecting game days
            game_days = st.multiselect("Select Game Days", sorted(data['game_day'].unique()))

            # Filter the data based on the selected game days
            filtered_data = data[data['game_day'].isin(game_days)]

            # Create a multiselect for selecting questions based on the filtered data
            questions = st.multiselect("Select Questions", sorted(filtered_data['question'].unique()))

            # Plot graphs and count tables based on selected game days and questions
            plot_data(filtered_data, questions)

        with tab2:
            st.header("Single Question Comparison by Date")
            # Create a selectbox for selecting a question
            question = st.selectbox("Select Question", sorted(data['question'].unique()))

            # Create a multiselect for selecting game days
            comparison_game_days = st.multiselect("Select Game Days for Comparison", sorted(data['game_day'].unique()))

            # Plot graphs side by side for comparison
            if comparison_game_days:
                plot_comparison_data(data, question, comparison_game_days)
            else:
                st.warning("Please select at least one game day for comparison.")

def plot_data(data, questions):
    for question in questions:
        question_data = data[data['question'] == question]

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

def plot_comparison_data(data, question, game_days):
    fig, axs = plt.subplots(1, len(game_days), figsize=(15, 5), sharey=True)

    if len(game_days) == 1:
        axs = [axs]  # Make sure axs is iterable if there's only one game day selected

    for ax, game_day in zip(axs, game_days):
        game_day_data = data[(data['game_day'] == game_day) & (data['question'] == question)]
        game_day_data.groupby('choice_text').size().sort_index().plot(kind='bar', ax=ax)
        ax.set_title(f'Game Day: {game_day}')
        ax.set_xlabel('Choices')
        ax.set_ylabel('Frequency')

    # Adjust layout
    plt.tight_layout()

    # Display bar charts side by side in Streamlit
    st.pyplot(fig)

if __name__ == "__main__":
    main()
