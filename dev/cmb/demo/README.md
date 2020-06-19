# Demo

Here is a demo of an "end-to-end workflow" using our current progress with CMB
and ipyparaview

1. Create the SMTK resource files by running `sh ./make_resources.sh`
    - This will create SMTK resources of out templates filled out for showcasing in CMB
    - generate subdirectories of each of the demos
    - generates the needed XML input to ATS
    - the model/mesh files will not be there though :(
3. Run any one of the demos with the `run-ats.sh` script giving the demo directory as an argument
    - This will run ATS with the XML input file in that directory and save the results under a new `sim_dump` subdirectory
4. Launch the `ipp` docker via:
    - `docker run -p 8877:8877 -v $PWD:/root/ipyparaview/notebooks/ats-demo ipp2`
    - Launch the `post-vis.ipynb` notebook and change the demo directoy to point at the right data. The notebook will handle the rest.
