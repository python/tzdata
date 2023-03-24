# Version 2023.2
Upstream version 2023b released 2023-03-24T02:50:38+00:00

## Briefly:

Lebanon delays the start of DST this year.

## Changes to future timestamps

This year Lebanon springs forward April 20/21 not March 25/26. (Thanks to
Saadallah Itani.)

---

# Version 2023.1
Upstream version 2023a released 2023-03-22T19:39:33+00:00

## Briefly:

Egypt now uses DST again, from April through October. This year Morocco springs
forward April 23, not April 30. Palestine delays the start of DST this year.
Much of Greenland still uses DST from 2024 on. America/Yellowknife now links to
America/Edmonton. tzselect can now use current time to help infer timezone. The
code now defaults to C99 or later. Fix use of C23 attributes.

## Changes to future timestamps

Starting in 2023, Egypt will observe DST from April's last Friday through
October's last Thursday.  (Thanks to Ahmad ElDardiry.) Assume the transition
times are 00:00 and 24:00, respectively.

In 2023 Morocco's spring-forward transition after Ramadan will occur April 23,
not April 30.  (Thanks to Milamber.) Adjust predictions for future years
accordingly.  This affects predictions for 2023, 2031, 2038, and later years.

This year Palestine will delay its spring forward from March 25 to April 29 due
to Ramadan.  (Thanks to Heba Hamad.) Make guesses for future Ramadans too.

Much of Greenland, represented by America/Nuuk, will continue to observe DST
using European Union rules.  When combined with Greenland's decision not to
change the clocks in fall 2023, America/Nuuk therefore changes from -03/-02 to
-02/-01 effective 2023-10-29 at 01:00 UTC.  (Thanks to Thomas M. Steenholdt.)
This change from 2022g doesn't affect timestamps until 2024-03-30, and doesn't
affect tm_isdst until 2023-03-25.

## Changes to past timestamps

America/Yellowknife has changed from a Zone to a backward compatibility Link, as
it no longer differs from America/Edmonton since 1970.  (Thanks to Almaz
Mingaleev.)  This affects some pre-1948 timestamps.  The old data are now in
'backzone'.

## Changes to past time zone abbreviations

When observing Moscow time, Europe/Kirov and Europe/Volgograd now use the
abbreviations MSK/MSD instead of numeric abbreviations, for consistency with
other timezones observing Moscow time.

## Changes to commentary

tz-link.html has a new section "Coordinating with governments and distributors".
(Thanks to Neil Fuller for some of the text.)

To improve tzselect diagnostics, zone1970.tab's comments column is now limited
to countries that have multiple timezones.

Note that leap seconds are planned to be discontinued by 2035.

---

# Version 2022.7
Upstream version 2022g released 2022-11-29T16:58:31+00:00

## Briefly:

The northern edge of Chihuahua changes to US timekeeping. Much of Greenland
stops changing clocks after March 2023. Fix some pre-1996 timestamps in northern
Canada. C89 is now deprecated; please use C99 or later. Portability fixes for
AIX, libintl, MS-Windows, musl, z/OS In C code, use more C23 features if
available. C23 timegm now supported by default Fixes for unlikely integer
overflows

## Changes to future timestamps

In the Mexican state of Chihuahua, the border strip near the US will change to
agree with nearby US locations on 2022-11-30. The strip's western part,
represented by Ciudad Juárez, switches from -06 all year to -07/-06 with US DST
rules, like El Paso, TX. The eastern part, represented by Ojinaga, will observe
US DST next year, like Presidio, TX.  (Thanks to Heitor David Pinto.) A new Zone
America/Ciudad_Juarez splits from America/Ojinaga.

Much of Greenland, represented by America/Nuuk, stops observing winter time
after March 2023, so its daylight saving time becomes standard time.  (Thanks to
Jonas Nyrup and Jürgen Appel.)

## Changes to past timestamps

Changes for pre-1996 northern Canada (thanks to Chris Walton):

Merge America/Iqaluit and America/Pangnirtung into the former, with a backward
compatibility link for the latter name. There is no good evidence the two
locations differ since 1970. This change affects pre-1996 America/Pangnirtung
timestamps.

Cambridge Bay, Inuvik, Iqaluit, Rankin Inlet, Resolute and Yellowknife did not
observe DST in 1965, and did observe DST from 1972 through 1979.

Whitehorse moved from -09 to -08 on 1966-02-27, not 1967-05-28.

Colombia's 1993 fallback was 02-06 24:00, not 04-04 00:00. (Thanks to Alois
Treindl.)

Singapore's 1981-12-31 change was at 16:00 UTC (23:30 local time), not 24:00
local time.  (Thanks to Geoff Clare via Robert Elz.)

---

# Version 2022.6
Upstream version 2022f released 2022-10-29T01:04:57+00:00

## Briefly:

Mexico will no longer observe DST except near the US border. Chihuahua moves to
year-round -06 on 2022-10-30. Fiji no longer observes DST. Move links to
'backward'. In vanguard form, GMT is now a Zone and Etc/GMT a link. zic now
supports links to links, and vanguard form uses this. Simplify four Ontario
zones. Fix a Y2438 bug when reading TZif data. Enable 64-bit time_t on 32-bit
glibc platforms. Omit large-file support when no longer needed. In C code, use
some C23 features if available. Remove no-longer-needed workaround for Qt bug
53071.

## Changes to future timestamps.

Mexico will no longer observe DST after 2022, except for areas near the US
border that continue to observe US DST rules. On 2022-10-30 at 02:00 the Mexican
state of Chihuahua moves from -07 (-06 with DST) to year-round -06, thus not
changing its clocks that day.  The new law states that Chihuahua near the US
border no longer observes US DST.

Fiji will not observe DST in 2022/3.  (Thanks to Shalvin Narayan.) For now,
assume DST is suspended indefinitely.

## Changes to data

Move links to 'backward' to ease and simplify link maintenance. This affects
generated data only if you use 'make BACKWARD='.

GMT is now a Zone and Etc/GMT a link instead of vice versa, as GMT is needed for
leap second support whereas Etc/GMT is not. However, this change exposes a bug
in TZUpdater 2.3.2 so it is present only in vanguard form for now.

Vanguard form now uses links to links, as zic now supports this.

## Changes to past timestamps

Simplify four Ontario zones, as most of the post-1970 differences seem to have
been imaginary.  (Problem reported by Chris Walton.) Move America/Nipigon,
America/Rainy_River, and America/Thunder_Bay to 'backzone'; backward-
compatibility links still work, albeit with some different timestamps before
November 2005.

---

# Version 2022.5
Upstream version 2022e released 2022-10-11T18:13:02+00:00

## Briefly:

Jordan and Syria switch from +02/+03 with DST to year-round +03.

## Changes to future timestamps

Jordan and Syria are abandoning the DST regime and are changing to permanent
+03, so they will not fall back from +03 to +02 on 2022-10-28.  (Thanks to
Steffen Thorsen and Issam Al-Zuwairi.)

## Changes to past timestamps

On 1922-01-01 Tijuana adopted standard time at 00:00, not 01:00.

## Changes to past time zone abbreviations and DST flags

The temporary advancement of clocks in central Mexico in summer 1931 is now
treated as daylight saving time, instead of as two changes to standard time.

---

# Version 2022.4
Upstream version 2022d released 2022-09-23T19:02:57+00:00

## Briefly:

Palestine transitions are now Saturdays at 02:00. Simplify three Ukraine zones
into one.

## Changes to future timestamps

Palestine now springs forward and falls back at 02:00 on the first Saturday on
or after March 24 and October 24, respectively. This means 2022 falls back 10-29
at 02:00, not 10-28 at 01:00. (Thanks to Heba Hamad.)

## Changes to past timestamps

Simplify three Ukraine zones to one, since the post-1970 differences seem to
have been imaginary.  Move Europe/Uzhgorod and Europe/Zaporozhye to 'backzone';
backward-compatibility links still work, albeit with different timestamps before
October 1991.

---

# Version 2022.3
Upstream version 2022c released 2022-08-16T00:47:18+00:00

## Briefly:

Work around awk bug in FreeBSD, macOS, etc. Improve tzselect on intercontinental
Zones.

---

# Version 2022.2
Upstream version 2022b released 2022-08-10T22:38:32+00:00

## Briefly:

Chile's DST is delayed by a week in September 2022. Iran no longer observes DST
after 2022. Rename Europe/Kiev to Europe/Kyiv. New zic -R option Vanguard form
now uses %z. Finish moving duplicate-since-1970 zones to 'backzone'. New build
option PACKRATLIST New tailored_tarballs target, replacing rearguard_tarballs

## Changes to future timestamps

Chile's 2022 DST start is delayed from September 4 to September 11. (Thanks to
Juan Correa.)

Iran plans to stop observing DST permanently, after it falls back on 2022-09-21.
(Thanks to Ali Mirjamali.)

## Changes to past timestamps

Finish moving to 'backzone' the location-based zones whose timestamps since 1970
are duplicates; adjust links accordingly. This change ordinarily affects only
pre-1970 timestamps, and with the new PACKRATLIST option it does not affect any
timestamps. In this round the affected zones are Antarctica/Vostok, Asia/Brunei,
Asia/Kuala_Lumpur, Atlantic/Reykjavik, Europe/Amsterdam, Europe/Copenhagen,
Europe/Luxembourg, Europe/Monaco, Europe/Oslo, Europe/Stockholm,
Indian/Christmas, Indian/Cocos, Indian/Kerguelen, Indian/Mahe, Indian/Reunion,
Pacific/Chuuk, Pacific/Funafuti, Pacific/Majuro, Pacific/Pohnpei, Pacific/Wake
and Pacific/Wallis, and the affected links are Arctic/Longyearbyen,
Atlantic/Jan_Mayen, Iceland, Pacific/Ponape, Pacific/Truk, and Pacific/Yap.

From fall 1994 through fall 1995, Shanks wrote that Crimea's DST transitions
were at 02:00 standard time, not at 00:00. (Thanks to Michael Deckers.)

Iran adopted standard time in 1935, not 1946.  In 1977 it observed DST from
03-21 23:00 to 10-20 24:00; its 1978 transitions were on 03-24 and 08-05, not
03-20 and 10-20; and its spring 1979 transition was on 05-27, not 03-21. (Thanks
to Roozbeh Pournader and Francis Santoni.)

Chile's observance of -04 from 1946-08-29 through 1947-03-31 was considered DST,
not standard time.  Santiago and environs had moved their clocks back to rejoin
the rest of mainland Chile; put this change at the end of 1946-08-28.  (Thanks
to Michael Deckers.)

Some old, small clock transitions have been removed, as people at the time did
not change their clocks.  This affects Asia/Hong_Kong in 1904, Asia/Ho_Chi_Minh
in 1906, and Europe/Dublin in 1880.

## Changes to zone name

Rename Europe/Kiev to Europe/Kyiv, as "Kyiv" is more common in English now.
Spelling of other names in Ukraine has not yet demonstrably changed in common
English practice so for now these names retain old spellings, as in other
countries (e.g., Europe/Prague not "Praha", and Europe/Sofia not "Sofiya").

---

# Version 2022.1
Upstream version 2022a released 2022-03-16T06:02:01+00:00

## Briefly:

Palestine will spring forward on 2022-03-27, not -03-26. zdump -v now outputs
better failure indications. Bug fixes for code that reads corrupted TZif data.

## Changes to future timestamps

Palestine will spring forward on 2022-03-27, not 2022-03-26. (Thanks to Heba
Hamad.)  Predict future transitions for first Sunday >= March 25.  Additionally,
predict fallbacks to be the first Friday on or after October 23, not October's
last Friday, to be more consistent with recent practice.  The first differing
fallback prediction is on 2025-10-24, not 2025-10-31.

## Changes to past timestamps

From 1992 through spring 1996, Ukraine's DST transitions were at 02:00 standard
time, not at 01:00 UTC.  (Thanks to Alois Treindl.)

Chile's Santiago Mean Time and its LMT precursor have been adjusted eastward by
1 second to align with past and present law.

## Changes to commentary

Add several references for Chile's 1946/1947 transitions, some of which only
affected portions of the country.

---

# Version 2021.5
Upstream version 2021e released 2021-10-22T01:41:00+00:00

## Changes to future timestamps

Palestine will fall back 10-29 (not 10-30) at 01:00. (Thanks to P Chan and Heba
Hemad.)

---

# Version 2021.4
Upstream version 2021d released 2021-10-15T20:48:18+00:00

## Briefly:

Fiji suspends DST for the 2021/2022 season. 'zic -r' marks unspecified
timestamps with "-00".

## Changes to future timestamps

Fiji will suspend observance of DST for the 2021/2022 season. Assume for now
that it will return next year.  (Thanks to Jashneel Kumar and P Chan.)

---

# Version 2021.3
Upstream version 2021c released 2021-10-01T21:21:49+00:00

## Briefly:

Revert most 2021b changes to 'backward'. Fix 'zic -b fat' bug in pre-1970 32-bit
data. Fix two Link line typos. Distribute SECURITY file.

This release is intended as a bugfix release, to fix compatibility problems and
typos reported since 2021b was released.

## Changes to Link directives

Revert almost all of 2021b's changes to the 'backward' file, by moving Link
directives back to where they were in 2021a. Although 'zic' doesn't care which
source file contains a Link directive, some downstream uses ran into trouble
with the move. (Problem reported by Stephen Colebourne for Joda-Time.)

Fix typo that linked Atlantic/Jan_Mayen to the wrong location (problem reported
by Chris Walton).

Fix 'backzone' typo that linked America/Virgin to the wrong location (problem
reported by Michael Deckers).

## Changes to documentation

Distribute the SECURITY file (problem reported by Andreas Radke).

---

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


---

# Version 2021.2
Upstream version 2021b released 2021-09-24T23:23:00+00:00

## Briefly:

This is an intermediate release that cherry-picks only the changes to Jordan and
Samoa's DST. It will not match upstream 2021b, which includes many other
changes.

## Changes to future timestamps

Jordan now starts DST on February's last Thursday. (Thanks to Steffen Thorsen.)

Samoa no longer observes DST.  (Thanks to Geoffrey D. Bennett.)

---

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
