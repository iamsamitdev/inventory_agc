import streamlit as st
import pandas as pd
from .models import Person

def main():
    # Read data from the database
    data = Person.objects.all().values()

    # Convert data to a Pandas DataFrame
    df = pd.DataFrame.from_records(data)

    # Display the DataFrame in Streamlit
    st.dataframe(df)

if __name__ == '__main__':
    main()
