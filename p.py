import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

def download_results(dataframe, filename):
            output_buffer = BytesIO()
            dataframe.reset_index().to_excel(output_buffer, index=False)
            output_buffer.seek(0)
            st.download_button(label=f'Download {filename}', data=output_buffer, file_name=filename, key=f'download_{filename}')

def main():
    st.title('Matching Variants Application')

    st.sidebar.image('leoniWhite.png', width=200)

    st.sidebar.header('Upload Forecast')
    uploaded_file2 = st.sidebar.file_uploader("Choose a file", type=["xlsx", "xls"])

    st.sidebar.header('Upload History')
    uploaded_file1 = st.sidebar.file_uploader("Choose another file", type=["xlsx", "xls"])

    if uploaded_file2 is not None and uploaded_file1 is not None:

        decomp_data = pd.read_excel(uploaded_file1)
        forecast_data = pd.read_excel(uploaded_file2)

        grouped_decomp = decomp_data.groupby('Variant')['Number'].apply(lambda x: ','.join(str(i) for i in x)).reset_index()
        xs = grouped_decomp.drop_duplicates(subset='Number')

        # Drop duplicates for ys
        ys = forecast_data

        def sequence_same_elements(seq1, seq2):
            return set(seq1) == set(seq2)

        df1 = xs
        df2 = ys

        df1['Variant'] = df1['Variant'].astype('object')
        for index, row in df2.iterrows():
            wh_values = list(map(int, row['WH'].split(',')))  
            for index_1, row_1 in df1.iterrows():
                module_numbers = list(map(int, row_1['Number'].split(','))) 
        
                if sequence_same_elements(wh_values, module_numbers):
                    df2.at[index, 'Variant'] = row_1['Variant']
                    break 
        
        result_df = df2.groupby(['DDATE', 'Variant', 'WH'], as_index=False)['QTY'].sum()

        # Filter df2 for rows where 'Variant' is null
        df2_null = df2[df2['Variant'].isnull()]

        # Filter df2 for rows where 'Variant' is not null
        df2_non_null = df2[df2['Variant'].notnull()]

        st.write("### Results:")
        st.dataframe(result_df)

        if st.button('Download All Results', key='download_results'):
            download_results(result_df, 'results_all.xlsx')

        st.write("### History:")
        st.dataframe(grouped_decomp)

        st.write("### Forecast:")
        st.dataframe(forecast_data)

        st.write("### Results:")
        st.dataframe(df2)

        # Download button for all results
        if st.button('Download All Results', key='download_all_results'):
            download_results(df2, 'results_all.xlsx')

        st.write("### Results not Null:")
        st.dataframe(df2_non_null)

        # Download button for non-null results
        if st.button('Download Non-Null Results', key='download_non_null_results'):
            download_results(df2_non_null, 'results_non_null.xlsx')

        st.write("### Results Null:")
        st.dataframe(df2_null)

        # Download button for null results
        if st.button('Download Null Results', key='download_null_results'):
            download_results(df2_null, 'results_null.xlsx')



if __name__ == '__main__':
    main()
