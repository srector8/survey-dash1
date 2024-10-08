# -*- coding: utf-8 -*-
"""Survey Data Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Gr_RwxdK7WksZZraCxQmHQvTKIjZh3Ls
"""
import pandas as pd
import streamlit as st
import altair as alt

def preprocess_data(data):
    try:
        # Check if 'CHOICE_TEXT' column values can be converted to float
        data['CHOICE_TEXT'] = data['CHOICE_TEXT'].apply(lambda x: float(x) if isinstance(x, (int, float)) or x.replace('.', '', 1).isdigit() else x)
    except ValueError:
        pass

    # Find questions that have numeric values in the 'CHOICE_TEXT' column
    numeric_questions = data.groupby('QUESTION')['CHOICE_TEXT'].apply(lambda x: x.apply(lambda y: isinstance(y, (int, float))).any())

    rating_questions = numeric_questions[numeric_questions].index.tolist()

    # Filter out 'Test Question' if present
    if 'Test Question' in rating_questions:
        rating_questions.remove('Test Question')

    return data, rating_questions

def main():
    st.title("Survey Data Dashboard")

    # File upload widget
    file_path = "Feedback_Responses_0815.csv"

    if file_path is not None:
        # Read the uploaded CSV file
        data = pd.read_csv(file_path)

        data['date'] = pd.to_datetime(data['RESPONSE_TIMESTAMP']).dt.date

        # Preprocess the data
        data, rating_questions = preprocess_data(data)

        # Define game days
        game_days = [
            (pd.to_datetime('2024-05-14').date(), pd.to_datetime('2024-05-17').date()),
            (pd.to_datetime('2024-05-17').date(), pd.to_datetime('2024-05-23').date()),
            (pd.to_datetime('2024-05-23').date(), pd.to_datetime('2024-05-28').date()),
            (pd.to_datetime('2024-05-28').date(), pd.to_datetime('2024-05-31').date()),
            (pd.to_datetime('2024-05-31').date(), pd.to_datetime('2024-06-04').date()),
            (pd.to_datetime('2024-06-04').date(), pd.to_datetime('2024-06-08').date()),
            (pd.to_datetime('2024-06-08').date(), pd.to_datetime('2024-06-10').date()),
            (pd.to_datetime('2024-06-10').date(), pd.to_datetime('2024-06-18').date()),
            (pd.to_datetime('2024-06-18').date(), pd.to_datetime('2024-06-28').date()),
            (pd.to_datetime('2024-06-28').date(), pd.to_datetime('2024-07-07').date()),
            (pd.to_datetime('2024-07-07').date(), pd.to_datetime('2024-07-10').date()),
            (pd.to_datetime('2024-07-10').date(), pd.to_datetime('2024-07-14').date()),
            (pd.to_datetime('2024-07-14').date(), pd.to_datetime('2024-08-20').date()),
            (pd.to_datetime('2024-08-20').date(), pd.to_datetime('2024-08-23').date()),
            (pd.to_datetime('2024-08-23').date(), pd.to_datetime('2024-09-01').date()),
            (pd.to_datetime('2024-09-01').date(), pd.to_datetime('2024-09-03').date()),
            (pd.to_datetime('2024-09-03').date(), pd.to_datetime('2024-09-06').date()),
            (pd.to_datetime('2024-09-06').date(), pd.to_datetime('2024-09-17').date()),
            (pd.to_datetime('2024-09-17').date(), pd.to_datetime('2024-09-19').date())
        ]

        # Categorize the responses based on the date
        def categorize_date(date):
            for start_date, end_date in game_days:
                if start_date <= date < end_date:
                    return start_date.strftime('%Y-%m-%d')
            return None

        
        # Categorize the responses based on the date
        data['game_day'] = data['date'].apply(categorize_date)

        # Filter out rows with None game_day
        data = data.dropna(subset=['game_day'])

        # Create tabs
        tab1, tab2, tab3 = st.tabs(["Cumulative Responses by Question", "Average Ratings by Date", "Single Question Comparison by Date"])

        with tab1:
            st.header("Cumulative Responses by Question")
            st.write("Select multiple questions and game days to see the distribution of responses.")

            # Create a multiselect for selecting game days
            game_days = st.multiselect("Select Game Days", sorted(data['game_day'].unique()))

            # Filter the data based on the selected game days
            filtered_data = data[data['game_day'].isin(game_days)]

            # Create a multiselect for selecting questions based on the filtered data
            questions = st.multiselect("Select Questions", sorted(filtered_data['QUESTION'].unique()))

            # Plot graphs and count tables based on selected game days and questions
            plot_data(filtered_data, questions)

        with tab2:
            st.header("Average Ratings by Date")
            st.write("Select rating questions to see the average ratings over time.")
            
            if rating_questions:
                selected_rating_questions = st.multiselect("Select Rating Questions", rating_questions)
                if selected_rating_questions:
                    plot_average_ratings(data, selected_rating_questions)
                else:
                    st.warning("Please select at least one rating question.")
            else:
                st.warning("No rating questions found in the dataset.")

        with tab3:
            st.header("Single Question Comparison by Date")
            st.write("Select a single question and multiple game days for comparison.")
            
            # Create a selectbox for selecting a question
            question = st.selectbox("Select Question", sorted(data['QUESTION'].unique()))

            # Create a multiselect for selecting game days
            comparison_game_days = st.multiselect("Select Game Days for Comparison", sorted(data['game_day'].unique()))

            # Plot graphs side by side for comparison
            if comparison_game_days:
                plot_comparison_data(data, question, comparison_game_days)
            else:
                st.warning("Please select at least one game day for comparison.")

        

def plot_data(data, questions):
    for question in questions:
        question_data = data[data['QUESTION'] == question]

        # Create a bar chart using Altair
        chart = alt.Chart(question_data).mark_bar().encode(
            x=alt.X('CHOICE_TEXT', type='nominal', title='Choices'),
            y=alt.Y('count()', title='Frequency'),
            tooltip=['CHOICE_TEXT', 'count()']
        ).properties(
            title=f'Question: {question}'
        ).interactive()

        # Display the chart in Streamlit
        st.altair_chart(chart, use_container_width=True)

        # Display count table
        st.table(question_data['CHOICE_TEXT'].value_counts().sort_index())

def plot_comparison_data(data, question, game_days):
    charts = []
    for game_day in game_days:
        game_day_data = data[(data['game_day'] == game_day) & (data['QUESTION'] == question)]
        proportions = game_day_data['CHOICE_TEXT'].value_counts(normalize=True).sort_index()
        
        proportions_df = pd.DataFrame({
            'CHOICE_TEXT': proportions.index,
            'percentage': proportions.values
        })

        chart = alt.Chart(proportions_df).mark_bar(size=30).encode(
            x=alt.X('CHOICE_TEXT', type='nominal', title='Choices'),
            y=alt.Y('percentage:Q', axis=alt.Axis(format='%'), title='Percentage'),
            tooltip=['CHOICE_TEXT', alt.Tooltip('percentage:Q', format='.1f')],
        ).properties(
            title=f'Game Day: {game_day}',
            width=alt.Step(50),
        )
    
        charts.append(chart)

    if charts:  
        st.altair_chart(alt.hconcat(*charts), use_container_width=True)
    else:
        st.write("No charts to display.")

    cols = st.columns(len(game_days))
    for col, game_day in zip(cols, game_days):
        with col:
            game_day_data = data[(data['game_day'] == game_day) & (data['QUESTION'] == question)]
            percentages_table = (game_day_data['CHOICE_TEXT'].value_counts(normalize=True).sort_index() * 100).round(1)
            percentages_table = percentages_table.apply(lambda x: f'{x:.1f}%')
            st.table(percentages_table)


def plot_average_ratings(data, selected_rating_questions):
    for question in selected_rating_questions:
        question_data = data[data['QUESTION'] == question]

        average_ratings = question_data.groupby('game_day')['CHOICE_TEXT'].mean().reset_index()
        
        # Create a bar chart using Altair
        chart = alt.Chart(average_ratings).mark_bar().encode(
            x=alt.X('game_day:O', title='Game Day'),
            y=alt.Y('CHOICE_TEXT:Q', title='Average Rating'),
            tooltip=['game_day', 'CHOICE_TEXT']
        ).properties(
            title=f'Average Rating Over Time for "{question}"',
        ).interactive()

        # Display the chart in Streamlit
        st.altair_chart(chart, use_container_width=True)

        # Display average ratings table
        st.table(average_ratings.rename(columns={'game_day': 'Game Day', 'CHOICE_TEXT': 'Average Rating'}))



if __name__ == "__main__":
    main()

