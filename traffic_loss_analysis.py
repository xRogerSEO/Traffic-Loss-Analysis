import streamlit as st
import pandas as pd

# Function to load data from various file types
def load_data(file):
    if file.type == "text/csv":
        return pd.read_csv(file)
    else:  # This covers both xls and xlsx file formats
        return pd.read_excel(file)

# Function to process data and generate the new tab content
def process_data_for_new_tab(data):
    # Aggregate data by URL
    # Assuming the existence of columns: 'URL', 'Search Volume', 'Current Position', 'Previous Position'
    data_agg = data.groupby('URL').agg(
        Vol=('Search Volume', 'sum'),
        Num_of_KWs=('Keyword', 'count'),
        Organic_Pos_Declined=lambda x: (x['Previous Position'] - x['Current Position']).sum()
    ).reset_index()
    
    return data_agg

# Streamlit app setup
st.title('Traffic Loss Analysis - Output Generation')

# Uploaders
declined_file = st.file_uploader("Upload the 'Declined' report (CSV, XLS, XLSX):", type=['csv', 'xls', 'xlsx'], key="declined")
lost_file = st.file_uploader("Upload the 'Lost' report (CSV, XLS, XLSX):", type=['csv', 'xls', 'xlsx'], key="lost")

if declined_file and lost_file:
    # Load data
    declined_data = load_data(declined_file)
    lost_data = load_data(lost_file)
    
    # Process data
    declined_output = process_data_for_new_tab(declined_data)
    lost_output = process_data_for_new_tab(lost_data)
    
    # Save outputs to a new Excel file with separate tabs
    with pd.ExcelWriter('/mnt/data/SEO_Analysis_Output.xlsx') as writer:
        declined_output.to_excel(writer, sheet_name='Declined Keywords Analysis', index=False)
        lost_output.to_excel(writer, sheet_name='Lost Keywords Analysis', index=False)
    
    st.success('Analysis completed. Download the Excel file from the link below:')
    st.markdown('[Download SEO Analysis Output.xlsx](/mnt/data/SEO_Analysis_Output.xlsx)')
else:
    st.write("Please upload both reports to start the analysis.")
