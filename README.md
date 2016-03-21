This little script uses https://bibtexparser.readthedocs.org/en/v0.6.2/ and a string edit distance from http://www.nltk.org/

To run it just provide your bib files as arguments. It will compare the first one against the rest and output a report like this:


<pre>
./check_duplicates.py "/Users/josepvalls/Dropbox/projects-santi/Proposal/References.bib" "/Users/josepvalls/Dropbox/projects-santi/Proposal/References 2.bib" "/Users/josepvalls/Dropbox/projects-santi/Proposal/References 3.bib"

File:  /Users/josepvalls/Dropbox/projects-santi/Proposal/References 2.bib
 NEW RECORDS
   fonseca2013two
   srivastava2015inferring
 DIFFERENT RECORDS
   int2013
   int2014
File:  /Users/josepvalls/Dropbox/projects-santi/Proposal/References 3.bib
 NEW RECORDS
   valls2013cig
   valls2011textmodification
   valls2015aiide
   lyon2014chiplay
   valls2014int
   valls2015int
   valls2015gls
   valls2014aiide
   valls2013int
   valls2012iccbr
 DIFFERENT RECORDS
   valls2013towards
   mateas1999narrative
   Fairclough2007
   Hartsook2011
   valls2015ijcai
CHECKING DUPLICATES
   Elson2010socialnetworks elson2010extracting
   chambers2009unsupervised chambers2009
   chambers2009unsupervised Chambers2009a
   int2013 valls2013int
   int2014 valls2014toward
   int2014 valls2014int
   int2014 valls2015int
   int2014 valls2014aiide
   chambers2008unsupervised Chambers2008
   </pre>
