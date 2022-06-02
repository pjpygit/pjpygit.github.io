  if ($.fn.mediaelementplayer) {
            $('audio.mediaElementPlaylist').mediaelementplayer({
                audioWidth: '100%',
                alwaysShowControls: true,
                error: function (media, node) {
                    $(media).parents('.mediaElementPlaylist').addClass('playlist_cannotplay');
                },
                features: ['playlistfeature', 'prevtrack', 'playpause', 'nexttrack', 'current', 'progress', 'duration',  'playlist', 'volume']
            });

            $('video.mediaElementPlaylist').mediaelementplayer({
                stretching: 'responsive',
                playlistposition: 'bottom',
                alwaysShowControls: true,
                alwaysShowPlaylist: true,
                features: ['playlistfeature', 'prevtrack', 'playpause', 'nexttrack', 'current',  'progress', 'duration', 'playlist', 'volume']
            });
        }
