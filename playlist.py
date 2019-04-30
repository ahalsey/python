def playlist(songs):
    count = 0
    i = 0
    j = 1
    while i < len(songs):
        j = i + 1
        while j < len(songs):
            if (songs[i] + songs[j]) % 60 == 0:
                count = count + 1
            j = j+1

        i = i+1

    return count

songs_count = int(input().strip())

songs = []

for _ in range(songs_count):
    songs_item = int(input().strip())
    songs.append(songs_item)

result = playlist(songs)

print(result)