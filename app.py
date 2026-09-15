import streamlit as st
import numpy as np
import cv2
import joblib
from PIL import Image
from pathlib import Path

st.set_page_config(
    page_title="Smart Crop AI",
    page_icon="🌱",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
MODEL_DIR = BASE_DIR / "models"

CROPS = ["Tomato", "Potato", "Pepper", "Rice"]

st.title("🌱 Smart Crop AI")
st.write("AI-Based Crop Disease Detection with Soil and Weather Monitoring")

st.sidebar.title("Smart Crop AI")
page = st.sidebar.selectbox(
    "Choose a feature",
    [
        "Disease Detection",
        "Soil Monitoring",
        "Weather Information",
        "Recommendations",
        "Model Status"
    ]
)


def extract_features(image):
    """Convert a crop-leaf image into the same basic image features
    used by the trained models."""
    
    image = image.convert("RGB")
    img = np.array(image)

    img = cv2.resize(
        img,
        (32, 32),
        interpolation=cv2.INTER_AREA
    )

    img = img.astype(np.float32) / 255.0

    small = cv2.resize(img, (16, 16)).ravel()

    histograms = []

    for channel in range(3):
        hist = np.histogram(
            img[:, :, channel],
            bins=12,
            range=(0, 1),
            density=True
        )[0]
        histograms.append(hist)

    hist = np.concatenate(histograms)

    mean = img.mean(axis=(0, 1))
    std = img.std(axis=(0, 1))

    features = np.concatenate([
        small,
        hist,
        mean,
        std
    ])

    return features.astype(np.float32).reshape(1, -1)


def load_model(crop):
    model_file = MODEL_DIR / f"{crop.lower()}.joblib"

    if not model_file.exists():
        return None, f"Model file not found: {model_file.name}"

    try:
        model = joblib.load(model_file)
        return model, None
    except Exception as e:
        return None, str(e)


# ---------------------------------------------------------
# DISEASE DETECTION
# ---------------------------------------------------------

if page == "Disease Detection":

    st.header("🔬 Crop Disease Detection")

    crop = st.selectbox(
        "Select Crop",
        CROPS
    )

    uploaded_file = st.file_uploader(
        "Upload a crop leaf image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file).convert("RGB")

        st.image(
            image,
            caption="Uploaded Crop Leaf",
            width=350
        )

        if st.button("🔍 Analyze Leaf"):

            model, error = load_model(crop)

            if error:
                st.error(
                    f"Unable to load the {crop} model. "
                    f"{error}"
                )
            else:

                try:
                    features = extract_features(image)

                    prediction = model.predict(features)[0]

                    st.success("Analysis completed!")

                    st.subheader("Prediction")
                    st.write(f"**Crop:** {crop}")
                    st.write(f"**Condition:** {prediction}")

                    if hasattr(model, "predict_proba"):

                        probabilities = model.predict_proba(
                            features
                        )[0]

                        classes = model.classes_

                        results = sorted(
                            zip(classes, probabilities),
                            key=lambda x: x[1],
                            reverse=True
                        )

                        st.subheader("Prediction Confidence")

                        for label, probability in results[:3]:

                            st.write(
                                f"**{label}** — "
                                f"{probability * 100:.2f}%"
                            )

                except Exception as e:

                    st.error(
                        "The image could not be analyzed "
                        "with this model."
                    )

                    st.code(str(e))


# ---------------------------------------------------------
# SOIL MONITORING
# ---------------------------------------------------------

elif page == "Soil Monitoring":

    st.header("🌱 Soil Monitoring")

    crop = st.selectbox(
        "Select Crop",
        CROPS
    )

    moisture = st.number_input(
        "Soil Moisture",
        min_value=0.0,
        max_value=100.0,
        value=50.0
    )

    ph = st.number_input(
        "Soil pH",
        min_value=0.0,
        max_value=14.0,
        value=6.5
    )

    nitrogen = st.number_input(
        "Nitrogen (N)",
        min_value=0.0,
        value=0.0
    )

    phosphorus = st.number_input(
        "Phosphorus (P)",
        min_value=0.0,
        value=0.0
    )

    potassium = st.number_input(
        "Potassium (K)",
        min_value=0.0,
        value=0.0
    )

    if st.button("Save Soil Information"):

        st.success("Soil information recorded successfully.")

        st.write(f"**Crop:** {crop}")
        st.write(f"**Moisture:** {moisture}")
        st.write(f"**pH:** {ph}")
        st.write(f"**Nitrogen:** {nitrogen}")
        st.write(f"**Phosphorus:** {phosphorus}")
        st.write(f"**Potassium:** {potassium}")


# ---------------------------------------------------------
# WEATHER
# ---------------------------------------------------------

elif page == "Weather Information":

    st.header("🌦️ Weather Information")

    st.info(
        "The current prototype uses entered/sample weather "
        "information. It is not connected to a live weather API."
    )

    temperature = st.number_input(
        "Temperature (°C)",
        value=30.0
    )

    humidity = st.number_input(
        "Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=70.0
    )

    rainfall = st.number_input(
        "Rainfall (mm)",
        min_value=0.0,
        value=0.0
    )

    if st.button("Save Weather Information"):

        st.success("Weather information recorded.")

        st.write(f"**Temperature:** {temperature} °C")
        st.write(f"**Humidity:** {humidity} %")
        st.write(f"**Rainfall:** {rainfall} mm")


# ---------------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------------

elif page == "Recommendations":

    st.header("💡 Farming Recommendations")

    crop = st.selectbox(
        "Select Crop",
        CROPS
    )

    moisture = st.number_input(
        "Soil Moisture (%)",
        min_value=0.0,
        max_value=100.0,
        value=50.0
    )

    humidity = st.number_input(
        "Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=70.0
    )

    rainfall = st.number_input(
        "Rainfall (mm)",
        min_value=0.0,
        value=0.0
    )

    if st.button("Generate Recommendation"):

        recommendations = []

        if moisture < 30:
            recommendations.append(
                "Consider providing additional water if appropriate."
            )

        elif moisture > 80:
            recommendations.append(
                "Avoid excessive watering and check soil drainage."
            )

        else:
            recommendations.append(
                "Soil moisture is within the entered range."
            )

        if humidity > 80:
            recommendations.append(
                "High humidity may increase the risk of some plant diseases. Monitor the leaves regularly."
            )

        if rainfall > 20:
            recommendations.append(
                "Frequent rainfall can increase disease risk. Check the crop leaves regularly."
            )

        recommendations.append(
            f"Continue monitoring the {crop} crop and check for visible signs of disease."
        )

        st.subheader("Recommendation")

        for recommendation in recommendations:
            st.write("• " + recommendation)


# ---------------------------------------------------------
# MODEL STATUS
# ---------------------------------------------------------

elif page == "Model Status":

    st.header("🤖 AI Model Status")

    st.write(
        "The system checks whether the trained crop models "
        "are available in the models folder."
    )

    for crop in CROPS:

        model_file = MODEL_DIR / f"{crop.lower()}.joblib"

        if model_file.exists():
            st.success(
                f"✅ {crop} model found — {model_file.name}"
            )
        else:
            st.error(
                f"❌ {crop} model missing — {model_file.name}"
            )

    st.write("")

    st.info(
        "The disease detection feature uses trained machine-learning "
        "models. Predictions should be treated as research/prototype "
        "results and not as professional agricultural diagnosis."
    )