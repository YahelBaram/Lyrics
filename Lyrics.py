import requests
import lyricsgenius as genius
import os

code = input("Enter Genius API code (can create a new one in https://genius.com/api-clients): ") # the API code
songsFind = input("Enter songs folder path: ") # the folder that include the music files
textsave = input("Where do you want to save the lyrics (note: this will be deleted after the end of the program. DO NOT USE A FOLDER WITH OTHER FILES, THEY MAY BE DELETED TOO): ") # the place the lyrics will be saved in (read the warnings!)
title = input("Enter title sign: ") # the thing that will be written before the name of the song (I used "title: ")
fulllyrics = input("Where do you want to save the final result (must be a txt file. not overwriting files): ") # the .txt file that will include the full data
fulllyrics = fulllyrics.replace("\u202a", '') # a bug i found when i tried to copy the name of the file

arr = os.listdir(songsFind) # getting the data in the given folder
dead = ""

api = genius.Genius(code)

for place in arr:

    if place != "מילים": # an old part of the program that I didn't want to remove. can be ignored

        if('~' in place): # if you want to use a protocol I found as useful: artist~albul~number of song in the album~the name of the song
            place2 = place
            place2 = place[place.find("~") + 1 : ]
            place2 = place2[place2.find("~") + 1 : ]
            print(place2)
            place = place[ : place.find('~')] + ' ' + place2[place2.find('~') + 1: place2.find(".mp3")]

        else:
            place = place[: place.find('.')]
            count = place.count('-')
            if(count > 1):
                place = place.replace('-', '&', 1)
                place = place[: place.find('&')] + place[place.find('-'): ]

        place = place.replace("'", '"') # because you can't use " in the file's name I used ' instead

        try:
            search = api.search_song(place) # searching for the lyrics

            l = search.lyrics

        except:
            dead = dead + '\n' + place # if the search failed
        place = place + ".txt"
        place = place.replace('"', '')
        print(textsave+place)
        F = open(textsave + r'\\' + place, 'w')
        F = open(textsave + r'\\' + place, 'a', encoding='utf-8')
        for letter in l:
            try:
                F.write(letter)
            except:
                F.write(' ')
        F.close()

arr = os.listdir(textsave)
final = ""
arr.sort() # sorting the songs
for place in arr:
    print(place)
    f = textsave + r'\\' + place
    F = open(f, 'r', encoding='utf-8')
    F = F.read()

    final = final + "\n\n\n" + title + place[:len(place) - 4] + "\n\n" + F # creating a string with the entire lyrics

print ("\n\n\n\n\n")
print(final)

try:
    file = open(fulllyrics, 'r', encoding='utf-8')
    final = file.read() + final
    file.close()
except:
    print('')

file = open(fulllyrics, 'w', encoding='utf-8')
file = open(fulllyrics, 'a', encoding='utf-8')
final = final.split("\n" + title)
final.sort()  # sorting the lyrics in the list

for place in final:

    if(not(place=="\n\n")):  # fixing a bug i found
        file.write("\n" + title + place + "\n\n")

file.close()

file = open(fulllyrics, 'r', encoding='utf-8')
final = file.read()
final = final.replace("""




""", '\n\n\n')  # fixing a bug i found
final = final.replace("""
""" + title + """


""", '')
file.close()

file = open(fulllyrics, 'w', encoding='utf-8')
file.write(final)

for place in arr:
    os.remove(textsave + r'\\' + place)  # deleting the lyrics files that aren't the final result
print(dead)
