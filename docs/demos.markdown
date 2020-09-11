---
layout: page

# Hero Section
# include located in /_includes/hero.html
title: Demos
permalink: /demos/
breadcrumbs: true
hero_image: /assets/img/page_hero_placeholder.jpg

# Demos
# included in /_layouts/page.html
demos:
  - name: Richard's Steady State
    description: |
      <code class="language-plaintext highlighter-rouge">demo-01/demo.01.smtk</code>: This is a simple verticle, pseudo-1D column of water with a water table below the surface. It solves the pressure to steady-state. For constant density and incompressible solid, this would be a linear pressure profile, but we include a pressure-dependent density.
    image: /assets/img/demos/01-regions.png
    git_link: https://github.com/amanzi/ats-demos/blob/master/01_richards_steadystate/richards_steadystate.xml

  - name: Richard's Infiltration
    description: |
      <code class="language-plaintext highlighter-rouge">demo-02/demo.02.smtk</code>: This is a single column of cells, oriented vertically, and initialized as the hydrostatic solution. Infilitration is turned on to lower the water table.
    image: /assets/img/demos/02-bc.png
    git_link: https://github.com/amanzi/ats-demos/blob/master/02_richards/richards-infiltration.xml

  - name: Surface Water
    description: |
      <code class="language-plaintext highlighter-rouge">demo-03/demo.03.smtk</code>: This is a simple 1D ramp on which add a rain water mass source.
    image: /assets/img/demos/03-mass-source.png
    git_link: https://github.com/amanzi/ats-demos/blob/master/03_surface_water/surface_water.xml

  - name: Integrated Hydro V
    description: |
      <code class="language-plaintext highlighter-rouge">demo-04/demo.04.smtk</code> and <code class="language-plaintext highlighter-rouge">demo-04/att.demo.04.mesh.smtk</code>: We rain on a V-catchment in 2D, allowing the water to pond. This demonstrates that water runs downhill (in a coupled environment). Plot shows saturation.
    image: /assets/img/demos/04-v-animation.gif
    git_link: https://github.com/amanzi/ats-demos/blob/master/04_integrated_hydro/integrated_hydro-v.xml

---

We have curated a few demos to show off our work building a front-end user
interface for creating ATS input decks. Each of our demos are available under
the `demos-vX.Y.Z.zip` asset on our [releases page](https://github.com/Kitware/resonanthpc/releases/).

Please follow the [Getting Started](../getting-started/) guide to download
Computational Model Builder (CMB) and the download the demos asset from the
latest release before proceeding.

In the posts below, each demo will first list the file name of the prefilled
templates for that demo. Load the prepoluated forms (`.smtk` resource files)
listed in each example.
