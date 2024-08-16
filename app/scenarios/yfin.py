'''
@author: Youwei Zheng
@target: scenarios with yfinance
@update: 2024.08.16
'''

import taipy as tp
from taipy.core.config import Config as tcc # TaipyCoreConfig

from app.tools import download_yfin

args_in = (
    '^SPX',
    '1d',
    '2024-08-01',
    '2024-08-15',    
    )

# tool verified
df = download_yfin(args_in)

# Configure job execution mode
tcc.configure_job_executions(
    mode="standalone", 
    max_nb_of_workers=2
    )

# Configuration of Data Nodes
node_yfin_args_in = tcc.configure_data_node("node_yfin_args_in")
node_yfin = tcc.configure_data_node("node_yfin")

# Configuration of tasks
task_cfg_yfin = tcc.configure_task(
    id="task_yfin",
    function=download_yfin,
    input=node_yfin_args_in,
    output=node_yfin
    )

# Configuration of scenario
scenario_cfg_yfin = tcc.configure_scenario(
    id="scenario_yfin",
    task_configs=[task_cfg_yfin]
    )

# ------------------------------
# run scenario
# ------------------------------

# Run core
tp.Core().run()

# 1.create
scenario_yin = tp.create_scenario(scenario_cfg_yfin)

# 2.initialize input
scenario_yin.data_nodes['node_yfin_args_in'].write(args_in)
scenario_yin.data_nodes['node_yfin_args_in'].read()

# 3.submit: error freeze_support()
scenario_yin.submit(wait=True, timeout=120)
data_out = scenario_yin.data_nodes['node_yfin'].read()
print(data_out)

tp.Core().stop()