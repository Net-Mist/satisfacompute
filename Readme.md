# Satisfactory calculator

## Modelisation

a _base_ is a building or a set of building importing and exporting resources and consuming energy.

More specifically, a base can be :

- a single building
- a set of similar building with a common conveyer belt as input and as output
- a list of set of similar building. In this case we consider that the *N*th building in the list is connected to the _N-1_ previous ones (or have access to their resources)
- a collection of bases. In this case the base is marly a container for organization. internal bases probably imports and export resources between themselves.

The Calculator works in 2 steps : first we define the list of bases and the connections between them, then the calculator tries to compute the number of resources generated. This will be done doing a graph exploration starting from the Miners.
