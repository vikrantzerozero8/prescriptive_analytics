from github import Github

import numpy as np
import pandas as pd
import streamlit as st

g = Github("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")

user = g.get_user()

repository = user.get_repo('pres')

file_content = repository.get_contents('jun23.csv')

bytes_data=file_content.decoded_content

s=str(bytes_data,'utf-8')

file = open("data.txt","w")

file.write(s)

df = pd.read_csv('data.txt')
df.columns = df.columns.str.replace(' ', '')
df.rename(columns = {'CustomerName':"Party_Name","Plant":"Warehouse","TargetQuantity":"Net_Weight"},inplace = True)

def main():
    st.title("Transportation cost prediction")
    
    # Store the initial value of widgets in session state
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
    
    html_temp="""
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;"> Transportation cost prediction </h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html = True)
    
    brand = st.selectbox('Select Brand',df.Warehouse.unique())

    model=st.multiselect('Select your model', df.loc[df.Warehouse==brand]['Party_Name'].unique())

    if st.button("submit"):
        st.write('You selected ' + ' ' + brand + ' ' + model)

    if st.button("About"):
        st.text("Lets learn") 
        st.text("Built with streamlit")  

if __name__=='__main__':
    main()
