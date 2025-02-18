# A few important things about the program
- search_ingredients is my main file
- This program is not perfect, and it could use some work on error handling with the webpage
- This program does not have all the functionality that I originally intented (not even close) but I am still very proud of it, and I look forward to expanding it :)
- Your webdrivers must be
    - a: For your browser
    - b: For your version of the browser
    - The webdriver I'm using is for the most recent version of Chrome (as of writing this)
    - You **must** add your webdriver path to PATH in order for this to work (as far as I know)


# What I learned!
## Fuzzy text matching
Combining any combination of the following methods allows for really, really powerful text matching. Hence spellcheck.
### Edit distance based methods
How many edits does it take to turn one string into another?
- Levenshtein Distance, measures based on insertions, deletions and substitutions
- Damerau-Levenshtien Distance: extends measure to include transpositions
    - Say I have some text like: "liek". Switching "e" and "k" to make "like" would be a transposition
- Hamming distance: Only counts substitutions
    - I'm studying signal processing and this came up when I was taking an FFT, this topic applies much more broadly
### Token-Based Methods
Break down words into small words (tokens) that are individually meaningful.
- Jaccard Similarity: Overlap between two tokens (character matching)
- Cosine Similarity: Represents tokens as vector then calculates the angle
AI models (LLMs) use tokenization as a basis for producing text. Tokens almost definetly have applications in signal processing (I just haven't learned them yet)
### Phonetic Methods
Was a string spelled one way because it sounds right when you sound it out? Was the write (<-) word not actually correct but if you read it outloud everything would be fine?
- You can encode words phonetically so we can match them using different methods
    - Soundex: Old method
    - Metaphone: More accuarate (and complex)
    - Double Metaphone: Gives two encodings for each word so you have options

## ReGex
ReGex is a super powerful tool (available in most programming langauges in some form) for processing text in an exact, well-defined way that at the same time is flexible enough to account for the many variations in strings.
- AI is pretty good at writing ReGex patterns, it wrote pretty much all of mine
    - I figured I should understand all the ReGex patterns so I had AI explain them for me. Here are my notes
        - this one's easy, I wrote it myself `r"\d+"`
            - All ReGex patterns are raw strings
            - This basically says match all decimal values (digits 0-9) in the word
        - `r"<[^>]*>"`
            - "<" matches the opening bracket
            - "[]" means I'm defining a character class
            - "^" means not so "^>" means not ">", the closing bracket
            - "*" means zero or more occurances of. In other words it matches all the occurances of characters that aren't ">"
            - `r"^total\s+"`
                - "^" anchors position to the start of the string
                - "\s+" matches one or more white space characters
            - `r"([a-zA-Z]+)"`
                - Everything in () is a capturing group, it can be accessed later using `re.match().group(1)`
                - "a-z" is any character a-z
                - "A-Z" is any uppercase letter A-Z
                - "+" match one or more occurances of our chacter
                - Captures all letters as a group
            - 
- Using ReGex and fuzzy matching together gives you some pretty hefty algorithms who can handle pretty much anything

## Scraping Notes
- Webscraping it is actually a lot easier to just grab all HTML you can and then process it as text
    - The fewer individual items you have to find the less finicky the program will be
- You have to have try and excepts for everything
    - Websites do not always respond to you exactly how and when you would like, you have to handle it
- XPATH (which is kind of like a file directory but instead it tells you all the divs and stuff your HTML tag is nested in) proved to be the most effective method for finding elements. ID didn't work as often as it should have (and not all elements have an ID) and classes proved unreliable

## General Practices
- Write lots of functions
- Split into multiple files
- Test functions thoroughly and ensure complete functionality before you put it into the code, get everything broken, and have to rewrite your tests. Why would a function work the first time its implemented?
- Keep going, there are a finite number of ways to fail
- Acknowledge that projects that initially seem "difficult but not too difficult" are at least 10x more difficult than you think
- Stack up all the resources you can against your problems. AI, teachers, peers, StackOverflow, YouTube, all of it
