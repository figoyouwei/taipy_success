'''
@author: Youwei Zheng
@target: scenarios with yfinance, run main?
@update: 2024.08.17
'''

import taipy as tp
from taipy.core.config import Config as tcc # TaipyCoreConfig

from app.tools import download_yfin, process_yfin

args_in = (
    '^SPX',
    '1d',
    '2024-08-01',
    '2024-08-15',    
    )

# tool verified
# df = download_yfin(args_in)

# Put the rest of your code in this "if"
if __name__ == "__main__":
    # Configure job execution mode
    tcc.configure_job_executions(mode="standalone", max_nb_of_workers=2)

    # Configuration of Data Nodes
    node_yfin_args_in = tcc.configure_data_node("node_yfin_args_in")
    node_yfin = tcc.configure_data_node("node_yfin")
    node_yfin_pcs = tcc.configure_data_node("node_yfin_pcs")

    # Configuration of tasks
    task_cfg_yfin = tcc.configure_task(
        id="task_yfin", function=download_yfin, input=node_yfin_args_in, output=node_yfin
    )
    task_cfg_yfin_pcs = tcc.configure_task(
        id="task_yfin_pcs", function=process_yfin, input=node_yfin, output=node_yfin_pcs
    )

    # Configuration of scenario
    scenario_cfg_yfin = tcc.configure_scenario(
        id="scenario_yfin", task_configs=[task_cfg_yfin, task_cfg_yfin_pcs]
    )

    # ------------------------------
    # run scenario
    # ------------------------------

    # Run core
    tp.Core().run()

    # 1.create
    scenario_yin = tp.create_scenario(scenario_cfg_yfin)

    # 2.initialize input
    scenario_yin.data_nodes["node_yfin_args_in"].write(args_in)
    # scenario_yin.data_nodes["node_yfin_args_in"].read()

    # 3.submit: error freeze_support()
    scenario_yin.submit(wait=True, timeout=120)
    data_out = scenario_yin.data_nodes["node_yfin_pcs"].read()
    print(data_out)

    tp.Core().stop()