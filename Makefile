
signal:
	python setup_signal.py build_ext --inplace

mixin:
	python setup_mixin.py build_ext --inplace

evas:
	python setup_evasobj.py build_ext --inplace

base:
	python setup_eobjdefault.py build_ext --inplace

clean:
	rm -rf *.so *~ *.c build/
	rm elwboxedbutton.* ElwBoxedButton.* elwbox.* ElwBox.* elwbutton.* ElwButton.* elwwin.* ElwWin.* evasobject.* EvasObject.* simple.* Simple.* Mixin.* mixin.*
