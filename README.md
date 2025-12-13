# 🛒 SHOPVISION  
## Smart Grocery Recognition System

**ShopVision** is an AI-powered smart billing system that automatically identifies loose fruits and vegetables using an uploaded image or live camera feed and generates accurate billing with confidence scores.

---

# 🚀 FEATURES
- 📷 **Image upload & webcam-based recognition**
- 🥕 **76 fruit & vegetable categories**
- 📊 **Confidence probability for each prediction**
- 💰 **Automatic price mapping & billing**
- ✍️ **Manual fallback option for low-confidence predictions**
- 📈 **Model explainability using confusion matrix & dataset gallery**

---

# 🧠 MODEL OVERVIEW
- **Architecture:** EfficientNet-based Convolutional Neural Network (CNN)
- **Dataset:** Fruits-360 (cleaned & auto-grouped)
- **Input Size:** 224 × 224 RGB images
- **Validation Accuracy:** ~97%

> ⚠️ The trained model file is not included in this repository due to GitHub file size limits.

---

# 📓 MODEL TRAINING & EXPERIMENTATION

The complete model training pipeline, preprocessing steps, evaluation, and visualizations are documented in the Google Colab notebook below:

👉 **Google Colab Notebook**  
🔗 [https://colab.research.google.com/drive/1nbT1zrrTklEHX3MZZ0Dma-MneO_C_95x?usp=sharing](https://colab.research.google.com/drive/1nbT1zrrTklEHX3MZZ0Dma-MneO_C_95x?usp=sharing)

### This notebook includes:
- Dataset exploration, augmentation and preparation
- Class auto-grouping strategy
- Model architecture design
- Training & validation process
- Confusion matrix visualization
- Sample image gallery

---

# 🛠️ BACKEND SETUP (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
