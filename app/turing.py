'''
@author: Youwei Zheng
@target: Backend computation
@update: 2024.07.25
'''

def levels(starting_level, target_level):
    # Formula
    points_net = target_level - starting_level
    points_pct = ((target_level - starting_level) / starting_level) * 100

    # Formata
    points_net = "{:.2f}".format(points_net)
    points_pct = "{:.2f}".format(points_pct)
    
    return (points_net, points_pct)
