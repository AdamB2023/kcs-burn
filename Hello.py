import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Ustawienie dark mode dla matplotlib
plt.style.use('dark_background')

# Tytuł aplikacji
st.title('Kalkulator opłacalności spalania KCS')

# Dodajemy komentarz
st.markdown("""
Poniższe wartości mocy są przykładowe.<br>
Wprowadź własne ze strony Burningdropa: 0 dla podstawowy, i kolejne jak na stronie.
""", unsafe_allow_html=True)

# Prepare initial data as lists ensuring they are the same length
spalone_kcs = [0, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3, 3.2, 3.4, 3.6, 3.8, 4, 4.2, 4.4, 4.6, 4.8, 5, 5.2, 5.4, 5.6, 5.8, 6, 6.2]
moc_obliczeniowa = [4648.50, 4868.44, 4917.99, 4974.34, 5038.40, 5111.02, 5192.74, 5283.63, 5382.95, 5488.93, 5598.80, 5709.09, 5816.25, 5917.29, 6010.21, 6094.06, 6168.73, 6234.69, 6292.74, 6343.76, 6388.66, 6428.28, 6463.35, 6494.51, 6522.31, 6547.22]

# Create a DataFrame with matching lengths
df = pd.DataFrame({
    'Spalone KCS': spalone_kcs,
    'Moc obliczeniowa': moc_obliczeniowa
})

# User inputs for computational power
user_input_values = {}

# Organize user inputs for computational power in a grid
num_columns = 6
cols = st.columns(num_columns)
for i, kcs in enumerate(spalone_kcs):
    with cols[i % num_columns]:  # Distributes input boxes across columns
        # Display input field without the label, only showing the KCS value
        user_input_values[kcs] = st.number_input(f'{kcs:.1f}', value=df.at[i, 'Moc obliczeniowa'])

# Update the DataFrame with the user input values
df['Moc obliczeniowa'] = df['Spalone KCS'].apply(lambda x: user_input_values[x])

# Calculate the increase in computational power
df['Wzrost mocy obliczeniowej'] = df['Moc obliczeniowa'].diff().fillna(0)

# Display the DataFrame
# st.write(df)

# Generate a plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['Spalone KCS'], df['Wzrost mocy obliczeniowej'], marker='o', linestyle='-', color='orange')
ax.set_xlabel('Spalone KCS')
ax.set_ylabel('Wzrost mocy obliczeniowej')
ax.set_title('Wykres wzrostu mocy')
ax.set_xticks(np.arange(min(spalone_kcs), max(spalone_kcs) + 0.2, 0.2))  # X-axis ticks

# Y-axis grid lines with more precise scale
y_max = max(df['Wzrost mocy obliczeniowej']) + 10
y_step = 2  # Set step for Y-axis
ax.set_yticks(np.arange(0, y_max, 10))  # Y-axis ticks every 10 units

ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.tick_params(axis='x', rotation=90)

# Display the plot in Streamlit
st.pyplot(fig)