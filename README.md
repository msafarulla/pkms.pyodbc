# Author: Mohamed Safarulla
# Description: This module will help you connect to a PkMS environment and query tables using the iSeries library list concept. Schema need not be explicitly mentioned.
# Date: 06/30/2020 
# Lincense : Open Source FSF. If you happen to augment it, please share it, so that all of us can benefit from it. 

This module will help you to connect to Manhattan WMS environment (SE command). Backbone is python module pyodbc (make sure you are on 
python 3.8, if not make necessary changes to the code to make it backward compatible)

Prerequisites:
iSeries access driver should be available in the host system. 
For Windows it automatically comes with i Series Client Access solutions 
if not, for Windows/Linux/Unix, how to get the ODBC driver configured should be available here:
https://www.reddit.com/r/linux/comments/2cd3y2/debian_redhat_ibm_iseries_odbc_integration/


For Mac this driver is not available, atleast as far as I digged, you probably have to go the Linux VirtualBox path to get things working there.

I will add code samples as I get time. 
