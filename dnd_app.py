# import modules and components needed
import streamlit as st
import pandas as pd
import numpy as np
import random
import time

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
