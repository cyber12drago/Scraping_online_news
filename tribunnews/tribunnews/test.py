# Python program to generate WordCloud 
  
# importing all necessery modules 
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd 
import collections
  
# Reads 'Youtube04-Eminem.csv' file  
df = pd.read_csv(r"tribunnews-covid19.csv", encoding ="latin-1") 
  
comment_words = '' 
STOPWORDS = ["di", "untuk", "corona","corona," , "covid-19","covid19," ,"covid", "hingga", "ini", "ke", "dari" , "saat" , "pandemi" , "ini" ,"dan", "indonesia" ,"tetap","yang","karena","jika","setelah","akan","selama","bagi","virus","tanpa","juga","ingin","kepada","sebagai","lebih","bersama","jangan","hanya","soal","tidak","ada","para","tapi","tetapi","tak","saya","kita","kami","a","r","dengan","â","yakni","atau","jadi","masih","&","1","2","3","4","5","6","7","8","9","0","mereka","adalah","seperti","itu","selain","pada","telah",",","sudah","tersebut","menjadi","harus","-","agar","pun","ia","dalam"]
stopwords = set(STOPWORDS) #membuang kata yang tidak digunakan

# iterate through the csv file 
for val in df.content: 
      
    # typecaste each val to string 
    val = str(val) 
  
    # split the value 
    tokens = val.split() 
      
    # Converts each token into lowercase 
    for i in range(len(tokens)): 
        tokens[i] = tokens[i].lower() 
      
    comment_words += " ".join(tokens)+" "

  
wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 10).generate(comment_words) 


# plot the WordCloud image                        
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show() 

#show most words
d = collections.defaultdict(int)
for word in comment_words.split():
    if(word not in stopwords):
        d[word] +=1
finalFreq = sorted(d.items(), key=lambda t: t[1], reverse=True)[:100]
print(finalFreq)
#final = Counter(finalFreq)
#final.most_common(100)
