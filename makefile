cp: cp-latex cp-python cp-alex
	echo "done"

cp-latex:
	# should go into /usr/share/texlive/texmf-local/tex/latex/yliow
	-mkdir latex
	cp -r /home/student/yliow/Documents/work/projects/latex-yliow latex

cp-python:
	# should go into /usr/lib/python*.*/site-packages
	-mkdir python
	cp -r /home/student/shares/yliow/Documents/work/projects/latextool/latextool_basic.py python/
	cp -r /home/student/shares/yliow/Documents/work/projects/latextool/latexcircuit.py python/
	cp -r /home/student/shares/yliow/Documents/work/projects/latextool/data python/
	cp -r /home/student/shares/yliow/Documents/work/projects/makemake/makemake.py python/

cp-alex:
	-mkdir alex
	cp /home/student/yliow/Documents/work/projects/alex05/code/alexcode/python39/alex*.py alex/
