import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

def main():
    st.title('Matching Variants Application')





    st.sidebar.image('leoniWhite.png', width=200)

    st.sidebar.header('Upload Forcast')
    uploaded_file1 = st.sidebar.file_uploader("Choose a file", type=["xlsx", "xls"])

    st.sidebar.header('Upload History')
    uploaded_file2 = st.sidebar.file_uploader("Choose another file", type=["xlsx", "xls"])

    if uploaded_file1 is not None and uploaded_file2 is not None:
        df2 = pd.read_excel(uploaded_file1)
        df1 = pd.read_excel(uploaded_file2)

        df2['WH'] = df2['WH'].str.split(',').apply(lambda x: np.array(x, dtype=int))
        df1['Module Number'] = df1['Module Number'].str.split(',').apply(lambda x: np.array(x, dtype=int))

        df1['Tuple_Module'] = df1['Module Number'].apply(tuple)

        variant_dict = dict(zip(df1['Tuple_Module'], df1['Variant']))

        df2['Variant'] = df2['WH'].apply(lambda x: variant_dict.get(tuple(x), np.nan))

        df_non_null = df2.dropna(subset=['Variant'])
        df_null = df2[df2['Variant'].isnull()]

        df_non_null.to_excel('output_non_null.xlsx', index=False)
        df_null.to_excel('output_null.xlsx', index=False)

        df_non_null['Variant'] = df_non_null['Variant']
        df_non_null['WH'] = df_non_null['WH'].apply(tuple)

        grouped_data = df_non_null.groupby(['Variant', 'WH', 'DDATE'])['QTY'].sum()
        grouped_data.reset_index().to_excel('output_no_null.xlsx', index=False)
        print(grouped_data)

        st.write("### Results Variants with total quantity:")
        st.dataframe(grouped_data)

        if st.button('Show Download link'):
            output_buffer = BytesIO()
            grouped_data.reset_index().to_excel(output_buffer, index=False)
            output_buffer.seek(0)
            st.download_button(label='Download Results', data=output_buffer, file_name='grouped_data.xlsx', key='download_button')

        st.write("### History:")
        st.dataframe(df1)

        st.write("### Forcast:")
        st.dataframe(df2)

if __name__ == '__main__':
    main()
