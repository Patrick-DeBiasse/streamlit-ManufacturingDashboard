import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Set page config
st.set_page_config(page_title="Manufacturing Dashboard", layout="wide")

# Generate sample data for SPC chart
def generate_spc_data(n_days=30, mean=100, std=5):
    dates = pd.date_range(end=pd.Timestamp.today(), periods=n_days)
    values = np.random.normal(mean, std, n_days)
    return pd.DataFrame({'Date': dates, 'Value': values})

line1_data = generate_spc_data(mean=100)
line2_data = generate_spc_data(mean=95)
line3_data = generate_spc_data(mean=105)

# Generate sample data for scrap reasons
scrap_data = pd.DataFrame({
    'Reason': ['Material Defect', 'Machine Error', 'Operator Error', 'Tool Wear', 'Other'],
    'Percentage': [35, 25, 20, 15, 5]
})

# Function to plot interactive SPC chart
def plot_spc_interactive(data, line_name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Value'], mode='lines+markers', name=line_name))
    fig.add_hline(y=data['Value'].mean(), line_dash="dash", line_color="red", annotation_text="Mean")
    fig.add_hline(y=data['Value'].mean() + 3*data['Value'].std(), line_dash="dot", line_color="red", annotation_text="UCL")
    fig.add_hline(y=data['Value'].mean() - 3*data['Value'].std(), line_dash="dot", line_color="red", annotation_text="LCL")
    fig.update_layout(title=f'SPC Chart - {line_name}', xaxis_title='Date', yaxis_title='Value',
                      hovermode="x unified")
    return fig

# Main app
def main():
    st.title("Manufacturing Dashboard")

    # Sidebar for date range selection
    st.sidebar.header("Filters")
    date_range = st.sidebar.date_input("Select Date Range", value=(line1_data['Date'].min(), line1_data['Date'].max()))

    # SPC Charts Page
    st.header("Statistical Process Control")
    tab1, tab2, tab3 = st.tabs(["Line 1", "Line 2", "Line 3"])
    
    with tab1:
        st.plotly_chart(plot_spc_interactive(line1_data, "Line 1"), use_container_width=True)
    with tab2:
        st.plotly_chart(plot_spc_interactive(line2_data, "Line 2"), use_container_width=True)
    with tab3:
        st.plotly_chart(plot_spc_interactive(line3_data, "Line 3"), use_container_width=True)

    # Scrap Reasons Page
    st.header("Top Scrap Reasons")
    fig = px.bar(scrap_data.sort_values('Percentage', ascending=True), 
                 x='Percentage', y='Reason', orientation='h',
                 title='Percentage Breakdown of Top Scrap Reasons')
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=0.6)
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

    # Add some interactivity
    st.header("Drill Down Analysis")
    selected_line = st.selectbox("Select Production Line", ["Line 1", "Line 2", "Line 3"])
    if selected_line == "Line 1":
        data = line1_data
    elif selected_line == "Line 2":
        data = line2_data
    else:
        data = line3_data
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Average Value", f"{data['Value'].mean():.2f}")
    with col2:
        st.metric("Standard Deviation", f"{data['Value'].std():.2f}")

if __name__ == "__main__":
    main()