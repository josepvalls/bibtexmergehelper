#!/usr/bin/env python

# Author: Josep Valls Vargas
# http://josep.valls.name

import bibtex
import sys
import pprint
from nltk_ import string_edit_distance

def collect(records,field):
	return [i.get(field,None) for i in records]

def fix_authors(records):
	for i in records:
		for k,v in i.items():
			if isinstance(v,dict):
				i[k] = str(v)
			elif isinstance(v,list):
				i[k] = ",".join([j.get('id','?') if isinstance(v,dict) else '?' for j in v])
	return records


def different_values(a,b):
	return set(a.items())^set(b.items())

def string_edit_distance_norm(s1, s2):
	return 1.0*string_edit_distance(s1,s2)/max(len(s1),len(s2))

def string_edit_distance(s1, s2):
    """
    Calculate the Levenshtein edit-distance between two strings.
    The edit distance is the number of characters that need to be
    substituted, inserted, or deleted, to transform s1 into s2.  For
    example, transforming "rain" to "shine" requires three steps,
    consisting of two substitutions and one insertion:
    "rain" -> "sain" -> "shin" -> "shine".  These operations could have
    been done in other orders, but at least three steps are needed.

    :param s1, s2: The strings to be analysed
    :type s1: str
    :type s2: str
    :rtype int
    """

    def _edit_dist_init(len1, len2):
        lev = []
        for i in range(len1):
            lev.append([0] * len2)  # initialize 2-D array to zero
        for i in range(len1):
            lev[i][0] = i  # column 0: 0,1,2,3,4,...
        for j in range(len2):
            lev[0][j] = j  # row 0: 0,1,2,3,4,...
        return lev


    def _edit_dist_step(lev, i, j, c1, c2):
        a = lev[i - 1][j] + 1  # skipping s1[i]
        b = lev[i - 1][j - 1] + (c1 != c2)  # matching s1[i] with s2[j]
        c = lev[i][j - 1] + 1  # skipping s2[j]
        lev[i][j] = min(a, b, c)  # pick the cheapest

    # set up a 2-D array
    len1 = len(s1)
    len2 = len(s2)
    lev = _edit_dist_init(len1 + 1, len2 + 1)

    # iterate over the array
    for i in range(len1):
        for j in range(len2):
            _edit_dist_step(lev, i + 1, j + 1, s1[i], s2[j])
    return lev[len1][len2]

def compare(records,records_):
	records = dict(zip(collect(records,'id'),records))
	records_ = dict(zip(collect(records_,'id'),records_))
	rnew = set(records_.keys()) - set(records.keys())
	rintersect = set(records.keys()) & set(records_.keys())
	rupdated = [i for i in rintersect if different_values(records[i],records_[i])]
	return rnew,rupdated

def main(argv):
	if len(argv)<2:
		sys.stderr.write("Arguments must be bib files\n")
	elif len(argv)==2:
		records, metadata = bibtex.BibTexParser(open(argv[1])).parse()
		if len(records) > 0:
			pprint.pprint(records)
		else:
			sys.stderr.write('Zero records were parsed from the data\n')
	else:
		records, metadata = bibtex.BibTexParser(open(argv[1])).parse()
		records = fix_authors(records)
		records_new = list(records)
		for bib in argv[2:]:
			records_, metadata_ = bibtex.BibTexParser(open(bib)).parse()
			records_ = fix_authors(records_)
			if len(records_) > 0:
				print "File: ",bib
				r_new,r_diferent = compare(records,records_)
				records_ = dict(zip(collect(records_,'id'),records_))
				if r_new:
					print " NEW RECORDS"
					for i in r_new:
						records_new.append(records_[i])
						print "  ",i
				if r_diferent:
					print " DIFFERENT RECORDS"
					for i in r_diferent:
						print "  ",i
			else:
				sys.stderr.write('Zero records were parsed from %s\n' % bib)
		print "CHECKING DUPLICATES"
		dups = set()
		for i in records_new:
			for j in records_new:
				if string_edit_distance_norm(i.get('title',''),j.get('title',''))<0.3 and not i.get('id',None)==j.get('id',None):
					key = tuple(sorted([i.get('id','?'),j.get('id','?')]))
					if not key in dups:
						print "  ",i.get('id','?'),j.get('id','?')
						dups.add(key)


if __name__=="__main__":
	main(sys.argv)