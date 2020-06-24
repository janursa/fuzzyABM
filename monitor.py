import sys
sys.path.insert(1,'/Users/matin/Downloads/testProjs/realtime_monitoring')
from realtime import monitor
settings = {
    "Medium": {
            "graph_dir" : "/Users/matin/Downloads/testProjs/ABM/build/outputs/scatter3.csv",
            "graph_type" : 'scatter3',
            "graph_size" : 800
           },
    "Cell counts": {
            "graph_dir" : "/Users/matin/Downloads/testProjs/ABM/build/outputs/agents_traj.csv",
            "graph_type" : 'lines',
            'x-axis-moves': False
           },
   "pH": {
		    "graph_dir" : "/Users/matin/Downloads/testProjs/ABM/build/outputs/pH.csv",
		    "graph_type" : 'lines',
		    'x-axis-moves': False
		   },
    "lactate": {
        "graph_dir" : "/Users/matin/Downloads/testProjs/ABM/build/outputs/lactate.csv",
        "graph_type" : 'lines',
        'x-axis-moves': False
       }

}
monitor.watch(settings).run()