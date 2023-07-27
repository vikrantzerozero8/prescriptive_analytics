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
        manufacturer = st.selectbox('Select Manufacturer', options=['']+list(name.keys()))
        # display selectbox 2 if manufacturer is not "select"
        if manufacturer != '':
            model_number = st.selectbox('Select Model Number', options=[''] + name[manufacturer])
        if st.button('Submit'):
            
            print(df.columns)
            df.columns
            
            df['Customer Name'].nunique()
            
            df['Customer Name'].nunique()
            
            df.rename(columns = {'Customer Name':"Customer Name","Plant ":"Warehouse","Target Quantity":"Net Weight"},inplace = True)
            
            #df.rename(columns = {'Plant': 'Warehouse'} , inplace = True)
            
            # unique warehouses and party_names
            warehouses = df['Warehouse'].unique()
            party_names = df['Customer Name'].unique()
            
            print(warehouses)
            print("\n")
            print(party_names)
            
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
            
            # Create a pivot table with Warehouse as index, Customer Name as columns, and Distance as values
            distance_matrix = df.pivot_table(values= 'Distance', index='Warehouse', columns='Customer Name')
            # fill with 10000 Wherever no supply
            distance_matrix.fillna(10000, inplace = True)
            distance_matrix
            
            # Create a pivot table with Warehouse as index, Customer Name as columns, and freight rate as values
            freight_mat = df.pivot_table(values = 'Freight_Rate', index = 'Warehouse', columns = 'Customer Name')
            # Fill with 10000 wherever no supply
            freight_mat.fillna(100000, inplace = True)
            freight_mat
            
            # Create a pivot table with Warehouse as index, Customer Name as columns, and shipping cost as values
            cost_mat = df.pivot_table(values = 'shipping_cost', index = 'Warehouse', columns = 'Customer Name')
            #fill with 100000 wherever no supply
            cost_mat = cost_mat.fillna(100000)
            cost_mat
            
            # Create a pivot table with Warehouse as index, Customer Name as columns, and Net weight as values
            weight_mat = df.pivot_table(values = 'Net Weight', index = 'Warehouse', columns = 'Customer Name', aggfunc =sum )
            # fill with zeros wherever no sulpply
            weight_mat = weight_mat.fillna(0)
            weight_mat
            
            # create pivot table with warehouse as index and sum of net weight for particular warehouse as values
            supply = pd.pivot_table(df, values='Net Weight', index = 'Warehouse', aggfunc=sum, margins=True)
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
            supply
            
            #create a pivot_tabel for total demand of each party (Before optimization the Quantity of df Transport from Warehouse the Party)
            demand = pd.pivot_table(df, values='Net Weight', index ='Warehouse', columns ='Customer Name', aggfunc = sum, margins =True, margins_name='Grand Total')
            demand
            
            # Only consider the Demand
            demand = demand.iloc[6:]
            # Rename the column
            demand.rename(index= {'Grand Total': 'Demand'}, inplace = True)
            demand
            
            # Define the problem
            prob = LpProblem("Transportation Problem", LpMinimize)
            
            # Define decision variables
            route_vars = LpVariable.dicts("Route", (warehouses, party_names), lowBound=0, cat='Continuous')
            route_vars
            
            # Define the objective function
            prob += lpSum([route_vars[w][p] * cost_mat.loc[w][p] for w in warehouses for p in party_names]), " Transportation Cost"
            
            # Define the supply constraint
            for w in warehouses:
                prob += lpSum([route_vars[w][p]   for p in party_names]) <= supply.loc[w] , "Sum of quatity supplied from Warehouse to paty %s" % w
            
            demand2 = demand.T
            demand2
            
            # Define Demand Constraints
            for p in party_names:
                prob += lpSum([route_vars[w][p] for w in warehouses]) >= demand2.loc[p], 'Sum of Demand of party %s' % p
            
            # Execute the problem
            prob.solve()
            # save transformation pipeline and model
            
            
            #print('Total_transportation_Costs = {:,} '.format(int(value(prob.objective))))
            
            # shows the status of the Problem
            #print(f"Status: {LpStatus[prob.status]}")
            
            # Create DataFrame
            decision_var_df = pd.DataFrame(index=distance_matrix.index, columns=distance_matrix.columns, dtype='float')
            
            # Fill the DataFrame with the optimized values of the decision variables
            for w in distance_matrix.index:
                for p in distance_matrix.columns:
                    decision_var_df.loc[w, p] = route_vars[w][p].varValue
            
            # Decision_Variables(How Much Quantity of df Transport form Warehouse to Party )
            decision_var_df
            
            # Verify the cost after Optimization
            total_after_opt = [decision_var_df.loc[w][p] * cost_mat.loc[w][p] .sum().sum() for w in warehouses for p in party_names]
            
            total1 = sum(total_after_opt)
            #print('total_cost_after_opt',total1)
            
            # Before_Optimization the Transportation Cost in ₹
            before_opt_cost = df['Amount'].sum()
            #print('total_cost_before_opt',before_opt_cost)
            
            #Total Cost - Total Minimized Cost
            #print("Difference_ before- after:",(before_opt_cost) -  sum(total_after_opt))
            
            # Calculating the percentage decrease in total transportation cost
            #print("percentage_decrease:",((((before_opt_cost) -  sum(total_after_opt)))/((before_opt_cost)))*100)

            st.write('You selected ' + manufacturer + ' ' + model_number)

            st.table("Output : {}".format(distance_matrix))

             st.success("Output : {}".format(freight_mat))

            st.success("Output : {}".format(cost_mat))
    
            st.success("Output : {}".format(weight_mat))
    
            st.success("Output : {}".format(route_vars))
    
            st.success("Output : {}".format(cost_mat))
    
            st.success('Total_transportation_Costs = {:,} '.format(int(value(prob.objective))))
    
            st.success('total_cost_before_opt',before_opt_cost)
    
            st.success('total_cost_after_opt',total1)
    
            st.success("Difference_ before- after:",(before_opt_cost) -  sum(total_after_opt))
    
            st.success("percentage_decrease:",((((before_opt_cost) -  sum(total_after_opt)))/((before_opt_cost)))*100)

          
            
        

        

        



    
    if st.button("About"):
        st.text("Lets learn") 
        st.text("Built with streamlit")  

if __name__=='__main__':
    main()
