# Computational Intelligence, Final Project: Quarto Agents

| **Contributors** | **sID** |
|---|---|
| Alessio Carachino | s296138 |
| Giuseppe Atanasio | s300733 |
| Francesco Sorrentino | s301665 |
| Francesco Di Gangi | s301793 |

## Note
**ALL MEMBERS EQUALLY CONTRIBUTED TO THE PROJECT. FIRST EACH MEMBER MAINLY FOCUSED ON ONE IDEA AND THEN WE MERGED THE FINDINGS**

## Directory Tree

```
.
├── README.md
├── poetry.lock
├── pyproject.toml
└── quarto
    ├── GA_MinMaxPlayer.py
    ├── GA_Player.py
    ├── MinMax_Player.py
    ├── RandomPlayer.py
    ├── __init__.py
    ├── __pycache__
    │   ├── GA_MinMaxPlayer.cpython-310.pyc
    │   ├── GA_Player.cpython-310.pyc
    │   ├── MinMax_Player.cpython-310.pyc
    │   ├── RandomPlayer.cpython-310.pyc
    │   └── minimax.cpython-310.pyc
    ├── image.jpg
    ├── image2.jpg
    ├── main.py
    ├── main_RL.py
    ├── minimax.py
    ├── quarto
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   ├── __init__.cpython-310.pyc
    │   │   └── objects.cpython-310.pyc
    │   └── objects.py
    ├── readme.md
    └── reinforcement
        ├── Memory.py
        ├── Q_data_RL_GA.dat
        ├── __init__.py
        ├── images
        │   ├── RL&GA_vs_GA_2nd_test.svg
        │   ├── RL&GA_vs_GA_2nd_train.svg
        │   ├── RL&GA_vs_GA_eps0.95_alpha0.1_train.svg
        │   ├── RL&GA_vs_GA_eps0.995_alpha0.1_train.svg
        │   ├── RL&GA_vs_GA_eps0.995_alpha0.3_train.svg
        │   ├── RL&GA_vs_GA_eps0.9995_alpha0.1_train.svg
        │   └── RL&GA_vs_Random_2nd_test.svg
        ├── rl_agent.py
        ├── tables.py
        └── utils.py
```

## Setting up the environment
First of all you have to install `poetry` on your pc. Then, you have to move inside the "quarto_ci_2022_2023" folder and launch this command:
```
poetry install
```
After that, to test our code you have to launch the following:
```
poetry run python quarto/[main_RL or main].py
```
## Summary
- [GA Agent](#ga-agent)
- [MinMax](#minmax)
- [GA+MinMax Agent](#gaminmax-agent)
- [RL Agent](#rl-agent)
- [Conclusion](#conclusion)

## GA Agent

GA Agent is described in the `GA_Player.py` file. The file describes the agent using only the Genetic Algorithm strategy.

## MinMax

The main file for the **minmax** are: `minmax.py` and `MinMax_Player.py`. These files describe the two strategies using only MinMax.

## GA+MinMax Agent

GA+MinMax Agent is described in the file `GA_MinMaxPlayer.py`. This file describes the strategy used by our final agent: Genetic ALgorithm and MinMax.

## RL Agent
RL agent is developed between `rl_agent.py` and `main_RL.py`.

## Conclusion

The best strategy is to use the `GA_MinMaxPlayer.py`, that is the combination of MinMax and Genetic Algorithm. 
