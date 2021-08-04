# Ion-Ion scripts

1. Generate ion pairs using `a1-make_ion_pairs.sh ion-ion [ion-ion ...]`
2. Upload ions to TSCC
3. Use `submit_many_charges.sh ion-ion [ion-ion ...]` to submit your charge transfer check jobs to TSCC
4. Use `submit_many_testset.sh ion-ion [ion-ion ...]` to submit your testset jobs to TSCC
5. Use `submit_many.sh ion-ion [ion-ion ...]` to submit your reference energy jobs to TSCC
6. Download ions from TSCC
7. Collect charges using `a2-collect-charges.sh ion-ion [ion-ion ...]`
8. Generate training and test sets from data using `a3-collect_ts.sh ion-ion [ion-ion ...]`. This will also generate a plot of the interaction energies.
9. Ensure that the basis sets you are using are implemented in `../gaussian_basis_sets/` and optionally with their accompanied pseudopotential.
10. Calculate the c6 values using `a4-calculate_c6.sh ion-ion [ion-ion ...]`. Note that these are in bohr^6 * hartree 
11. Generate and perform fits using `a5-do_fitting.sh ion-ion [ion-ion ...]`. This will perform MB, MB_overTTM, and TTM fits.
12. Implement each fit into MBX-tmp using `a6-do_implementation`. Manual instructions are located in testMBX/README. In addition to comparing the script's output, you should also verify that all the files within MBX are as expected.
13. Commit your changes to a temp branch and push to Github
