#
# Copyright (c) 2019 Plex Development Team. All rights reserved.
#
import os, string, re, unicodedata, sys, urllib, urlparse

NFO_TEXT_REGEX_1 = re.compile(
    r'&(?![A-Za-z]+[0-9]*;|#[0-9]+;|#x[0-9a-fA-F]+;)'
)
NFO_TEXT_REGEX_2 = re.compile(r'^\s*<.*/>[\r\n]+', flags=re.MULTILINE)
RATING_REGEX_1 = re.compile(
    r'(?:Rated\s)?(?P<mpaa>[A-z0-9-+/.]+(?:\s[0-9]+[A-z]?)?)?'
)
RATING_REGEX_2 = re.compile(r'\s*\(.*?\)')

def Start():pass

def GetParentDir(directories):
  parent_dirs = {}
  for d in directories:
    try:
      parent = os.path.split(d)[0]
      parent_dirs[parent] = True
    except:pass
  
  if parent_dirs.has_key(''):
    del parent_dirs['']
  return parent_dirs

#searches for a valid nfo file, loads it up ands returns it
def FindNfo(paths, nfo):
  for path in paths:
    for f in os.listdir(path):
      (fn, ext) = os.path.splitext(f)
      if(fn == nfo and not fn.startswith('.') and ext[1:] == "nfo"):
        nfo_file = os.path.join(path, f)
        nfo_text = Core.storage.load(nfo_file)
        # work around failing XML parses for things with &'s in them. This may need to go farther than just &'s....
        nfo_text = NFO_TEXT_REGEX_1.sub('&amp;', nfo_text)
        # remove empty xml tags from nfo
        nfo_text = NFO_TEXT_REGEX_2.sub('', nfo_text)

        nfo_text_lower = nfo_text.lower()
        if nfo_text_lower.count('<'+nfo) > 0 and nfo_text_lower.count('</'+nfo+'>') > 0:
          # Remove URLs (or other stuff) at the end of the XML file
          content = nfo_text.rsplit('</'+nfo+'>', 1)[0]
          nfo_text = '{content}</{nfo}>'.format(content=content,nfo=nfo)

          # likely a kodi nfo file
          try:
            nfo_xml = XML.ElementFromString(nfo_text).xpath('//'+nfo)[0]
          except:
            Log("ERROR: Cant parse %s from XML in %s Skipping!", nfo, nfo_file)
            continue

          nfo_xml = remove_empty_tags(nfo_xml)
          Log("%s data loaded from file %s", nfo, nfo_file)
          return nfo_xml

def remove_empty_tags(document):
  """
  Removes empty XML tags.

  :param document: An HTML element object.
      see: http://lxml.de/api/lxml.etree._Element-class.html
  :return:
  """
  empty_tags = []
  for xml_tag in document.iter('*'):
    if not(len(xml_tag) or (xml_tag.text and xml_tag.text.strip())):
      empty_tags.append(xml_tag.tag)
      xml_tag.getparent().remove(xml_tag)
  Log('Empty XMLTags removed: {number} {tags}'.format(
    number=len(empty_tags) or None,
    tags=sorted(set(empty_tags)) or ''
  ))
  return document
    
#searches for artist.nfo in Artist folder and adds fields to the metadata if not already set 
def ReadArtistNfo(metadata, paths):
  nfo_xml = FindNfo(paths,'artist')
  if nfo_xml:
    metadata.summary = get_tagnfo(nfo_xml, 'biography', metadata.summary)
    add_tagsnfo(nfo_xml, metadata.genres, 'genre')
    add_tagsnfo(nfo_xml, metadata.styles, 'style')
    add_tagsnfo(nfo_xml, metadata.moods, 'mood')
    add_tagsnfo(nfo_xml, metadata.collections, 'tag') #works

    Log("finished artist nfo import")
   
    
#searches for album.nfo in Album folder and adds fields to the metadata if not already set
def ReadAlbumNfo(metadata, paths):
  nfo_xml = FindNfo(paths,'album')
  if nfo_xml:
    metadata.summary = get_tagnfo(nfo_xml, 'review', metadata.summary)
    metadata.studio = get_tagnfo(nfo_xml, 'label', metadata.studio)    
    metadata.originally_available_at =  get_datenfo(nfo_xml, 'releasedate', metadata.originally_available_at)
    
    add_tagsnfo(nfo_xml, metadata.genres, 'genre')
    add_tagsnfo(nfo_xml, metadata.styles, 'style')
    add_tagsnfo(nfo_xml, metadata.moods, 'mood')
    add_tagsnfo(nfo_xml, metadata.collections, 'tag') #doesn't work? 
    
    Log("finished album nfo import")

#returns existing value or if none, gets from nfo 
def get_tagnfo(nfo_xml, name, value=None):
  try:
    if not value or value == BLANK_FIELD:
      value = nfo_xml.xpath(name)[0].text.strip()
      Log('added <%s> tag = %s... from nfo', name, value[:50])
    else:
      Log('found existing <%s> tag = %s... ignoring nfo', name, value[:50])
    return value
  except:
    Log('Exception getting <%s> tag from nfo', name)

#returns existing date or if none, gets from nfo 
def get_datenfo(nfo_xml, name, value=None):
  try:
    if not value:
      dt = nfo_xml.xpath(name)[0].text.strip()
      value = Datetime.ParseDate(dt, '%Y-%m-%d').date()
      Log('added <%s> tag = %s... from nfo', name, value)
    else:
      Log('found existing <%s> date = %s, ignoring nfo', name, value)
    return value
  except:
    Log('Exception getting <%s> date from nfo', name)

#adds tags from nfo if no existing ones
def add_tagsnfo(nfo_xml, metadata_tags, name):
  try:
    if metadata_tags:
      Log('found %s existing <%s> tags, ignoring nfo', len(metadata_tags), name)
      return
    tags = nfo_xml.xpath(name)
    [metadata_tags.add(t.strip()) for tagXML in tags for t in tagXML.text.split('/')]
    Log('added %s <%s> tags from nfo', len(metadata_tags), name)
  except:
    Log('exception adding <%s> tags from nfo', name)
        
Languages = [Locale.Language.English, Locale.Language.Arabic, Locale.Language.Bulgarian, Locale.Language.Chinese, Locale.Language.Croatian,
             Locale.Language.Czech, Locale.Language.Danish, Locale.Language.Dutch, Locale.Language.Finnish, Locale.Language.French,
             Locale.Language.German, Locale.Language.Greek, Locale.Language.Hungarian, Locale.Language.Indonesian, Locale.Language.Italian,
             Locale.Language.Japanese, Locale.Language.Korean, Locale.Language.NorwegianNynorsk, Locale.Language.Polish,
             Locale.Language.Portuguese, Locale.Language.Romanian, Locale.Language.Russian, Locale.Language.Serbian, Locale.Language.Slovak,
             Locale.Language.Spanish, Locale.Language.Swedish, Locale.Language.Thai, Locale.Language.Turkish, Locale.Language.Vietnamese,
             Locale.Language.Unknown]

BLANK_FIELD = '\x7f'

def StringOrBlank(s):
  if s is not None:
    s = str(s).strip('\0')
    if len(s) == 0:
      s = BLANK_FIELD
  else:
    s = BLANK_FIELD
  return s

def Start():
  HTTP.CacheTime = 0

def find_songkick_events(artist_mbid):
  try: return Core.messaging.call_external_function('com.plexapp.agents.lastfm', 'MessageKit:GetArtistEventsFromSongkickById', kwargs = dict(artist_mbid=artist_mbid))
  except: return None

def add_graphics(object, graphics):
  valid_keys = []
  for i, graphic in enumerate(graphics):
    try:
      key = graphic.get('key')
      preview = graphic.get('previewKey')
      order = '%02d' % (i + 1)
      if key not in object:
        if preview:
          object[key] = Proxy.Preview(HTTP.Request(preview).content, sort_order = order)
        else:
          object[key] = Proxy.Media(HTTP.Request(key), sort_order = order)
      valid_keys.append(key)
    except Exception, e:
      Log('Couldn\'t add poster (%s %s): %s' % (graphic.get('key'), graphic.get('previewKey'), str(e)))

  object.validate_keys(valid_keys)

#bm added flag to handle clearing
def add_tags(res, metadata_tags, name, clr=1):
  #if clr != 2:
  metadata_tags.clear()
  if clr != 0:
    for tag in res.xpath('//Directory/' + name):
      metadata_tags.add(tag.get('tag'))

class PlexMusicArtistAgent(Agent.Artist):
  name = 'Plex Music'
  languages = Languages
  contributes_to = ['com.plexapp.agents.localmedia']

  def search(self, results, media, lang='en', manual=False, tree=None, primary=True):
    pass

  def update(self, metadata, media, lang, prefs):
    Log('#bm Starting PlexMusicArtistAgent')
    Log('Updating : %s (GUID: %s) : %s' % (media.title, media.guid, prefs))

    # Fetch the artist.
    rating_key = media.guid.split('://')[1].split('/')[1]
    url = 'http://127.0.0.1:32400/metadata/agents/music/library/metadata/' + rating_key + '?includeAlternates=1'
    res = XML.ElementFromURL(url)
    artists = res.xpath('//Directory[@type="artist"]')
    if len(artists) == 0:
      return

    # The basics.
    artist = artists[0]
    metadata.title = artist.get('title')
    metadata.title_sort = ''  # artist.get('titleSort')

    summary = artist.get('summary')
    metadata.summary = summary if (prefs['artistBios'] == 1 and summary) else BLANK_FIELD
    #Log('metadata.summary = %s', metadata.summary)

    # Add artist posters and artwork. #bm Use album flag for artists art as well
    if prefs['albumPosters'] != 3:
      add_graphics(metadata.posters, res.xpath('//Directory[@type="artist"]/Thumb'))
      add_graphics(metadata.art, res.xpath('//Directory[@type="artist"]/Art'))
    # else: #bm commented out as unsure if works
      # metadata.posters.validate_keys([])
      # metadata.art.validate_keys([])
    
    # Tags.
    add_tags(res, metadata.genres, 'Genre', prefs['genres'])
    add_tags(res, metadata.styles, 'Style', prefs['genres'])
    add_tags(res, metadata.moods, 'Mood', prefs['genres'])

    add_tags(res, metadata.countries, 'Country')

    # Similar.
    metadata.similar.clear()
    for similar in res.xpath('//Directory[@type="artist"]/Similar'):
      metadata.similar.add(similar.get('tag'))

    # Concerts.
    metadata.concerts.clear()
    if prefs['concerts'] != 0:
      guids = res.xpath('//Directory[@type="artist"]/Guid')
      mbid_guids = [guid.get('id') for guid in guids if guid.get('id').startswith('mbid')]
      if len(mbid_guids) > 0:
        events = find_songkick_events(mbid_guids[0].split('://')[1])
        for event in events:
          try:
            concert = metadata.concerts.new()
            concert.title = event['displayName']
            concert.venue = event['venue']['displayName']
            concert.city = event['venue']['metroArea']['displayName']
            concert.country = event['venue']['metroArea']['country']['displayName']
            concert.date = Datetime.ParseDate(event['start']['date'], '%Y-%m-%d')
            concert.url = event['uri']
          except:
            pass

    Log("started artist nfo import")
    dirs = {}
    
    for a in media.albums:
      for t in media.albums[a].tracks:
        track = media.albums[a].tracks[t].items[0]
        dirs[os.path.dirname(track.parts[0].file)] = True
    
    artist_dirs = GetParentDir(dirs)    
    
    ReadArtistNfo(metadata, artist_dirs) 
    
##################################################################################
class PlexMusicAlbumAgent(Agent.Album):
  name = 'Plex Music'
  languages = Languages
  contributes_to = ['com.plexapp.agents.localmedia']

  def search(self, results, media, lang, manual=False, tree=None, primary=False):
    pass

  def update(self, metadata, media, lang, prefs):
    Log('#bm Starting PlexMusicAlbumAgent')

    # Fetch the album, preferring the instance rating key.
    Log('Updating : %s (GUID: %s) : %s' % (media.title, media.guid, prefs))
    rating_key = media.instanceRatingKey or media.guid.split('://')[1].split('/')[1]
    url = 'http://127.0.0.1:32400/metadata/agents/music/library/metadata/' + rating_key + '?includeAlternates=1&includeChildren=1'
    res = XML.ElementFromURL(url)
    albums = res.xpath('//Directory[@type="album"]')
    if len(albums) == 0:
      return

    # The basics.
    album = albums[0]
    metadata.title = album.get('title')

    summary = album.get('summary')
    metadata.summary = summary if (prefs['albumReviews'] == 1 and summary) else BLANK_FIELD
    metadata.rating = float(album.get('rating') or -1.0) #if (prefs['albumReviews'] == 1) else -1.

    # Release date.
    if album.get('originallyAvailableAt'):
      metadata.originally_available_at = Datetime.ParseDate(album.get('originallyAvailableAt').split('T')[0])
    
    # Posters, if we want them.
    if prefs['albumPosters'] != 3:
      add_graphics(metadata.posters, res.xpath('//Directory[@type="album"]/Thumb'))
    # else: #bm commented out as unsure if works
      # metadata.posters.validate_keys([])

    add_tags(res, metadata.genres, 'Genre', prefs['genres'])
    add_tags(res, metadata.styles, 'Style', prefs['genres'])
    add_tags(res, metadata.moods, 'Mood', prefs['genres'])
    
    metadata.studio = album.get('studio') or BLANK_FIELD

    # Build a map of tracks.
    cloud_tracks = {}
    for track in res.xpath('//Track'):
      cloud_tracks[track.get('guid')] = track

    # Get track data.
    use_rating_count = (prefs['popularTracks'] == 1)
    valid_keys = []
    for track in media.children:
      guid = track.guid
      valid_keys.append(guid)
      metadata_track = metadata.tracks[guid]
      if guid in cloud_tracks:
        cloud_track = cloud_tracks[guid]
        if cloud_track and metadata_track:
          metadata_track.title = cloud_track.get('title')
          metadata_track.track_index = int(cloud_track.get('index'))
          metadata_track.disc_index = int(cloud_track.get('parentIndex') or '1')
          metadata_track.original_title = cloud_track.get('originalTitle') or BLANK_FIELD
          metadata_track.rating_count = int(cloud_track.get('ratingCount') or '0') if use_rating_count else 0
    metadata.tracks.validate_keys(valid_keys)

    Log("started album nfo import")
    dirs = {}
    
    for t in media.tracks:
      track = media.tracks[t].items[0]
      dirs[os.path.dirname(track.parts[0].file)] = True
    
    ReadAlbumNfo(metadata, dirs) 
