import streamlit as st
from PIL import Image

st.set_page_config(page_title="Smart Crop AI", page_icon="🌱")

CROPS = {
    "Tomato": ["Healthy", "Early Blight", "Late Blight", "Leaf Mold"],
    "Potato": ["Healthy", "Early Blight", "Late Blight"],
    "Pepper": ["Healthy", "Bacterial Spot"],
    "Rice": ["Healthy", "Leaf Blast", "Brown Spot"],
}

st.title("🌱 Smart Crop AI")
st.caption("AI-based crop disease detection with soil, weather, and recommendations")

page = st.sidebar.radio("Menu", [
    "Dashboard", "Disease Detection", "Soil Monitoring",
    "Weather", "Recommendations"
])

if "soil" not in st.session_state:
    st.session_state.soil = {"moisture": 50.0, "ph": 6.5, "n": 50.0, "p": 30.0, "k": 40.0}

if page == "Dashboard":
    st.subheader("Welcome to Smart Crop AI")
    st.write("A web-based prototype for crop leaf image analysis and basic crop monitoring.")
    st.info("Once hosted, this page can be opened from Android, iPhone, tablet, or computer using a normal web browser.")
    st.markdown("### Features")
    st.write("🌿 Crop selection  •  📷 Leaf upload  •  🤖 AI detection  •  🧪 Soil  •  🌦️ Weather  •  💡 Recommendations")

elif page == "Disease Detection":
    st.subheader("🌿 Disease Detection")
    crop = st.selectbox("Select crop", list(CROPS))
    photo = st.file_uploader("Upload or take a leaf photo", type=["jpg", "jpeg", "png"])
    if photo:
        image = Image.open(photo).convert("RGB")
        st.image(image, caption="Selected leaf", use_container_width=True)
        if st.button("🔍 Analyze Leaf", use_container_width=True):
            st.warning("Demo mode: connect your trained model before using predictions as research results.")
            st.success("Leaf image received successfully.")
            st.write("Crop:", crop)
            st.write("Classes prepared for this crop:", ", ".join(CROPS[crop]))

elif page == "Soil Monitoring":
    st.subheader("🧪 Soil Monitoring")
    s = st.session_state.soil
    s["moisture"] = st.number_input("Soil moisture (%)", 0.0, 100.0, s["moisture"])
    s["ph"] = st.number_input("Soil pH", 0.0, 14.0, s["ph"])
    s["n"] = st.number_input("Nitrogen (N)", 0.0, 500.0, s["n"])
    s["p"] = st.number_input("Phosphorus (P)", 0.0, 500.0, s["p"])
    s["k"] = st.number_input("Potassium (K)", 0.0, 500.0, s["k"])
    st.success("Soil information saved for this session.")

elif page == "Weather":
    st.subheader("🌦️ Weather Monitoring")
    st.info("These are sample values in the current prototype. A live weather API can be connected for deployment.")
    a, b, c = st.columns(3)
    a.metric("Temperature", "30 °C")
    b.metric("Humidity", "75 %")
    c.metric("Rainfall", "5 mm")

elif page == "Recommendations":
    st.subheader("💡 Recommendations")
    s = st.session_state.soil
    if s["moisture"] < 30:
        st.warning("Soil moisture is low. Check the crop's water needs.")
    elif s["moisture"] > 80:
        st.warning("Soil moisture is high. Check drainage.")
    else:
        st.success("Soil moisture is within the sample monitoring range.")
    if s["ph"] < 5.5:
        st.info("The entered soil pH is acidic. Check the crop's recommended pH range.")
    elif s["ph"] > 7.5:
        st.info("The entered soil pH is alkaline. Check the crop's recommended pH range.")
    else:
        st.success("The entered soil pH is within a general monitoring range.")
    st.write("• Regularly inspect leaves for visible changes.")
    st.write("• Keep records of soil conditions.")
    st.write("• Consider weather conditions when planning crop care.")
    st.caption("Recommendations are general and should not replace agricultural advice.")
