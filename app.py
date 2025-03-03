import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image

# GitHub repository URL for images
GITHUB_REPO_URL = "https://raw.githubusercontent.com/slunara/InteriorDesignAI/main/images/"

# Define the logo image URL
logo_url = f"{GITHUB_REPO_URL}logo.jpeg"

# Display the logo in the top right corner
col1, col2 = st.columns([3, 1])
with col2:
    st.image(logo_url, width=350)

# **Updated Title and Description**
st.title("DecorAIte")
st.write("Answer a few questions to receive a personalized furniture recommendation!")

st.markdown("<hr style='border: 2px solid #bbb;'>", unsafe_allow_html=True)

# **Step 4: Upload or Capture a Room Image**
st.subheader("📸 Upload or Take a Picture of Your Space")

option = st.radio("How would you like to provide the image?", ["Upload a Photo", "Take a Picture"])
image_rgb = None
show_furniture = False  # Flag to control when to show furniture images

if option == "Upload a Photo":
    uploaded_file = st.file_uploader("📤 Upload a well-lit photo of your space", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Display uploaded image
        st.image(image_rgb, caption="Uploaded Room Image", use_container_width=True)
        
        # **"Find My Dream Furniture" Button**
        if st.button("🔍 Find My Dream Furniture"):
            show_furniture = True

elif option == "Take a Picture":
    picture = st.camera_input("📸 Capture a photo using your webcam")
    if picture:
        file_bytes = np.asarray(bytearray(picture.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Display captured image
        st.image(image_rgb, caption="Captured Room Image", use_container_width=True)

        # **"Find My Dream Furniture" Button**
        if st.button("🔍 Find My Dream Furniture"):
            show_furniture = True

# **Show Furniture Images Only After Clicking "Find My Dream Furniture"**
if show_furniture:
    st.subheader("🛋️ Recommended Furniture for Your Space")

    furniture_images = {
        "Chair": f"{GITHUB_REPO_URL}chair.jpeg",
        "Sofa": f"{GITHUB_REPO_URL}sofa.jpeg",
        "Coffee Table": f"{GITHUB_REPO_URL}coffee_table.jpeg",
        "Painting": f"{GITHUB_REPO_URL}painting.jpeg",
    }

    col1, col2, col3, col4 = st.columns(4)  # 4 columns for 4 furniture items

    for idx, (label, img_url) in enumerate(furniture_images.items()):
        with [col1, col2, col3, col4][idx]:  # Arrange in 4 columns
            st.image(img_url, caption=label, use_container_width=True)
            if st.button(f"Replace {label}", key=f"replace_{idx}"):
                st.write(f"🔄 You selected to replace **{label}**.")

st.markdown("<hr style='border: 2px solid #bbb;'>", unsafe_allow_html=True)

# **Generate the Dream Space**
if st.button("✨ Generate Your Dream Space"):
    st.subheader("🏡 Your Dream Space Design")
    
    # Display output image from GitHub
    output_image_url = f"{GITHUB_REPO_URL}output.png"
    st.image(output_image_url, caption="Your AI-Generated Design", use_container_width=True)

    # Display 3 options in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🛍️ Shop it Directly")
        st.write("Find and purchase the exact items in one click.")
        st.button("🛒 Shop Now", key="shop_now")
    
    with col2:
        st.subheader("🏬 Buy from Retailer")
        st.write("Browse similar items from recommended retailers.")
        st.button("🛍️ Browse Retailers", key="browse_retailers")
    
    with col3:
        st.subheader("📞 Contact a Designer")
        st.write("Need help bringing this vision to life? Contact a professional designer.")
        st.button("📩 Get in Touch", key="contact_designer")
