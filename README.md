# Smoothed Particle Hydrodynamics (SPH) via Inductiva API

[**Inductiva API**](https://github.com/inductiva/inductiva/tree/main) empowers users to run large-scale simulations. With a simple interface, users have access to several simulators and features that help manage complex simulation workflows. 

Here, we explore Smoothed Particle Hydrodynamics (SPH) with two simulators available via **Inductiva API** - [SplishSplash](https://github.com/inductiva/inductiva/wiki/SPlisHSPlasH) and [DualSPHysics](https://github.com/inductiva/inductiva/wiki/DualSPHysics). 

In this repository, we make a tour of **Inductiva API**:
- [Create a scenario](scenario/README.md);
- [Generate a dataset via scenario](dataset/README.md).

### Install

To start experimenting with these scenarios you need to clone the public GitHub repository

```bash
git clone https://github.com/inductiva/inductiva-sph-demos.git
```

and install the `inductiva` package and other extra dependencies that are useful for this scenario.

Install `inductiva` package:
```bash
pip install inductiva
```

Install extra dependencies from within the `inductiva-sph-demos`:
```bash
pip install -r requirements.txt
```

To further learn about the `inductiva` package, check the [Inductiva API documentation](https://github.com/inductiva/inductiva/wiki).
