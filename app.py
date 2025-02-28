import streamlit as st
import cv2
import numpy as np
import torch
from ultralytics import YOLO
from transformers import DPTFeatureExtractor, DPTForDepthEstimation
from fastai.learner import load_learner
from fastai.vision.core import PILImage


# Load AI Models
yolo_model = YOLO("yolov8n.pt")  # Object Detection
depth_model = DPTForDepthEstimation.from_pretrained("Intel/dpt-large")  # Depth Estimation
style_model = load_learner("fastai_style_transfer.pkl")  # Style Transfer Model

st.title("🏠 AI Interior Design Assistant")
st.write("Answer some questions and receive your personalized design!")

# **Step 1: Collect User Information**
age = st.slider("📅 What's your age?", 18, 80, 30)
gender = st.selectbox("👤 What's your gender?", ["Male", "Female", "Other"])
space_type = st.selectbox("🏡 What space do you want to design?", ["Living Room", "Bedroom", "Kitchen", "Office"])

st.write("🎨 Choose your favorite styles:")
styles = ["Modern", "Minimalist", "Classic", "Industrial", "Bohemian", "Scandinavian"]
selected_styles = st.multiselect("✨ Select styles", styles)

special_request = st.text_area("✍️ Any special requests for your space?")

# **Step 2: Choose Image Upload or Take a Picture**
st.write("📸 Upload a photo OR take one now")

option = st.radio("How do you want to provide the image?", ["Upload a Photo", "Take a Picture"])

if option == "Upload a Photo":
    uploaded_file = st.file_uploader("📤 Upload a well-lit photo of your space", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        st.image(image_rgb, caption="Uploaded Room Image", use_column_width=True)

elif option == "Take a Picture":
    picture = st.camera_input("📸 Capture a photo using your webcam")

    if picture:
        file_bytes = np.asarray(bytearray(picture.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        st.image(image_rgb, caption="Captured Room Image", use_column_width=True)

    # **Step 3: AI Object Detection**
    st.write("🔍 Detecting existing furniture...")
    results = yolo_model(image_rgb)

    mask = np.zeros(image_rgb.shape[:2], dtype=np.uint8)
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            mask[y1:y2, x1:x2] = 255  # Mask furniture

    # **Step 4: AI-Based Furniture Removal**
    st.write("🛠️ Removing existing furniture...")
    image_cleaned = cv2.inpaint(image_rgb, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
    st.image(image_cleaned, caption="Furniture Removed", use_column_width=True)

    # **Step 6: Style Transfer**
    st.write("🎨 Applying your selected style...")
    content_image = PILImage.create(image_cleaned)
    style_image = PILImage.create(f"{selected_styles[0].lower()}_style.jpg") if selected_styles else None
    if style_image:
        styled_image = style_model.predict(content_image, style_image)
        st.image(styled_image, caption="Styled Room", use_column_width=True)

    # **Step 7: Generate Furniture Recommendations**
    st.write("🛋️ Generating furniture recommendations...")
    furniture_links = {
        "Modern": "https://www.ikea.com/us/en/cat/living-room-furniture-rooms/",
        "Minimalist": "https://www.muji.com/",
        "Classic": "https://www.wayfair.com/furniture/cat/classic-style",
        "Industrial": "https://www.homedepot.com/c/industrial_style_furniture",
        "Bohemian": "https://www.worldmarket.com/category/furniture/living-room.do",
        "Scandinavian": "https://www.nordicnest.com/furniture/"
    }

    for style in selected_styles:
        st.markdown(f"[🛒 Explore {style} furniture]({furniture_links[style]})")

    st.write("✅ Your design process is complete! You can now explore furniture suggestions and implement the AI-based changes.")

# **Final Step: Download Design Report**
if st.button("📄 Generate Design Report"):
    st.write("🔽 Your customized interior design recommendations will be generated soon!")

