# collect text classification if bds and update elastic

## purpose
The service is designed to receive podcast text from Kafka and categorizes the text as to whether the text supports BDS and adds a column to the Elastic document as to whether it supports BDS and another column as to what the level of support is. I will explain the formula below.

## workflow
1. Receives 2 Base64 encoded codes and decodes them into word lists, one a list of words that indicate high hostility and the other a low hostility level.
2. Reads messages from Kafka in Topic `muezzin_text` (I posted in Service `event_processing`) and extracts the document id and text
3. I calculate the text risk level score based on the occurrence of hostile words.
4. Updates the screen elastically and adds a column to the index if it supports BDS
5. Updates the screen elastically and adds a column indexing the level of support high, medium, or none

## BDS Classification Formula

I score the risk level of the text according to the number of occurrences of a dangerous expression in the text, when there is a category of more dangerous and less dangerous expressions. In my rating, I gave the meaning of the occurrence of a more dangerous expression, 2 times compared to a less dangerous expression.
Then I gave weight to the number of expressions compared to the amount of text.
I represented the ranking as follows:
   - More dangerous phrase = 2 points
   - Less dangerous phrase = point
   - Risk percentage = number of words in the text divided by the total points.

I chose to give a significant factor to the length of the text, because from a long podcast it makes sense that even an Israel supporter would mention a word or two from the list of hostile words, so we need a strong enough ratio of hostile words to the amount of text.
I segmented the classification as follows:
   - Above 0 to 40 - high level of hostility
   - Between 60 and 100 - medium
   - Above 100 is either a very dangerous word for every 200 words or a less dangerous word for every 100 words, which is something that can also be common in regular podcasts, so I classified it as non-hostile