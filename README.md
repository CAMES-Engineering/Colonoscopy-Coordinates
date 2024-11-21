```
# Colonoscope Coordinates Dataset

## Overview

Colonoscopy is a endoscopic technique of the large bowel, many AI solutions exists for the imaging part. However, until now, no publicly available database has existed that includes the colonoscope’s spatial coordinates, allowing for mapping with timestamps to trace the colonoscope path through the colon over the procedure.

The colonoscope contains electromagnetic coils that provide position data through magnetic endoscopic imaging. Such data have previously been used to develop the Colonoscopy Retraction Score (which correlates with the adenoma detection rate) and the Colonoscopy Progression Score (which correlates with patient-experienced pain).

In this repository, we provide code examples to a dataset consisting of:

- **1399 Clinical Colonoscopies**: Real-world data from clinical procedures.
- **100 Simulated Colonoscopies**: Standardized data from a simulated environment.

These data are freely available to researchers and developers at [DOI DATA]. Potential applications include:

- Mapping the inspection of the colon.
- Defining and tracking typical motion patterns.
- Generating heatmaps to ensure equally distributed inspection.

## Contents

This repository contains code examples for utilizing the dataset effectively. Some key applications of the dataset include:

- **Colonoscope Path Mapping**: Visualizing the movement of the colonoscope through the colon over time.
- **Heatmap Generation**: Creating heatmaps to visualize coverage of the colon during endoscopy

## Dataset Description
See [DOI] and [DOI Data]
- **Clinical Colonoscopies**: 1400 procedures, including timestamped coordinate data for mapping the colonoscope path in real-world settings.
- **Simulated Colonoscopies**: 100 procedures from a standardized simulated environment, providing a controlled reference for analysis and development.


## Getting Started

1. **Clone this repository**: 
   ```sh
   git clone https://github.com/CAMES-Engineering/Colonoscopy-Coordinates
   ```
2. **Access the dataset**: Download the dataset from [DOI DATA] and place it in the [appropriate folder].
3. **Run the examples**: Use the provided code to explore how to start working with the dataset.

## Examples

- **Path Visualization**: 
  - Scripts to visualize the colonoscope's path and annotate points of interest.
- **Retraction and Progression Scoring**: 
  - Examples of calculating the Colonoscopy Retraction Score and Colonoscopy Progression Score.
- **Heatmap Generation**: 
  - Tools to create inspection heatmaps for assessing procedural coverage.

## Usage

The examples in this repository aim to help users familiarize themselves with the dataset and inspire new ways to leverage these data. Contributions and suggestions for further development are welcome.

## Contributing

If you wish to contribute to this project, feel free to fork this repository and submit pull requests. We welcome improvements, new features, and additional analyses.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

We would like to thank the clinicians and patients who made this work possible. 

## Contact

For more information or inquiries, please [DOI publication]

We would be grateful if you cited the [DOI publication] when using the code or/and dataset

```

