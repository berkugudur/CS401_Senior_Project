# This is the test for data for punching standing agent according to its hp.

- Standing agent is P1, we are learning P2 (P2 is human player).

- Some frames will be removed, there are frames that;
    - Both players standing.
    - Consecutive ones(If frame's action is same with previous frame, it will be removed).
    - If we are(P2) in RECOV frame(Since we don't make RECOV frames ourselves).
    
### Pre process data

- In the pre process phase, we remove P2's datas from training set in order to crate labels. Labels are just actions of P2.

- We calculate the distance for each coordinate axis. (x distance, y distance)

- We also make actions one-hot encoding. 

- One-hot encoding for inputs and labels are not same. For example, Dash action in the input may have encoding [0,1] while Dash action in the label have encoding [0, 0, 1, 0].

- Integer values normalized. (P1-HP, P2-HP, X-Distance, Y-Distance)

- <font color='green'>There must be mechanism for understanding is player closing or move away.</font>

- There is no test and validation set preparation. Data that gathered from different rounds can be used for this problem.

- After pre-process we just have <font color='red'>[P1-Action, P1-HP, P2-HP, X-Distance, Y-Distance] -> P2-Action</font>

### Neural Network Design

Our neural network has two hidden layers in this test. They has 12 and 8 neurons respectively.
