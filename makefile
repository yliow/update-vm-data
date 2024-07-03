cp: cp-latex cp-python cp-alex cp-unix
	echo "done"

cp-latex:
	# should go into /usr/share/texlive/texmf-local/tex/latex/yliow
	-rm -rf latex
	-mkdir latex
	-mkdir latex/yliow
	cp -r /home/student/yliow/Documents/work/projects/latex-yliow/* latex/yliow/
	rm -rf latex/.git

cp-python:
	# should go into /usr/lib/python*.*/site-packages
	-rm -rf python
	-mkdir python
	cp -r /home/student/shares/yliow/Documents/work/projects/latextool/latextool_basic.py      python/
	cp -r /home/student/shares/yliow/Documents/work/projects/latextool/latexcircuit.py         python/
	cp -r /home/student/shares/yliow/Documents/work/projects/latextool/data                    python/
	cp -r /home/student/shares/yliow/Documents/work/projects/makemake/makemake.py              python/
	cp -r /home/student/shares/yliow/Documents/work/projects/findgrep/findgrep.py              python/
	cp -r /home/student/shares/yliow/Documents/work/projects/recognizelatex/recognizelatex.py  python/
	cp -r /home/student/shares/yliow/Documents/work/projects/xcapture/xcapture.py              python/
	cp -r /home/student/shares/yliow/Documents/work/projects/solutions/solutions.py            python/
	cp -r /home/student/shares/yliow/Documents/work/projects/latex-templates/quiz/makequiz.py  python/
	cp -r /home/student/shares/yliow/Documents/work/projects/latex-templates/checklatexbook.py python/
	cp -r /home/student/shares/yliow/Documents/work/projects/mips/formatmips/formatmips.py     python/

cp-alex:
	-rm -rf alex
	-mkdir alex
	cp /home/student/yliow/Documents/work/projects/alex05/code/alexcode/python39/alex*.py alex/
