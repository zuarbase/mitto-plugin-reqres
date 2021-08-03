# Mitto Plugin ReqRes - Jobs

.. todo::

	* Add an intro and a description for each job created by the wizard.
	* Explain job templates and template substitution.  Perhaps
      there should be a meta-documentation page covering this.

.. note::

    A very simple plugin, that primarily exists so that
	its inputter can be used in an "ordinary" Mitto job, can probably just
	document its inputters.  Because this plugin has a wizard that creates
	jobs, it seems apropos to provide an example of each job here.
	
.. note::

    The files contained in this document are located in the
	``reqres/conf`` directory.  That directory is not accessible by
	Sphinx documentation.  To work around this, a symbolic lik is
	created at ``docs/src/conf`` that points to ``../../reqres/conf``.
	The ``literalinclude`` reST directives below access the files via
	the link.

## ReqRes `users` Endpoint

Add description.

.. comment::
   Unfortunately, pygments does not have a lexer for hjson and using
   `:language: json` causes pygements to fail.  It appears that we
   must use `text` here and forego syntax highlighting for the job
   configs.

.. admonition:: Job Configuration - Users
   :class: dropdown

   .. literalinclude:: conf/users.hjson
	     :language: text
         :linenos:
	
## ReqRes `unknown` Endpoint

Add description.

.. admonition:: Job Configuration - Unknown
   :class: dropdown

   .. literalinclude:: conf/unknown.hjson
	     :language: text
         :linenos:

.. comment
   comment
