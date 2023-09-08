import streamlit as st
import pandas as pd
import numpy as np
import time

# write a dataframe
st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 50],
    'third column': [100, 200, 300, 500],
    'fourth column': [1000, 2000, 3000, 5000],
    'fifth column': [10000, 20000, 30000, 50000]
}))

# write a line of text
some_text = "This is some text."
st.write(some_text)

# write a dataframe and highlight the max values
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))

# draw a line chart
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)

# plot a map
map_data = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [40.8, -73.95],
    columns=['lat', 'lon'])

st.map(map_data)



# ***************************************************************
# widgets
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

st.text_input("Your name", "Type Here ...", type='default', key='name')
st.session_state.name

# use checkboxes to show/hide data
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

    chart_data
    
# use a selectbox for options
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 50]
})

option = st.selectbox(
    'Which number do you like best?',
    df['first column'])

'You selected: ', option

# ***************************************************************
# layout

# add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)
st.sidebar.write(add_slider[0], " and ", add_slider[1])

# columns
left_column, right_column = st.columns(2)
# you can use a column just like st.sidebar:
left_column.button('Press me!')

# or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

# progress bar
'Start a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    # update the progress bar with each iteration.
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i + 1)
    time.sleep(0.01)

'...and now we\'re done!'

# ***************************************************************
# caching

@st.cache_data
def expensive_computation(a, b):
    time.sleep(3)
    return a * b

st.write("Result:", expensive_computation(2, 6))

