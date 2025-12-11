Lieke van Son (2022) - GW Landscape

"No peaks without valleys: The stable mass transfer channel for gravitational-wave sources in light of the neutron star-black hole mass gap"

Source: https://zenodo.org/records/7080725

Docs: https://compas.readthedocs.io/en/latest/pages/User%20guide/Program%20options/program-options-list-defaults.html

## Model Parameters

| Acronym | COMPAS Flag | Variations | Default | Definition |
|---|---|---|---|---|
| `beta` | `mass-transfer-fa` | 0, 0.25, 0.5, 0.75, 1.0 | 0.5 | Mass Transfer fraction accreted (beta). |
| `fcircum` | `mass-transfer-angular-momentum-fcircumb` | 0.0, 0.25, 0.5, 0.75, 1.0 |
| `zetaHG` | `zeta-radiative-giant-star` | 3.5, 4.5, 5.5, 6.0, 6.5 | 6.0 | Value of logarithmic derivative of radius with respect to mass, ζ for radiative-envelope giant-like stars (including Hertzsprung Gap (HG) stars).
| `fcore` | `core-mass-multiplier` | 0.8, 0.9, 1.0, 1.1, 1.2 |
| `remRx` | `remnant-mass-prescription` | FRYER2012, FRYER2022 | FRYER2012 | Remnant mass prescription. |
| `fmix` | `fryer-22-fmix` | 0.5, 0.7, 1.0, 1.4, 2.0, 2.8, 4.0 | 0.5 | Parameter describing the mixing growth time when using the 'FRYER2022' remnant mass prescription [Fryer et al., 2022].
| `SN` | `fryer-supernova-engine` | DELAYED, RAPID | DELAYED | Supernova engine type if using the remnant mass prescription from [Fryer et al., 2012].
