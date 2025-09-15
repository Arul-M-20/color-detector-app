import streamlit as st
import pandas as pd
import cv2
import numpy as np

# Load the color dataset
# Ensure colors.csv is in the same directory as app.py
df = pd.read_csv("colors.csv")

# Function to get the closest color name from RGB values
def get_color_name(R, G, B):
    min_dist = float('inf')
    closest_color_name = "Unknown"
    for i in range(len(df)):
        d = np.sqrt(
            (R - df.loc[i, "R"]) ** 2
            + (G - df.loc[i, "G"]) ** 2
            + (B - df.loc[i, "B"]) ** 2
        )
        if d < min_dist:
            min_dist = d
            closest_color_name = df.loc[i, "color_name"]
    return closest_color_name

# Streamlit app layout
st.title("🎨 Image Color Detector")
st.markdown("Upload an image and click on it to see the color details.")

# Image uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image using OpenCV
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    # Display the image and handle clicks
    with st.container():
        st.subheader("Click on the image to detect color")
        st.image(image, channels="BGR", use_column_width=True)

    # Get click coordinates and display color info
    # Note: Streamlit's click functionality can be tricky.
    # The following is a conceptual approach. A more robust solution might use
    # st-click-detector or similar custom components for precise coordinates.
    # For this hackathon, a simple workaround is to let the user select a point.

    # Conceptual part: In a real app, you would get x, y from a click event.
    # For this example, let's assume we have a simple placeholder.
    if st.button("Get Color at Center"):
        h, w, _ = image.shape
        x, y = w // 2, h // 2
        
        # Get BGR values (OpenCV reads in BGR)
        b, g, r = image[y, x]
        
        # Convert to RGB
        rgb_tuple = (int(r), int(g), int(b))
        
        # Get color name
        color_name = get_color_name(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])
        
        st.subheader("Detected Color Details:")
        st.write(f"**Color Name:** {color_name}")
        st.write(f"**RGB Values:** {rgb_tuple}")
        
        # Display a color box
        st.color_picker("Color Reference", "#%02x%02x%02x" % rgb_tuple)