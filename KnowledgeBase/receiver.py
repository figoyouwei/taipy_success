'''
@author: Youwei Zheng
@target: Run receiver first
@update: 2024.08.14
'''

# ------------------------------
# Imports and defining the socket parameters.
# ------------------------------

import socket
from threading import Thread
from taipy.gui import Gui, State, invoke_callback, get_state_id

HOST = "127.0.0.1"
PORT = 5050

# ------------------------------
# Gather the list of state identifiers.
# ------------------------------

state_id_list = []

def on_init(state: State):
    state_id = get_state_id(state)
    if (state_id := get_state_id(state)) is not None:
        state_id_list.append(state_id)
        
# ------------------------------
# Socker listener
# ------------------------------
        
def client_handler(gui: Gui, state_id_list: list):
    # establish a listening server/socker
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, _ = s.accept()
    
    while True:
        if data := conn.recv(1024):
            print(f"Data received: {data.decode()}")
            if hasattr(gui, "_server") and state_id_list:
                invoke_callback(
                    gui=gui, 
                    state_id=state_id_list[0], 
                    callback=update_received_data, 
                    args=(int(data.decode()),)
                )
        else:
            print("Connection closed")
            break

def update_received_data(state: State, val):
    state.received_data = val
    
# ------------------------------
# Main app
# ------------------------------

def create_page():
    import taipy.gui.builder as tgb

    with tgb.Page() as page:
        tgb.text("Receiver", mode="md", class_name="text-center pb1")
        tgb.text("{received_data}", mode="md", class_name="text-center pb1")
        
    return page
    

if __name__ == "__main__":
    received_data = 98

    page = create_page()
    gui = Gui(page=page)

    t = Thread(
        target=client_handler,
        args=(
            gui,
            state_id_list,
        ),
    )
    t.start()

    gui.run(title="Receiver Page")