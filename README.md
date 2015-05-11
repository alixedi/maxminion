maxminion
=========

A test minion that compiles the given apps using MaxCompiler 2015.1 release and produces a report.

This is the first draft, alpha version that is broken by design. Here are some of the problems:

* Takes the username and password for the source control in plain text on the CLI.
* Creates a tmp directory for cloning the apps. In case of an error, no clean-up is performed resulting in possible inconsistencies in following runs.
* Redirects the output of the compilation process to STDNULL and produces a minimal report saying 'OK' or 'ERROR'.
* Have not tested this with SVN yet. Should work though. For obvious reasons.
