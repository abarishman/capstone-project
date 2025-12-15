# Name: Alexandra Barishman    Course: EN.585.771.81.FA25



# import modules and components needed
import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# opening message on streamlit page, introduces goal for building Dungeons & Dragons (D&D) character
st.write("""
# Dungeons & Dragons Character Stat Builder
Hello there, adventurer!
         
This Dungeons & Dragons character creator is your first step in fabricating a hero (or villain) ready to step into lands of magic, mystery, and danger. Whether you’re forging a fearless warrior, a cunning rogue, or a sharp spellcaster, this app will be able to guide you to the start of your journey. So get ready to sharpen your imagination, gather your courage, and let’s bring your character to life!
         
*To simplify the mechanics, characters will be set to start at 1st level.*
""")

# create two coloumns on streamlit page for user selection: Race and Class

col1, col2 = st.columns(2)

# first column creates a selection drop menu for some D&D races
# pulls Ability Score Modifiers from dataframe associated with the user's selection for character
# returns selected race and associated modifiers in the app view

with col1:
    st.header("Race")
    race = st.selectbox(
        "Please select a race from the following options:",
        ('None Selected','Dragonborn', 'Dwarf', 'Elf', 'Gnome', 'Halfling', 'Human', 'Tiefling'),
    )
    race_data = {
            'Race': ['Dragonborn', 'Dwarf', 'Elf', 'Gnome', 'Halfling', 'Human', 'Tiefling'],
            'Strength': [2, 2, 0, 0, 0, 1, 0],
            'Dexterity': [0, 0, 2, 0, 2, 1, 0],
            'Constitution': [0, 2, 0, 1, 1, 1, 0],
            'Intelligence': [0, 0, 0, 2, 0, 1, 1],
            'Wisdom': [0, 0, 1, 0, 0, 1, 0],
            'Charisma': [1, 0, 0, 0, 0, 1, 2],}
    df_race = pd.DataFrame(race_data)

    df_character_race = df_race[df_race['Race'] == race]
    df_race_disp=df_character_race.loc[:, (df_character_race != 0).any(axis=0)]

    st.write("""Ability Score Modifiers""")
    st.dataframe(df_race_disp, hide_index=True)

# second column creates a selection drop menu for some D&D classes
# pulls Saving Throw Proficencies from dataframe associated with the user's selection for character (value of 2 per game mechanics)
# returns selected class and associated modifiers in the app view

with col2:
    st.header("Class")
    clss = st.selectbox(
        "Please select a class from the following options:",
        ('None Selected','Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin','Ranger','Rogue','Sorcerer','Warlock','Wizard'),
    )
    class_data = {
            'Class': ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin','Ranger','Rogue','Sorcerer','Warlock','Wizard'],
            'Strength': [2, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0],
            'Dexterity': [0, 2, 0, 0, 0, 2, 0, 2, 2, 0, 0, 0],
            'Constitution': [2, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0],
            'Intelligence': [0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2],
            'Wisdom': [0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 2, 2],
            'Charisma': [0, 2, 2, 0, 0, 0, 2, 0, 0, 2, 2, 0],}
    df_class = pd.DataFrame(class_data)
    
    st.write("""Saving Throw Modifiers""")
    df_character_class = df_class[df_class['Class'] == clss]
    df_class_disp=df_character_class.loc[:, (df_character_class != 0).any(axis=0)]
    st.dataframe(df_class_disp, hide_index=True)

# new section to determine base ability scores
# uses a random numnber generator to generate a number 1-6 representing rolling a six-sided die (d6)
# rolls 4d6 for each character ability stat, removes the lowest of the four returned numbers and sums the three higher values
# this mimics the mechanics for rolling for stats in D&D
# two columns are created after stat generation that pull data from dataframes associated with selected Race and Class and are combined with generated stats to return values used in D&D gameplay

st.write("""
## Roll For Stats!
""")

if st.button('Roll :game_die:'):
            def roll_ability_score():
                rolls = [random.randint(1, 6) for _ in range(4)]
                rolls.sort()
                return sum(rolls[1:])

            def generate_character_stats():
                stats = {
                    'Strength': roll_ability_score(),
                    'Dexterity': roll_ability_score(),
                    'Constitution': roll_ability_score(),
                    'Intelligence': roll_ability_score(),
                    'Wisdom': roll_ability_score(),
                    'Charisma': roll_ability_score(),
                }
                return stats
            df_stats_gen = pd.DataFrame([generate_character_stats()])

            df_character_ability = pd.concat([df_stats_gen, df_character_race])
            df_character_ability=df_character_ability.drop('Race', axis=1)
            df_character_ability=df_character_ability.sum(axis=0)
            df_character_ability = df_character_ability.reset_index()
            df_character_ability.columns = ['Ability', 'Score']

            st.write("""**Ability Scores**""")
            st.dataframe(df_character_ability, hide_index=True)

            with st.container():
                col3, col4 = st.columns(2)

                with col3:
                    st.write("""Ability Modifiers""")
                    df_character_ability['Modifier'] = (df_character_ability['Score']-10)//2
                    st.dataframe(df_character_ability[['Ability', 'Modifier']], hide_index=True)

                with col4:
                    st.write("""Saving Throw Modifiers""")
                    df_character_save=df_character_class.drop('Class', axis=1)
                    df_character_save=df_character_save.T
                    df_character_save = df_character_save.reset_index()
                    df_character_save.columns = ['Ability', 'Prof']
                    df_character_ability['SaveProf']=df_character_save['Prof']
                    df_character_ability['Save'] = (df_character_ability['Modifier']+df_character_ability['SaveProf'])
                    st.dataframe(df_character_ability[['Ability', 'Save']], hide_index=True)

            
# creating a predictive model for D&D character stats based on the selection of race and class
# add a predictive aspect to the app and see what expected outputs may be

                abilities = ['Strength', 'Dexterity', 'Constitution','Intelligence', 'Wisdom', 'Charisma']

                def roll_ability_score():
                    rolls = [random.randint(1, 6) for _ in range(4)]
                    rolls.sort()
                    return sum(rolls[1:])

                def generate_training_data(n_samples=1000):
                    rows = []

                    for _ in range(n_samples):
                        race_row = df_race.sample(1).iloc[0]
                        class_row = df_class.sample(1).iloc[0]
                        base_stats = {a: roll_ability_score() for a in abilities}
                        final_stats = {
                            a: base_stats[a] + race_row[a]
                            for a in abilities
                        }
                        rows.append({
                            'Race': race_row['Race'],
                            'Class': class_row['Class'],
                            **final_stats
                        })

                    return pd.DataFrame(rows)

                df_training_data = generate_training_data()

                X = df_training_data[['Race', 'Class']]
                y = df_training_data[abilities]

                encoder = OneHotEncoder(sparse_output=False)
                X_encoded = encoder.fit_transform(X)

                X_train, X_test, y_train, y_test = train_test_split(
                    X_encoded, y, test_size=0.2, random_state=42)
                model = Sequential([
                    Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
                    Dense(32, activation='relu'),
                    Dense(6)])
                model.compile(
                    optimizer=Adam(learning_rate=0.001),
                    loss='mse')
                model.fit(
                    X_train,
                    y_train,
                    epochs=40,
                    batch_size=32)

                predictions = model.predict(X_test)
                mae = mean_absolute_error(y_test, predictions)

                example = pd.DataFrame(
                    [[race, clss]],
                    columns=['Race', 'Class'])

                example_encoded = encoder.transform(example)
                predicted_stats = model.predict(example_encoded)[0]

                st.write("## Example Neural Network Prediction")

                example_character = pd.DataFrame(
                    [[race, clss]],
                    columns=['Race', 'Class'])

                if race != 'None Selected' and clss != 'None Selected':

                    example_encoded = encoder.transform(example_character)
                    predicted_stats = model.predict(example_encoded)[0]

                    df_prediction = pd.DataFrame({
                        'Ability': abilities,
                        'Predicted Score (Average)': np.round(predicted_stats, 1)})

                    st.write(
                        f"Predicted average ability scores for a {race} {clss}:")
                    st.dataframe(df_prediction, hide_index=True)

                else:
                    st.spinner("Waiting for selection...")

                st.write('### *Model Accuracy*')

                # Make predictions on test data
                predictions = model.predict(X_test)

                # Compute MAE
                mae = mean_absolute_error(y_test, predictions)

                st.write(
                    f"*Mean Absolute Error:* {mae:.2f} points")