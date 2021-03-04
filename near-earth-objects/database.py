"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""
from filters import DateFilter

class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        
        # TODO: What additional auxiliary data structures will be useful?
        self.approaches = approaches
        
        
        self._neos = {neo.designation: neo for neo in neos}
        # for get_neo_by_name
        # names are not always present (the '' key will not be unique), 
        # but this is not a restriction because it will only be used for a name that the user provides
        self._name_to_des = {neo.name: neo.designation for neo in neos}
        self._approaches = {}
        for approach in approaches:
            if self._approaches.get(approach.designation, None):
                self._approaches[approach.designation].append(approach)
            else:
                self._approaches[approach.designation] = [approach]
            for a in self._approaches[approach.designation]:
                a.neo = self._neos[approach.designation]
            self._neos[approach.designation].approaches.append(approach)

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        # TODO: Fetch an NEO by its primary designation.
        return self._neos.get(designation.upper(), None)
        
    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        # TODO: Fetch an NEO by its name.
        designation = self._name_to_des.get(name.capitalize(), None)
        if designation:
            return self.get_neo_by_designation(designation)
        return None

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        # TODO: Generate `CloseApproach` objects that match all of the filters.
        date_filters = ["date", "start_date", "end_date"]
        no_date = all([f for f in filters.keys() if f not in date_filters])
        
        for approach in self.approaches:
            passed_dates = True
            if no_date and all((map(lambda x: x(approach), filters.values()))):
                yield approach
            elif not no_date:
                if "date" in filters:
                    passed_dates = filters["date"](approach)
                    if passed_dates and all((map(lambda x: x(approach), [f for name, f in filters.items() if name not in date_filters]))): # passed the exact date and all the non-date related filters 
                        yield approach
                    elif not passed_dates:
                        # should be between start and end date
                        passed_dates = all((map(lambda x: x(approach), [f for name, f in filters.items() if name in ["start_date", "end_date"]])))
                        if passed_dates and all((map(lambda x: x(approach), [f for name, f in filters.items() if name not in date_filters]))): 
                            yield approach
                else:
                    if all((map(lambda x: x(approach), filters.values()))):
                        yield approach