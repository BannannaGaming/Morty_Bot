from wordcloud import WordCloud
import matplotlib.pyplot as plt

allvar = "this this this this this is is is a a a testt test ok ok ok ok ok ok ok ok k k k kk k k k k k kk k k k k k kk k kk k k k k k kk k k k k k k kk k kk k kk k this this this this is is is a a a testt test ok ok ok ok ok ok ok ok k k k kk k k k k k kk k k k k k kk k kk k k k k k kk k k k k k k kk k kk k kk k this this this is is is a a a testt test ok ok ok ok ok ok ok ok k k k kk k k k k k kk k k k k k kk k kk k k k k k kk k k k k k k kk k kk k kk k"

wordcloud = WordCloud().generate(allvar)
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig("fig")
plt.show()
