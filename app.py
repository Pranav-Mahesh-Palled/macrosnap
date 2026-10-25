import streamlit as st
import smtplib
from email.mime.text import MIMEText
from google import genai
from google.genai import types
 
from prompts import (
    SYSTEM_PROMPT,
    WELCOME_MESSAGE_TEMPLATE,
    SUMMARY_REQUEST_PROMPT,
)
 
MODEL_NAME = "gemini-3.5-flash"
st.set_page_config(page_title="MacroSnap", page_icon="🥗")
 
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GMAIL_ADDRESS = st.secrets["GMAIL_ADDRESS"]
GMAIL_APP_PASSWORD = st.secrets["GMAIL_APP_PASSWORD"]
 
 
@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)
 
 
gemini_client = get_gemini_client()
 
 
def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"])
 
 
def add_message(role, kind, content):
    st.session_state.messages.append({"role": role, "kind": kind, "content": content})
    render_message(st.session_state.messages[-1])
 
 
def ask_gemini(parts):
    try:
        response = st.session_state.chat.send_message(parts)

        if not response.text:
            st.warning(
                "Gemini returned an empty response. Please try again."
            )
            return None

        return response.text

    except Exception as error:
        # Print the underlying error to the application logs.
        print(
            f"Gemini API error: "
            f"{type(error).__name__}: {error}"
        )

        # Show a friendly message to the user.
        st.error(
            "Gemini couldn't process your request. "
            "Please check the application logs for details."
        )

        return None
 
 
def send_email(to_address, subject, body):
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = GMAIL_ADDRESS
    message["To"] = to_address
 
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.send_message(message)


# Step 1: onboarding
if "onboarded" not in st.session_state:
    st.title("🥗 MacroSnap")
    st.caption("Snap it. Track it. Understand your nutrition.")

    with st.form("onboarding_form"):
        name = st.text_input("Your name")
        email = st.text_input(
            "Your Gmail address",
            placeholder="you@gmail.com",
            help="Your nutrition summaries will be sent to this email address.",
        )

        submitted = st.form_submit_button("Let's go 🚀")

    if submitted:
        if not name.strip() or not email.strip():
            st.warning("Please enter both your name and email address.")
        elif "@" not in email or "." not in email.split("@")[-1]:
            st.warning("Please enter a valid email address.")
        else:
            st.session_state.name = name.strip()
            st.session_state.email = email.strip()

            st.session_state.chat = gemini_client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                ),
            )

            st.session_state.messages = []
            st.session_state.onboarded = True
            st.rerun()

    st.stop()


# Step 2: Main MacroSnap interface

st.title("🥗 MacroSnap")

st.caption(
    f"Logged in as {st.session_state.name} "
    f"({st.session_state.email})"
)


# Detect when the user wants to finish the conversation
def is_done_message(text):
    text = " ".join(
        (text or "").lower().replace("’", "'").split()
    )

    completion_phrases = (
        "i'm done",
        "im done",
        "i am done",
        "done for now",
        "done with the chat",
        "i'm finished",
        "im finished",
        "i am finished",
        "that's all",
        "thats all",
        "finish the chat",
        "generate my summary",
        "show my nutrition summary",
    )

    return any(phrase in text for phrase in completion_phrases)


# Initialise summary state
if "nutrition_summary" not in st.session_state:
    st.session_state.nutrition_summary = None


# Display the existing conversation
if not st.session_state.messages:
    add_message(
        "assistant",
        "text",
        WELCOME_MESSAGE_TEMPLATE.format(
            name=st.session_state.name
        ),
    )
else:
    for message in st.session_state.messages:
        render_message(message)


# Chat input
user_input = st.chat_input(
    "Ask a question, or attach a photo of your meal",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)


# Process user input
if user_input:

    photo = user_input.files[0] if user_input.files else None
    text = (user_input.text or "").strip()

    # Check whether this is the user's completion message
    done_requested = (
        photo is None and is_done_message(text)
    )

    # A new message invalidates the previously generated summary
    st.session_state.nutrition_summary = None

    # Check whether the user has interacted with the chat before
    has_previous_messages = any(
        message["role"] == "user"
        for message in st.session_state.messages
    )

    if done_requested:

        add_message("user", "text", text)

        if not has_previous_messages:

            st.warning(
                "Please discuss a meal or upload a meal photo "
                "before requesting your nutrition summary."
            )

        else:

            summary_prompt = """
            The user has indicated that they have finished
            their nutrition-tracking conversation.

            Create a clear, well-organised nutrition summary
            using the meal information discussed in this chat.

            Include:
            1. Foods and meals discussed.
            2. Estimated calories for each meal, when available.
            3. Protein, carbohydrates, and fats, when available.
            4. Estimated total calories and macronutrients,
               when sufficient information is available.

            Important:
            - Do not invent missing nutritional values.
            - Clearly label estimates as approximate.
            - Mention uncertainty about portion sizes,
              ingredients, or preparation methods.
            - If insufficient meal information is available,
              explain what information is missing.

            Make the result easy to read in an email.
            """

            with st.spinner(
                "🥗 Preparing your nutrition summary..."
            ):

                summary = ask_gemini([summary_prompt])

            if summary:

                st.session_state.nutrition_summary = summary

                st.success(
                    "Your nutrition summary is ready below! 🎉"
                )


    else:

        parts = []

        # Add the uploaded image
        if photo is not None:

            photo_bytes = photo.getvalue()

            add_message(
                "user",
                "image",
                photo_bytes
            )

            parts.append(
                types.Part.from_bytes(
                    data=photo_bytes,
                    mime_type=photo.type,
                )
            )

        # Add the user's text
        if text:

            add_message(
                "user",
                "text",
                text
            )

            parts.append(text)

        elif photo is not None:

            parts.append(
                "Analyse this meal and estimate its calories, "
                "protein, carbohydrates, and fats. Explain "
                "any uncertainty in the estimates."
            )

        # Ask Gemini to analyse the input
        if parts:

            with st.spinner("🥗 Analysing your meal..."):

                answer = ask_gemini(parts)

            if answer:

                add_message(
                    "assistant",
                    "text",
                    answer
                )


# Step 3: Display the nutrition summary only after completion

if st.session_state.nutrition_summary:

    st.divider()

    with st.container(border=True):

        st.subheader("🥗 Your Nutrition Summary")

        st.markdown(
            st.session_state.nutrition_summary
        )

        st.caption(
            "Nutrition values are estimates and may vary "
            "depending on ingredients and portion sizes."
        )

        st.divider()

        st.markdown(
            f"📧 **Send this summary to:** "
            f"{st.session_state.email}"
        )

        if st.button(
            "📧 Email My Nutrition Summary",
            key="email_nutrition_summary",
            use_container_width=True,
        ):

            try:

                with st.spinner("🥗 Preparing your nutrition summary..."):
                    summary = ask_gemini([SUMMARY_REQUEST_PROMPT])

                if summary:
                    st.session_state.nutrition_summary = summary

                    st.success(
                        "Your nutrition summary is ready below! 🎉"
                    )

            except Exception:

                st.error(
                    "Unable to send the email. Please check "
                    "your Gmail configuration and try again."
                )

