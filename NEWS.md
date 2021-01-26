# Version 2021.1
Upstream version 2021a released 2021-01-24T18:54:57+00:00

## Changes to future timestamps

South Sudan changes from +03 to +02 on 2021-02-01 at 00:00. (Thanks to Steffen
Thorsen.)

---

# Version 2020.6
Upstream version 2020f released 2020-12-29T08:17:46+00:00

## Change to build procedure

'make rearguard_tarballs' no longer generates a bad rearguard.zi, fixing a 2020e
bug.  (Problem reported by Deborah Goldsmith.)

---

# Version 2020.5
Upstream version 2020e released 2020-12-22T23:14:34+00:00

## Briefly:

Volgograd switches to Moscow time on 2020-12-27 at 02:00.

## Changes to future timestamps

Volgograd changes time zone from +04 to +03 on 2020-12-27 at 02:00. (Thanks to
Alexander Krivenyshev and Stepan Golosunov.)

## Changes to past timestamps

Correct many pre-1986 transitions, fixing entries originally derived from
Shanks.  The fixes include:

- Australia: several 1917 through 1971 transitions
- Bahamas: several 1941 through 1945 transitions
- Bermuda: several 1917 through 1956 transitions
- Belize: several 1942 through 1968 transitions
- Ghana: several 1915 through 1956 transitions
- Israel and Palestine: several 1940 through 1985 transitions
- Kenya and adjacent: several 1908 through 1960 transitions
- Nigeria and adjacent: correcting LMT in Lagos, and several 1905 through 1919 transitions
- Seychelles: the introduction of standard time in 1907, not 1906
- Vanuatu: DST in 1973-1974, and a corrected 1984 transition

(Thanks to P Chan.)

Because of the Australia change, Australia/Currie (King Island) is no longer
needed, as it is identical to Australia/Hobart for all timestamps since 1970 and
was therefore created by mistake. Australia/Currie has been moved to the
'backward' file and its corrected data moved to the 'backzone' file.

## Changes to past time zone abbreviations and DST flags

To better match legislation in Turks and Caicos, the 2015 shift to year-round
observance of -04 is now modeled as AST throughout before returning to Eastern
Time with US DST in 2018, rather than as maintaining EDT until 2015-11-01.
(Thanks to P Chan.)

## Changes to documentation

The zic man page now documents zic's coalescing of transitions when a zone falls
back just before DST springs forward.


---

# Version 2020.4
Upstream version 2020d released 2020-10-21T18:24:13+00:00

## Briefly:

Palestine ends DST earlier than predicted, on 2020-10-24.

## Changes to past and future timestamps

Palestine ends DST on 2020-10-24 at 01:00, instead of 2020-10-31 as previously
predicted (thanks to Sharef Mustafa.)  Its 2019-10-26 fall-back was at 00:00,
not 01:00 (thanks to Steffen Thorsen.)  Its 2015-10-23 transition was at 01:00
not 00:00, and its spring 2020 transition was on March 28 at 00:00, not March 27
(thanks to Pierre Cashon.)  This affects Asia/Gaza and Asia/Hebron.  Assume
future spring and fall transitions will be on the Saturday preceding the last
Sunday of March and October, respectively.

---

# Version 2020.3
Upstream version 2020c released 2020-10-16T18:15:53+00:00

## Briefly:

Fiji starts DST later than usual, on 2020-12-20.

## Changes to future timestamps

Fiji will start DST on 2020-12-20, instead of 2020-11-08 as previously
predicted.  DST will still end on 2021-01-17. (Thanks to Raymond Kumar and Alan
Mintz.)  Assume for now that the later-than-usual start date is a one-time
departure from the recent pattern.


---

# Version 2020.2
Upstream version 2020b released 2020-10-07T01:35:04+00:00

## Briefly:

Revised predictions for Morocco's changes starting in 2023. Canada's Yukon
changes to -07 on 2020-11-01, not 2020-03-08. Macquarie Island has stayed in
sync with Tasmania since 2011. Casey, Antarctica is at +08 in winter and +11 in
summer. zic no longer supports -y, nor the TYPE field of Rules.

## Changes to future timestamps

Morocco's spring-forward after Ramadan is now predicted to occur no sooner than
two days after Ramadan, instead of one day. (Thanks to Milamber.)  The first
altered prediction is for 2023, now predicted to spring-forward on April 30
instead of April 23.

## Changes to past and future timestamps

Casey Station, Antarctica has been using +08 in winter and +11 in summer since
2018.  The most recent transition from +08 to +11 was 2020-10-04 00:01.  Also,
Macquarie Island has been staying in sync with Tasmania since 2011.  (Thanks to
Steffen Thorsen.)

## Changes to past and future time zone abbreviations and DST flags

Canada's Yukon, represented by America/Whitehorse and America/Dawson, changes
its time zone rules from -08/-07 to permanent -07 on 2020-11-01, not on
2020-03-08 as 2020a had it. This change affects only the time zone abbreviation
(MST vs PDT) and daylight saving flag for the period between the two dates.
(Thanks to Andrew G. Smith.)

## Changes to past timestamps

Correct several transitions for Hungary for 1918/1983. For example, the
1983-09-25 fall-back was at 01:00, not 03:00. (Thanks to Géza Nyáry.)  Also, the
1890 transition to standard time was on 11-01, not 10-01 (thanks to Michael
Deckers).

The 1891 French transition was on March 16, not March 15.  The 1911-03-11 French
transition was at midnight, not a minute later. Monaco's transitions were on
1892-06-01 and 1911-03-29, not 1891-03-15 and 1911-03-11.  (Thanks to Michael
Deckers.)

## Changes to documentation and commentary

The long-obsolete files pacificnew, systemv, and yearistype.sh have been removed
from the distribution.  (Thanks to Tim Parenti.)


---

# Version 2020.1
Upstream version 2020a released 2020-04-23T23:03:47+00:00

## Briefly:

Morocco springs forward on 2020-05-31, not 2020-05-24. Canada's Yukon advanced
to -07 year-round on 2020-03-08. America/Nuuk renamed from America/Godthab. zic
now supports expiration dates for leap second lists.

## Changes to future timestamps

Morocco's second spring-forward transition in 2020 will be May 31, not May 24 as
predicted earlier.  (Thanks to Semlali Naoufal.) Adjust future-year predictions
to use the first Sunday after the day after Ramadan, not the first Sunday after
Ramadan.

Canada's Yukon, represented by America/Whitehorse and America/Dawson, advanced
to -07 year-round, beginning with its spring-forward transition on 2020-03-08,
and will not fall back on 2020-11-01.  Although a government press release calls
this "permanent Pacific Daylight Saving Time", we prefer MST for consistency
with nearby Dawson Creek, Creston, and Fort Nelson. (Thanks to Tim Parenti.)

## Changes to past timestamps

Shanghai observed DST in 1919.  (Thanks to Phake Nick.)

## Changes to timezone identifiers

To reflect current usage in English better, America/Godthab has been renamed to
America/Nuuk.  A backwards-compatibility link remains for the old name.

## Changes to commentary

The Îles-de-la-Madeleine and the Listuguj reserve are noted as following
America/Halifax, and comments about Yukon's "south" and "north" have been
corrected to say "east" and "west".  (Thanks to Jeffery Nichols.)
