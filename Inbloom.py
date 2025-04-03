import streamlit as st
import pandas as pd
import random
import plotly.express as px
import plotly.figure_factory as ff
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageFilter, ImageEnhance
import os

# Function to generate dataset
def generate_dataset():
    events = ["Dance", "Music", "Drama", "Painting", "Debate", "Photography", "Poetry", "Fashion Show", "Singing", "Quiz"]
    colleges = ["XYZ University", "ABC College", "LMN Institute", "PQR Academy", "DEF College"]
    states = ["California", "Texas", "New York", "Florida", "Illinois"]
    feedback_options = [
        "Amazing experience!", "Loved the event!", "Could be better.", "Great organization!", "Had lots of fun!",
        "Enjoyed every moment!", "Too crowded.", "Judging was fair.", "Will participate again!", "Not well managed."
    ]
    
    data = []
    for i in range(250):
        participant_id = f"P{i+1:03d}"
        name = f"Participant {i+1}"
        age = random.randint(18, 25)
        college = random.choice(colleges)
        state = random.choice(states)
        event = random.choice(events)
        date = f"2025-04-{random.randint(1, 5):02d}"
        score = random.randint(1, 10)
        feedback = random.choice(feedback_options)
        
        data.append([participant_id, name, age, college, state, event, date, score, feedback])
    
    columns = ["Participant_ID", "Name", "Age", "College", "State", "Event", "Date", "Score", "Feedback"]
    df = pd.DataFrame(data, columns=columns)
    return df

# Load Dataset
df = generate_dataset()

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["InBloom Dataset", "Dashboard", "Text Analysis", "Image Processing"])

if page == "InBloom Dataset":
    st.title("🎭 INBLOOM '25")
    st.dataframe(df)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇ Download CSV", csv, "inbloom_dataset.csv", "text/csv", key="download-csv")

elif page == "Dashboard":
    st.title("📊 Participation Trends Dashboard")
    selected_event = st.selectbox("🎭 Select Event", ["All"] + sorted(df["Event"].unique().tolist()))
    selected_college = st.selectbox("🏫 Select College", ["All"] + sorted(df["College"].unique().tolist()))
    selected_state = st.selectbox("🌎 Select State", ["All"] + sorted(df["State"].unique().tolist()))
    
    filtered_df = df.copy()
    if selected_event != "All":
        filtered_df = filtered_df[filtered_df["Event"] == selected_event]
    if selected_college != "All":
        filtered_df = filtered_df[filtered_df["College"] == selected_college]
    if selected_state != "All":
        filtered_df = filtered_df[filtered_df["State"] == selected_state]
    
    st.write("### 🎭 Event-wise Participation")
    fig_pie_event = px.pie(filtered_df, names="Event", title="Event-wise Participation Distribution")
    st.plotly_chart(fig_pie_event)
    
    st.write("### 📅 Day-wise Participation Trend")
    fig_line_day = px.line(filtered_df, x="Date", y="Score", markers=True, title="Day-wise Participation Trend", color="Date")
    st.plotly_chart(fig_line_day)
    
    st.write("### 🏫 College-wise Score Distribution")
    fig_scatter_college = px.scatter(filtered_df, x="College", y="Score", color="College", title="College-wise Score Distribution", size_max=10)
    st.plotly_chart(fig_scatter_college)
    
    st.write("### 🌳 Treemap of Event-wise Participation")
    fig_treemap = px.treemap(filtered_df, path=["Event", "College"], values="Score", title="Event-wise Participation Treemap")
    st.plotly_chart(fig_treemap)
    
    st.write("### 🔥 Heatmap of Score Correlation")
    correlation = df[["Age", "Score"]].corr()
    fig_heatmap = ff.create_annotated_heatmap(z=correlation.values, x=list(correlation.columns), y=list(correlation.index), colorscale='Viridis')
    st.plotly_chart(fig_heatmap)
    
    st.write("### 📊 Score Distribution Histogram")
    fig_histogram = px.histogram(filtered_df, x="Score", nbins=10, title="Score Distribution Histogram", color="Event")
    st.plotly_chart(fig_histogram)

elif page == "Text Analysis":
    st.title("📝 Text Analysis - Feedback Processing")
    event_selected = st.selectbox("🎭 Select Event for Feedback Analysis", df["Event"].unique())
    event_feedback = df[df["Event"] == event_selected]["Feedback"].tolist()
    
    feedback_text = " ".join(event_feedback)
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='plasma').generate(feedback_text)
    
    st.write(f"### Word Cloud for {event_selected} Feedback")
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
    
    st.write(f"### 📊 Feedback Comparison for {event_selected}")
    feedback_counts = pd.Series(event_feedback).value_counts()
    fig_feedback_chart = px.bar(x=feedback_counts.index, y=feedback_counts.values, labels={'x':'Feedback', 'y':'Count'}, title="Feedback Distribution", color=feedback_counts.index, color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_feedback_chart)

elif page == "Image Processing":
    st.title("📸 Image Processing")
    uploaded_file = st.file_uploader("Upload an event-related image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image")

        if st.button("Convert to Grayscale"):
            grayscale_img = image.convert("L")
            st.image(grayscale_img, caption="Grayscale Image")

        if st.button("Apply Blur"):
            blurred_img = image.filter(ImageFilter.BLUR)
            st.image(blurred_img, caption="Blurred Image")

        if st.button("Sharpen Image"):
            sharpened_img = image.filter(ImageFilter.SHARPEN)
            st.image(sharpened_img, caption="Sharpened Image")

        if st.button("Increase Brightness"):
            brightened_img = ImageEnhance.Brightness(image).enhance(1.5)
            st.image(brightened_img, caption="Brightened Image")

        if st.button("Increase Contrast"):
            contrast_img = ImageEnhance.Contrast(image).enhance(1.5)
            st.image(contrast_img, caption="High Contrast Image")

    # 📅 Day-wise Image Gallery
    st.write("### 📅 Day-wise Image Gallery")
    selected_day = st.selectbox("📅 Select Day", sorted(df["Date"].unique()))
    
    image_folder = "Event_Images"
    image_files = [f for f in os.listdir(image_folder) if selected_day in f]
    
    if not image_files:
        st.write("🚫 No images found for the selected date.")
    else:
        num_cols = 3  # Display images in 3 columns
        cols = st.columns(num_cols)

        for idx, image_file in enumerate(image_files):
            img = Image.open(os.path.join(image_folder, image_file))
            with cols[idx % num_cols]:  # Arrange images in columns
                st.image(img, caption=f"{image_file} - {selected_day}")
