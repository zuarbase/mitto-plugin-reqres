## TODO

`todo_list.md` contains the reST directive `.. todolist::`, which is
replaced by all todo items in the package, both source code and
documentation. This file `_todo_list.md` is a catch-all for todo
items.  It is never explicitly rendered as part of the documentation,
but the items here will appear in `todo_list.html`.

These items could be included in `todo_list.md`, but then they would
appear twice on that page.

.. todo::

   May want to provide documentation for these topics:

   * how to build the plugin
   * how to install the plugin
   * how does the plugin integrate with Mitto
   * how does the wizard work; how to write one
   * how to write a plugin without the complexity of a wizard; what
     can be left out of this package
   * documentation
	 * how to build the documentation (breifly covered in 
	   [index-original.md)(index-original.md)
	 * either explain public vs. private documentation or remove support
	   for private
     * explain `conf.py` and symlinks in `src` and `srcp`.

.. todo::

   Other stuff that would be nice:

   * cleanup/simplify `docs/conf.py`
   * inhibit sphinx warnings
   * modify CSS to enlarge font size


.. comment
   comment
