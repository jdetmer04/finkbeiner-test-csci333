Analysis

**Precision and Recall**
Recall: Our model has excellent recall on the 'Not Biased' articles, catching 100% of them. However, its recall is awful (0%) on the two other sets.
Precision: Unfortunately, it is also overpredicting this class to a fairly ridiculous extent. It has identified 13/14 of our test articles as "Not Biased" when only 5 of them were. The one exception was a "Somewhat biased" article incorrectly marked as "Extremely biased". 

**So Why Did This Happen?**
Well, simply, the Finkbeiner test is complicated and our model is simple. Even for human evaluators some of these test cases were pretty complex to navigate, and for a robot with no real prior knowledge of English this challenge is amplified. It would likely take far, far more training data for our model to perform well and recognize patterns, and unfortunately labelling 100 articles was already a lot of work for our small group! 
This reflects common challenges with small scale NLP. With our small training set, the model lacks sufficient data to learn the subtle linguistic cues of bias. Our simple neural architecture was insufficient for this nuanced task.

**Interpretation for Finkbeiner Test:**
If deployed, our system would err heavily on the side of caution, rarely flagging articles as biased. While this avoids false accusations (high recall for unbiased content), it fails the core objective of identifying problematic coverage.

**Honor Code**
We have adhered to the Honor Code on this assignment.
Jackson Detmer
Sylvie Schenck
Hunter Harnphanich


