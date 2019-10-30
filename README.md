# event_generation

library to simulate photon generation events from SPDC source on satellite, accounting for the losses and distortions that happen during transmission and detection at the ground station.

## basic distribution
- SPDC type-0, collinear, non-degenerate phase matching
- Poissonian

## losses (attenuation)
- atmospheric loss, diffraction loss, pointing loss
- dead time of passively quenched detectors (1us)
- low resolution of time stamp device => accidental coincidences where two uncorrelated pairs are generated within one coincidence time window
- adjustable in a range from 0 to 40 dB

## distortions
- clock drift 165us/s leads to dynamic time bin shift
- Doppler shift

