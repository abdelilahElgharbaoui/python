import streamlit as st
import pandas as pd
import numpy as np


def save_updated_classeur2(classeur2,s):
    classeur2.to_excel(f'result{s}.xlsx', index=False)
    st.success(f"result{s} saved successfully!")

def main():
    st.title('Matching Variants App')

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

        # Save the updated file
        st.write("### Save Results Variants not Null:")
        st.write("Click the button below to download the updated Results not Null.")
        st.button("Download Results not Null", on_click=save_updated_classeur2, args=(df_non_null,1))


          # Save the updated file
        st.write("### Save Results Variants Null:")
        st.write("Click the button below to download the updated Results not Null.")
        st.button("Download Results Varuants Null", on_click=save_updated_classeur2, args=(df_null,2))



  # Save the updated file
        st.write("### Save Results Variants with total quantity:")
        st.write("Click the button below to download the updated Results not Null.")
        st.button("Download Results Variants with total quantity", on_click=save_updated_classeur2, args=(grouped_data,3))


if __name__ == '__main__':
    main()
