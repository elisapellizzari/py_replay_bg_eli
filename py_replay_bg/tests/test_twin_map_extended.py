import os
import numpy as np

from py_replay_bg.tests import load_test_data_extended, load_patient_info

from py_replay_bg.py_replay_bg import ReplayBG
from py_replay_bg.visualizer import Visualizer
from py_replay_bg.analyzer import Analyzer

def test_replay_bg():

    # Set verbosity
    verbose = True
    plot_mode = False

    # Set other parameters for twinning
    blueprint = 'multi-meal'
    save_folder = os.path.join(os.path.abspath(''))
    parallelize = True

    # load patient_info
    patient_info = load_patient_info()
    p = np.where(patient_info['patient'] == 1)[0][0]
    # Set bw and u2ss
    bw = float(patient_info.bw.values[p])
    u2ss = float(patient_info.u2ss.values[p])

    # Instantiate ReplayBG
    rbg = ReplayBG(blueprint=blueprint, save_folder=save_folder,
                   yts=5, exercise=False,
                   seed=1,
                   verbose=verbose, plot_mode=plot_mode)

    # Load data and set save_name
    data = load_test_data_extended(day=1)
    # Cut data up to 11:00
    data = data.iloc[0:348, :]
    # Modify label of second day
    data.loc[312, "cho_label"] = 'B2'

    save_name = 'data_day_' + str(1) + '_extended'

    print("Twinning " + save_name)

    # Run twinning procedure using also the burn-out period
    rbg.twin(data=data, bw=bw, save_name=save_name,
             twinning_method='map',
             parallelize=parallelize,
             u2ss=u2ss,
             extended=True,
             find_start_guess_first=False)

    # Cut data up to 4:00
    data = data.iloc[0:264,:]

    # Replay the twin with the data up to the start of the burn-out period
    replay_results = rbg.replay(data=data, bw=bw, save_name=save_name,
                                twinning_method='map',
                                save_workspace=True,
                                save_suffix='_twin_map_extended')

    # Visualize and analyze results
    Visualizer.plot_replay_results(replay_results, data=data)
    analysis = Analyzer.analyze_replay_results(replay_results, data=data)
    print('Fit MARD: %.2f %%' % analysis['median']['twin']['mard'])