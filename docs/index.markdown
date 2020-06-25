---
layout: home

# Hero Section
# include located in /_includes/hero.html
title: Welcome
subtitle: Increase scientific productivity by providing HPC capable pre-and-post processing for easier and faster turnaround and integration with modern and next-generation simulation systems.
hero_image: assets/img/hero_placeholder.png

hero_links:
  - text: View on GitHub
    icon: github
    url: https://github.com/Kitware/resonanthpc
    class: is-primary is-outlined is-inverted

# About Section
# include located in /_includes/home-about.html
about-heading: HPC-Enabled Pre- and Post-Processing with Jupyter
about-text: ResonantHPC is designed to increase scientific productivity by providing HPC capable pre-and-post processing for easier and faster turnaround and integration with modern and next-generation simulation systems. This system will extend the standard scientific computing environment (Jupyter) so that researchers can prepare, execute, and analyze the results of remote exascale-level simulation from their workstations.

about-features:
  - name: Data Integration
    description: Provide a data integration module that enables pulling data from heterogeneous sources as well as running required preprocessing.
    icon: /assets/img/custom-icons/icon_data_integration.svg
  - name: Modeling Interface
    description: Include a modeling interface that enables the user to generate an input mesh (through the execution of an external mesher) and to associate additional attributes to mesh elements.
    icon: /assets/img/custom-icons/icon_modeling_interface.svg
  - name: User Interface
    description: Enable, through a simple user interface, the execution and monitoring of HPC jobs such as preprocessing, simulation and visualization modules.
    icon: /assets/img/custom-icons/icon_user_interface.svg
  - name: Analysis Module
    description: Incorporate a leading parallel analysis and visualization module.
    icon: /assets/img/custom-icons/icon_analysis_module.svg
  - name: Web App
    description: Run inside a web browser and provide both user interface and scripting access to its functionality.
    icon: /assets/img/custom-icons/icon_web_app.svg

# Utilized Software Section
# include located in /_includes/home-software.html
software-heading: Software we are utilizing
software-text: We are utilizing some opensource software that helps us add functionality and increase project’s efficiency.

utilized-software:
  - name: ParaView
    logo: /assets/img/logos/ParaView_Logo.svg
    github-link: https://gitlab.kitware.com/paraview/paraview
    website-link: https://www.paraview.org/
  - name: Amanzi and ATS
    logo: /assets/img/logos/amanzi_ats_logo.png
    github-link: https://github.com/amanzi/ats
    website-link: https://amanzi.github.io/
  - name: CMB
    logo: /assets/img/logos/cmb_logo.png
    github-link: https://gitlab.kitware.com/cmb/cmb
    website-link: https://www.computationalmodelbuilder.org/
  - name: LaGriT
    logo: /assets/img/logos/lagrit_logo.png
    github-link: https://github.com/lanl/LaGriT
    website-link: https://lagrit.lanl.gov/
  - name: Project Jupyter
    logo: /assets/img/logos/jupyter_logo.svg
    github-link: https://github.com/jupyter
    website-link: https://jupyter.org/
  - name: SMTK
    logo: /assets/img/logos/smtk_logo_mark.png
    github-link: https://gitlab.kitware.com/cmb/smtk
    website-link: https://smtk.readthedocs.io/en/latest/

# Associated Repositories Section
# include located in /_includes/home-repos.html
repos-background: /assets/img/repos_section_bg.jpg
repos-heading: Associated GitHub repositories
repos-text: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore

repos:
  - title: ResonantHPC
    description: HPC pre/post processing for easier and faster integration with modern simulation systems
    link: https://github.com/Kitware/resonanthpc
  - title: iPyParaView
    description: A widget for interactive server-side ParaView rendering.
    link: https://github.com/Kitware/ipyparaview

# Associated Repositories Section
# include located in /_includes/home-repos.html
collab-heading: Our Collaborators
collab-text: We are proud to collaborate with researchers from prestigious organizations.

collaborators:
  - name: Lawrence Berkeley National Laboratory
    link: https://www.lbl.gov/
    logo: /assets/img/collaborators/berkeley_lab_logo.png
  - name: Los Alamos National Laboratory
    link: https://www.lanl.gov/
    logo: /assets/img/collaborators/los_alamos_logo.svg
  - name: Kitware, Inc.
    link: https://kitware.com
    logo: /assets/img/collaborators/kw_logo.svg
---
