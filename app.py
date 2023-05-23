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

.custom-btn-highlight {
    border: none !important;
    background: rgb(243 244 246) !important;
    box-shadow: none !important;
    display: block !important;
    text-align: left !important;
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
  border-radius: 35px !important;
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
    box-shadow: 0.3px 0.3px 0.3px gray !important;
}

#example-title {
  margin-bottom: 15px;
}

#aux-btns-popup {
    z-index: 200;
    position: absolute !important;
    bottom: 75px !important;
    right: 15px !important;
}

#aux-btns-popup > div {
    flex-wrap: nowrap;
    width: auto;
    margin: auto;  
}

.aux-btn {
    height: 30px !important;
    flex-wrap: initial !important;
    flex: none !important;
    min-width: min(100px,100%) !important;
    font-weight: unset !important;
    font-size: 10pt !important;

    background: linear-gradient(to bottom right, #f7faff, #ffffff) !important;
    box-shadow: none !important;
    border-radius: 20px !important;    
}

.aux-btn:hover {
    box-shadow: 0.3px 0.3px 0.3px gray !important;
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

update_left_btns_state = """
(v)=>{
  document.querySelector('.custom-btn-highlight').classList.add('custom-btn');
  document.querySelector('.custom-btn-highlight').classList.remove('custom-btn-highlight');

  const elements = document.querySelectorAll(".custom-btn");

  for(var i=0; i < elements.length; i++) {
    const element = elements[i];
    if(element.textContent == v) {
      console.log(v);
      element.classList.add('custom-btn-highlight');
      element.classList.remove('custom-btn');
      break;
    }
  }
}""" 

channels = [
    "1st Channel",
    "2nd Channel",
    "3rd Channel",
    "4th Channel",
    "5th Channel",
    "6th Channel",
    "7th Channel",
    "8th Channel",
    "9th Channel",
    "10th Channel"
]
channel_btns = []

examples = [
    "hello world", 
    "what's up?", 
    "this is GradioChat"
]
ex_btns = []

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

  for idx, channel in enumerate(channels):
    if channel == btn_title:
      choice = idx

  return choice

def set_chatbot(btn, ld):
  choice = channel_num(btn)

  res = [
      GradioAlpacaChatPPManager.from_json(json.dumps(ppm_str))
      for ppm_str in ld
  ]
  empty = len(res[choice].pingpongs) == 0
  return (
      res[choice].build_uis(), 
      choice,
      gr.update(visible=empty)
  )

def set_example(btn):
  return btn, gr.update(visible=False)

def set_popup_visibility(ld, example_block):
  return example_block

with gr.Blocks(css=STYLE, elem_id='container-col') as block:
  idx = gr.State(0)
  local_data = gr.JSON({},visible=False)

  with gr.Row():
    with gr.Column(scale=1, min_width=180):
      gr.Markdown("GradioChat", elem_id="left-top")
        
      with gr.Column(elem_id="left-pane"):
        with gr.Accordion("Histories", elem_id="chat-history-accordion"):
          channel_btns.append(gr.Button(channels[0], elem_classes=["custom-btn-highlight"]))

          for channel in channels[1:]:
            channel_btns.append(gr.Button(channel, elem_classes=["custom-btn"]))
        
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
          with gr.Row() as text_block:
            for example in examples:
              ex_btns.append(gr.Button(example, elem_classes=["example-btn"]))

      with gr.Column(elem_id="aux-btns-popup", visible=True):
        with gr.Row():
          stop = gr.Button("Stop", elem_classes=["aux-btn"])
          regenerate = gr.Button("Regenerate", elem_classes=["aux-btn"])
          clean = gr.Button("Clean", elem_classes=["aux-btn"])

      chatbot = gr.Chatbot(elem_id='chatbot')
      instruction_txtbox = gr.Textbox(
          placeholder="Ask anything", label="",
          elem_id="prompt-txt"
      )

  for btn in channel_btns:
    btn.click(
      set_chatbot,
      [btn, local_data],
      [chatbot, idx, example_block]        
    ).then(
      None, btn, None, 
      _js=update_left_btns_state        
    )
  
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

block.queue().launch(debug=True)
