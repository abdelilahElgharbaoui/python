import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

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

        # Group by and concatenate values in 'Number' column for xs
        xs = decomp_data.groupby('Variant')['Number'].apply(lambda x: ','.join(str(i) for i in x)).reset_index().drop_duplicates(subset='Number')

        # ys is forecast_data
        ys = forecast_data

        def sequence_same_elements(seq1, seq2):
            return np.array_equal(np.sort(seq1), np.sort(seq2))

        for index, row in ys.iterrows():
            wh_values = np.array(list(map(int, row['WH'].split(','))))

            for index_1, row_1 in xs.iterrows():
                module_numbers = np.array(list(map(int, row_1['Number'].split(','))))

                if sequence_same_elements(wh_values, module_numbers):
                    ys.at[index, 'Variant'] = row_1['Variant']
                    break

        result_df = ys.groupby(['DDATE', 'Variant', 'WH'], as_index=False)['QTY'].sum()

        # Filter ys for rows where 'Variant' is null
        ys_null = ys[ys['Variant'].isnull()]

        # Filter ys for rows where 'Variant' is not null
        ys_non_null = ys[ys['Variant'].notnull()]

        st.write("### Results Variants with total quantity:")
        st.dataframe(result_df)

        if st.button('Show Download link'):
            output_buffer = BytesIO()
            result_df.reset_index().to_excel(output_buffer, index=False)
            output_buffer.seek(0)
            st.download_button(label='Download Results', data=output_buffer, file_name='results.xlsx', key='download_button')

        st.write("### History:")
        st.dataframe(xs)

        st.write("### Forecast:")
        st.dataframe(forecast_data)

        st.write("### Results:")
        st.dataframe(ys)

        st.write("### Results not Null:")
        st.dataframe(ys_non_null)

        st.write("### Results Null:")
        st.dataframe(ys_null)

if __name__ == '__main__':
    main()
