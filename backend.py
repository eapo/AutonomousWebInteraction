import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 
from openai import OpenAI
import json
#-----------------------------------------------------------
import asyncio
from pyppeteer import launch
import nest_asyncio
nest_asyncio.apply()

import pyppeteer
pyppeteer.DEBUG = True
#------------------------------------------------------------
from functionschema import functions
import gradio as gr
from gradio import ChatMessage
import os
from PIL import Image, ImageDraw
#------------------------------------------------------------


tools = [{"type": "function", "function": f} for f in functions]

#______________________________________________________________________________________________

async def monitor_browser(browser):
    try:
        # Monitor the browser and detect closure
        while True:
            if not browser.process or browser.process.poll() is not None:
                print("Browser closed. Exiting the script.")
                break
            await asyncio.sleep(1)  # Check every 1 second
    except asyncio.CancelledError:
        pass
    finally:
        # Ensure the browser is closed cleanly
        if browser.process and browser.process.poll() is None:
            await browser.close()
            print("Browser closed programmatically.")


async def main(url, conversation_history):
    # try:
    # Launch Chrome in non-headless mode with the specified executable path
    browser = await launch(
        {
            "headless": False,
            "handleSIGINT": False,  # Disable signal handling
            "handleSIGTERM": False,
        },
        executablePath='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    )
    pages = await browser.pages()
    print(pages)

    # Use the default page instead of creating a new one
    page = pages[0]


    # Set the viewport of the page
    await page.setViewport({"width": 1280, "height": 720})

    # Navigate to the desired website
    # await page.goto("https://www.unisys.com")
    await page.goto(url)
    print("Page Loaded ...")

    # Take a screenshot of the first page and store in the static folder
    await page.screenshot({"path": "./static/1.png"})
    print(f"screenshot 1 {pages[0].url} saved....")
    conversation_history.append({"role": "assistant", "content": pages[0].url, "metadata" : {"title": f"Screenshot of {pages[0].url}"}, })
    conversation_history.append({"role": "assistant", "content": gr.Image(os.path.join("static", "1.png")), "metadata" : {"title": "💥 Screenshot"}, })

    # wait 3s for page to load
    await page.waitFor(3000)

    download = await page.querySelectorAll("#main > div:nth-child(1) > section > div > div > header > div.short-title__button")
    print("download selector 1", download)
    await download[0].click()

    # wait 3s for page to load
    await page.waitFor(3000)


    await page.screenshot({"path": "./static/2.png"})
    print(f"screenshot 2 {pages[0].url} saved....")
    conversation_history.append({"role": "assistant", "content": pages[0].url, "metadata" : {"title": f"Screenshot of {pages[0].url}"}, })
    conversation_history.append({"role": "assistant", "content": gr.Image(os.path.join("static", "2.png")), "metadata" : {"title": "💥 Screenshot"}, })

    # wait 3s for page to load
    await page.waitFor(3000)

    await page.waitForSelector("#main > div:nth-child(1) > section > div > aside > header > div > a > div")
    download1 = await page.querySelectorAll("#main > div:nth-child(1) > section > div > aside > header > div > a > div")
    print("download selector 2", download1)
    await download1[0].click()

    # wait for page to load
    await page.waitFor(7000)

    
    # Take a screenshot of the second page
    # await page.screenshot({"path": "./static/3.png"})
    # print(f"screenshot 3 {page.url} saved")
    conversation_history.append({"role": "assistant", "content": pages[0].url, "metadata" : {"title": f"Screenshot of {pages[0].url}"}, })
    conversation_history.append({"role": "assistant", "content": gr.Image(os.path.join("static", "3.png")), "metadata" : {"title": "💥 Screenshot"}, })

    # wait for page to load
    await page.waitFor(7000)
    

    # Get the page HTML content
    htmlContent = 'The page opened & executed successfully'
    # htmlContent = await page.content()
    # print("HTML content fetched. The browser will remain open.")

    # Return the HTML content and browser object
    return htmlContent, browser, conversation_history

    # except Exception as e:
    #     return str(e), None

#_____________________________________________________________________________________________________

class XaiModel:
    def aiModel(self):
        XAI_API_KEY = os.getenv("XAI_API_KEY")
        client = OpenAI(
            api_key=XAI_API_KEY,
            base_url="https://api.x.ai/v1",
        )
        return client

        

async def chatbot_interaction(user_input: str, conversation_history: list):
    model = XaiModel()
    _auth = model.aiModel()
    MODEL_NAME = "grok-beta"
    

    # conversation_history = [
    #     {"role": "system", "content": "You are a helpful webpage navigation assistant. Use the supplied tools to assist the user."}
    # ]
    conversation_history.append({"role": "user", "content": user_input})
    # conversation_history.append({'role': 'user', 'metadata': {'title': None}, 'content': 'Ask me anything!', 'options': None})
    print("conversation_history FIRST", conversation_history)

    response = _auth.chat.completions.create(
        model=MODEL_NAME,
        messages=conversation_history,
        tools=tools,
    )
    print(response)
    print(response.choices[0].message)
    if(response.choices[0].message.tool_calls == None):
        print(response.choices[0].message.content)
        function_call_result = {
            "role": "assistant",
            "content": response.choices[0].message.content,
            # "tool_call_id": response.id
        }
        conversation_history.append(function_call_result)
        # conversation_history.append({'role': 'assistant', 'metadata': {'title': None}, 'content': , 'options': None})
        print("conversation_history, IF not function call",  conversation_history)
        return conversation_history
    else:
        tool_call = response.choices[0].message.tool_calls[0]
        print(tool_call)
        arguments = json.loads(tool_call.function.arguments)
        print(arguments)
        functionName =  tool_call.function.name
        print(functionName)
        function_call_result_message = {
                "role": "assistant",
                "content": response.choices[0].message.content,
                # "tool_call_id": response.choices[0].message.tool_calls[0].id
        }
        conversation_history.append(function_call_result_message)
        print("conversation_history, IF FUNCTION CALL HAPPENS", conversation_history)
        if(functionName == 'open_website'):
            url = arguments.get('url')
            print(url)
            try:
                response, browser, conversation_history = asyncio.run(main(url, conversation_history))
                function_call_result_open = {
                    "role": "assistant",
                    "content": response
                }
                print("Top of the function call", conversation_history)
                conversation_history.append(function_call_result_open)
                print("conversation_history, INSIDE FUNCTION CALL HAPPENS", conversation_history)
                print(response)
                monitoring_task = asyncio.get_event_loop().create_task(monitor_browser(browser))
                asyncio.get_event_loop().run_until_complete(monitoring_task)
                return conversation_history
            except KeyboardInterrupt:
                print("\nScript interrupted by user.")
                function_call_result = {
                    "role": "assistant",
                    "content": "Script interrupted by user.",
                }
                conversation_history.append(function_call_result)
                return conversation_history
            except Exception as e:
                print(f"An error occurred: {e}")
                function_call_result = {
                    "role": "assistant",
                    "content": f"An error occurred: {e}",
                }
                conversation_history.append(function_call_result)
                return conversation_history
    
    return conversation_history



            

# user_input = "Hi, can you go to the page of website https://unisys.com/?"
# user_input = "Hi, can click the button page of website ?"
# asyncio.run(chatbot_interaction(user_input))
# response, browser = asyncio.run(main('https://unisys.com'))