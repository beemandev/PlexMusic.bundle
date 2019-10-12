Details
-------
2019-10-11 PlexMusic.bundle Modded by Beeman to support adding data from artist.nfo + album.nfo files + tweak settings.
Tested on Plex version 1.18.0.1913, won't work on any previous Plex versions.  
May not work properly on non 'Plex Music' libraries if changed, noticed strange effects sometimes.  
Works OK on brand new Plex Server setup though (empty Plex Media Server folder)

Install
-------
Copy PlexMusic.bundle folder into C:\Program Files (x86)\Plex\Plex Media Server\Resources\Plug-ins-e5cc93306 overwriting existing files.  
On other o/s locate the relevant folder. No other way to do this but to mod existing plex music agent, as plugins won't work with Plex Music agent, so will be overwritten when upgrading Plex Media Server!

Usage
-------
If any of the fields are not set by PlexMusic agent, this will attempt to get them from the nfo file.  
The following fields are read:- 
  artist.nfo = biography, genre, style, mood, tag (tag = added to collection)
  album.nfo = review, label, releasedate, genre, style, mood, tag (tag = doesn't work for album collections though! + releasedate gets displayed wrong by Plex, but is correctly stored internally!)

Plex Advanced Settings changes:-   
  Genres = None => don't load genres, styles, moods for artist or album using PlexMusic agent.  
  Album Art = Local Files Only => load BOTH album AND artist art locally.  
  
Note:- Scanner + Agent must = Plex Music. If PlexMusic cannot match album or artist, then plugin does not get called at all, so NO nfo data gets added! You could use KodiMusicNfo agent for these but it needs agent to be set to Personal Media Artists.


Plex Issues 
-------
Tag fields not added for album? (code is in place but Plex doesn't accept it)  
If artist or album not found by PlexMusic, the agent code is NOT called at all so will not pick up any tags from the .nfo files.  
If you change a music library agent from Plex Music to Personal Media Artists, Plex ignores the change and continues using Plex Music Agent for all existing music. The opposite also applies.  
However if you add NEW music AFTER changing agent, it will use the new agent for those newly added files, so you would end up with music in the same library using different agents! This COULD be used to your advantage but is more likely to just cause confusion. 


License 
-------
If the software submitted to this repository accesses or calls any software provided by Plex (“Interfacing Software”), then as a condition for receiving services from Plex in response to such accesses or calls, you agree to grant and do hereby grant to Plex and its affiliates worldwide a worldwide, nonexclusive, and royalty-free right and license to use (including testing, hosting and linking to), copy, publicly perform, publicly display, reproduce in copies for distribution, and distribute the copies of any Interfacing Software made by you or with your assistance; provided, however, that you may notify Plex at legal@plex.tv if you do not wish for Plex to use, distribute, copy, publicly perform, publicly display, reproduce in copies for distribution, or distribute copies of an Interfacing Software that was created by you, and Plex will reasonable efforts to comply with such a request within a reasonable time.
