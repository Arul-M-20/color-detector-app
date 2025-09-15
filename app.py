import streamlit as st
import pandas as pd
import cv2
import numpy as np

# Load the dataset
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv", names=["color", "color_name", "hex", "R", "G", "B"], header=None)

colors_df = load_colors()

# Function to get color name
def get_color_name(R, G, B):
    minimum = 10000
    cname = ""
    for i in range(len(colors_df)):
        d = abs(R - int(colors_df.loc[i, "R"])) + abs(G - int(colors_df.loc[i, "G"])) + abs(B - int(colors_df.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = colors_df.loc[i, "color_name"]
    return cname

# Streamlit UI
st.title("🎨 Color Detector App")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Convert file to OpenCV image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    # Convert BGR → RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    st.image(img_rgb, caption="Uploaded Image", use_column_width=True)

    st.markdown("### 👉 Click anywhere on the image to detect color")

    # Use Streamlit image coordinates (extra package already added in your logs)
    from streamlit_image_coordinates import streamlit_image_coordinates

    coords = streamlit_image_coordinates(img_rgb, key="color_picker")

    if coords is not None:
        x, y = coords["x"], coords["y"]
        b, g, r = img[y, x]
        color_name = get_color_name(r, g, b)

        st.markdown(f"**Detected Color:** {color_name}")
        st.write(f"RGB: ({r}, {g}, {b})")

        # Show detected color as a swatch
        st.image(np.zeros((100, 100, 3), dtype=np.uint8) + [b, g, r], caption=color_name)
