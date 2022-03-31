****
TODO
****

core calculator code
####################
* Allow for irregularly spaced dilutions. Could require getting rid of, or at least tweaking, RM and SK.

command-line tool (src/*py, bin)
################################
* Add option to create graph as pdf, svg, png, etc.?
* Fix handling of special characters in Label and Comment fields

django web interface (src/web)
##############################
* Fix dilmin and dilfac in form to allow 1/10 and 1e-3 entries
* Make field.help_text appear as floating pop-ups on-click or hover
* Web interface fails when more than about 45 entries in batch mode
