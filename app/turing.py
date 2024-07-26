'''
@author: Youwei Zheng
@target: Backend computation
@update: 2024.07.25
'''

from models import Level, Point

def compute_points(levels: Level) -> Point:
    # compute output values
    try:
        points_net = levels.target_level - levels.starting_level
        points_pct = (points_net / levels.starting_level) * 100
    except ZeroDivisionError:
        raise ValueError("Starting level cannot be zero.")

    # update output model
    points = Point(
        points_net=points_net,
        points_pct=points_pct
    )
    points.update()

    return points