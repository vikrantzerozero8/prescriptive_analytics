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
    name = {"GIR":[x for x in df.Party_Name if (True for NUM in df.Warehouse if NUM == "GIR")] ,
            "LKDRM2":[x for x in df.Party_Name if (True for NUM in df.Warehouse if NUM == "LKDRM2")],
            "RSDSH":[x for x in df.Party_Name if (True for NUM in df.Warehouse if NUM == "RSDSH")],       
            "SLKPY":[x for x in df.Party_Name if (True for NUM in df.Warehouse if NUM == "SLKPY")],
            "GIR II":[x for x in df.Party_Name if (True for NUM in df.Warehouse if NUM == "GIR II")],     
            "KSR4":[x for x in df.Party_Name if (True for NUM in df.Warehouse if NUM == "KSR4")]  }

    
    if __name__ == "__main__":
        # adding "select" as the first and default choice
        manufacturer = st.multiselect('Select Manufacturer', options=['select']+list(name.keys()))
        # display selectbox 2 if manufacturer is not "select"
        if manufacturer != 'select':
            model_number = st.multiselect('Select Model Number', options=name[manufacturer])
        if st.button('Submit'):
            st.write('You selected ' + manufacturer + ' ' + model_number)      

    if st.button("About"):
        st.text("Lets learn") 
        st.text("Built with streamlit")  

if __name__=='__main__':
    main()
