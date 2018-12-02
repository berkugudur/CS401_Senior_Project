# CS401 Senior Project

This repository includes our working for our senior project.

- You can find our neural network tests & implementations in the notebooks folder
  - Datas can be found in /data directory.
  - Models and other necassary saving files can be found in /out directory.
  - Tensorboard logs can be found in logs folder.
- Util package currently has csv exporter and ai - game connection objects.
  - AIConnection directory responsible for using our neural network implementation with the FightingICE game that written in Java.
  - Csv exporter is implemented for converting json files to csv files. While we 
  converting them to csv we will remove some unneeded frames for better results.


### Prerequisites

You have to install libraries using pip with the requirements file. 

```
pip install -r requirements.txt
```

Besides of these libraries you have to install [Jupyter Notebook](http://jupyter.org/install.html) for using notebooks.

