# -*- coding: utf-8 -*-
"""Survey Data Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Gr_RwxdK7WksZZraCxQmHQvTKIjZh3Ls
"""

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def preprocess_data(data):
    try:
        # Check if 'choice_text' column values can be converted to float
        data['choice_text'] = data['choice_text'].apply(lambda x: float(x) if isinstance(x, (int, float)) or x.replace('.', '', 1).isdigit() else x)
    except ValueError:
        pass

    # Find questions that have numeric values in the 'choice_text' column
    numeric_questions = data.groupby('question')['choice_text'].apply(lambda x: x.apply(lambda y: isinstance(y, (int, float))).any())

    rating_questions = numeric_questions[numeric_questions].index.tolist()

    return data, rating_questions




def main():
    st.title("Survey Data Dashboard")

    # File upload widget
    file_path = "Feedback-Responses-2024-05-17_updated.csv"

    if file_path is not None:
        # Read the uploaded CSV file
        data = pd.read_csv(file_path)

        data['date'] = pd.to_datetime(data['timestamp'], format='%m/%d/%y %H:%M').dt.date


        # Preprocess the data
        data, rating_questions = preprocess_data(data)

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

        # Create tabs
        tab1, tab2, tab3 = st.tabs(["Multi-Question by Date", "Single Question Comparison by Date", "Average Ratings by Date"])

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

        with tab3:
            st.header("Average Ratings by Date")
            if rating_questions:
                selected_rating_questions = st.multiselect("Select Rating Questions", rating_questions)
                if selected_rating_questions:
                    plot_average_ratings(data, selected_rating_questions)
                else:
                    st.warning("Please select at least one rating question.")
            else:
                st.warning("No rating questions found in the dataset.")

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
        proportions = game_day_data['choice_text'].value_counts(normalize=True).sort_index() * 100
        proportions.plot(kind='bar', ax=ax)
        ax.set_title(f'Game Day: {game_day}')
        ax.set_xlabel('Choices')
        ax.set_ylabel('Percentage')

        # Format y-axis as percentage with one decimal
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1f}%'))

    # Adjust layout
    plt.tight_layout()

    # Display bar charts side by side in Streamlit
    st.pyplot(fig)
    
    # Display percentage tables side by side
    cols = st.columns(len(game_days))
    for col, game_day in zip(cols, game_days):
        with col:
            st.subheader(f'Game Day: {game_day}')
            game_day_data = data[(data['game_day'] == game_day) & (data['question'] == question)]
            percentages_table = (game_day_data['choice_text'].value_counts(normalize=True).sort_index() * 100).round(1)
            percentages_table = percentages_table.apply(lambda x: f'{x:.1f}%')
            st.table(percentages_table)

def plot_average_ratings(data, selected_rating_questions):
    for question in selected_rating_questions:
        question_data = data[data['question'] == question]

        # Calculate average rating for each game day
        average_ratings = question_data.groupby('game_day')['choice_text'].mean()

        # Plot time-series bar plot
        plt.figure(figsize=(10, 5))
        average_ratings.plot(kind='bar')
        plt.title(f'Average Rating Over Time for "{question}"')
        plt.xlabel('Game Day')
        plt.ylabel('Average Rating')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Display bar plot in Streamlit
        st.pyplot(plt)

if __name__ == "__main__":
    main()
