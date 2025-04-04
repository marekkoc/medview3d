

# MedView3D Installation Guide

## Creating the Conda Environment

To set up the MedView3D application, follow these steps:

1. Ensure you have Anaconda or Miniconda installed on your system.

2. Download the `environment.yml` file to your computer.

3. Open a terminal or command prompt.

4. Navigate to the directory containing the `environment.yml` file.

5. Create the conda environment by running:
   ```
   conda env create -f environment.yml
   ```

6. Activate the newly created environment:
   ```
   conda activate medview3d
   ```

7. Run the application:
   ```
   python medview3d.py
   ```

## Requirements

The application requires:
- Python 3.8
- PyQt5
- Matplotlib 3.5.1
- NumPy 1.20
- NiBabel 3.2
- SciPy 1.8
- scikit-image 0.19

All dependencies will be automatically installed when creating the environment from the provided YAML file.
