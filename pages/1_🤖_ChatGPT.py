import os
import time

import openai
import pandas as pd
import streamlit as st

import bard_api as google
import bard_api_1 as config_bard
import demo4 as demo
import doctep as apikey1
import doctepdavinci as doctep
import gpt2_NLPHUST as gpt2hgf
import layDSModel_FineTune_davinci as dsdavinci
import layDSModel_FineTune_OpenAiAPI as dsfinetune
import LLam as llam
import LLam_vie as llamvi
import openAI_API_using_APIkey as openai_key
import openAI_API_using_Breaber_Token as openai_token
import openAI_API_usingAPI_text_davinci_003 as openai_text
import rapidapi1
import rapidapi2
import rapidapi3
import rapidapi_kethop2
import ViT5 as viT5
from utils import (load_prompt_templates, load_prompts, render_footer,
                   render_github_info)

st.session_state.sync_flag1 = ''
st.session_state.sync_flag2 = ''
st.session_state.sync_flag3 = ''
icon_path = r"https://raw.githubusercontent.com/ohhhchank3/hello/main/t%E1%BA%A3i%20xu%E1%BB%91ng.ico"
st.set_page_config(page_title="ChatBot Web", page_icon=icon_path)
import os

# Gộp lại hai điều kiện thành một dòng
os.environ["keyOpenAI_dvc"], os.environ["originalID"] = doctep.main() if "keyOpenAI_dvc" not in os.environ or "originalID" not in os.environ else (os.environ.get("keyOpenAI_dvc", ""), os.environ.get("originalID", ""))
if "keyOpenAI" not in os.environ:
    os.environ["keyOpenAI"] = apikey1.main()
keyOpenAIdvc = ""
originalID = ""
keyOpenAIdvc = os.environ["keyOpenAI_dvc"]
originalID = os.environ["originalID"]
keyOpenAI = ""
keyOpenAI = "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"
flag1 = None
flag2 = None
flag3 = None

@st.cache_resource
def init_openai_settings():
    openai.api_key = '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'
    if st.secrets.get("OPENAI_PROXY"):
        openai.proxy = st.secrets["OPENAI_PROXY"]

def init_session():
    if not st.session_state.get("params"):
        st.session_state["params"] = dict()
    if not st.session_state.get("chats"):
        st.session_state["chats"] = {}
    if "input" not in st.session_state:
        st.session_state["input"] = "Hello, how are you!"

def new_chat(chat_name):
    if not st.session_state["chats"].get(chat_name):
        st.session_state["chats"][chat_name] = {
            "answer": [],
            "question": [],
            "messages": [
                {"role": "system", "content": st.session_state["params"]["prompt"]}
            ],
            "is_delete": False,
            "display_name": chat_name,
        }
    return chat_name

def switch_chat(chat_name):
    if st.session_state.get("current_chat") != chat_name:
        st.session_state["current_chat"] = chat_name
        render_chat(chat_name)
        st.stop()

def switch_chat_name(chat_name):
    if st.session_state.get("current_chat") != chat_name:
        st.session_state["current_chat"] = chat_name
        render_sidebar()
        render_chat(chat_name)
        st.stop()

def delete_chat(chat_name):
    if chat_name in st.session_state['chats']:
        st.session_state['chats'][chat_name]['is_delete'] = True
    current_chats = [chat for chat, value in st.session_state['chats'].items() if not value['is_delete']]
    if len(current_chats) == 0:
        switch_chat(new_chat(f"Chat{len(st.session_state['chats'])}"))
        st.stop()
    if st.session_state["current_chat"] == chat_name:
        del st.session_state["current_chat"]
        switch_chat_name(current_chats[0])

def edit_chat(chat_name, zone):
    def edit():
        if not st.session_state['edited_name']:
            print('Tên bị trống!!')
            return None
        if (st.session_state['edited_name'] != chat_name
                and st.session_state['edited_name'] in st.session_state['chats']):
            print('Tên bị trùng lặp!!')
            return None
        if st.session_state['edited_name'] == chat_name:
            print('Không thể thay đổi tên!!')
            return None
        st.session_state['chats'][chat_name]['display_name'] = st.session_state['edited_name']
    edit_zone = zone.empty()
    time.sleep(0.1)
    with edit_zone.container():
        st.text_input('Tên mới', st.session_state['chats'][chat_name]['display_name'], key='edited_name')
        column1, _, column2 = st.columns([1, 5, 1])
        column1.button('✅', on_click=edit)
        column2.button('❌')

def render_sidebar_chat_management(zone):
    new_chat_button = zone.button(label="➕ Tạo đoạn chat mới", use_container_width=True)
    if new_chat_button:
        new_chat_name = f"Chat{len(st.session_state['chats'])}"
        st.session_state["current_chat"] = new_chat_name
        new_chat(new_chat_name)

    with st.sidebar.container():
        for chat_name in st.session_state["chats"].keys():
            if st.session_state['chats'][chat_name]['is_delete']:
                continue
            if chat_name == st.session_state.get('current_chat'):
                column1, column2, column3 = zone.columns([7, 1, 1])
                column1.button(
                    label='💬 ' + st.session_state['chats'][chat_name]['display_name'],
                    on_click=switch_chat_name,
                    key=chat_name,
                    args=(chat_name,),
                    type='primary',
                    use_container_width=True,
                )
                column2.button(label='📝', key='edit', on_click=edit_chat, args=(chat_name, zone))
                column3.button(label='🗑️', key='remove', on_click=delete_chat, args=(chat_name,))
            else:
                zone.button(
                    label='💬 ' + st.session_state['chats'][chat_name]['display_name'],
                    on_click=switch_chat_name,
                    key=chat_name,
                    args=(chat_name,),
                    use_container_width=True,
                )
    if new_chat_button:
        switch_chat(new_chat_name)

def render_sidebar_rapidapi_config_tab(zone):
   st.session_state.sync_flag3 =  'hello'
   st.session_state["params"]["model_rapid"] = zone.selectbox(
        "Vui lòng chọn loại mô hình bạn muốn sử dụng!!",
        ["Harleychatbot_translate","ChatGPT","BingChat","Lemurbot"],
        help="Ở trên là 3 mô hình được sử dụng trong Hugging Face",
    )

def render_sidebar_huggingface_config_tab(zone):
   st.session_state.sync_flag3 =  'hello'
   st.session_state["params"]["model_4"] = zone.selectbox(
        "Vui lòng chọn loại mô hình bạn muốn sử dụng!!",
        ["Model LLama2","GPT2","ViT5"],
        help="Ở trên là 3 mô hình được sử dụng trong Hugging Face",
    )
   if st.session_state["params"]["model_4"] == "Model LLama2":
       st.session_state["params"]["model_llama_4"] = zone.selectbox(
        "Vui lòng chọn hình thức sử dụng",
        ["LLama English","LLama VietNamese"],
        help="Lựa chọn hình thức sử dụng của model LLama", )

def render_sidebar_gpt_config_tab(zone):
   st.session_state.sync_flag3 =  'hello'
   prompt_text5 = zone.empty()
   st.session_state["params"] = dict()
   st.session_state["params"]["model"] = zone.selectbox(
        "Vui lòng chọn loại mô hình bạn muốn sử dụng!!",
        ["Google-bard","ChatBot_openAPI","Model LLama"],
        help="Nên sử dụng ChatBot_openAPI để dùng các dịch vụ của openAI, dùng Google Bard để sử dụng mô hình do Google tạo ra,LLama là một model mới gần đây",
    )
   if st.session_state["params"]["model"] == "ChatBot_openAPI":
        st.session_state["params"]["model_openai"] = zone.selectbox(
        "Vui lòng chọn hình thức sử dụng",
        ["Use_API_Key","Use_Breaber_Token","text-davinci-003_API"], 
        help="Chọn hình thức sử dụng trong OpenAPI, dùng API sẽ sử dụng API key và sử dụng Breaber sẽ dùng mã token cá nhân,text-davinci-003 là một mô hình văn bản của OpenAI",
      )
        if st.session_state["params"]["model_openai"] in ["Use_API_Key","Use_Breaber_Token"]:
            st.session_state["params"]["model_openAI_API"] = zone.selectbox(
                "Vui lòng chọn Model muốn sử dụng trong OpenAI",
                ["gpt-3.5-turbo", "gpt-3.5-turbo-16k-0613", "gpt-3.5-turbo-1106", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-16k"],
                help="ID mô hình bạn muốn sử dụng, nên dùng gpt-3.5-turbo-1106 hoặc gpt-3.5-turbo",
            ) 
            real_psid = st.session_state["params"].get("apikey3", "")
            st.session_state["params"]["apikey3"] = prompt_text5.text_input(
        "Nhập mã API key",
        value='***' if real_psid else "None",
        key="input_psid1112",
        help="Hãy nhập mã API key",
        type="password"  # Đặt kiểu dữ liệu là password để ẩn giá trị nhập vào
    )
            st.session_state["params"]["temperature"] = zone.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.01,
        format="%0.2f",
        key ="tmpea",
        help="Nên sử dụng nhiệt độ lấy mẫu nào, trong khoảng từ 0 đến 2. Các giá trị cao hơn như 0,8 sẽ làm cho đầu ra ngẫu nhiên hơn, trong khi các giá trị thấp hơn như 0,2 sẽ làm cho đầu ra tập trung và mang tính quyết định hơn.",
    )
            st.session_state["params"]["max_tokens"] = zone.slider(
        "Max Token",
        value=2000,
        step=1,
        min_value=100,
        max_value=4096,
        key = "maxtoken",
        help="The maximum number of tokens to generate in the chat completion. The total length of input tokens and generated tokens is limited by the model's context length.",
    )
            st.session_state["params"]["presence_penalty"] = zone.slider(
        "Max Presence Penalty",
        value=0.0,
        step=0.01,
        min_value=-2.0,
        max_value=2.0,
        key ="pre",
        help="Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.",
    )
            st.session_state["params"]["frequency_penalty"] = zone.slider(
        "Max Frequency Penalty",
        value=0.0,
        step=0.01,
        min_value=-2.0,
        max_value=2.0,
        key = "fre",
        help="Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.",
    )
            st.session_state["params"]["top_p"] = zone.slider(
        "Max Top P",
        value=0.7,
        step=0.01,
        min_value=0.0,
        max_value=1.0, key = "topp",
        help="An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.",
    )
            st.session_state["params"]["stream"] = zone.checkbox(
        "Steaming output",
        value=True,
        key ="stream1",
        help="Nếu được đặt, một phần delta tin nhắn sẽ được gửi, giống như trong ChatGPT. Mã thông báo sẽ được gửi dưới dạng sự kiện do máy chủ gửi chỉ dữ liệu khi chúng có sẵn, với luồng được kết thúc bằng thông báo dữ liệu: [DONE]",
    )
            zone.caption('Tìm kiếm sự giúp đỡ tại https://platform.openai.com/docs/api-reference/chat')
   if "params" in st.session_state and st.session_state["params"].get("model_openai") in {"text-davinci-003_API"}:
     st.session_state["params"]["temperature1_1"] = zone.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.01,
        format="%0.2f",
        key="tmp12",
        help="Nên sử dụng nhiệt độ lấy mẫu nào, trong khoảng từ 0 đến 2. Các giá trị cao hơn như 0,8 sẽ làm cho đầu ra ngẫu nhiên hơn, trong khi các giá trị thấp hơn như 0,2 sẽ làm cho đầu ra tập trung và mang tính quyết định hơn.",
    )
     st.session_state["params"]["max_tokens1_1"] = zone.slider(
        "Max Token",
        value=2000,
        step=1,
        min_value=100,
        max_value=4096,
        key ="token12",
        help="The maximum number of tokens to generate in the chat completion. The total length of input tokens and generated tokens is limited by the model's context length.",
    )
     st.session_state["params"]["stop_1"] = zone.text_area(
        "Từ Stop: ",
        "None",
        key="stop12",
        help="Hãy nhập Mã ID tổ chức của bạn trong OpenAI Platform, tiềm kiếm sự trợ giúp tại đường dẫn https://platform.openai.com/account/organization",  # Đặt kiểu dữ liệu là password để ẩn giá trị nhập vào
    )
     zone.caption('Tìm kiếm sự giúp đỡ tại https://platform.openai.com/docs/api-reference/chat')

def render_sidebar_using_model_finetune_config_tab(zone):
    prompt_text12 = zone.empty()
    st.session_state["params"]["model_2"] = zone.selectbox(
        "Vui lòng chọn loại mô hình bạn muốn sử dụng!!",
        ["Finetune_XLM_Roberta","FineTune_OpenAI","FineTune_PhoBERT"],
        help="Đây là các mô hình ngôn ngữ do nhóm FineTune với PhoBERT kiến trúc base và XLM Roberta kiến trúc base, OpenAI sử dụng mô hình gpt-3.5-turbo-1106 hoặc gpt-3.5-turbo-0613",
    )
    if st.session_state["params"]["model_2"] == "FineTune_OpenAI":
        st.session_state["params"]["model_openai_2"] = zone.selectbox(
        "Vui lòng chọn hình thức sử dụng",
        ["gpt-3.5-turbo","text-davinci-002"],
        help="Chọn hình thức sử dụng trong model FineTune",
      )
        if st.session_state["params"]["model_openai_2"] == "gpt-3.5-turbo":
            model_finetune = []
            model_finetune = dsfinetune.main()
            st.session_state["params"]["model_openAI_API_1"] = zone.selectbox(
                "Vui lòng chọn Model muốn sử dụng trong FineTune OpenAI",
                model_finetune,
                help="ID mô hình bạn muốn sử dụng trong FineTune OpenAI",
            )
            st.session_state["params"]["temperature_2"] = zone.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.01,
        format="%0.2f",
        key = "1234",
        help="Nên sử dụng nhiệt độ lấy mẫu nào, trong khoảng từ 0 đến 2. Các giá trị cao hơn như 0,8 sẽ làm cho đầu ra ngẫu nhiên hơn, trong khi các giá trị thấp hơn như 0,2 sẽ làm cho đầu ra tập trung và mang tính quyết định hơn.",
    )
            st.session_state["params"]["max_tokens_2"] = zone.slider(
        "Max Token",
        value=1000,
        step=1,
        min_value=100,
        max_value=4096,
        key = "token2",
        help="The maximum number of tokens to generate in the chat completion. The total length of input tokens and generated tokens is limited by the model's context length.",
    )
            st.session_state["params"]["presence_penalty_2"] = zone.slider(
        "Max Presence Penalty",
        value=0.0,
        step=0.01,
        min_value=-2.0,
        max_value=2.0,
        help="Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.",
    )
            st.session_state["params"]["frequency_penalty_2"] = zone.slider(
        "Max Frequency Penalty",
        value=0.0,
        step=0.01,
        min_value=-2.0,
        max_value=2.0,
        help="Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.",
    )
            st.session_state["params"]["top_p_2"] = zone.slider(
        "Max Top P",
        value=0.7,
        step=0.01,
        min_value=0.0,
        max_value=1.0,
        help="An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.",
    )
            st.session_state["params"]["stream_2"] = zone.checkbox(
        "Steaming output",
        value=True,
        help="Nếu được đặt, một phần delta tin nhắn sẽ được gửi, giống như trong ChatGPT. Mã thông báo sẽ được gửi dưới dạng sự kiện do máy chủ gửi chỉ dữ liệu khi chúng có sẵn, với luồng được kết thúc bằng thông báo dữ liệu: [DONE]",
    )
            zone.caption('Tìm kiếm sự giúp đỡ tại https://platform.openai.com/docs/api-reference/chat')
    if "params" in st.session_state and st.session_state["params"].get("model_openai_2") in {"text-davinci-002"}:
      model_finetune = []
      model_finetune = dsdavinci.main()
      st.session_state["params"]["model_openAI_API_2"] = zone.selectbox(
                "Vui lòng chọn Model muốn sử dụng trong OpenAI",
                model_finetune,
                help="ID mô hình bạn muốn sử dụng",
            )
      st.session_state["params"]["temperature_3"] = zone.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.01,
        format="%0.2f",
        key="tmp123",
        help="Nên sử dụng nhiệt độ lấy mẫu nào, trong khoảng từ 0 đến 2. Các giá trị cao hơn như 0,8 sẽ làm cho đầu ra ngẫu nhiên hơn, trong khi các giá trị thấp hơn như 0,2 sẽ làm cho đầu ra tập trung và mang tính quyết định hơn.",
    )
      st.session_state["params"]["max_tokens_3"] = zone.slider(
        "Max Token",
        value=2000,
        step=1,
        min_value=100,
        max_value=4096,
        key ="token123",
        help="The maximum number of tokens to generate in the chat completion. The total length of input tokens and generated tokens is limited by the model's context length.",
    )
      st.session_state["params"]["stop_2"] = zone.text_area(
        "Từ Stop: ",
        "None",
        key="stop123",
        help="Hãy nhập Mã ID tổ chức của bạn trong OpenAI Platform, tiềm kiếm sự trợ giúp tại đường dẫn https://platform.openai.com/account/organization",  # Đặt kiểu dữ liệu là password để ẩn giá trị nhập vào
    )
      zone.caption('Tìm kiếm sự giúp đỡ tại https://platform.openai.com/docs/api-reference/chat')
    if st.session_state["params"]["model_2"] == "Finetune_XLM_Roberta":
        st.session_state["params"]["text2"] = prompt_text12.text_area(
        "Hãy nhập đoạn văn: ",
        "None",
        key="doanvan123",
        help="Hãy nhập đoạn văn của bạn vào",
    )
    if st.session_state["params"]["model_2"] == "FineTune_PhoBERT":
        st.session_state["params"]["model_phobert"] = zone.selectbox(
        "Vui lòng chọn phiên bản FineTune PhoBERT bạn sử dụng!!",
        ["Version","FineTune 32 batch","FineTune 64 batch"],
        help="Đây là các mô hình ngôn ngữ do nhóm FineTune",key = "hello123",)
        if st.session_state["params"]["model_phobert"] == "Version":
              st.session_state["params"]["model_phobert_version"] =zone.selectbox(
              "Vui lòng chọn phiên bản Version bạn sử dụng!!",
              ["Version1","Version2","Version3","Version4"],
              help="Đây là các mô hình ngôn ngữ do nhóm FineTune",key = "pbversion",)
        if st.session_state["params"]["model_phobert"] == "FineTune 32 batch":
              st.session_state["params"]["model_phobert_32"] = zone.selectbox(
              "Vui lòng chọn phiên bản FineTune có kích thước batch 32 bạn sử dụng!!",
              ["Model_32_batch 50_epoch","Model_32_batch 100_epoch","Model_32_batch 150_epoch"],
              help="Đây là các mô hình ngôn ngữ do nhóm FineTune với kích thước batch size là 32 và số lần lặp từ 50 đến 150",key = "pbbatch32",)
        if st.session_state["params"]["model_phobert"] == "FineTune 64 batch":
               st.session_state["params"]["model_phobert_64"] = zone.selectbox(
               "Vui lòng chọn phiên bản FineTune có kích thước Batch 64 bạn sử dụng!!",
               ["Model_64_batch 50_epoch","Model_64_batch 100_epoch"],
               help="Đây là các mô hình ngôn ngữ do nhóm FineTune với kích thước batch size là 64 và số lần lặp từ 50 đến 100",key = "pbbatch64",)
   
def render_sidebar_gpt_using_my_key_config_tab(zone):
    st.session_state.sync_flag1 =  'gptmykey'
    prompt_text5 = zone.empty()
    prompt_text6 = zone.empty()
    prompt_text8 = zone.empty()
    prompt_text9 = zone.empty()
    prompt_text10 = zone.empty()
    prompt_text11 = zone.empty()
    real_apikey = st.session_state["params"].get("api_key1", "")
    real_id = st.session_state["params"].get("original_ID", "")
    prompt_text7 = zone.empty()
    st.session_state["params"]["api_key1"] = zone.text_input(
        "Khóa API của bạn:",
        value='***' if real_apikey else "None",
        key="input_apikey",
        help="Hãy nhập mã API Key của bạn trong OpenAI Platform, Lấy thông tin API key tại https://platform.openai.com/api-keys",
        type="password"  # Đặt kiểu dữ liệu là password để ẩn giá trị nhập vào
    )
    st.session_state["params"]["model_key"] = prompt_text5.selectbox(
        "Chọn Mô hình bạn muốn sử dụng: ",
        ["Use_API_Key", "text-davinci-003_API"],
        help="ID mô hình bạn sử dụng trong OpenAI sử dụng API key sẽ dùng vào mô hình gpt-3.5-turbo trở lên",
    )
    if st.session_state["params"]["model_key"] in {'Use_API_Key'}:
     st.session_state["params"]["model_key_openAI"] = prompt_text6.selectbox(
            "Vui lòng chọn model sử dụng trong OpenAI API",
            ["gpt-3.5-turbo-1106", "gpt-3.5-turbo-16k-0613", "gpt-3.5-turbo", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-16k"],
            help="ID của model bạn sử dụng khuyến nghị sử dụng gpt-3.5-turbo-1106, thông tin chi tiết tại https://platform.openai.com/docs/models",
            key ="typeModel"
        )
    if st.session_state["params"]["model_key"] in {"text-davinci-003_API"}:
     st.session_state["params"]["original_ID"] = prompt_text8.text_input(
        "Mã ID tổ chức của bạn: ",
        value='***' if real_id else "None",
        key="input_apiid",
        help="Hãy nhập Mã ID tổ chức của bạn trong OpenAI Platform, tiềm kiếm sự trợ giúp tại đường dẫn https://platform.openai.com/account/organization",
        type="password"  # Đặt kiểu dữ liệu là password để ẩn giá trị nhập vào
    )
     st.session_state["params"]["temperature1"] = prompt_text9.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.01,
        format="%0.2f",
        key="tmp1",
        help="Nên sử dụng nhiệt độ lấy mẫu nào, trong khoảng từ 0 đến 2. Các giá trị cao hơn như 0,8 sẽ làm cho đầu ra ngẫu nhiên hơn, trong khi các giá trị thấp hơn như 0,2 sẽ làm cho đầu ra tập trung và mang tính quyết định hơn.",
    )
     st.session_state["params"]["max_tokens1"] = prompt_text10.slider(
        "Max Token",
        value=2000,
        step=1,
        min_value=100,
        max_value=4096,
        key ="token1",
        help="The maximum number of tokens to generate in the chat completion. The total length of input tokens and generated tokens is limited by the model's context length.",
    )
     st.session_state["params"]["stop"] = prompt_text11.text_area(
        "Từ Stop: ",
        "None",
        key="stop1",
        help="Hãy nhập Mã ID tổ chức của bạn trong OpenAI Platform, tiềm kiếm sự trợ giúp tại đường dẫn https://platform.openai.com/account/organization",  # Đặt kiểu dữ liệu là password để ẩn giá trị nhập vào
    )
    zone.caption('Tìm kiếm sự trợ giúp tại https://platform.openai.com/docs/api-reference/chat')

def render_sidebar_prompt_config_tab(zone):
    prompt_text = zone.empty()
    st.session_state["params"]["prompt"] = prompt_text.text_area(
        "Phản hồi lời nhắc",
        "You are a helpful assistant that answer questions as possible as you can.",
        help="The prompt(s) to generate completions for, encoded as a string, array of strings, array of tokens, or array of token arrays.",
    )
    template = zone.selectbox('Loading From Prompt Template', load_prompt_templates())
    if template:
        prompts_df = load_prompts(template)
        actor = zone.selectbox('Đang tải lời nhắc', prompts_df.index.tolist())
        if actor:
            st.session_state["params"]["prompt"] = prompt_text.text_area(
                "Hệ thống lời nhắc",
                prompts_df.loc[actor].prompt,
                help="The prompt(s) to generate completions for, encoded as a string, array of strings, array of tokens, or array of token arrays.",
            )
import streamlit as st


def render_sidebar_google_bard_config_tab(zone):
    st.session_state.sync_flag2 = 'bard'
    # Sử dụng biến trung gian để lưu giữ giá trị thực và giá trị ẩn
    real_psid = st.session_state["params"].get("1_PSID", "")
    real_psidcc = st.session_state["params"].get("1_PSIDCC", "")
    real_psidts = st.session_state["params"].get("1_PSIDTS", "")
    st.session_state["params"]["1_PSID"] = zone.text_input(
        "Nhập mã Secure 1_PSID",
        value='***' if real_psid else "None",
        key="input_psid",
        help="Hãy nhập mã Cookie Secure 1_PSID, hãy vào trang https://bard.google.com/chat chọn F12 chọn Application và chọn các Cookie cần thiết!",
        type="password"  # Đặt kiểu dữ liệu là password để ẩn giá trị nhập vào
    )
    st.session_state["params"]["1_PSIDCC"] = zone.text_input(
        "Nhập mã Secure 1_PSIDCC",
        value='***' if real_psidcc else "None",
        key="input_psidcc",
        help="Secure 1_PSIDCC, hãy vào trang https://bard.google.com/chat chọn F12 chọn Application và chọn các Cookie cần thiết!",
        type="password"  # Đặt kiểu dữ liệu là password để ẩn giá trị nhập vào
    )
    st.session_state["params"]["1_PSIDTS"] = zone.text_input(
        "Nhập mã Secure 1_PSIDTS",
        value='***' if real_psidts else "None",
        key="input_psidts",
        help="Secure 1_PSIDTS, hãy vào trang https://bard.google.com/chat chọn F12 chọn Application và chọn các Cookie cần thiết!",
        type="password"# Đặt kiểu dữ liệu là password để ẩn giá trị nhập vào
    )
# Sử dụng hàm
def render_download_zone(zone):
    from io import BytesIO, StringIO
    if not st.session_state.get('current_chat'):
        return
    chat = st.session_state['chats'][st.session_state['current_chat']]
    col1, col2 = zone.columns([1, 1])
    chat_messages = ['# ' + chat['display_name']]
    if chat["question"]:
        for i in range(len(chat["question"])):
            chat_messages.append(f"""💎 **YOU:** {chat["question"][i]}""")
            if i < len(chat["answer"]):
                chat_messages.append(f"""🤖 **AI:** {chat["answer"][i]}""")
        col1.download_button('📤 Markdown', '\n'.join(chat_messages).encode('utf-8'),
                             file_name=f"{chat['display_name']}.md", help="Download messages to a markdown file",
                             use_container_width=True)
    tables = []
    for answer in chat["answer"]:
        filter_table_str = '\n'.join([m.strip() for m in answer.split('\n') if m.strip().startswith('| ') or m == ''])
        try:
            tables.extend(
                [pd.read_table(StringIO(filter_table_str.replace(' ', '')), sep='|').dropna(axis=1, how='all').iloc[1:]
                 for m in filter_table_str.split('\n\n')])
        except Exception as e:
            print(e)
    if tables:
        buffer = BytesIO()
        with pd.ExcelWriter(buffer) as writer:
            for index, table in enumerate(tables):
                table.to_excel(writer, sheet_name=str(index + 1), index=False)
        col2.download_button('📉 Excel', buffer.getvalue(), file_name=f"{chat['display_name']}.xlsx",
                             help="Download tables to a excel file", use_container_width=True)
selected_tab = None

def get_session():
    if "selected_tab" not in st.session_state:
        st.session_state.selected_tab = 'ChatGPT'
    if "prompt_checked" not in st.session_state:
        st.session_state.prompt_checked = False
    if "bard_checked" not in st.session_state:
        st.session_state.bard_checked = False
    if "apikey_checked" not in st.session_state:
        st.session_state.apikey_checked = False
    if "gpt_checked" not in st.session_state:
        st.session_state.gpt_checked = False
    if "finetune_checked" not in st.session_state:
        st.session_state.finetune_checked = False
    if "huggingface_checked" not in st.session_state:
        st.session_state.huggingface_checked = False
    if "rapidapi_checked" not in st.session_state:
        st.session_state.rapidapi_checked = False
    return st.session_state

def render_sidebar():
    # Initialize session state
    session_state = get_session()
    # Set up the sidebar components
    chat_name_container = st.sidebar.container()
    chat_config_expander = st.sidebar.expander('⚙️ Cấu hình Chat', True)
    tab_gpt,tab_rapid, tab_prompt, tab_bard, chatgpt_mykey,huggingface = chat_config_expander.tabs(
        ['🌐  ChatBot','❄️ Rapid API','👥 Hộp thoại gợi ý', '🌏  Google Bard', '📚  ChatGPT use APIKey',"🤗 Hugging Face"]
    )
    download_zone = st.sidebar.empty()
    github_zone = st.sidebar.empty()
    # Render the content of each tab
    render_sidebar_gpt_config_tab(tab_gpt)
    render_sidebar_rapidapi_config_tab(tab_rapid)
    render_sidebar_prompt_config_tab(tab_prompt)
    render_sidebar_google_bard_config_tab(tab_bard)
    render_sidebar_gpt_using_my_key_config_tab(chatgpt_mykey)
   # render_sidebar_using_model_finetune_config_tab(model_finetune)
    render_sidebar_huggingface_config_tab(huggingface)
    render_sidebar_chat_management(chat_name_container)
    render_download_zone(download_zone)
    render_github_info(github_zone)
    # Gán giá trị cho selected_tab khi không nhấn vào button
    if tab_gpt.checkbox('🌐 ChatGPT', value=(session_state.selected_tab == 'ChatGPT')):
        session_state.selected_tab = 'ChatGPT'
        session_state.prompt_checked = False
        session_state.bard_checked = False
        session_state.apikey_checked = False
        session_state.finetune_checked = False
        session_state.huggingface_checked = False
        session_state.rapidapi_checked = False
        st.write(f"Đã chọn tab: {session_state.selected_tab}")
    if tab_prompt.checkbox('👥 Prompt', value=(session_state.selected_tab == 'Prompt')):
        session_state.selected_tab = 'Prompt'
        session_state.gpt_checked = False
        session_state.bard_checked = False
        session_state.apikey_checked = False
        session_state.finetune_checked = False
        session_state.huggingface_checked = False
        session_state.rapidapi_checked = False
        st.write(f"Đã chọn tab: {session_state.selected_tab}")
    if tab_bard.checkbox('🌏 Google Bard', value=(session_state.selected_tab == 'Google Bard')):
        session_state.selected_tab = 'Google Bard'
        session_state.gpt_checked = False
        session_state.prompt_checked = False
        session_state.apikey_checked = False
        session_state.finetune_checked = False
        session_state.rapidapi_checked = False
        session_state.huggingface_checked = False
        st.write(f"Đã chọn tab: {session_state.selected_tab}")
    if chatgpt_mykey.checkbox('📚 ChatGPT APIKey', value=(session_state.selected_tab == 'ChatGPT APIKey')):
        session_state.selected_tab = 'ChatGPT APIKey'
        session_state.gpt_checked = False
        session_state.prompt_checked = False
        session_state.rapidapi_checked = False
        session_state.bard_checked = False
        session_state.finetune_checked = False
        session_state.huggingface_checked = False
        st.write(f"Đã chọn tab: {session_state.selected_tab}")
    if huggingface.checkbox('🤗 Hugging Face', value=(session_state.selected_tab == 'HuggingFace')):
        session_state.selected_tab = 'HuggingFace'
        session_state.gpt_checked = False
        session_state.prompt_checked = False
        session_state.bard_checked = False
        session_state.rapidapi_checked = False
        session_state.apikey_checked = False
        session_state.finetune_checked = False
        st.write(f"Đã chọn tab: {session_state.selected_tab}")
    if tab_rapid.checkbox('❄️ Rapid API', value=(session_state.selected_tab == 'Rapid API')):
        session_state.selected_tab = 'Rapid API'
        session_state.gpt_checked = False
        session_state.prompt_checked = False
        session_state.bard_checked = False
        session_state.huggingface_checked = False
        session_state.apikey_checked = False
        session_state.finetune_checked = False
        st.write(f"Đã chọn tab: {session_state.selected_tab}")

def render_user_message(message, zone):
    col1, col2 = zone.columns([1, 8])
    col1.markdown("👻 **Bạn:**")
    col2.markdown(message)

def render_ai_message(message, zone):
    col1, col2 = zone.columns([1, 8])
    col1.markdown("🤖 **Chat:**")
    col2.markdown(message)

def render_history_answer(chat, zone):
    zone.empty()
    time.sleep(0.1)
    with zone.container():
        if chat['messages']:
            st.caption(f"""ℹ️ Prompt: {chat["messages"][0]['content']}""")
        if chat["question"]:
            for i in range(len(chat["question"])):
                render_user_message(chat["question"][i], st)
                if i < len(chat["answer"]):
                    render_ai_message(chat["answer"][i], st)

def render_last_answer7(question,chat,zone):
    answer_zone = zone.empty()
    chat["messages"].append(question)
    chat["question"].append(question)
    response = ""
    question = ' '.join(question.split())
    if st.session_state["params"]["model_rapid"] in {'Harleychatbot_translate'}:
       with st.spinner("Chờ phản hồi..."):
        response = rapidapi_kethop2.main(question)
        answer = ""
        answer = response
        chat["answer"].append(answer)
        chat["messages"].append({"role": "assistant", "content": answer})
    if st.session_state["params"]["model_rapid"] in {'ChatGPT'}:
      with st.spinner("Chờ phản hồi..."):
        processed_question = ' '.join(question.split())
        response = rapidapi1.main(processed_question)
        answer = ""
        answer = response
        chat["answer"].append(answer)
        chat["messages"].append({"role": "assistant", "content": answer})
        render_ai_message(answer, answer_zone)
    if st.session_state["params"]["model_rapid"] in {'BingChat'}:
      with st.spinner("Chờ phản hồi..."):
        processed_question = ' '.join(question.split())
        response = rapidapi2.get_bingchat_response(processed_question)
        answer = ""
        answer = response
        chat["answer"].append(answer)
        chat["messages"].append({"role": "assistant", "content": answer})
        render_ai_message(answer, answer_zone)
    if st.session_state["params"]["model_rapid"] in {'Lemurbot'}:
      with st.spinner("Chờ phản hồi..."):
        processed_question = ' '.join(question.split())
        response = rapidapi3.get_chatbot_response(processed_question)
        answer = ""
        answer = response
        chat["answer"].append(answer)
        chat["messages"].append({"role": "assistant", "content": answer})
        render_ai_message(answer, answer_zone)

def render_last_answer6(question,chat,zone):
    answer_zone = zone.empty()
    chat["messages"].append(question)
    chat["question"].append(question)
    response = ""
    question = ' '.join(question.split())
    if st.session_state["params"]["model_4"] in {'Model LLama2'}:
      if st.session_state["params"]["model_llama_4"] in {'LLama English'}:
       with st.spinner("Chờ phản hồi..."):
        response = llam.get_assistant_response(question)
        answer = ""
        answer = response
        chat["answer"].append(answer)
        chat["messages"].append({"role": "assistant", "content": answer})
      elif st.session_state["params"]["model_llama_4"] in {'LLama VietNamese'}:
       with st.spinner("Chờ phản hồi..."):
        response = llamvi.get_assistant_response(question)
        answer = ""
        answer = response
        chat["answer"].append(answer)
        chat["messages"].append({"role": "assistant", "content": answer})
    elif st.session_state["params"]["model_4"] in {'GPT2'}:
      with st.spinner("Chờ phản hồi..."):
        processed_question = ' '.join(question.split())
        response = gpt2hgf.generate_text(processed_question)
        answer = ""
        answer = response
        chat["answer"].append(answer)
        chat["messages"].append({"role": "assistant", "content": answer})
        render_ai_message(answer, answer_zone)
    else:
      with st.spinner("Chờ phản hồi..."):
        processed_question = ' '.join(question.split())
        response = viT5.summarize_text(processed_question)
        answer = ""
        answer = response
        chat["answer"].append(answer)
        chat["messages"].append({"role": "assistant", "content": answer})
        render_ai_message(answer, answer_zone)
    


def render_last_answer4(question,chat,zone):
    answer_zone = zone.empty()
    chat["messages"].append(question)
    chat["question"].append(question)
    response = ""
    if st.session_state["params"]["model_key"] in {'Use_API_Key'}:
         with st.spinner("Chờ phản hồi..."):
          key = ""
          key = st.session_state["params"]["api_key1"]
          if key == None or len(key) == 0:
              key = keyOpenAI
          model_value = st.session_state["params"]["model_key_openAI"]
          response = get_openai_response_api_key(question,model_value,key)
          answer = ""
          answer = response
          chat["answer"].append(answer)
          chat["messages"].append({"role": "assistant", "content": answer})
          render_ai_message(answer, answer_zone)
    elif st.session_state["params"]["model_key"] in {'text-davinci-003_API'}:
         with st.spinner("Chờ phản hồi..."):
          key = ''
          key = st.session_state["params"]["api_key1"]
          if key == None or len(key) == 0:
              key = keyOpenAI
          token = st.session_state["params"]["max_tokens1"]
          temp = st.session_state["params"]["temperature1"]
          stp = ""
          stp = st.session_state["params"]["stop"]
          oriID = st.session_state["params"]["original_ID"]
          response = get_openai_response_text_davinci(question,token,key,oriID,temp,stp)
          answer = ""
          answer = response
          chat["answer"].append(answer)
          chat["messages"].append({"role": "assistant", "content": answer})
          render_ai_message(answer, answer_zone)

def render_last_answer3(question,chat,zone):
        with st.spinner("Chờ phản hồi..."):
         flag2 = False
         chat["messages"].append(question)
         chat["question"].append(question)
         response = ''
         answer_zone = zone.empty()
         psid =st.session_state["params"]["1_PSID"]
         psidts =st.session_state["params"]["1_PSIDTS"]
         psidcc =st.session_state["params"]["1_PSIDCC"]
         answer = ""
         bard1 = config_bard.initialize_bard_session(psid,psidts,psidcc)
         response = config_bard.send_message(question)
         answer = response
         chat["answer"].append(answer)
         chat["messages"].append({"role": "assistant", "content": answer})
         render_ai_message(answer, answer_zone)

def render_last_answer2(question, chat, zone):
    answer_zone = zone.empty()
    chat["messages"].append(question)
    chat["question"].append(question)
    response = ""
    question = ' '.join(question.split())
    if st.session_state["params"]["model"] in {'chatbot-fake'}:
      with st.spinner("Chờ phản hồi..."):
        response = get_openai_response2(question)
        answer = ""
        answer = response
        chat["answer"].append(answer)
        chat["messages"].append({"role": "assistant", "content": answer})
        render_ai_message(answer, answer_zone)
    elif st.session_state["params"]["model"] in {'Google-bard'}:
      with st.spinner("Chờ phản hồi..."):
        response = get_openai_response3(question)
        answer = ""
        answer = response
        chat["answer"].append(answer)
        chat["messages"].append({"role": "assistant", "content": answer})
        render_ai_message(answer, answer_zone)
    elif st.session_state["params"]["model"] in {'gpt-3.5-turbo','gpt-3.5-turbo-1106'}:
       with st.spinner("Chờ phản hồi..."):
        model_value = st.session_state["params"]["model"]
        temperature=st.session_state["params"]["temperature"]
        fre=st.session_state["params"]["frequency_penalty"]
        pre = st.session_state["params"]["presence_penalty"]
        max_tokens=st.session_state["params"]["max_tokens"]
        top_p=st.session_state["params"]["top_p"]
        response = get_openai_response1(question, model_value,temperature,pre,fre,max_tokens,top_p)
        answer = ""
        answer = response
        chat["answer"].append(answer)
        chat["messages"].append({"role": "assistant", "content": answer})
        render_ai_message(answer, answer_zone)
    elif st.session_state["params"]["model"] in {'Model LLama'}:
     with st.spinner("Chờ phản hồi..."):
        response = llam.get_assistant_response(question)
        answer = ""
        answer = response
        chat["answer"].append(answer)
        chat["messages"].append({"role": "assistant", "content": answer})
        render_ai_message(answer, answer_zone)
    elif st.session_state["params"]["model"] in {'ChatBot_openAPI'}:
        if st.session_state["params"]["model_openai"] in {'Use_API_Key'}:
         with st.spinner("Chờ phản hồi..."):
          apikey = st.session_state["params"]["apikey3"] 
          model_value = st.session_state["params"]["model_openAI_API"]
          response = get_openai_response_api_key(question,model_value,apikey)
          answer = ""
          answer = response
          chat["answer"].append(answer)
          chat["messages"].append({"role": "assistant", "content": answer})
          render_ai_message(answer, answer_zone)
        elif st.session_state["params"]["model_openai"] in {'Use_Breaber_Token'}:
         with st.spinner("Chờ phản hổi..."):
          model_value = st.session_state["params"]["model_openAI_API"]
          response = get_openai_response_api_token(question,model_value)
          answer = ""
          answer = response
          chat["answer"].append(answer)
          chat["messages"].append({"role": "assistant", "content": answer})
          render_ai_message(answer, answer_zone)
        else:
         with st.spinner("Chờ phản hồi..."):
          token = st.session_state["params"]["max_tokens1_1"]
          temp = st.session_state["params"]["temperature1_1"]
          stp = ""
          stp = st.session_state["params"]["stop_1"]
          response = get_openai_response_text_davinci(question,token,keyOpenAIdvc,originalID,temp,stp)
          answer = ""
          answer = response
          chat["answer"].append(answer)
          chat["messages"].append({"role": "assistant", "content": answer})
          render_ai_message(answer, answer_zone)
    else:
        if st.session_state["params"]["stream"]:
            with st.spinner("Chờ phản hồi..."):
                model_value = st.session_state["params"]["model"]
                temperature=st.session_state["params"]["temperature"]
                fre=st.session_state["params"]["frequency_penalty"]
                pre = st.session_state["params"]["presence_penalty"]
                max_tokens=st.session_state["params"]["max_tokens"]
                top_p=st.session_state["params"]["top_p"]
                answer = ""
                response = get_openai_response1(question, model_value,temperature,pre,fre,max_tokens,top_p)
                answer = response
                chat["answer"].append(answer)
                chat["messages"].append({"role": "assistant", "content": answer})
                render_ai_message(answer, answer_zone)
        else:
            with st.spinner("Chờ phản hồi..."):
                model_value = st.session_state["params"]["model"]
                temperature=st.session_state["params"]["temperature"]
                fre=st.session_state["params"]["frequency_penalty"]
                pre = st.session_state["params"]["presence_penalty"]
                max_tokens=st.session_state["params"]["max_tokens"]
                top_p=st.session_state["params"]["top_p"]
                answer = ""
                response = get_openai_response1(question, model_value,temperature,pre,fre,max_tokens,top_p)
                answer = response
                chat["answer"].append(answer)
                chat["messages"].append({"role": "assistant", "content": answer})
                render_ai_message(answer, zone)

# Call the function
def render_stop_generate_button(zone):
    def stop():
        st.session_state['regenerate'] = False
    zone.columns((2, 1, 2))[1].button('□ Dừng', on_click=stop)

def render_regenerate_button(chat, zone):
    def regenerate():
        chat["messages"].pop(-1)
        chat["messages"].pop(-1)
        chat["answer"].pop(-1)
        st.session_state['regenerate'] = True
        st.session_state['last_question'] = chat["question"].pop(-1)
    zone.columns((2, 1, 2))[1].button('🔄Tạo lại', type='primary', on_click=regenerate)

def render_chat(chat_name):
    def handle_ask():
        if st.session_state['input']:
            re_generate_zone.empty()
            render_user_message(st.session_state['input'], last_question_zone)
            render_stop_generate_button(stop_generate_zone)
            if st.session_state.selected_tab in ['ChatGPT','Prompt'] :
                render_last_answer2(st.session_state['input'], chat, last_answer_zone)
            if st.session_state.selected_tab == 'Google Bard' and st.session_state["params"]["1_PSID"] not in["None"]:
                render_last_answer3(st.session_state["input"],chat,last_answer_zone)
            if st.session_state.selected_tab == 'ChatGPT APIKey' and st.session_state["params"]["api_key1"]not in["None"]:
                render_last_answer4(st.session_state["input"],chat,last_answer_zone)
            if st.session_state.selected_tab == 'HuggingFace':
                render_last_answer6(st.session_state["input"],chat,last_answer_zone)
            if st.session_state.selected_tab == 'Rapid API':
                render_last_answer7(st.session_state["input"],chat,last_answer_zone)
            st.session_state['input'] = ''
    if chat_name not in st.session_state["chats"]:
        st.error(f'{chat_name} is not exist')
        return
    chat = st.session_state["chats"][chat_name]
    if chat['is_delete']:
        st.error(f"{chat_name} is deleted")
        st.stop()
    if len(chat['messages']) == 1 and st.session_state["params"]["prompt"]:
        chat["messages"][0]['content'] = st.session_state["params"]["prompt"]
    conversation_zone = st.container()
    history_zone = conversation_zone.empty()
    last_question_zone = conversation_zone.empty()
    last_answer_zone = conversation_zone.empty()
    ask_form_zone = st.empty()
    render_history_answer(chat, history_zone)
    ask_form = ask_form_zone.form(chat_name)
    col1, col2 = ask_form.columns([10, 1])
    col1.text_area("👻 Bạn: ",
                   key="input",
                   max_chars=4000,
                   label_visibility='collapsed')
    with col2.container():
        for _ in range(2):
            st.write('\n')
        st.form_submit_button("🚀", on_click=handle_ask)
    stop_generate_zone = conversation_zone.empty()
    re_generate_zone = conversation_zone.empty()
    if st.session_state.get('regenerate'):
        render_user_message(st.session_state['last_question'], last_question_zone)
        render_stop_generate_button(stop_generate_zone)
        if st.session_state.selected_tab in ['ChatGPT','Prompt'] :
                render_last_answer2(st.session_state['last_question'], chat, last_answer_zone)
        if st.session_state.selected_tab == 'Google Bard' and st.session_state["params"]["1_PSID"] not in["None"]:
                render_last_answer3(st.session_state["last_question"],chat,last_answer_zone)
        if st.session_state.selected_tab == 'ChatGPT APIKey' and st.session_state["params"]["api_key1"]not in["None"]:
                render_last_answer4(st.session_state["last_question"],chat,last_answer_zone)
        if st.session_state.selected_tab == 'HuggingFace':
                render_last_answer6(st.session_state["input"],chat,last_answer_zone)
        if st.session_state.selected_tab == 'Rapid API':
                render_last_answer7(st.session_state["input"],chat,last_answer_zone)
        st.session_state['regenerate'] = False
    if chat["answer"]:
        stop_generate_zone.empty()
        render_regenerate_button(chat, re_generate_zone)
    render_footer()

def get_openai_response1(messages,model,temperature,pre,fre,token,top_p):
    response = demo.get_chat_completion(messages,model,temperature,pre,fre,token,top_p)
    return response
def get_openai_response2(messages):
    return None
def get_openai_response3(messages):
    response = google.send_message(messages)
    return response
def get_openai_response_api_key(messages,model,apikey):
    response = openai_key.main(messages,model,apikey)
    return response
def get_openai_response_api_token(messages,model):
    response = openai_token.main(messages,model)
    return response
def get_openai_response_text_davinci(messages,token,keyOpenAIdvc,originalID,temp,stop):
    response = openai_text.main(messages,token,keyOpenAIdvc,originalID,temp,stop)
    return response


def get_openai_response(messages):
    if st.session_state["params"]["model"] in {'gpt-3.5-turbo', 'gpt4','text-davinci-002-render-sha','gpt-3.5-turbo-1106'}:
        response = openai.ChatCompletion.create(
            model=st.session_state["params"]["model"],
            temperature=st.session_state["params"]["temperature"],
            messages=messages,
            stream=st.session_state["params"]["stream"],
            max_tokens=st.session_state["params"]["max_tokens"],
        )
    else:
        raise NotImplementedError('Not implemented yet!')
    return response

if __name__ == "__main__":
    init_openai_settings()
    init_session()
    render_sidebar()
    if st.session_state.get("current_chat"):
        render_chat(st.session_state["current_chat"])
    if len(st.session_state["chats"]) == 0:
        switch_chat(new_chat(f"Chat{len(st.session_state['chats'])}"))
