import streamlit as st
import pandas as pd
import io
import plotly.express as px # requirements.txt এ plotly যোগ করতে হবে

st.set_page_config(page_title="Detailed Child Labor Monitor", layout="wide")

st.title("🇧🇩 Bangladesh Child Labor Analysis (2022)")
st.markdown("বিভাগ, খাত এবং জেন্ডার ভিত্তিক শিশুশ্রমের বিস্তারিত পরিসংখ্যান।")

# Dataset
csv_data = """division,year,sector,gender,child_labor_rate
Dhaka,2022,Agriculture,Boys,4.2
Dhaka,2022,Agriculture,Girls,1.1
Dhaka,2022,Industry,Boys,5.1
Dhaka,2022,Industry,Girls,1.4
Dhaka,2022,Services,Boys,5.8
Dhaka,2022,Services,Girls,1.6
Chittagong,2022,Agriculture,Boys,6.5
Chittagong,2022,Agriculture,Girls,1.8
Chittagong,2022,Industry,Boys,7.2
Chittagong,2022,Industry,Girls,1.9
Chittagong,2022,Services,Boys,7.9
Chittagong,2022,Services,Girls,2.1
Rajshahi,2022,Agriculture,Boys,3.8
Rajshahi,2022,Agriculture,Girls,1.0
Rajshahi,2022,Industry,Boys,2.9
Rajshahi,2022,Industry,Girls,0.8
Rajshahi,2022,Services,Boys,3.4
Rajshahi,2022,Services,Girls,0.9
Sylhet,2022,Agriculture,Boys,4.1
Sylhet,2022,Agriculture,Girls,1.2
Sylhet,2022,Industry,Boys,3.2
Sylhet,2022,Industry,Girls,0.9
Sylhet,2022,Services,Boys,3.7
Sylhet,2022,Services,Girls,1.1"""

df = pd.read_csv(io.StringIO(csv_data))

# Sidebar Filters
st.sidebar.header("ফিল্টার কন্ট্রোল")
selected_div = st.sidebar.multiselect("বিভাগ নির্বাচন করুন", df["division"].unique(), default=df["division"].unique())
selected_sector = st.sidebar.multiselect("খাত নির্বাচন করুন", df["sector"].unique(), default=df["sector"].unique())

filtered_df = df[(df["division"].isin(selected_div)) & (df["sector"].isin(selected_sector))]

# Top Overview Metrics
st.subheader("📊 দ্রুত সারসংক্ষেপ")
c1, c2, c3 = st.columns(3)
avg_rate = filtered_df["child_labor_rate"].mean()
c1.metric("গড় শিশুশ্রমের হার", f"{round(avg_rate, 2)}%")
c2.metric("সর্বোচ্চ হার (ছেলে)", f"{filtered_df[filtered_df['gender']=='Boys']['child_labor_rate'].max()}%")
c3.metric("সর্বোচ্চ হার (মেয়ে)", f"{filtered_df[filtered_df['gender']=='Girls']['child_labor_rate'].max()}%")

# Visualizations
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("সেক্টর ভিত্তিক তুলনা (ছেলে বনাম মেয়ে)")
    fig = px.bar(filtered_df, x="sector", y="child_labor_rate", color="gender", barmode="group", 
                 title="Sector-wise Gender Comparison")
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("বিভাগ ভিত্তিক বন্টন")
    fig2 = px.sunburst(filtered_df, path=['division', 'sector'], values='child_labor_rate',
                       title="Division & Sector Hierarchy")
    st.plotly_chart(fig2, use_container_width=True)

# Comparison Table
st.subheader("বিস্তারিত ডেটা টেবিল")
st.dataframe(filtered_df, use_container_width=True)

# Key Findings
st.info("💡 **মূল পর্যবেক্ষণ:** বাংলাদেশে শিশুশ্রম মূলত সার্ভিস ও ইন্ডাস্ট্রি সেক্টরে বেশি এবং ছেলেদের হার মেয়েদের চেয়ে ৩-৪ গুণ বেশি।")
