# UV Vis Absorption Spectrum

Written by Rob Parrish

This script reads TeraChem TDDFT and/or FOMO output files and automatically plots absorption spectra.

Each individual excited state is given a color, with the overall spectrum plotted in black on top.

The script includes options to plot with Lorentzian or Gaussian broadening. To change it, modify the ```plot_spectra``` function to change:

```Ostate += spectrum[state, 1] * lorentzian(E, spectrum[state, 0], delta)```

to 

```Ostate += spectrum[state, 1] * gaussian(E, spectrum[state, 0], delta)```

It also includes options to plot in eV or nm, with ```plot_spectra``` or ```plot_spectra_nm``` respectively.

Modify the following code block with appropriate paths for your system, choice of fomo or tddft for ```read_*_output```, and choice of eV of nm for ```plot_*```.  

```
filenames = glob.glob("/path/to/*/filename*.out")
spectra = [read_fomo_outfile(x) for x in filenames]
spectra = [x for x in spectra if x is not None]
plot_spectra("spectra.pdf", spectra, E=np.linspace(5.0, 9.0, 1000), delta=0.10)
```

