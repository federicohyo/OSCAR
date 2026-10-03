Tool requirements
-----------------

OpenPDKs need to be installed and PDK\_ROOT and PDK need to be set.  Klayout and magic are also required (should be available already from the analog flow)

Yosys is needed, a pre-built copy is available from https://github.com/YosysHQ/oss-cad-suite-build

OpenROAD binary install from https://github.com/Precision-Innovations/OpenROAD/releases

A copy of the OpenROAD-flow-scripts needs to be available https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts


Tool settings
-------------

To run on our servers (currently only co28 is supported), set up the following environment variables


```
export OPENROAD_EXE=`which openroad`
export YOSYS_CMD=`which yosys`
export PDK_ROOT=/opt/shared/avlsi-tools/share/pdk
export PDK=sky130A
export FLOW_HOME=/opt/shared/avlsi-tools/share/OpenROAD-flow-scripts/flow
```

Running synthesis
-----------------

To run synthesis, change your shell into the directory that contains this readme and run `make`

By default this will the onehot2bin design, to select another design run `make DESIGN_CONFIG=bin2onehot/config.mk`

To clean out previous synthesis results for the currently selected target, run `make clean_all`
