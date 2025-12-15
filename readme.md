# Dungeons & Dragons Character Stat Builder
*by Alexandra Barishman*


A Streamlit application that helps users with the creation of a 1st-level D&D character. The app combines the traditional tabletop game mechanics with machine learning to both generate and predict character ability scores based on race and class selection by the user.

---

## Overview

This app allows players to:
- Select a race and class
- Roll ability scores using standard D&D rules
- Apply racial modifiers and class saving throw proficiencies
- View final ability scores, modifiers, and saving throws
- Compare rolled stats against a neural network’s predicted averages


## How to Use the App

1. **Launch the App**
   - Run the Streamlit application to open the character builder interface using Python.

2. **Select a Race**
   - Choose from available D&D races in the corresponding selection box.
   - The app displays applicable ability score modifiers.

3. **Select a Class**
   - Choose from available D&D classes in the corresponding selection box.
   - The app displays applicable saving throw proficency modifiers.

4. **Roll Ability Scores**
   - Click the 🎲 **Roll** button to simulate rolling for base ability scores as in traditional D&D.
   - *Ability scores are generated using the 4d6 drop-lowest rule.*

5. **Review Character Stats**
   - View final ability scores after racial modifiers have been added.
   - Saving throw values are computed using the final ability scores and class proficiencies.

6. **View Neural Network Predictions**
   - The app predicts average ability scores based on the user's selction of race and class.
   - Allows you to compare predicted values to your rolled stats.

7. **Check Model Accuracy**
   - The Mean Absolute Error (MAE) indicates the model’s average prediction error.