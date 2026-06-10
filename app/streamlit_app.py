import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="SpamShield AI",
    page_icon="📧",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.stApp{
    background:#050816;
    color:white;
}

[data-testid="stSidebar"]{
    background:#081020;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

.main-title{
    font-size:42px;
    font-weight:800;
    color:white;
}

.sub-title{
    color:#94A3B8;
    font-size:18px;
}

.metric-card{
    background:#0f172a;
    padding:25px;
    border-radius:18px;
    border:1px solid #1e293b;
    text-align:center;
}

.metric-number{
    font-size:34px;
    font-weight:bold;
    color:#38bdf8;
}

.card{
    background:#0f172a;
    padding:20px;
    border-radius:18px;
    border:1px solid #1e293b;
}

.result-safe{
    background:#064e3b;
    padding:25px;
    border-radius:15px;
    text-align:center;
}

.result-spam{
    background:#7f1d1d;
    padding:25px;
    border-radius:15px;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("# 📧 SpamShield AI")
    st.caption("Intelligent Email Security Platform")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Email Scanner",
            "Analytics",
            "Dataset",
            "About"
        ]
    )

# =====================================================
# DASHBOARD
# =====================================================

if page == "Dashboard":

    st.markdown("""
    <div class='main-title'>
    SpamShield AI Dashboard
    </div>
    <p class='sub-title'>
    Real-Time Email Threat Detection Platform
    </p>
    """, unsafe_allow_html=True)

    st.write("")

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class='metric-card'>
        <div class='metric-number'>98.4%</div>
        Accuracy
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='metric-card'>
        <div class='metric-number'>97.8%</div>
        Precision
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class='metric-card'>
        <div class='metric-number'>98.1%</div>
        Recall
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class='metric-card'>
        <div class='metric-number'>97.9%</div>
        F1 Score
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    left,right = st.columns([2,1])

    with left:

        hourly = pd.DataFrame({
            "Hour":["9AM","10AM","11AM","12PM","1PM","2PM","3PM"],
            "Emails":[12,18,25,22,30,28,35]
        })

        fig = px.line(
            hourly,
            x="Hour",
            y="Emails",
            title="Email Assessment Volume"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        spam_df = pd.DataFrame({
            "Type":["Ham","Spam"],
            "Count":[4825,747]
        })

        fig2 = px.pie(
            spam_df,
            names="Type",
            values="Count",
            hole=0.65,
            title="Spam Distribution"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

# =====================================================
# EMAIL SCANNER
# =====================================================

elif page == "Email Scanner":

    st.title("📨 Email Scanner")

    st.write(
        "Paste an email and classify it using the deployed ML model."
    )

    message = st.text_area(
        "Email Content",
        height=250
    )

    st.caption(
        f"Characters: {len(message)}"
    )

    API_URL = "http://127.0.0.1:8000/predict"

    if st.button(
        "🚀 Predict",
        use_container_width=True
    ):

        if not message.strip():

            st.warning(
                "Please enter email text."
            )

        else:

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "email_text": message
                    },
                    timeout=10
                )

                if response.status_code == 200:

                    data = response.json()

                    prediction = data.get(
                        "prediction",
                        ""
                    )

                    if prediction.lower() == "spam":

                        st.markdown("""
                        <div class='result-spam'>
                        <h2>🚨 SPAM DETECTED</h2>
                        <h4>Prediction : SPAM</h4>
                        <p>
                        Potential phishing or promotional content identified.
                        </p>
                        </div>
                        """,
                        unsafe_allow_html=True)

                    else:

                        st.markdown("""
                        <div class='result-safe'>
                        <h2>✅ SAFE EMAIL</h2>
                        <h4>Prediction : HAM</h4>
                        <p>
                        Email appears legitimate and safe.
                        </p>
                        </div>
                        """,
                        unsafe_allow_html=True)

                else:

                    st.error(
                        f"Backend Error {response.status_code}"
                    )

            except Exception as e:

                st.error(
                    "FastAPI backend is not running."
                )

                st.code(str(e))

# =====================================================
# ANALYTICS
# =====================================================

elif page == "Analytics":

    st.title("📊 Model Analytics")

    model_df = pd.DataFrame({

        "Algorithm":[
            "Naive Bayes",
            "Logistic Regression",
            "Random Forest",
            "SVM"
        ],

        "Accuracy":[
            97.2,
            98.1,
            96.8,
            98.4
        ]
    })

    st.dataframe(
        model_df,
        use_container_width=True
    )

    fig = px.bar(
        model_df,
        x="Algorithm",
        y="Accuracy",
        title="Algorithm Comparison"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# DATASET
# =====================================================

elif page == "Dataset":

    st.title("📂 Dataset Insights")

    d1,d2,d3,d4 = st.columns(4)

    d1.metric(
        "Total Emails",
        "5572"
    )

    d2.metric(
        "Spam",
        "747"
    )

    d3.metric(
        "Ham",
        "4825"
    )

    d4.metric(
        "Features",
        "7000+"
    )

    st.info("""
    Dataset → Text Cleaning → TF-IDF →
    Feature Engineering → Model Training →
    Prediction
    """)

# =====================================================
# ABOUT
# =====================================================

elif page == "About":

    st.title("🚀 About Project")

    st.success("""
    SpamShield AI is an NLP-powered
    email classification platform.

    Features:
    ✔ Text Preprocessing

    ✔ TF-IDF Vectorization

    ✔ Naive Bayes

    ✔ Logistic Regression

    ✔ SVM

    ✔ FastAPI Backend

    ✔ Streamlit Frontend

    ✔ Real-Time Prediction

    ✔ 98%+ Accuracy
    """)

    st.markdown("""
    ### Tech Stack

    Python • NLP • Scikit-Learn • TF-IDF

    FastAPI • Streamlit • Plotly

    ### Workflow

    EDA → Data Cleaning → Vectorization →
    Training → Evaluation → Deployment
    """)
