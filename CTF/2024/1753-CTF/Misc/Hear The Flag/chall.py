import mido
from mido import MidiFile, MidiTrack


def text_to_base_7(text):
    text_as_int = int.from_bytes(text.encode(), "big")
    base_7_string = ""
    while text_as_int:
        base_7_string = str(text_as_int % 7) + base_7_string
        text_as_int //= 7
    return base_7_string


def generate_midi(base_7_string, filename="output.mid"):
    scale = {
        "0": [60, 64, 67],
        "1": [62, 65, 69],
        "2": [64, 67, 71],
        "3": [65, 69, 72],
        "4": [67, 71, 74],
        "5": [69, 72, 76],
        "6": [71, 74, 77],
    }

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(50)))

    for digit in base_7_string:
        chord = scale[digit]
        for note in chord:
            track.append(mido.Message("note_on", note=note, velocity=64, time=0))

        track.append(mido.Message("note_off", note=chord[0], velocity=64, time=480))

        for note in chord[1:]:
            track.append(mido.Message("note_off", note=note, velocity=64, time=0))

    mid.save(filename)



if __name__ == "__main__":
    # text = "something"
    # base_7_string = text_to_base_7(text)
    generate_midi("0123456", "0 to 6.mid")
