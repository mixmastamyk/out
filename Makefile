

check_readme:
	# requires readme_renderer
	python3 setup.py check --restructuredtext --strict


clean:
	git gc
	rm -f readme.html
	rm -rf .pytest_cache build dist

	-find -type d -name __pycache__ -exec rm -rf '{}' \;


demos:
	python3 out/demos.py


# check_readme
publish: test clean
	rm -rf build dist  # possible wheel bug
#~ 	python3 setup.py sdist bdist_wheel --universal # no longer supported
	python3 -m build
	# upload
	twine upload --verbose dist/*

readme.html: readme.rst
	rst2html readme.rst > readme.html
	send_refresh.sh Out


test:
	pyflakes **.py



# all targets for now
.PHONY: $(MAKECMDGOALS)
