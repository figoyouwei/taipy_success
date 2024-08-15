'''
@author: Youwei Zheng
@target: Job Execution mode
@source: https://docs.taipy.io/en/develop/tutorials/scenario_management/5_job_execution/
@update: 2024.08.15
'''

import time

import taipy as tp
from taipy.core.config import Config

# Normal function used by Taipy
def double(nb):
    return nb * 2

def add(nb):
    print("Wait 5 seconds in add function")
    time.sleep(5)
    return nb + 10

if __name__=="__main__":
    # ------------------------------
    # configure scenario
    # ------------------------------

    # configure job execution mode
    Config.configure_job_executions(
        mode="standalone", 
        max_nb_of_workers=2
        )

    data_in = 8

    # Configuration of Data Nodes
    input_node = Config.configure_data_node("data_in")
    intermediate_node = Config.configure_data_node("intermediate")
    output_node = Config.configure_data_node("data_out")

    # Configuration of tasks
    first_task_cfg = Config.configure_task(
        "double",
        double,
        input_node,
        intermediate_node
        )

    second_task_cfg = Config.configure_task(
        "add",
        add,
        intermediate_node,
        output_node
        )

    # Configuration of the scenario
    scenario_cfg = Config.configure_scenario(
        id="two_scenarios",
        task_configs=[
            first_task_cfg,
            second_task_cfg]
        )

    Config.export("config.toml")

    # ------------------------------
    # run scenario
    # ------------------------------

    tp.Core().run()

    # 1.create
    scenario_1 = tp.create_scenario(scenario_cfg)

    # 2.initialize input
    scenario_1.data_nodes['data_in'].write(data_in)
    scenario_1.data_nodes['data_in'].read()

    # 3.submit
    scenario_1.submit()

    # 4.output
    data_out = scenario_1.data_nodes['data_out'].read()
    print(data_out)
    
    tp.Core().stop()
