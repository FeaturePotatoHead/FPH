# FPH
## Why use FPH?
Existing approaches to feature interaction detection require a fixed order in which the features are to be composed but do not provide guidance on how to define this order or how to determine a relative order of a newly-developed feature w.r.t.existing ones.
We argue that classic feature non-commutativity analysis, i.e., when an order of composition of features affects properties of interest, can be used to complement feature interaction detection to help build orders between features and determine many interactions.  To this end, we develop and evaluate Mr. Feature Potato Head (FPH) -- a modular approach to non-commutativity analysis that does not rely on temporal properties and applies to systems expressed in Java.  Our experiments running FPH on 29 examples show its efficiency and effectiveness.

## How to Use FPH?
FPH consists of a commutativity analysis on FPH features.

#### Input - FPH Features:
- Input: Text File containing the FPH representation of features

To transform the features we slightly modified the code provided by [FeatureHouse](http://www.infosun.fim.uni-passau.de/spl/apel/fh/) to extract only the information that is relevant to our technique.
The initial code of the systems we analyzed is provided by [FeatureHouse](http://www.infosun.fim.uni-passau.de/spl/apel/fh/).
We provide the output files of this process of the 29 systems we analyzed in FPH_input_systems.zip.

#### Commutativity Analysis:
