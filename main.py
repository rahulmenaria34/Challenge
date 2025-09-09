import streamlit as st
import time
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage

# --- Set up the Streamlit Page ---
st.set_page_config(
    page_title="PAR Reduction Training Module",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Initialize LangChain Model ---
# Ensure you have the Ollama server running and the specified model pulled.
# To pull a model, use the command: ollama pull llama3
llm = ChatOllama(model="llama3")

# --- Few-Shot Prompting Examples ---
# These examples teach the model the desired conversational style and output format.
few_shot_examples = [
    HumanMessage(content="I think my team is a little burnt out with the constant collections push."),
    AIMessage(content="You're right, that's a valid concern. How can we make the task feel more manageable and less like a burden? Feedback: Good Coaching. You've validated their feelings and opened a collaborative discussion."),
    HumanMessage(content="Just tell me what to do to make the customer pay."),
    AIMessage(content="While that's a direct approach, it might not lead to a lasting solution. Let's focus on strategies that address the customer's situation, not just the debt. Feedback: Needs Improvement. This response is too direct and doesn't address the CSR's underlying issue."),
    HumanMessage(content="You just need to be tougher with customers. It's your job."),
    AIMessage(content="I hear your frustration, but aggressive tactics often backfire. Let's focus on empathy and problem-solving, which builds trust and improves long-term outcomes. Feedback: Poor Coaching. This response is critical and does not offer a solution or encourage a positive behavior change."),
]

# --- LangChain Prompt Template ---
system_prompt = "You are an AI simulating a professional CSR named Alex. Your goal is to respond to your manager's coaching and provide real-time feedback on their responses. The feedback should be a single sentence that explains why the response was 'Good Coaching', 'Poor Coaching', or 'Needs Improvement'."
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{user_input}")
])

# --- Initialize Session State ---
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = [
        AIMessage(content="Hey, thanks for meeting with me. I'm a little worried about our collections. It's tough because a lot of customers get upset and it feels like I'm just bothering them.")
    ]
if 'simulation_started' not in st.session_state:
    st.session_state.simulation_started = False
if 'show_action_plan' not in st.session_state:
    st.session_state.show_action_plan = False

# --- Streamlit UI and Logic ---
st.title("PAR Reduction Training Module")

if st.session_state.simulation_started:
    if st.session_state.show_action_plan:
        st.header("Your Action Plan")
        with st.spinner("Generating action plan..."):
            # A more robust prompt for the action plan
            action_plan_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a professional HR coach. Based on the following conversation transcript, generate a concise, simple action plan for the branch manager. The plan should be a bulleted list of 3-5 concrete, actionable steps."),
                *st.session_state.conversation_history
            ])
            action_plan = llm.invoke(action_plan_prompt.format_messages())
            st.markdown(action_plan.content)
        if st.button("Start Over"):
            st.session_state.clear()
            st.rerun()
    else:
        st.header('Coaching Simulation: "Alex"')
        # Display chat history
        for message in st.session_state.conversation_history:
            if message.type == "human":
                with st.chat_message("user"):
                    st.markdown(message.content)
            elif message.type == "ai":
                parts = message.content.split('Feedback:', 1)
                alex_response = parts[0].strip()
                feedback = parts[1].strip() if len(parts) > 1 else None
                with st.chat_message("assistant"):
                    st.markdown(alex_response)
                    if feedback:
                        if "Good Coaching" in feedback:
                            st.success(f"Feedback: {feedback}")
                        elif "Poor Coaching" in feedback:
                            st.error(f"Feedback: {feedback}")
                        else:
                            st.info(f"Feedback: {feedback}")

        # Handle user input
        user_input = st.chat_input("Type your coaching response...")
        if user_input:
            st.session_state.conversation_history.append(HumanMessage(content=user_input))
            
            # Construct the full message list with few-shot examples and conversation history
            messages_for_llm = few_shot_examples + st.session_state.conversation_history
            
            with st.spinner("Thinking..."):
                response = llm.invoke(messages_for_llm)

            st.session_state.conversation_history.append(AIMessage(content=response.content))
            
            # Check for conversation end
            if "great, thanks for the help." in response.content.lower() or len(st.session_state.conversation_history) >= 8: # Limit to 4 manager turns
                st.session_state.show_action_plan = True
            
            st.rerun()

else:
    # Initial introductory screen
    st.markdown("""
        <h1 style='text-align: center; font-size: 2.25rem; font-weight: 700; color: #1f2937;'>PAR Reduction Training Module</h1>
        <p style='text-align: center; color: #4b5563;'>Welcome, Branch Manager! This module will help you understand PAR90 and practice coaching your CSRs.</p>
        <div style='background-color: #f3f4f6; border-radius: 0.5rem; padding: 1rem; margin-top: 1.5rem;'>
            <h2 style='font-size: 1.25rem; font-weight: 600; color: #374151;'>What is PAR90 and Why Does It Matter?</h2>
            <p style='margin-top: 0.5rem; color: #4b5563;'>
                <span style='font-weight: 700;'>PAR90</span> stands for "Portfolio at Risk 90 days." It measures the percentage of your loan portfolio that is 1-90 days past due. It's a key metric for financial health.
            </p>
            <p style='margin-top: 0.5rem; color: #4b5563;'>
                <span style='font-weight: 700;'>Why it matters:</span> A low PAR90 indicates strong loan performance, which directly impacts your branch's profitability and reputation. High PAR90 suggests CSRs may need better coaching on collection techniques.
            </p>
            <p style='margin-top: 0.5rem; color: #4b5563;'>
                <span style='font-weight: 700;'>The connection to performance:</span> Improving PAR90 requires coaching CSRs on daily behaviors like making timely, empathetic, and effective collection calls. A CSR who masters these skills contributes directly to your branch's success.
            </p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Start Coaching Simulation", use_container_width=True):
        st.session_state.simulation_started = True
        st.rerun()
