import pandas as pd
import streamlit as st
import plotly.express as px

# Load cleaned data
df = pd.read_csv('jumia_cleaned_data.csv')

# Streamlit application
st.title("Jumia Liquor Market Dashboard")

# Dropdown for selecting multiple product names
selected_products = st.multiselect(
    "Select Products:",
    df['name'].unique(),
    default=df['name'].unique()[:4]  # Default to the first 4 products
)

# Filter DataFrame based on selected products
filtered_df = df[df['name'].isin(selected_products)]

# Create a sidebar for additional options
st.sidebar.header("Dashboard Options")
show_discounts = st.sidebar.checkbox("Show Discount Tracking", value=True)
show_avg_price = st.sidebar.checkbox("Show Average Prices", value=True)

# Best Price Pie Chart for selected products
st.subheader("Best Price Distribution")
best_price_pie_fig = px.pie(
    filtered_df,
    names='name',
    values='current_price',
    title="Best Price Distribution for Selected Products",
    hole=0.3
)
st.plotly_chart(best_price_pie_fig)

# Price Trend Column Chart for selected products
st.subheader("Price Trend")
price_trend_fig = px.bar(
    filtered_df,
    x='name',  # Use product name for x-axis
    y='current_price',
    color='name',
    labels={'current_price': 'Current Price (KSh)'},
    title="Price Trends for Selected Products"
)
price_trend_fig.update_layout(xaxis_title='Product', yaxis_title='Price (KSh)', legend_title='Products')
st.plotly_chart(price_trend_fig)

# Discount Tracking Bar Chart for selected products
if show_discounts:
    st.subheader("Discount Tracking")
    discount_bar_fig = px.bar(
        filtered_df,
        x='name',
        y='discount',
        color='name',
        labels={'name': 'Product', 'discount': 'Discount (%)'},
        title="Discount Tracking for Selected Products",
        text='discount'  # Show discount percentage on bars
    )
    discount_bar_fig.update_layout(xaxis_title='Product', yaxis_title='Discount (%)', showlegend=False)
    st.plotly_chart(discount_bar_fig)

# Best Buy Insights Scatter Plot for selected products
if show_avg_price:
    st.subheader("Best Buy Insights - Average Price Comparison")
    avg_price_df = filtered_df.groupby('name')['current_price'].mean().reset_index()

    avg_price_fig = px.scatter(
        avg_price_df,
        x='name',
        y='current_price',
        size='current_price',
        color='name',
        hover_name='name',
        title="Average Prices of Selected Products",
        labels={'current_price': 'Average Price (KSh)', 'name': 'Product'}
    )
    avg_price_fig.update_layout(xaxis_title='Product', yaxis_title='Average Price (KSh)', showlegend=False)
    st.plotly_chart(avg_price_fig)

# Run the Streamlit app
if __name__ == '__main__':
    st.write("This dashboard provides insights on price trends, discount tracking, and optimal buying times for various products.")