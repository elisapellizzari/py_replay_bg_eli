---
sidebar: auto
---
# Get started

## Installation

**ReplayBG** can be installed via pypi by simply 

```python
pip install py-replay-bg
```

### Requirements

* Python >= 3.11
* List of Python packages in `requirements.txt`

## Preparation: imports, setup, and data loading 

First of all import the core modules:
```python
import os
import numpy as np
import pandas as pd

from multiprocessing import freeze_support
```

Here, `os` will be used to manage the filesystem, `numpy` and `pandas` to manipulate and manage the data to be used, and
`multiprocessing.freeze_support` to enable multiprocessing functionalities and run the twinning procedure in a faster,
parallelized way. 

Then, we will import the necessary ReplayBG modules:
```python twoslash
from py_replay_bg.py_replay_bg import ReplayBG
from py_replay_bg.visualizer import Visualizer
from py_replay_bg.analyzer import Analyzer
```

Here, `ReplayBG` is the core ReplayBG object (more information in the [The ReplayBG Object](./replaybg_object.md) page),
while `Analyzer` and `Visualizer` are utility objects that will be used to
respectively analyze and visualize the results that we will produce with ReplayBG
(more information in the ([Visualizing Replay Results](./visualizing_replay_results.md) and
 [Analyzing Replay Results](./analyzing_replay_results.md) pages).

Next steps consist of setting up some variables that will be used by ReplayBG environment. 
First of all, we will run the twinning procedure in a parallelized way so let's start with:
```python
if __name__ == '__main__':
    freeze_support()
```

Then, we will set the verbosity of ReplayBG:
```python
    verbose = True
    plot_mode = False
```
 
Then, we need to decide what blueprint to use for twinning the data at hand. 
```python
    blueprint = 'multi-meal'
    save_folder = os.path.join(os.path.abspath(''),'..','..','..')
    parallelize = True
```

For more information on how to choose a blueprint, please refer to the [Choosing Blueprint](./choosing_blueprint.md) page.

Now, let's load some data to play with. In this example, we will use the data stored in `example/data/data_day_1.csv` 
which contains a day of data of a patient with T1D:

```python
data = pd.read_csv(os.path.join(os.path.abspath(''), '..', 'data', 'data_day_1.csv'))
data.t = pd.to_datetime(data['t'])
```

::: warning 
Be careful, data in PyReplayBG must be provided in a `.csv.` file that must follow some strict requirements. For more 
information see the [Data Requirements](./data_requirements) page.
:::

Let's also load the patient information (i.e., body weight and basal insulin `u2ss`) stored in the `example/data/patient_info.csv` file.

```python
patient_info = pd.read_csv(os.path.join(os.path.abspath(''), '..', 'data', 'patient_info.csv'))
p = np.where(patient_info['patient'] == 1)[0][0]
# Set bw and u2ss
bw = float(patient_info.bw.values[p])
u2ss = float(patient_info.u2ss.values[p])
```

Finally, instantiate a `ReplayBG` object:

```python
rbg = ReplayBG(blueprint=blueprint, save_folder=save_folder,
               yts=5, exercise=False,
               seed=1,
               verbose=verbose, plot_mode=plot_mode)

```

## Step 1: Creation of the digital twin

To create the digital twin, i.e., run the twinning procedure, using the MCMC method, use the `rbg.twin()` method:

```python
rbg.twin(data=data, bw=bw, save_name='data_day_1',
         twinning_method='mcmc',
         parallelize=parallelize,
         n_steps=5000,
         u2ss=u2ss)
```

For more information on the twinning procedure see the [Twinning Procedure](./twinning_procedure.md) page.


## Step 2: Run replay simulations

Now that we have the digital twin created, it's time to replay using the `rbg.replay()` method. For more details 
see the [Replaying](./replaying.md) page.

The possibilities are several, but for now let's just see what happens if we run a replay using the same input data used for twinning:

```python
replay_results = rbg.replay(data=data, bw=bw, save_name='data_day_1',
                            twinning_method='mcmc',
                            save_workspace=True,
                            u2ss=u2ss,
                            save_suffix='_step_2a')
```

It is possible to visualize the results of the simulation using:

```python
Visualizer.plot_replay_results(replay_results, data=data)
```

and analyzing the results using: 

```python
analysis = Analyzer.analyze_replay_results(replay_results, data=data)
print('Fit MARD: %.2f %%' % analysis['median']['twin']['mard'])
print('Mean glucose: %.2f mg/dl' % analysis['median']['glucose']['variability']['mean_glucose'])
```

As a second example, we can simulate what happens with different inputs, for example when we reduce insulin by 30%.
To do that run:

```python
data.bolus = data.bolus * .7
replay_results = rbg.replay(data=data, bw=bw, save_name=save_name,
                            twinning_method='mcmc',
                            save_workspace=True,
                            save_suffix='_step_2b')

# Visualize results
Visualizer.plot_replay_results(replay_results)
# Analyze results
analysis = Analyzer.analyze_replay_results(replay_results)

# Print, for example, the average glucose
print('Mean glucose: %.2f mg/dl' % analysis['median']['glucose']['variability']['mean_glucose'])
```

## Full example

A `.py` file with the full code of the get started example can be found in `example/code/get_started.py`.

```python
import os
import numpy as np
import pandas as pd

from multiprocessing import freeze_support

from py_replay_bg.py_replay_bg import ReplayBG
from py_replay_bg.visualizer import Visualizer
from py_replay_bg.analyzer import Analyzer


if __name__ == '__main__':
    freeze_support()

    # Set verbosity
    verbose = True
    plot_mode = False

    # Set other parameters for twinning
    blueprint = 'multi-meal'
    save_folder = os.path.join(os.path.abspath(''),'..','..','..')
    parallelize = True
    
    # Load data
    data = pd.read_csv(os.path.join(os.path.abspath(''), '..', 'data', 'data_day_1.csv'))
    data.t = pd.to_datetime(data['t'])
    
    # Load patient_info
    patient_info = pd.read_csv(os.path.join(os.path.abspath(''), '..', 'data', 'patient_info.csv'))
    p = np.where(patient_info['patient'] == 1)[0][0]
    # Set bw and u2ss
    bw = float(patient_info.bw.values[p])
    u2ss = float(patient_info.u2ss.values[p])
    
    # Instantiate ReplayBG
    rbg = ReplayBG(blueprint=blueprint, save_folder=save_folder,
                   yts=5, exercise=False,
                   seed=1,
                   verbose=verbose, plot_mode=plot_mode)

    # Set save name
    save_name = 'data_day_1'

    # Step 1. Run twinning procedure
    rbg.twin(data=data, bw=bw, save_name=save_name,
             twinning_method='mcmc',
             parallelize=parallelize,
             n_steps=5000,
             u2ss=u2ss)

    # Step 2a. Replay the twin with the same input data
    replay_results = rbg.replay(data=data, bw=bw, save_name=save_name,
                                twinning_method='mcmc',
                                save_workspace=True,
                                save_suffix='_step_2a')

    # Visualize results and compare with the original glucose data
    Visualizer.plot_replay_results(replay_results, data=data)
    # Analyze results
    analysis = Analyzer.analyze_replay_results(replay_results, data=data)
    # Print, for example, the fit MARD and the average glucose
    print('Fit MARD: %.2f %%' % analysis['median']['twin']['mard'])
    print('Mean glucose: %.2f mg/dl' % analysis['median']['glucose']['variability']['mean_glucose'])

    # Step 2b. Replay the twin with different input data (-30% bolus insulin) to experiment how glucose changes
    data.bolus = data.bolus * .7
    replay_results = rbg.replay(data=data, bw=bw, save_name=save_name,
                                twinning_method='mcmc',
                                save_workspace=True,
                                save_suffix='_step_2b')

    # Visualize results
    Visualizer.plot_replay_results(replay_results)
    # Analyze results
    analysis = Analyzer.analyze_replay_results(replay_results)

    # Print, for example, the average glucose
    print('Mean glucose: %.2f mg/dl' % analysis['median']['glucose']['variability']['mean_glucose'])
```
