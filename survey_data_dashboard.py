# -*- coding: utf-8 -*-
"""Survey Data Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Gr_RwxdK7WksZZraCxQmHQvTKIjZh3Ls
"""

import numpy as np
import streamlit as st
import pandas as pd
import streamlit as st
import io
"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""




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

        # Create a dropdown for selecting a game day
        game_day = st.selectbox("Select Game Day", data['game_day'].unique())

        # Plot graphs based on selected game day
        plot_graphs(data, game_day)

def plot_graphs(data, game_day):
    st.write(f"Game Day: {game_day}")

    filtered_data = data[data['game_day'] == game_day]
    questions = filtered_data['question'].unique()

    for question in questions:
        st.subheader(f'Question: {question}')
        question_data = filtered_data[filtered_data['question'] == question]
        st.bar_chart(question_data['choice_text'].value_counts())

if __name__ == "__main__":
    main()

import pandas as pd
import ipywidgets as widgets
from ipywidgets import interact_manual, Output
import matplotlib.pyplot as plt
import io

# Create file upload widget
upload = widgets.FileUpload(accept='.csv', multiple=False)
output = Output()

def process_file(change):
    # Clear previous output
    output.clear_output()

    with output:
        # Read the uploaded CSV file
        uploaded_file = list(upload.value.values())[0]
        content = uploaded_file['content']
        data = pd.read_csv(io.StringIO(content.decode('utf-8')))

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

        # Create a dropdown for selecting a game day
        game_day_dropdown = widgets.Dropdown(
            options=data['game_day'].unique(),
            description='Game Day:',
        )

        display(game_day_dropdown)

        # Function to plot graphs based on selected game day
        def plot_graphs(game_day):
            # Clear previous plots
            with output:
                output.clear_output(wait=True)
                filtered_data = data[data['game_day'] == game_day]
                questions = filtered_data['question'].unique()

                for question in questions:
                    plt.figure()
                    question_data = filtered_data[filtered_data['question'] == question]
                    question_data['choice_text'].value_counts().plot(kind='bar')
                    plt.title(f'Question: {question}')
                    plt.xlabel('Choices')
                    plt.ylabel('Frequency')
                    plt.show()

        interact_manual(plot_graphs, game_day=game_day_dropdown)

# Observe the file upload
upload.observe(process_file, names='value')

display(upload, output)

import pandas as pd
import ipywidgets as widgets
from ipywidgets import interact_manual, Output
import matplotlib.pyplot as plt
import io

# Create file upload widget
upload = widgets.FileUpload(accept='.csv', multiple=False)
output = Output()

def process_file(change):
    # Clear previous output
    output.clear_output()

    with output:
        # Read the uploaded CSV file
        uploaded_file = list(upload.value.values())[0]
        content = uploaded_file['content']
        data = pd.read_csv(io.StringIO(content.decode('utf-8')))

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

        # Create a dropdown for selecting a game day
        game_day_dropdown = widgets.Dropdown(
            options=data['game_day'].unique(),
            description='Game Day:',
        )


        # Function to plot graphs based on selected game day
        def plot_graphs(game_day):
            # Clear previous plots
            with output:
                output.clear_output(wait=True)
                filtered_data = data[data['game_day'] == game_day]
                questions = filtered_data['question'].unique()

                for question in questions:
                    plt.figure()
                    question_data = filtered_data[filtered_data['question'] == question]
                    question_data['choice_text'].value_counts().plot(kind='bar')
                    plt.title(f'Question: {question}')
                    plt.xlabel('Choices')
                    plt.ylabel('Frequency')
                    plt.show()

        interact_manual(plot_graphs, game_day=game_day_dropdown)

# Observe the file upload
upload.observe(process_file, names='value')

display(upload, output)