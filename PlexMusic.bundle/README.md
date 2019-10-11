2019-10-11 PlexMusic.bundle Modded by Beeman to support adding data from artist.nfo + album.nfo files + tweak settings
.tested on Plex version 1.18.0.1913, won't work on any previous Plex versions.
.may not work proeprly on non 'Plex Music' libraries if changed, noticed strange effects sometimes. 
.works OK on brand new Plex Server setup though (empty Plex Media Server folder)

--Usage
.copy PlexMusic.bundle folder into C:\Program Files (x86)\Plex\Plex Media Server\Resources\Plug-ins-e5cc93306 overwriting existing files. On other o/s locate the relevant folder. No other way to do this but to mod existing plex music agent, as plugins won't work with Plex Music agent, so will be overwritten when upgrading Plex Media Server!

--Plex Advanced Settings changes:-
.Artist Bios = off (or biog field empty) => load from artist.nfo biography tag 
.Album reviews = off (or review field empty) =>  load from album.nfo review tag but now ALWAYS loads critics rating
.Genres = None => load genres, styles, moods from artist.nfo for artist + load genre, style, mood, studio from album.nfo for album
.Album Art = Local Files Only => load both album AND artist art locally
.Add tag fields in nfo files to Plex collections (works for artist but not for album?)
.Scanner + Agent must = Plex Music
-------


License
-------

If the software submitted to this repository accesses or calls any software provided by Plex (“Interfacing Software”), then as a condition for receiving services from Plex in response to such accesses or calls, you agree to grant and do hereby grant to Plex and its affiliates worldwide a worldwide, nonexclusive, and royalty-free right and license to use (including testing, hosting and linking to), copy, publicly perform, publicly display, reproduce in copies for distribution, and distribute the copies of any Interfacing Software made by you or with your assistance; provided, however, that you may notify Plex at legal@plex.tv if you do not wish for Plex to use, distribute, copy, publicly perform, publicly display, reproduce in copies for distribution, or distribute copies of an Interfacing Software that was created by you, and Plex will reasonable efforts to comply with such a request within a reasonable time.