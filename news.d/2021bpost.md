# Version 2021.2.post0
Upstream version 2021b released 2021-09-24T23:23:00+00:00

## Briefly:

Jordan now starts DST on February's last Thursday. Samoa no longer observes DST.
Merge more location-based Zones whose timestamps agree since 1970. Move some
backward-compatibility links to 'backward'. Rename Pacific/Enderbury to
Pacific/Kanton. Correct many pre-1993 transitions in Malawi, Portugal, etc. zic
now creates each output file or link atomically.

This release is prompted by recent announcements by Jordan and Samoa. It
incorporates many other changes that had accumulated since 2021a. However, it
omits most proposed changes that merged all Zones agreeing since 1970, as
concerns were raised about doing too many of these changes at once.  It does
keeps some of these changes in the interest of making tzdb more equitable one
step at a time; see "Merge more location-based Zones" below.

## Changes to future timestamps

Jordan now starts DST on February's last Thursday. (Thanks to Steffen Thorsen.)

Samoa no longer observes DST.  (Thanks to Geoffrey D. Bennett.)

## Changes to zone name

Rename Pacific/Enderbury to Pacific/Kanton.  When we added Enderbury in 1993, we
did not know that it is uninhabited and that Kanton (population two dozen) is
the only inhabited location in that timezone.  The old name is now a backward-
compatility link.

## Changes to past timestamps

Correct many pre-1993 transitions, fixing entries originally derived from
Shanks, Whitman, and Mundell.  The fixes include:

- Barbados: standard time was introduced in 1911, not 1932; and DST was
  observed in 1942-1944
- Cook Islands: In 1899 they switched from east to west of GMT, celebrating
  Christmas for two days. They (and Niue) switched to standard time in 1952,
  not 1901.
- Guyana: corrected LMT for Georgetown; the introduction of standard time in
  1911, not 1915; and corrections to 1975 and 1992 transitions
- Kanton: uninhabited before 1937-08-31
- Niue: only observed -11:20 from 1952 through 1964, then went to -11 instead
  of -11:30
- Portugal: DST was observed in 1950
- Tonga: corrected LMT; the introduction of standard time in 1945, not 1901;
  and corrections to the transition from +12:20 to +13 in 1961, not 1941

Additional fixes to entries in the 'backzone' file include:

- Enderbury: inhabited only 1860/1885 and 1938-03-06/1942-02-09
- The Gambia: 1933 and 1942 transitions
- Malawi: several 1911 through 1925 transitions
- Sierra Leone: several 1913 through 1941 transitions, and DST was NOT observed
  in 1957 through 1962 (Thanks to P Chan, Michael Deckers, Alexander
  Krivenyshev and Alois Treindl.)

Merge more location-based Zones whose timestamps agree since 1970, as pre-1970
timestamps are out of scope.  This is part of a process that has been ongoing
since 2013.  This does not affect post-1970 timestamps, and timezone historians
who build with 'make PACKRATDATA=backzone' should see no changes to pre-1970
timestamps. When merging, keep the most-populous location's data, and move data
for other locations to 'backzone' with a backward link in 'backward'.  For
example, move America/Creston data to 'backzone' with a link in 'backward' from
America/Phoenix because the two timezones' timestamps agree since 1970; this
change affects some pre-1968 timestamps in America/Creston because Creston and
Phoenix disagreed before 1968.  The affected Zones are Africa/Accra,
America/Atikokan, America/Blanc-Sablon, America/Creston, America/Curacao,
America/Nassau, America/Port_of_Spain, Antarctica/DumontDUrville, and
Antarctica/Syowa.

## Changes to documentation

tzfile.5 better matches a draft successor to RFC 8536
<https://datatracker.ietf.org/doc/draft-murchison-rfc8536bis/01/>.
