Welcome to BottleFit, an example of creating a
web-based curve and surface fitting tool with
Python Bottle and the pyeq3 fitting library.
see http://commonproblems.readthedocs.io/en/latest/


Step 1: Install bottle, scipy and matplotlib

On Debian or Ubuntu Linux, you can use this command:

sudo apt-get install python3-bottle python3-scipy python3-matplotlib


On other operating systems, try the Canopy Express Free version:

https://store.enthought.com/

and install Bottle with:

easy_install bottle


Finally, install the pyeq3 fitting library using pip:

pip3 install pyeq3



Step 2: Run the BottleFit example

From a command prompt run this command:

python3 BottleFit.py

The command prompt should then display:

Bottle [version] server starting up (using WSGIRefServer())...
Listening on http://0.0.0.0:8080/
Hit Ctrl-C to quit.

When you open this URL you should see a form
that allows curve and surface fitting, with graphs.
The address "0.0.0.0" allows port 8080 to be seen
externally.  On my development laptop, I can open
the URL "127.0.0.1:8080/" and see the web server.

Use Control-C to exit the Bottle development server.



Step 3: Celebrate

You are now curve and surface fitting data using Bottle!



If you would like to create a feature complete web site
with django, see https://github.com/zunzun/zunzunsite3
which has "function finding" and animated surface rotations
along with SMP parallel processing for multi-core servers.
