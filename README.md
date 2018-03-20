# Fairy tailor

In this repository I am working on generation of text by using Marks chains. 
This means that generation of next word depends solely on previous word.
If you want to know more about generating text with Marks chains, you can find a
lot about it [here](https://blog.dataiku.com/2016/10/08/machine-learning-markov-chains-generate-clinton-trump-quotes).

In short, parser will separate text into words that will be saved in order in which they are written. 
Then, for every word we will have a property - list of next words. This list will contain
every word that occured after this specific word somewhere in text. Besides just next wods, it will also
contain how many times some word occured. For example, if you have sentence "I am going to the store, and I will buy something." - 
word "I" will have next_word_list of [("am", 1), ("will", 1)], which means that both word "am" and "will" occured once after word
"I".

These frequencies are important because I implemented roullette wheel selection of next word. So, text
generator will not always choose most likely word to appear, but it will choose most likely word with higher probability.
Here is a [link](https://www.tutorialspoint.com/genetic_algorithms/genetic_algorithms_parent_selection.htm) that might help you understand roullette wheel selection if you haven't done anything with it yet.

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

Every function is documented, so if you want to know more about some specific part of the 
code, please feel free to read its documentation.

Also, be aware that this repository is still a **__work in progress__**.


