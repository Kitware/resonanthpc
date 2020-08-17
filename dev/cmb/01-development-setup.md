# ResonantHPC Development Setup

You can use Kitware's [Computational ModelBuilder](https://www.computationalmodelbuilder.org)
to develop ATS analyses and generate ATS input files. CMB modelbuilder is a
desktop application for simulation modeling and preprocessing. To configre CMB
modelbuilder for ATS, follow these steps:

* Clone the [ResonantHPC](https://github.com/Kitware/resonanthpc) repository,
  which provides ATS "workflow files" used by modelbuilder. The workflow
  files include XML templates that specify the user interface, and python
  scripts that generate ATS input files.
* Download and install CMB modelbuilder (described below).
* Initialize the ATS workflow files (described below).


## Download and install CMB modelbuilder

CMB modelbuilder release packages are generated nightly as part of Kitware's
softwar development process and uploaded to a public collection named
ComputationalModelBuilder on data.kitware.com. The are a number of different
directories underneath that collection. Users should navigate to the
(CMB-public/Nightly/MasterBranch)[https://data.kitware.com/#collection/58fa68228d777f16d01e03e5/folder/5980ed698d777f16d01ea0e8] folder, where packages are uploaded to
subdirectories listed by date code (YYYY-MM-DD). Select the most recent
directory and look for the download matching your system type, for example

```
modelbuilder-6.3.0-rc1-20200810-Linux-64bit.tar.gz
modelbuilder-6.3.0-rc1-20200810-OSX-64bit.dmg
modelbuilder-6.3.0-rc1-20200810-Windows-64bit.zip
```

Note that one or more package might be missing for a given date; in that case
look in the previous date(s).

To install, simply download and unzip the file. (There is no `setup.ext` or
other installer for windows, for example.) The macOS dmg file contains two
folders; you only need to copy the `modelbuilder 6.3.0` folder onto your file
system.


## Initialize ATS workflow files

Before running modelbuilder, you must first initialize the workflow files
in the resonanthpc repository. To do that you need the `pvpython` executable
that is included in the modelbuilder package.

* For linux and windows systems, the pvpython executable is in the bin
  directory
* For macOS, the pvpython executable is inside the modelbuilder.app
  package, at the path `Contents/bin/pvpython`.

1. Open a shell (terminal) and navigate to the `resonanthpc` repository,
then to the folder at `dev/cmb/simulation-workflows/ats/internal`.

2. From the subfolder run pvpython and pass in the `build_ats.py` script.

```
    <Path-To-PVPython> build_ats.py
```

3. That will generate and finalize the template files. (You can also use
`pvpython` to run the `run_unittest.py` script to verify things are ready.)

4. Once the template files are initialized, you should be able to run the
modelbuilder executable:

* `bin/modelbulder` on linux
* `modelbuilder.app` on macOS
* `bin/modelbuilder.exe` on Windows


## Platform-specific Notes

### Linux

The Linux modelbuilder package is built using CentOS 7. On some other linux
systems, including Ubuntu 16.04, you might see an error message on startup
like this:

    error while loading shared libraries: libcrypto.so.10: cannot open shared object file: No such file or directory

You can workaround this by deleting or moving files that match libcrypt*,
for example

    rm -f lib/libcrypt*

These crypto libraries are not needed to run modelbuilder on the desktop
(they are for connecting paraview to remote servers).


### macOS

Because the app is not signed, macOS might not give you permission to run the
app by double-clicking " modelbuilder.app" in Finder. If that occurs,
right-click on "modelbuilder.app" and select the "Open" menu item. In
response, macOS should display a pop-up window where you can chose to open
the application.

On some macOS systems, modelbuilder crashes the first time it is run.
The underlying cause is not fully understood but is related to the python
libraries internal to modelbuilder. Restarting the application has been
successful.


### Windows

The first time you run modelbuilder.exe, your system might display a
blue popup with the title "Windows protected your PC". This because
our packages are not signed with MicroSoft. You can proceed to run
modelbuilder by clicking the "More Info" link, which brings up a
"Run anyway" button.
