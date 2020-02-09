# Qualitative Reasoning (qualreas)#

**qualreas** is a Python module that implements temporal and spatial *algebras* for performing qualitative reasoning
about space and time.  It includes the four temporal algebras found in ["Intervals, Points, and Branching Time"
(Reich, 1994)](https://www.researchgate.net/publication/220810644_Intervals_Points_and_Branching_Time).  (A scanned
copy of the paper can also be found [here](http://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0CCMQFjAA&url=http%3A%2F%2Fwww2.cs.uregina.ca%2F~temporal%2Ftime94%2Freich.pdf&ei=XeieVLnkFsX9yQSBi4G4Cw&usg=AFQjCNG8EUtVBz_5OFJXFbMJVtHGjj6b7w&sig2=RrmzWe5WcwCet7fr2AuLNg&bvm=bv.82001339,d.aWw).)  The [Region Connection Calculus (RCC8)](http://en.wikipedia.org/wiki/Region_connection_calculus) is also included.

### To Be Done

* Update timeX.ttl ontology to fix W3C reference & add branching time relations
* Change the name "Point" to "Instant" (to match https://www.w3.org/TR/owl-time/)
* Create Sphinx docs
* Update this Readme
* Create functionality for Algebra generation
* Generate all 4 temporal algebras and check them against the existing ones
* Generate an RCC8 variant that permits a region to have a single hole
* Add additional algebras: Matuzak (sp?), Anger's right-branching algebra, etc.
* Compare the additional algebras to those that I generated
* See if I can make contraint propagation more efficient by not propagating
constraints for temporal entities "contained" by other temporal entitites.

### What is this repository for? ###

* Quick summary
* Version 0.1
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner/admin: Alfred J. Reich, Ph.D. (al.reich@gmail.com)
* Other community or team contact
