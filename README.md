# Fairy tailor

In this repository I am working on generation of text by using Marks chains. 
This means that generation of next word depends solely on previous word.

## Code and data organization
``` tex
fairy-tailor
├── fairy_parser.py - parser JUST for grimm.txt
├── fairy_tailor.py - generating text (main)
├── grimm.txt - database of Grimms' fairy tales - found online
├── word_list.pkl - pickle file in which are saved words and their frequencies
├── word_list_output.txt - words, next words and their frequencies
```

## How does it work

If word_list.pkl exists, it is loaded. In this file are saved Word() class instances, 
and they have property "self.next_word_list". This property contains all the words that
appeared after this word, and their frequency - how many times they occured after this 
specific word.

After loading all of the words from pickle file, program connects these next words, 
in next_word_list properties, with their class instances, so we could know which words appear
after them.

In the end, text is generated with calling function "generate_text()".
