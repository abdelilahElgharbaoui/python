import streamlit as st
import pandas as pd
import numpy as np


def save_updated_classeur2(classeur2,s):
    file_path = f'result{s}.xlsx'
    classeur2.to_excel(file_path, index=False)
    st.success(f"result{s} saved successfully!")
    return file_path

def main():
    st.title('Matching Variants Application')

    # Upload Classeur1
    st.sidebar.header('Upload Forcast')
    uploaded_file1 = st.sidebar.file_uploader("Choose a file", type=["xlsx", "xls"])



    # Upload Classeur2
    st.sidebar.header('Upload History')
    uploaded_file2 = st.sidebar.file_uploader("Choose another file", type=["xlsx", "xls"])

    if uploaded_file1 is not None and uploaded_file2 is not None:
        # Load data from uploaded files
        df2 = pd.read_excel(uploaded_file1)

        df1 = pd.read_excel(uploaded_file2)

        df2['WH'] = df2['WH'].str.split(',').apply(lambda x: np.array(x, dtype=int))
        df1['Module Number'] = df1['Module Number'].str.split(',').apply(lambda x: np.array(x, dtype=int))

        # Create a new column with tuple representations of the arrays for merging
        df1['Tuple_Module'] = df1['Module Number'].apply(tuple)

        # Create a dictionary mapping tuples to variants
        variant_dict = dict(zip(df1['Tuple_Module'], df1['Variant']))

        # Use np.isin to find matching tuples and map the variants
        df2['Variant'] = df2['WH'].apply(lambda x: variant_dict.get(tuple(x), np.nan))

        # Separate DataFrame into rows with non-null and null variants
        df_non_null = df2.dropna(subset=['Variant'])
        df_null = df2[df2['Variant'].isnull()]

        # Save to separate Excel files
        df_non_null.to_excel('output_non_null.xlsx', index=False)
        df_null.to_excel('output_null.xlsx', index=False)

        df_non_null['Variant'] = df_non_null['Variant']
        df_non_null['WH'] = df_non_null['WH'].apply(tuple)

        grouped_data = df_non_null.groupby(['Variant', 'WH','DDATE'])['QTY'].sum()
        grouped_data.reset_index().to_excel('output_no_null.xlsx', index=False)
        # Print the result
        print(grouped_data)

        # Display the tables
        st.write("### History:")
        st.dataframe(df1)

        st.write("### Forcast:")
        st.dataframe(df2)

        st.write("### Results Variants Null:")

        st.dataframe(df_null)

        st.write("### Results Variants not Null:")

        st.dataframe(df_non_null)

        st.write("### Results Variants with total quantity:")

        st.dataframe(grouped_data)

        st.write("### Save Results Variants not Null:")
        st.write("Click the button below to download the updated Results not Null.")
        if st.button("Download Results not Null", key='download_not_null'):
            file_path = save_updated_classeur2(df_non_null, 1)
            st.markdown(get_download_link(file_path, 'Download Results not Null'), unsafe_allow_html=True)

        # Save the updated file
        st.write("### Save Results Variants Null:")
        st.write("Click the button below to download the updated Results Null.")
        if st.button("Download Results Variants Null", key='download_null'):
            file_path = save_updated_classeur2(df_null, 2)
            st.markdown(get_download_link(file_path, 'Download Results Variants Null'), unsafe_allow_html=True)

        # Save the updated file
        st.write("### Save Results Variants with total quantity:")
        st.write("Click the button below to download the updated Results with total quantity.")
        if st.button("Download Results Variants with total quantity", key='download_total_qty'):
            file_path = save_updated_classeur2(grouped_data.reset_index(), 3)
            st.markdown(get_download_link(file_path, 'Download Results Variants with total quantity'), unsafe_allow_html=True)

def get_download_link(file_path, label):
            """Generate a download link for a file."""
            href = f'<a href="/download/{file_path}" download="{file_path}">{label}</a>'
            return href
if __name__ == '__main__':
    main()
