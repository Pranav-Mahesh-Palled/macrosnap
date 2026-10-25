# 🥗 MacroSnap

**Snap it. Track it. Understand your nutrition.**

MacroSnap is an AI-powered meal-analysis web app built with Streamlit and Google's Gemini API. Describe a meal or upload a photo to get an approximate breakdown of calories and macronutrients. When you're finished logging meals, type **“I'm done”** to generate a nutrition summary, then email it to your registered address.

<p align="left">
  <a href="https://macrosnap-pranav-palled.streamlit.app/"><strong>🚀 Try MacroSnap</strong></a> ·
  <a href="https://github.com/Pranav-Mahesh-Palled/macrosnap"><strong>💻 View source code</strong></a>
</p>

## ✨ Features

- **Meal photo analysis:** Upload a JPG, JPEG, or PNG image for a visual meal estimate.
- **Text-based meal analysis:** Describe food or ask nutrition-related questions in a conversational chat.
- **Calories and macros:** Receive approximate calories, protein, carbohydrates, and fat where the available information supports an estimate.
- **Conversation-based summary:** Type **“I'm done”** (or another configured completion phrase) to generate a summary of the meals discussed.
- **Email summary:** Send the generated summary to the email address entered during onboarding through Gmail SMTP.
- **Streamlit interface:** Use the app in a browser without installing a separate desktop application.

## 🧭 How to use it

1. Open the [MacroSnap web app](https://macrosnap-pranav-palled.streamlit.app/).
2. Enter your name and email address.
3. Describe a meal or upload a meal photo.
4. Continue chatting to analyse additional meals.
5. When finished, type **“I'm done”** to request a combined nutrition summary.
6. Review the summary displayed in the app and select the email button to send it to your registered address.

## 🛠️ Tech stack

- **Python** — application logic
- **Streamlit** — web interface and chat UI
- **Google Gemini API (`google-genai`)** — conversational, text-and-image meal analysis and summary generation
- **Gmail SMTP with Python `smtplib`** — email delivery

## 📁 Project structure

```text
macrosnap/
├── app.py                  # Streamlit app, Gemini integration, chat and email flow
├── prompts.py              # System, welcome, and nutrition-summary prompts
├── requirements.txt        # Python dependencies
├── .gitignore
├── LICENSE
```

## ⚙️ Run locally

### 1. Clone the repository

```bash
git clone https://github.com/Pranav-Mahesh-Palled/macrosnap.git
cd macrosnap
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The app needs `streamlit` and `google-genai`. Email sending uses Python's standard-library modules. Since MacroSnap no longer uses WhatsApp or Twilio, remove `twilio` from `requirements.txt` if it is still listed.

### 4. Configure secrets

Create `.streamlit/secrets.toml` in the project root:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
GMAIL_ADDRESS = "your_gmail_address@gmail.com"
GMAIL_APP_PASSWORD = "your_16_character_app_password"
```

Replace the example values with your own credentials. Do not include real credentials in this README or commit them to Git.

- Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).
- For Gmail SMTP, use a Google App Password if your Google account is eligible. Google requires 2-Step Verification for App Passwords. Read [Google's App Password help page](https://support.google.com/accounts/answer/185833).
- Ensure `.streamlit/secrets.toml` and any `.env` files are listed in `.gitignore`.

### 5. Start the app

```bash
streamlit run app.py
```

Streamlit will print a local URL in the terminal, usually `http://localhost:8501`.

## ☁️ Deployment on Streamlit Community Cloud

MacroSnap is deployed here:

**[https://macrosnap-pranav-palled.streamlit.app/](https://macrosnap-pranav-palled.streamlit.app/)**

When deploying or updating the app, add the same three values (`GEMINI_API_KEY`, `GMAIL_ADDRESS`, and `GMAIL_APP_PASSWORD`) in the app's **Settings → Secrets** section. Do not upload `secrets.toml` to GitHub. See the [Streamlit secrets-management documentation](https://docs.streamlit.io/develop/concepts/connections/secrets-management).

## 🔐 Security and privacy

- Never commit API keys, Gmail App Passwords, or other credentials to source control.
- The Gmail account configured by the app is the sender; the email address entered by the user is the recipient.
- Do not use the app to submit confidential or highly sensitive information.
- Only send nutrition summaries to an address you control or have permission to use.

## ⚠️ Nutrition disclaimer

MacroSnap provides **estimates**, not medically verified nutrition data. Photo-based estimates can be affected by portion sizes, hidden ingredients, cooking methods, and image quality. Do not use the app as a substitute for professional medical or dietary advice.

## 📄 License

This project includes an MIT license. See [`LICENSE`](LICENSE) for details.

## 👨‍💻 Author

**Pranav Mahesh Palled**

- GitHub: [@Pranav-Mahesh-Palled](https://github.com/Pranav-Mahesh-Palled)
- Project repository: [macrosnap](https://github.com/Pranav-Mahesh-Palled/macrosnap)
- Live app: [MacroSnap on Streamlit](https://macrosnap-pranav-palled.streamlit.app/)
