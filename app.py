from pulp import*
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

def main():
    image_path = r"robo_Logo1.jpeg"
    image = Image.open(image_path)
    # Resize the image
    # new_width =300 # Specify the desired width
    # new_height = 200  # Specify the desired height
    # resized_image = image.resize((new_width, new_height))
    # st.image(resized_image, use_column_width=True)
    st.image(image) #, use_column_width=True)
    
    sidebar_image_path = r"INNODATATICS.png"
    sidebar_image = Image.open(sidebar_image_path)
    # resized_sidebar_image = sidebar_image.resize((450, 300))  # Adjust the width and height as desired
    # st.sidebar.image(resized_sidebar_image)
    st.sidebar.image(sidebar_image)
    
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
    
    uploadedFile = st.sidebar.file_uploader("Choose a file" ,type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
    if uploadedFile is not None :
        try:

            df=pd.read_csv(uploadedFile)
            
            
        except:
                try:
                    df = pd.read_excel(uploadedFile,engine = "openpyxl",sheet_name = 'Sheet1')
                    
                except:      
                    df = pd.DataFrame(uploadedFile)
                    
        
                    
    else:
        st.sidebar.warning("you need to upload a csv or excel file.")
    if uploadedFile is not None : 
        df.columns = df.columns.str.replace(' ', '')
        df.columns = df.columns.str.lower()
        
        df.rename(columns = {'customername':"Party_Name","plant":"Warehouse","targetquantity":"Net_Weight","freightrate":"Freight_Rate","distance":"Distance"},inplace = True)
        
        name = {"GIR":df.Party_Name[df['Warehouse'] == "GIR"].tolist() ,
                "LKDRM2":df.Party_Name[df['Warehouse'] == "LKDRM2"].tolist(),
                "RSDSH":df.Party_Name[df['Warehouse'] == "RSDSH"].tolist(),
                "SLKPY":df.Party_Name[df['Warehouse'] == "SLKPY"].tolist(),
                "GIR II":df.Party_Name[df['Warehouse'] == "GIR II"].tolist(),
                "KSR4":df.Party_Name[df['Warehouse'] == "KSR4"].tolist() }
        
        
        plan = st.selectbox('Select Party Name', options=[''] + df.Party_Name)
        if st.button('Submit'):
            
            if df["Net_Weight"].dtype == object:
                gh = []
                for i in df['Net_Weight']:
                        i = re.sub('[-_,a-zA-Z \n\.\s]', '', i)
                        gh.append(i)
                df1 = pd.DataFrame({'Net_Weight':gh})
                df['Net_Weight'] = df1['Net_Weight'].astype("float")
            
            df['Amount'] = 0
            for i in df.index:
                if (df['Freight_Rate'][i] == 100):
                    df.at[i, "Amount"] = df.at[i, 'Freight_Rate'] * df.at[i, 'Net_Weight'] 
                elif (df['Freight_Rate'][i] < 100):
                    df.at[i, "Amount"] = df.at[i, 'Freight_Rate'] * df.at[i, 'Distance'] * df.at[i, 'Net_Weight'] 
    
            # unique warehouses and party_names
            warehouses = df['Warehouse'].unique()
            party_names = df['Party_Name'].unique()
            
            #Assigning freight rate for all warehouse
            df['Freight_Rate'] = 0
            for i in df.index:
                if (df['Warehouse'][i] == 'GIR'):
                    df.at[i, 'Freight_Rate'] = 2.9
                elif (df['Warehouse'][i] == 'GIR II'):
                    df.at[i, 'Freight_Rate'] = 2.9
                elif (df['Warehouse'][i] == 'KSR4'):
                    df.at[i, 'Freight_Rate'] = 2.5
                elif (df['Warehouse'][i] == 'LKDRM2') and df['Distance'][i] <= 40:
                    df.at[i, 'Freight_Rate'] = 100
                elif (df['Warehouse'][i] == 'LKDRM2') and df['Distance'][i] > 40:
                    df.at[i, 'Freight_Rate'] = 2.5
                elif (df['Warehouse'][i] == 'RSDSH') and df['Distance'][i] <= 40:
                    df.at[i, 'Freight_Rate'] = 100
                elif (df['Warehouse'][i] == 'RSDSH') and df['Distance'][i] > 40:
                    df.at[i, 'Freight_Rate'] = 2.5
                elif (df['Warehouse'][i] == 'SLKPY') and df['Distance'][i] <= 40:
                    df.at[i, 'Freight_Rate'] = 100
                elif (df['Warehouse'][i] == 'SLKPY') and df['Distance'][i] > 40:
                    df.at[i, 'Freight_Rate'] = 2.5
            
            
            
            # Calculate Shipping Cost
            
            df['shipping_cost'] = 0
            for i in df.index:
                if (df['Freight_Rate'][i] == 100):
                    df.at[i, "shipping_cost"] = df.at[i, 'Freight_Rate']
                elif (df['Freight_Rate'][i] < 100):
                    df.at[i, "shipping_cost"] = df.at[i, 'Freight_Rate'] * df.at[i, 'Distance']
            
            # Create a pivot table with Warehouse as index, Party_Name as columns, and Distance as values
            distance_matrix = df.pivot_table(values= 'Distance', index='Warehouse', columns='Party_Name')
            # fill with 10000 Wherever no supply
            distance_matrix.fillna(10000, inplace = True)
            #distance_matrix
            
            # Create a pivot table with Warehouse as index, Party_Name as columns, and freight rate as values
            freight_mat = df.pivot_table(values = 'Freight_Rate', index = 'Warehouse', columns = 'Party_Name')
            # Fill with 10000 wherever no supply
            freight_mat.fillna(100000, inplace = True)
            #freight_mat
            
            # Create a pivot table with Warehouse as index, Party_Name as columns, and shipping cost as values
            cost_mat = df.pivot_table(values = 'shipping_cost', index = 'Warehouse', columns = 'Party_Name')
            #fill with 100000 wherever no supply
            cost_mat = cost_mat.fillna(100000)
            #cost_mat
            
            # Create a pivot table with Warehouse as index, Party_Name as columns, and Net_Weight as values
            weight_mat = df.pivot_table(values = 'Net_Weight', index = 'Warehouse', columns = 'Party_Name', aggfunc =sum )
            # fill with zeros wherever no sulpply
            weight_mat = weight_mat.fillna(0)
            #weight_mat
            
            # create pivot table with warehouse as index and sum of Net_Weight for particular warehouse as values
            supply = pd.pivot_table(df, values='Net_Weight', index = 'Warehouse', aggfunc=sum, margins=True)
            # Manually assign supply values
            supply.loc['GIR'] =    1000000  # Supply for Warehouse 'GIR'
            supply.loc['GIR II'] = 1000000  # Supply for Warehouse 'GIR II'
            supply.loc['KSR4'] =   1000000  # Supply for Warehouse 'KSR4'
            supply.loc['LKDRM2'] = 1000000 # Supply for Warehouse 'LKDRM2'
            supply.loc['RSDSH'] =  1000000 # Supply for Warehouse 'RSDSH'
            supply.loc['SLKPY'] =  1000000 # Supply for Warehouse 'SLKPY'
            # Add supply values for other warehouses in a similar manner
            # Remove the 'All' row from supply
            supply = supply.iloc[:-1]
            
            # Display the updated supply values
            #supply
            
            #create a pivot_tabel for total demand of each party (Before optimization the Quantity of df Transport from Warehouse the Party)
            demand = pd.pivot_table(df, values='Net_Weight', index ='Warehouse', columns ='Party_Name', aggfunc = sum, margins =True, margins_name='Grand Total')
            #demand
            
            # Only consider the Demand
            demand = demand.iloc[6:]
            # Rename the column
            demand.rename(index= {'Grand Total': 'Demand'}, inplace = True)
            #demand
            
            # Define the problem
            prob = LpProblem("Transportation Problem", LpMinimize)
            
            # Define decision variables
            route_vars = LpVariable.dicts("Route", (warehouses, party_names), lowBound=0, cat='Continuous')
            #route_vars
            
            # Define the objective function
            prob += lpSum([route_vars[w][p] * cost_mat.loc[w][p] for w in warehouses for p in party_names]), " Transportation Cost"
            
            # Define the supply constraint
            for w in warehouses:
                prob += lpSum([route_vars[w][p]   for p in party_names]) <= supply.loc[w] , "Sum of quatity supplied from Warehouse to paty %s" % w
            
            demand2 = demand.T
            #demand2
            
            # Define Demand Constraints
            for p in party_names:
                prob += lpSum([route_vars[w][p] for w in warehouses]) >= demand2.loc[p], 'Sum of Demand of party %s' % p
            
            # Execute the problem
            prob.solve()
           
            # Create DataFrame
            decision_var_df = pd.DataFrame(index=distance_matrix.index, columns=distance_matrix.columns, dtype='float')
            
            # Fill the DataFrame with the optimized values of the decision variables
            for w in distance_matrix.index:
                for p in distance_matrix.columns:
                    decision_var_df.loc[w, p] = route_vars[w][p].varValue
            
            # Verify the cost after Optimization
            total_after_opt = [decision_var_df.loc[w][p] * cost_mat.loc[w][p] .sum().sum() for w in warehouses for p in party_names]
            st.write("Distance decision variables")
            decision_var_df
            
            total1 = sum(total_after_opt)
            st.write('total_cost_after_opt= {:,} '.format(int(value(total1))))
            
            # Before_Optimization the Transportation Cost in ₹
            before_opt_cost = df['Amount'].sum()
            
            st.write('Party selected :   ' + plan)
    
            result = decision_var_df.loc[:,plan]
            
            #st.write("TARGET QUANTITY FOR "+ plan + '  = {:,} '.format(int(value(result))))
    
            #st.write('COMPLETE DECISION VARIABLE FOR TARGET QUANTITY')
    
            st.table(result)
    
            st.write('Total_transportation_Costs = {:,} '.format(int(value(prob.objective))))
    
            st.write('total_cost_before_opt= {:,} '.format(int(value(before_opt_cost))))
    
            st.write('Difference_ before- after= {:,} '.format(int(value((before_opt_cost) -  sum(total_after_opt)))))
    
            st.write('percentage_decrease= {:,} '.format(int(value(((((before_opt_cost) -  sum(total_after_opt)))/(before_opt_cost))*100))))






st.write("\n")
if __name__=='__main__':
    main()
#import xlrd
#book = xlrd.open_workbook("excel.xls") # in my case the directory contains the excel file named excel.xls


st.write("\n\n\n")


import streamlit as st
import time

st.set_page_config(
    page_title="Styled Buttons Demo",
    page_icon="🎨",
    layout="centered"
)

# Custom CSS for button styling
st.markdown("""
<style>
/* Green button for Data Link */
div.stButton > button:first-child {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 24px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 4px;
    transition: all 0.3s ease;
}

div.stButton > button:first-child:hover {
    background-color: #45a049;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* Orange button for About */
div.stButton > button:nth-child(2) {
    background-color: #FF9800;
    color: white;
    border: none;
    padding: 10px 24px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 4px;
    transition: all 0.3s ease;
}

div.stButton > button:nth-child(2):hover {
    background-color: #e68a00;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* Success message styling */
.success-msg {
    padding: 12px;
    background-color: #d4edda;
    color: #155724;
    border-radius: 4px;
    border: 1px solid #c3e6cb;
    margin: 10px 0;
}

/* Link styling */
.data-link {
    font-size: 18px;
    font-weight: bold;
    color: #1a73e8;
    text-decoration: none;
}
.data-link:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("🎨 Streamlit Button Styling Demo")
st.markdown("This demo shows how to properly style buttons in Streamlit with custom CSS.")

# Create two columns for buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Data Link", key="data_link_button"):
        st.session_state.show_data_link = True
        st.session_state.show_about = False

with col2:
    if st.button("ℹ️ About", key="data_about_button"):
        st.session_state.show_about = True
        st.session_state.show_data_link = False

# Display content based on button clicks
if st.session_state.get('show_data_link'):
    
    st.markdown('<a href="https://drive.google.com/file/d/1WERrd0WxfI18X_XIBe6NyAMGwle-LbIy/view?usp=sharing" class="data-link" target="_blank">📎 Open Data Link</a>', unsafe_allow_html=True)
    st.write("https://drive.google.com/file/d/1WERrd0WxfI18X_XIBe6NyAMGwle-LbIy/view?usp=sharing")

if st.session_state.get('show_about'):
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; border-left: 4px solid #FF9800;">
        <h3>About This Application</h3>
        
        <p><strong>Built with:</strong></p>
        <ul>
            <li>Streamlit</li>
          
            <li>Python</li>
        </ul>
        
    </div>
    """, unsafe_allow_html=True)


