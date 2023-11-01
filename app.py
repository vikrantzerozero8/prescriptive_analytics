import pandas as pd
import streamlit as st
from pulp import *
import numpy as np

# Function to optimize transportation and display results
# Streamlit UI
def main():
    st.title("Optimization Project")
    st.sidebar.title("Monthly Data")

    html_temp = """
    <div style="background-color: tomato; padding: 10px">
        <h2 style="color: white; text-align: center;">Data Report</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    st.text("")

    uploadedFile = st.sidebar.file_uploader("Upload a file", type=['csv', 'xlsx'], accept_multiple_files=False, key="fileUploader")
    if uploadedFile is not None:
        try:
            df = pd.read_excel(uploadedFile)
        except:
            try:
                df = pd.read_csv(uploadedFile)
            except:
                st.sidebar.warning("Invalid file format. Please upload a CSV or Excel file.")
                return
    else:
        st.sidebar.warning("Upload a CSV or Excel file.")
        return
    
    if uploadedFile is not None:
        
            
        df.columns = df.columns.str.replace(' ', '') 
        df.columns = df.columns.str.lower() 
    
        df.rename(columns = {'customername':"Party Name","plant":"Warehouse","targetquantity":"Net Weight","freightrate":"Freight_Rate","distance":"Distance"},inplace = True)
        
        customers_list = df['Party Name'].unique()
        selected_customer = st.selectbox("Select Customer Name to View Data:", customers_list)

        warehouses = df['Warehouse'].unique()
        party_names = df['Party Name'].unique()

        if st.button("Submit"):
        
            df['Freight_Rate'] = 0
            for i in df.index:
                if df['Warehouse'][i] in ['GIR', 'GIR II']:
                    df.at[i, 'Freight_Rate'] = 2.9
                elif df['Warehouse'][i] == 'KSR4':
                    df.at[i, 'Freight_Rate'] = 2.5
                elif df['Warehouse'][i] in ['LKDRM2', 'RSDSH', 'SLKPY']:
                    if df['Distance'][i] <= 40:
                        df.at[i, 'Freight_Rate'] = 100
                    else:
                        df.at[i, 'Freight_Rate'] = 2.5
    
            if df["Net Weight"].dtype == object:
                gh = []
                for i in df['Net Weight']:
                        i = re.sub('[-_,a-zA-Z \n\.\s]', '', i)
                        gh.append(i)
                df1 = pd.DataFrame({'Net Weight':gh})
                df['Net Weight'] = df1['Net Weight'].astype("float")
        
            df['Amount'] = 0
            for i in df.index:
                if (df['Freight_Rate'][i] == 100):
                    df.at[i, "Amount"] = df.at[i, 'Freight_Rate'] * df.at[i, 'Net Weight']
                elif (df['Freight_Rate'][i] < 100):
                    df.at[i, "Amount"] = df.at[i, 'Freight_Rate'] * df.at[i, 'Distance'] * df.at[i, 'Net Weight']
        
            df.dtypes
            # Calculate shipping cost based on Freight Rate and Distance
            df['shipping_cost'] = 0
            for i in df.index:
                if df['Freight_Rate'][i] == 100:
                    df.at[i, "shipping_cost"] = df.at[i, 'Freight_Rate']
                elif df['Freight_Rate'][i] < 100:
                    df.at[i, "shipping_cost"] = df.at[i, 'Freight_Rate'] * df.at[i, 'Distance']
        
            # Create distance matrix with 10,000 for missing values
            distance_matrix = df.pivot_table(values='Distance', index='Warehouse', columns='Party Name')
            distance_matrix.fillna(10000, inplace=True)
        
            # Create matrices for Freight Rate, Shipping Cost, and Net Weight
            freight_mat = df.pivot_table(values='Freight_Rate', index='Warehouse', columns='Party Name')
            freight_mat.fillna(100000, inplace=True)
        
            cost_mat = df.pivot_table(values='shipping_cost', index='Warehouse', columns='Party Name')
            cost_mat.fillna(100000, inplace=True)
        
            weight_mat = df.pivot_table(values='Net Weight', index='Warehouse', columns='Party Name', aggfunc=sum)
            weight_mat.fillna(0, inplace=True)
        
            # Supply constraints for warehouses
            # Supply constraints for warehouses
            supply = {'GIR': 1000000, 'GIR II': 1000000, 'KSR4': 1000000, 'LKDRM2': 1000000, 'RSDSH': 1000000, 'SLKPY': 1000000}
            
            # Demand for each party
            demand = df.groupby('Party Name')['Net Weight'].sum()
    
            # Create the optimization problem
            prob = LpProblem("Transportation Problem", LpMinimize)
        
            # Decision variables
            route_vars = LpVariable.dicts("Route", (distance_matrix.index, distance_matrix.columns), lowBound=0, cat='Continuous')
        
            # Objective function: Minimize transportation cost
            prob += lpSum([route_vars[w][p] * cost_mat.loc[w][p] for w in distance_matrix.index for p in distance_matrix.columns]), "Transportation Cost"
        
            # Supply constraints
            for w in distance_matrix.index:
                prob += lpSum([route_vars[w][p] for p in distance_matrix.columns]) <= supply[w], f"Supply from {w}"
        
            # Demand constraints
            for p in distance_matrix.columns:
                prob += lpSum([route_vars[w][p] for w in distance_matrix.index]) >= demand[p], f"Demand for {p}"
        
            # Solve the problem
            prob.solve()
        
            # Show total transportation cost
            st.write('Total Transportation Costs = {:,}'.format(int(value(prob.objective))))
        
            # Display optimization status
            st.write(f"Status: {LpStatus[prob.status]}")
        
            # Create a DataFrame to store optimized quantities
            decision_var_df = pd.DataFrame(index=distance_matrix.index, columns=distance_matrix.columns, dtype='float')
            
            # Fill the DataFrame with the optimized values of the decision variables
            for w in distance_matrix.index:
                for p in distance_matrix.columns:
                    decision_var_df.loc[w, p] = route_vars[w][p].varValue
            
            # Calculate transportation cost after optimization
            total_after_opt = [decision_var_df.loc[w][p] * cost_mat.loc[w][p].sum().sum() for w in warehouses for p in party_names]
            total1 = sum(total_after_opt)
            
            st.write('Party selected :   ' + selected_customer)
    
            result = decision_var_df.loc[:,selected_customer]
    
            decision_var_df = decision_var_df
            
            total_after_opt = (decision_var_df * df['Freight_Rate']).sum(axis=1).to_frame('After Optimization Amount')
            total_after_opt
            # Before Optimization the Transportation Cost in ₹
            before_opt_cost = df['Amount'].sum()
            
            st.table(result)
    
            st.write('Total_transportation_Costs = {:,} '.format(int(value(prob.objective))))

            
            st.write('total_cost_before_opt= {:,} '.format(int(value(before_opt_cost))))
            
            st.write('total_cost_after_opt= {:,} '.format(int(value(total1))))



if __name__ == '__main__':
    main()
