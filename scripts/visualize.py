import sys
sys.path.insert(1,'/Users/matin/Downloads/testProjs/RTvisualize')
from realtime import monitor
settings = {
    "Cells": {
            "graph_dir" : "/Users/matin/Downloads/testProjs/fuzzyABM/build/outputs/single/scatter3.csv",
            "graph_type" : 'scatter3',
            "graph_size" : 800
           },
    "BMP2": {
            "graph_dir" : "/Users/matin/Downloads/testProjs/fuzzyABM/build/outputs/single/BMP.csv",
            "graph_type" : 'lines',
            'x-axis-moves': False
           },
    "TGF-b": {
            "graph_dir" : "/Users/matin/Downloads/testProjs/fuzzyABM/build/outputs/single/TGF.csv",
            "graph_type" : 'lines',
            'x-axis-moves': False
           },
    # "agents_traj": {
    #         "graph_dir" : "/Users/matin/Downloads/testProjs/fuzzyABM/build/outputs/single/agents_traj.csv",
    #         "graph_type" : 'lines',
    #         'x-axis-moves': False
    #        },
   # "pH": {
		 #    "graph_dir" : "/Users/matin/Downloads/testProjs/ABM/build/outputs/pH.csv",
		 #    "graph_type" : 'lines',
		 #    'x-axis-moves': False
		 #   },
   #  "lactate": {
   #      "graph_dir" : "/Users/matin/Downloads/testProjs/ABM/build/outputs/lactate.csv",
   #      "graph_type" : 'lines',
   #      'x-axis-moves': False
   #     }

}
monitor.watch(settings).run()