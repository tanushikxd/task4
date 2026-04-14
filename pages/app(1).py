import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Whole sales")

df = pd.read_csv("final_DATA1.csv")

df['date'] = pd.to_datetime(df['date'])

# top5 (days)
daily_revenue = df.groupby('date')['paid_price'].sum()

top5_days = (
    daily_revenue
    .sort_values(ascending=False)
    .head(5)
)

# changed date type
top5_days.index = top5_days.index.strftime('%Y-%m-%d')

# working users (unique)
unique_users = df['user_key'].nunique()

# authors (unique)
unique_author_sets = df['author_set'].nunique()

# most popular author
# top_author = (
#     df.groupby('author')['quantity']
#     .sum()
#     .sort_values(ascending=False)
#     .head(1)
# )

# most popular author
authors_df = df.copy()

authors_df['author'] = authors_df['author'].astype(str).str.split(',') #if i guessed it correctly, to get a proper authors i need to break the col into list

authors_df = authors_df.explode('author')

authors_df['author'] = authors_df['author'].str.strip()

top_author = (
    authors_df.groupby('author')['quantity']
    .sum()
    .sort_values(ascending=False)
    .head(1)
)

# best costumer
best_costumer = (
    df.groupby('user_key')
    .agg({
        'paid_price': 'sum',
        'user_id': lambda x: list(set(x))
    })
    .sort_values('paid_price', ascending=False)
    .head(1)
)

# kpi (avg sales)
col1, col2, col3 = st.columns(3)

col1.metric("Unique users", unique_users)
col2.metric("Author sets", unique_author_sets)

if len(best_costumer) > 0:
    ids = best_costumer['user_id'].values[0]
    ids_str = ", ".join(map(str, ids))
    col3.metric("Best costumer IDs", ids_str)
else:
    col3.metric("Best costumer IDs", "No info")

# table
col4, col5 = st.columns(2)

with col4:
    st.subheader("Top 5 days by revenue")
    st.dataframe(top5_days)

with col5:
    st.subheader("Most popular author")
    st.dataframe(top_author)

# chart
st.subheader("Daily revenue")

fig, ax = plt.subplots()
daily_revenue.plot(ax=ax)
ax.set_xlabel("Date")
ax.set_ylabel("Revenue")

st.pyplot(fig)