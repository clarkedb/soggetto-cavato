# Soggetto Cavato Encoder

A python program to encode text into music motifs with one of the early soggetto cavato methods using vowels.

## About Soggetto Cavato

Soggetto Cavanto or 'carved subject' is the practice of taking text and encoding it into music to be included as a motif in a work of music. In western music, this began wit the Renaissance composer Josquin des Prez.

In the 16th century it was described as:

>soggetto cavato dalle vocali di queste parole

Translated literally to:

>a subject 'carved out of the vowels from these words'

It takes the vowels from the text and maps each one to one of five solfege terms correpsonding to five notes.

Read more about Soggetto Cavato [here](https://en.wikipedia.org/wiki/Soggetto_cavato).

## Running the Program

Clone or download this repository:

```bash
git clone https://github.com/clarkedb/soggetto-cavato.git
```

Run the program in Python from the terminal:

```bash
python soggetto/soggeto.py
```

The app with prompt the user for input. This can be any string of characters, but traditionally would be a name.

```python
>>> Please enter text to be encoded:
```

Then the encoding is printed out and the an audio `.wav` file is stored with the motif from the text. For example for the input `Josquin des Prez`:

```python
>>> Josquin des Prez
>>> Solfege: sol ut mi re re
>>> Notes C G E D D
```

with [this audio output](audio/josquin_example.wav).

## Author

Written by Clark Brown in Python.
