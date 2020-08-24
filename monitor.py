import sys
sys.path.insert(1,'../realtime_visualization/')
from realtime import monitor
settings = {
    # "Medium": {
    #         "graph_dir" : "./build/outputs/scatter3.csv",
    #         "graph_type" : 'scatter3',
    #         "graph_size" : 800
    #        },
    "Cell counts": {
            "graph_dir" : "./build/outputs/agents_traj.csv",
            "graph_type" : 'lines',
            'x-axis-moves': False
           },
   "pH": {
		    "graph_dir" : "./build/outputs/pH.csv",
		    "graph_type" : 'lines',
		    'x-axis-moves': False
		   },
    "TGF": {
        "graph_dir" : "./build/outputs/TGF.csv",
        "graph_type" : 'lines',
        'x-axis-moves': False
       },
    "BMP": {
        "graph_dir" : "./build/outputs/BMP.csv",
        "graph_type" : 'lines',
        'x-axis-moves': False
       },
    "maturity": {
        "graph_dir" : "./build/outputs/maturity.csv",
        "graph_type" : 'lines',
        'x-axis-moves': False
       },
    "ALP": {
        "graph_dir" : "./build/outputs/ALP.csv",
        "graph_type" : 'lines',
        'x-axis-moves': False
       },
    "OC": {
        "graph_dir" : "./build/outputs/OC.csv",
        "graph_type" : 'lines',
        'x-axis-moves': False
       }

}
monitor.watch(settings).run()