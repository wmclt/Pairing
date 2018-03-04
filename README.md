# Pairing
This application is to quickly create pairs in the team, taking 
into account:
* absent devs
* devs working solo
* pairs staying together
* leads working on stories 

The algorithm strives to make everyone pair with everyone else as equally as possible.


# TODO
* Document public functions
	* pairing
	* bash_io
	* history_io
* Not same pairs as yesterday => meantime, just say "no"
* Maybe notify if some pair/solo has been doing much more than the rest
* In an ideal world, mathchmaker.form_pairs() would work functionally. But for this the whole stack would need to work functionally too.