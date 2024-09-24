'''
@author: Youwei Zheng
@target: Helloworld example of Taipy scheduler
@update: 2024.09.24
'''

import taipy as tp
from taipy import Config, Core, Gui
import taipy.gui.builder as tgb

def build_message(name: str):
    return f"Hello {name}!"

# Input node
name_data_node_cfg = Config.configure_data_node(
    id="input_name", default_data="Figo"
)

# Output node
message_data_node_cfg = Config.configure_data_node(id="message")

# Task node
build_msg_task_cfg = Config.configure_task(
    id="build_msg", 
    function=build_message, 
    input=name_data_node_cfg, 
    output=message_data_node_cfg
)

scenario_cfg = Config.configure_scenario("scenario", task_configs=[build_msg_task_cfg])

data_node = None

# Note: Create page to display the completion of scenario
with tgb.Page() as page:
    tgb.job_selector()
    # with tgb.layout("30 70", columns__mobile="1"):
    #     tgb.scenario_selector("{scenario}")
    #     tgb.scenario("{scenario}")
    with tgb.layout("30 70", columns__mobile="1"):
        tgb.data_node_selector("{data_node}")
        tgb.data_node("{data_node}")

if __name__ == "__main__":
    core = Core()
    gui = Gui(page)
    core.run()

    # Create scenario object
    scenario = tp.create_scenario(config=scenario_cfg)

    # Every 10 seconds, submit the scenario
    tp.Scheduler.every(10).seconds.do(tp.submit, scenario)

    # Every 10 seconds, the scheduler will see if he has to submit the scenario
    tp.Scheduler().start(interval=5)
    gui.run()