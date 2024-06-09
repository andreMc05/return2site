import streamlit as st
import pandas as pd
import os
from urllib.parse import urlparse
from st_aggrid import AgGrid, GridOptionsBuilder

# This is the command to launch th app
# streamlit run return2site.py --server.enableXsrfProtection false
# ADD AgGrid https://github.com/PablocFonseca/streamlit-aggrid

def read_uploaded_file(file):
    content = file.read().decode("utf-8").strip().split('\n\n')
    return content

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read().strip().split('\n\n')
    return content

def parse_content(content):
    parsed_content = []
    for group in content:
        lines = group.split('\n')
        if len(lines) == 2:
            parsed_content.append({"Title": lines[0], "URL": lines[1]})
    return parsed_content

def list_files_in_directory(directory_path):
    return [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.txt')]

def get_website_name(url):
    domain = urlparse(url).netloc
    return domain

def main():
    st.title("Text File Content Viewer")

    option = st.selectbox("Choose input method", ("Single File", "Folder"))
    data_collection = []

    if option == "Single File":
        uploaded_file = st.file_uploader("Choose a text file", type="txt")
        if uploaded_file is not None:
            content = read_uploaded_file(uploaded_file)
            parsed_content = parse_content(content)
            data_collection.extend(parsed_content)
    
    elif option == "Folder":
        directory_path = st.text_input("Enter the folder path")
        if directory_path:
            if os.path.isdir(directory_path):
                files = list_files_in_directory(directory_path)
                if files:
                    for file_path in files:
                        content = read_text_file(file_path)
                        parsed_content = parse_content(content)
                        data_collection.extend(parsed_content)
                else:
                    st.write("No text files found in the directory.")
            else:
                st.write("Invalid directory path.")

    if data_collection:
        # Create DataFrame and add Website Name and Button columns
        df = pd.DataFrame(data_collection)
        #df['Website'] = df['URL'].apply(get_website_name)
        #df['Button'] = df['URL'].apply(lambda x: f'<a href="{x}" target="_blank"><button>Go to Website</button></a>')
        
        st.data_editor(
            df,
            column_config={
                'Title': st.write(df['Title']),
                'URL': st.column_config.LinkColumn(
                    'Link', display_text=st.write(df['URL'].apply(get_website_name))
                )
            }
        )
        
        # Display the DataFrame for debugging purposes
        # st.write("DataFrame Preview:")
        # st.write(df[['Title', 'Website', 'Button']])
        
        # Configure AgGrid
        # gb = GridOptionsBuilder.from_dataframe(df)
        # gb.configure_column("Button", headerName="Go to Website", cellRenderer='HtmlCellRenderer')
        # gb.configure_pagination(paginationAutoPageSize=True)
        # gb.configure_default_column(editable=True, filter=True, sortable=True)
        # gridOptions = gb.build()

        st.write("Data Grid")
        # AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True, allowHtml=True)
    else:
        st.write("No data to display.")

if __name__ == "__main__":
    main()
