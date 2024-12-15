import gradio as gr
from gradio import ChatMessage
import os
from PIL import Image, ImageDraw

#_____________________________________________________________________________________________________
import asyncio
from backend import chatbot_interaction
import nest_asyncio
nest_asyncio.apply()

#_____________________________________________________________________________________________________

async def respond(message, chat_history):
    if len(chat_history) == 0 or chat_history[-1]["role"] != "system":
        chat_history.append({"role": "system", "content": "You are a helpful webpage navigation assistant. Use the supplied tools to assist the user."})
    print(chat_history)
    # res = await  asyncio.run(chatbot_interaction(message, chat_history))
    res = await chatbot_interaction(message, chat_history)
    return "", res
        # chat_history.append({"role": "user", "content": message})
        # # chat_history.append({"role": "assistant", "content": bot_message})
        # chat_history.append({"role": "assistant", "content": "api eerrr", "metadata" : {"title": "💥 Screenshot"}, })
        # chat_history.append({"role": "assistant", "content": gr.Image(os.path.join("static", "1.png")), "metadata" : {"title": "💥 Screenshot"}, })
        # time.sleep(2)
        # return "", chat_history

import time
# Custom CSS for styling
custom_css = """

/* Change background color and text color for the Markdown title and description */
.markdown {
    # background-color: #333333; /* Dark background */
    color: white; /* White text */
    padding: 15px; /* Add padding around the text */
    border-radius: 10px; /* Rounded corners */
    text-align: center; /* Center align the text */
    margin-bottom: 10px; /* Space below the Markdown blocks */
}

/* Change background color */
.gradio-container {
    background-color: #ffffff;
}

/* Customize user chat bubble */
.message.user .message-content {
    background-color: white;
    color: white;
    border-radius: 10px;
}

/* Customize assistant chat bubble */
.message.assistant .message-content {
    background-color: #EFEFEF;
    color: #333;
    border-radius: 2px;
}

/* Customize tool response chat bubble */
.message.tool .message-content {
    background-color: #FFDCB9;
    color: #7A3E3E;
    border-radius: 10px;
}
.wrapper svelte-g3p8na {
    background-color: #66ff99;
    color: #7A3E3E;
    border-radius: 10px;
}
"""


with gr.Blocks(css=custom_css, theme="compact") as demo:  # You can use other themes like "ocean" or "default"
    gr.Markdown("# Gen AI-Driven Autonomous Web Interaction for Citizens")  # Title
    gr.Markdown("## NavigatorX")  # Title
    gr.Markdown("NavigatorX guides you through websites, offering navigation support and screenshots to help you reach your target.")  # Description
    
    chatbot = gr.Chatbot(type="messages", height=600, show_copy_button=True, avatar_images=(None, "https://em-content.zobj.net/source/twitter/53/robot-face_1f916.png"))
    msg = gr.Textbox(label="Ask Here", placeholder="Type your query here . . . ")
    clear = gr.ClearButton([msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

# Launch the app
demo.launch(share=True)
