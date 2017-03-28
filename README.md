# FPH
## Why FPH?
Existing approaches to feature interaction detection require a fixed order in which the features are to be composed but do not provide guidance on how to define this order or how to determine a relative order of a newly-developed feature w.r.t.existing ones.
We argue that classic feature non-commutativity analysis, i.e., when an order of composition of features affects properties of interest, can be used to complement feature interaction detection to help build orders between features and determine many interactions.  To this end, we develop and evaluate Mr. Feature Potato Head (FPH) -- a modular approach to non-commutativity analysis that does not rely on temporal properties and applies to systems expressed in Java.  Our experiments running FPH on 29 examples show its efficiency and effectiveness.

## Replication Instructions
### Running environment
64bit - Ubuntu 16.04

### Note
The input in “CaseStudySystems_java_replication.zip” contains the systems from SPLVerifier and FeatureHouse with the information about the separated features.

### Setting up the environment
- Setting the file system
  - Extract “CaseStudySystems_java_replication.zip” into some folder (path)
  - Copy “soot-types.jar” to some folder (pathSoot)
  - Copy “FPH.py” to some folder (FPHLocation)
  - Choose output directory (outputPath)
- Configuring
  - Edit the first three assignments in  "FPH.py" according to (path), (pathSoot) and (outputPath)
- Executing
  - Run python FPH.py
  
### Output
  For each system [s]:
  * "interactions_[s].txt" contains the information of the non-commutative pairs and the reason.
  * "summaryPerPair_[s].txt" contains for each pair of features whether an interaction was found and the time to reach the conclusion.
  
  * “numChecks.txt” contains for each system the number of “shared location” checks, the number of “behaviour preservation” checks, and the number of “shared variable” checks.
  * “timeTaken.txt” contains a summary of “summaryPerPair_*.txt
