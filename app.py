import json
import gradio as gr
from pingpong import PingPong
from pingpong.gradio import GradioAlpacaChatPPManager

STYLE = """
.custom-btn {
    border: none !important;
    background: none !important;
    box-shadow: none !important;
    display: block !important;
    text-align: left !important;
}
.custom-btn:hover {
    background: rgb(243 244 246) !important;
}
#prompt-txt > label > span {
    display: none !important;
}
#prompt-txt > label > textarea {
    border: transparent;
    box-shadow: none;
}
#chatbot {
    height: 800px; 
    overflow: auto;
    box-shadow: none !important;
    border: none !important;
}
#chatbot > .wrap {
    max-height: 780px;
}
#chatbot + div {
  border-radius: 35px;
  width: 80% !important;
  margin: auto !important;  
}

#left-pane {
    background-color: #f9fafb;
    border-radius: 15px;
    padding: 10px;
}

#left-top {
    padding-left: 10px;
    padding-right: 10px;
    text-align: center;
    font-weight: bold;
    font-size: large;    
}

#chat-history-accordion {
    background: transparent;
    border: 0.8px !important;  
}

#right-pane {
  margin-left: 20px;
  margin-right: 70px;
}

#initial-popup {
    z-index: 100;
    position: absolute;
    width: 50%;
    top: 50%;
    height: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 35px;
    padding: 15px;
}

#initial-popup-title {
    text-align: center;
    font-size: 18px;
    font-weight: bold;    
}

#initial-popup-left-pane {
    min-width: 150px !important;
}

#initial-popup-right-pane {
    text-align: right;
}

.example-btn {
    padding-top: 20px !important;
    padding-bottom: 20px !important;
    padding-left: 5px !important;
    padding-right: 5px !important;
    background: linear-gradient(to bottom right, #f7faff, #ffffff) !important;
    box-shadow: none !important;
    border-radius: 20px !important;
}

.example-btn:hover {
    box-shadow: 0.3px 0.3px 0.3px gray !important
}

#example-title {
  margin-bottom: 15px;
}
"""

get_local_storage = """
function() {
  globalThis.setStorage = (key, value)=>{
    localStorage.setItem(key, JSON.stringify(value));
  }
  globalThis.getStorage = (key, value)=>{
    return JSON.parse(localStorage.getItem(key));
  }

  var local_data = getStorage('local_data');
  var history = [];

  if(local_data) {
    local_data[0].pingpongs.forEach(element =>{ 
      history.push([element.ping, element.pong]);
    });
  }
  else {
    local_data = [];
    for (let step = 0; step < 10; step++) {
      local_data.push({'ctx': '', 'pingpongs':[]});
    }
    setStorage('local_data', local_data);
  }

  if(history.length == 0) {
    document.querySelector("#initial-popup").classList.remove('hide');
  }

  return [history, local_data];
}
"""

def add_pingpong(idx, ld, ping):
  res = [
      GradioAlpacaChatPPManager.from_json(json.dumps(ppm))
      for ppm in ld
  ]

  ppm = res[idx]
  ppm.add_pingpong(PingPong(ping, "dang!!!!!!!"))
  return "", ppm.build_uis(), str(res)

def channel_num(btn_title):
  choice = 0
    
  if btn == "1st Channel":
    choice = 0
  elif btn == "2nd Channel":
    choice = 1
  elif btn == "3rd Channel":
    choice = 2
  elif btn == "4th Channel":
    choice = 3
  elif btn == "5th Channel":
    choice = 4
  elif btn == "6th Channel":
    choice = 5
  elif btn == "7th Channel":
    choice = 6
  elif btn == "8th Channel":
    choice = 7
  elif btn == "9th Channel":
    choice = 8
  elif btn == "10th Channel":
    choice = 9

  return choice

def set_chatbot(btn, ld):
  choice = channel_num(btn)

  res = [
      GradioAlpacaChatPPManager.from_json(json.dumps(ppm_str))
      for ppm_str in ld
  ]
  empty = len(res[choice].pingpongs) == 0
  return res[choice].build_uis(), choice, gr.update(visible=empty)

def set_example(btn):
  return btn, gr.update(visible=False)

def set_popup_visibility(ld, example_block):
  print(ld)
  return example_block

with gr.Blocks(css=STYLE, elem_id='container-col') as block:
  idx = gr.State(0)
  local_data = gr.JSON({},visible=False)

  with gr.Row():
    with gr.Column(scale=1, min_width=180):
      gr.Markdown("GradioChat", elem_id="left-top")
        
      with gr.Column(elem_id="left-pane"):
        with gr.Accordion("Histories", elem_id="chat-history-accordion"):
          first = gr.Button("1st Channel", elem_classes=["custom-btn"])
          second = gr.Button("2nd Channel", elem_classes=["custom-btn"])
          third = gr.Button("3rd Channel", elem_classes=["custom-btn"])
          fourth = gr.Button("4th Channel", elem_classes=["custom-btn"])
          fifth = gr.Button("5th Channel", elem_classes=["custom-btn"])
          sixth = gr.Button("6th Channel", elem_classes=["custom-btn"])
          seventh = gr.Button("7th Channel", elem_classes=["custom-btn"])
          eighth = gr.Button("8th Channel", elem_classes=["custom-btn"])
          nineth = gr.Button("9th Channel", elem_classes=["custom-btn"])
          tenth = gr.Button("10th Channel", elem_classes=["custom-btn"])            
          
    with gr.Column(scale=8, elem_id="right-pane"):
      with gr.Column(elem_id="initial-popup", visible=False) as example_block:
        with gr.Row(scale=1):
          with gr.Column(elem_id="initial-popup-left-pane"):
            gr.Markdown("GradioChat", elem_id="initial-popup-title")
            gr.Markdown("Making the community's best AI chat models available to everyone.")
          with gr.Column(elem_id="initial-popup-right-pane"):
            gr.Markdown("Chat UI is now open sourced on Hugging Face Hub")
            gr.Markdown("check out the [↗ repository](https://huggingface.co/spaces/chansung/test-multi-conv)")

        with gr.Column(scale=1):
          gr.Markdown("Examples")
          with gr.Row():
            ex_btn1 = gr.Button("hello world", elem_classes=["example-btn"])
            ex_btn2 = gr.Button("what's up?", elem_classes=["example-btn"])
            ex_btn3 = gr.Button("this is GradioChat", elem_classes=["example-btn"])

      chatbot = gr.Chatbot(elem_id='chatbot')
      instruction_txtbox = gr.Textbox(
          placeholder="Ask anything", label="",
          elem_id="prompt-txt"
      )

  btns = [
      first, second, third, fourth, fifth,
      sixth, seventh, eighth, nineth, tenth
  ]
  for btn in btns:
    btn.click(
      set_chatbot,
      [btn, local_data],
      [chatbot, idx, example_block]
    )
  
  ex_btns = [ex_btn1, ex_btn2, ex_btn3]
  for btn in ex_btns:
    btn.click(
      set_example,
      [btn],
      [instruction_txtbox, example_block]  
    )

  instruction_txtbox.submit(
    lambda: gr.update(visible=False),
    None,
    example_block
  ).then(
    add_pingpong,
    [idx, local_data, instruction_txtbox],
    [instruction_txtbox, chatbot, local_data]
  ).then(
    None, local_data, None, 
    _js="(v)=>{ setStorage('local_data',v) }"
  )

  block.load(
      None,
      inputs=None,
      outputs=[chatbot, local_data],
      _js=get_local_storage,
  )  

block.queue().launch(share=False)
