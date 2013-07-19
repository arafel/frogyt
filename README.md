Python libraries required: httplib2, gflags. On Debian, do:

	sudo apt-get install python-gflags python-httplib2

The Google API Python module is also required. If you have `mr` installed, run `mr update`, after
adding `.mrconfig` in this directory to your `$HOME/.mrtrust` file:

	echo $PWD/.mrconfig >> $HOME/.mrtrust	
	mr update
	
If you don't have `mr` installed:

	sudo apt-get install mr

