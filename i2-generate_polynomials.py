# The library that will enable the fitting generation and energy calculation
import mbfit
# Some other useful libraries
import os
import sys

cwd = os.getcwd()
if os.path.basename(cwd) == "scripts":
    os.chdir("../polynomials")
cwd = os.getcwd()
if os.path.basename(cwd) != "polynomials":
    sys.exit('Make sure to run this script either in the `script` or `polynomials` directory')

# Directory where the polynomials will be generated
poly_base_directory = "polynomial_generation"

# Degree of the polynomials
polynomial_order = 9 # MUST be the same as in template_2b_fitting.ipynb
with open(f"POLYNOMIAL ORDER: {polynomial_order}") as f:
    f.write(f"The polynomial order is {polynomial_order}. This should match that of template_2b_fitting.ipynb")

for sym in ['A1_A1','A1_B1']:
    poly_directory = f"{poly_base_directory}_{sym}"
    poly_in = f"{sym}_poly.in"
    dim_settings = f"{sym}_dimer_settings.ini"
    # help(mbfit.generate_polynomials)
    mbfit.generate_polynomials(dim_settings, poly_in, polynomial_order, 
                                        poly_directory, generate_direct_gradients=False)

    #### 4.8.3. Optimize the polynomial evaluation
    # help(mbfit.execute_maple)
    # will be used for ALL systems of same symmetry for consistency. Only generated once.
    mbfit.execute_maple(dim_settings, poly_directory)
