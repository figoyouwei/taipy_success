'''
@author: Youwei Zheng
@target: Scenario for Beginner with simple data node and task
@linked: https://docs.taipy.io/en/develop/tutorials/fundamentals/2_scenario_management_overview/
@update: 2024.08.12
'''

from taipy import Config
import taipy as tp
import pandas as pd
import datetime as dt

data = pd.read_csv(
    "https://raw.githubusercontent.com/Avaiga/taipy-getting-started-core/develop/src/daily-min-temperatures.csv"
    )

data

def predict_temperature(historical_temperature: pd.DataFrame, date_to_forecast: dt.datetime) -> float:
    print(f"Running baseline...")
    historical_temperature['Date'] = pd.to_datetime(historical_temperature['Date'])
    historical_same_day = historical_temperature.loc[
        (historical_temperature['Date'].dt.day == date_to_forecast.day) &
        (historical_temperature['Date'].dt.month == date_to_forecast.month)
    ]
    
    # simple take the mean of historical same day.
    return historical_same_day['Temp'].mean()

# ------------------------------
# Creating Scenario DAG
# Task consists of nodes and processors, while scenario contains tasks.
# ------------------------------

# Configuration of nodes
historical_temperature_cfg = Config.configure_data_node("historical_temperature")
date_to_forecast_cfg = Config.configure_data_node("date_to_forecast")
predictions_cfg = Config.configure_data_node("predictions")

# Configuration of tasks
task_predict_cfg = Config.configure_task(
    id="task_predict_temperature",
    function=predict_temperature,
    input=[historical_temperature_cfg, date_to_forecast_cfg],
    output=predictions_cfg
    )

# Configuration of scenario
scenario_cfg = Config.configure_scenario(
    id="scenario_predict_temperature",
    task_configs=[task_predict_cfg]
    )

def run_scenario():
    # Run of the Core
    tp.Core().run()

    # Creation of the scenario and execution
    scenario = tp.create_scenario(scenario_cfg)
    scenario.historical_temperature.write(data)
    scenario.date_to_forecast.write(dt.datetime.now())
    tp.submit(scenario)

    print("Value at the end of task", scenario.predictions.read())

def run_scenario_gui():
    # Run of the Core
    tp.Core().run()

    # Creation of the scenario and execution
    scenario = tp.create_scenario(scenario_cfg)
    scenario.historical_temperature.write(data)
    scenario.date_to_forecast.write(dt.datetime.now())
    tp.submit(scenario)
    
    import taipy.gui.builder as tgb

    def save(state):
        # write values of Data Node to submit scenario
        state.scenario.historical_temperature.write(data)
        state.scenario.date_to_forecast.write(state.date)
        state.refresh('scenario')
        tp.gui.notify(state, "s", "Saved! Ready to submit")

    date = None
    with tgb.Page() as scenario_page:
        tgb.scenario_selector("{scenario}")
        tgb.text("Select a Date")
        tgb.date("{date}", on_change=save, active="{scenario}")

        tgb.text("Run the scenario")
        tgb.scenario("{scenario}")
        tgb.scenario_dag("{scenario}")

        tgb.text("View all the information on your prediction here")
        tgb.data_node("{scenario.predictions}")

    tp.Gui(scenario_page).run()



if __name__ == "__main__":
    run_scenario_gui()