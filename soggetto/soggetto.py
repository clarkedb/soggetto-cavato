# soggetto.py

import re
import time
from sound import audio_sequence

SOLFEGE_MAP = {
  'a': 'fa',
  'e': 're',
  'i': 'mi',
  'o': 'sol',
  'u': 'ut'
}

NOTE_MAP = {
  'a': 'F',
  'e': 'D',
  'i': 'E',
  'o': 'C',
  'u': 'G'
}

def encode_string(text):
  """Enocdes the text in music using the simple soggetto cavato
  method from the 16th century 'soggetto cavato dalle vocali di
  queste parole.' 

  Prameters:
    text (str): The text to encode in music.

  Returns:
    solfege (list(str)): The solfege terms for the encoding.
    notes (list(str)): The note values for the encoding (e.g. 'C').
  """

  # extract vowels from text
  vowel_pattern = r'[^AEIOU]'
  vowels = re.sub(vowel_pattern, '', text, flags=re.IGNORECASE).lower()

  # encode solfege and notes
  solfege = [SOLFEGE_MAP[v] for v in vowels]
  notes = [NOTE_MAP[v] for v in vowels]

  return solfege, notes

def main():
  """Accept user input, encode it, export the corresponding audio
  and print the encoding to console.
  """
  text = input('Please enter text to be encoded:\n')

  solfege, notes = encode_string(text)
  audio = audio_sequence(notes)

  # export audio
  fname = f'soggetto_cavato_{time.strftime("%Y%m%d-%H%M%S")}.wav'
  audio.export(f'audio/{fname}')

  # print encoding
  print('Solfege:', ' '.join(solfege))
  print('Notes', ' '.join(notes))

if __name__ == '__main__':
  main()
