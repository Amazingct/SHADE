import streamlit as st
import pandas as pd
import os



st.write(
    
    
    """
    ### Crystal Technologies
    # ![logo] SHA-DE DASHBOARD 
    ```python
    print("your home uinfied...")
    ```
    [Github](https://www.github.com/Amazingct/SHADE) | [Youtube](https://www.youtube.com/watch?v=C3DmehDGIww&list=PLQDvLS_MNLkf7i2TDSJD13QhRDkX_hE9F)

    ---
    
     
    [logo]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
    """
)

devices_json = os.path.join("MainController","Configurations","devices.json")
scenes_json = os.path.join("MainController","Configurations","scenes_copy.json")

scenes = pd.read_json(scenes_json, orient="index")
devices = pd.read_json(devices_json, orient="index")
st.write(
    """
    ## DEVICES
    """
)
st.write(pd.DataFrame(devices))
st.write(
    """
    ## SCENCES
    """
)
st.write(pd.DataFrame(scenes))

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)


left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")
    
st.select_slider("Displayed values:", ["Normalized", "Absolute"])


st.markdown(
            "###### [![this is an image link](https://i.imgur.com/mQAQwvt.png)](https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=686079794781-0bt8ot3ie81iii7i17far5vj4s0p20t7.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fwebmasters.readonly&state=vryYlMrqKikWGlFVwqhnMpfqr1HMiq&prompt=consent&access_type=offline)"
        )
    



