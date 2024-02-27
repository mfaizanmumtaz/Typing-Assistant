from pynput.keyboard import Controller,Key
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from pynput import keyboard
import pyperclip,time

controller = Controller()
model = GoogleGenerativeAI(model="gemini-pro",temperature=0)

def fix_text(text):
    prompt = ChatPromptTemplate.from_template("""Fix all typos and casing and punctuation in this text, but preserve all new line characters:
    Text: ```{text}
    Return only the corrected text, don't include a preamble.""")
    chain = prompt | model | StrOutputParser()
    try: 
        return chain.invoke({"text":text})
    except Exception as e:
        return str(f"Error {e}")

def fix_selection():
    with controller.pressed(Key.ctrl_l):
        controller.tap('c')

    time.sleep(0.1)
    text = pyperclip.paste()

    fixed_text = fix_text(text)
    pyperclip.copy(fixed_text)

    with controller.pressed(Key.ctrl_l):
        controller.tap('v')

def fix_current_line():
    controller.press(Key.ctrl)
    controller.press(Key.shift)
    controller.press(Key.left)

    controller.release(Key.ctrl_l)
    controller.release(Key.shift)
    controller.release(Key.left)

    fix_selection()

def on_press(key):
    if key == keyboard.Key.f9:
        fix_current_line()

    elif key == keyboard.Key.f10:
        fix_selection()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
