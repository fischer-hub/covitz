<p align="center">  # RiskRanger :microbe:    <img src="data/riskranger_logo.jpeg" width="150"></p>


Repository containing the project 3 of the sc2 analysis workshop.

![couldn't load title image](data/flowchart.png "Standard workflow figure.")

# getting started
First clone this repository recursively since the pipeline relies on tools like `CovSonar` and the `SARS2-RBD-escape-calculator` like this:
```
git clone --recurse-submodules https://github.com/fischer-hub/covvitz.git
```

# running the pipeline
To start the pipeline change into the project directory and run the follwing command in your terminal:
```
cd covvitz
nextflow riskranger.nf -profile conda,local
```

This will run the pipeline with all default parameters on the provided test data that can be found in the `data/` directory of the project.


<p align="center">
    <img src="data/riskranger_logo2.png" width="300">
</p>
