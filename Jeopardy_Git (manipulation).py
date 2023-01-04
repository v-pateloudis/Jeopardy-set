# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 11:03:02 2022

@author: billp
"""

import pandas as pd
import seaborn as sns
import re

jep = pd.read_csv("C:/Users/billp/Downloads/This is Jeopardy/jeopardy.csv")

pd.set_option("display.max_colwidth", None)
#print (jep.head()); print (jep.columns); print (len(jep))
#print (jep.info())

#the columns are renamed to be easier to use
jep.columns = ["show_number", "air_date", "round", "category", "reward", "question", "answer"]

#EXPLORE
"""This right here is a short script that I designed to take an exploratory look into the columns. 
By calling  the function with a column's number, it quickly prints basic information to help comprehend the data."""

def explore (name):
    
    name = str(jep.columns[name])
    
    print (jep[name].head(5))
    print ("Missing percentage:", jep[name].isnull().sum()/len(jep))

    if type(jep[name][0]) == str:
        
        print (jep[name].unique()); print (len(jep[name].unique()))
        
    elif type(jep[name][0]) != str:
        
        print (jep[name].max()); print (jep[name].min())
        print (jep[name].mean()); print (jep[name].var())
        
        sns.boxplot(x = jep[name])
        plt.show()
        plt.clf()

#explore()

#TIDY
"""The following line converts the rewards from strings into floats, so that they may be analyzed.
Since the format was uniform and simple, there was no need for the use of regular expressions."""

#print (jep.reward.head(20))
jep.reward = jep.apply(lambda x: float("".join(x.reward.split(",")).replace("$", "")) if x.reward != "None" else 0, axis = 1)
#print (jep.reward.head(20)); print (jep.reward.mean()); print (jep.reward.var())

#checking the type of round that was taking place
#print (jep.groupby("round").size())
#checking the most frequent categories
#print (jep.groupby("category").size().sort_values(ascending = False).head(20))

#CHECKING FOR SPECIFIC WORDS
"""While I could use regular expressions to match similar words, the nature of the data (taken from a TV game)
is such that erroneous entries are highly unlikely, so as long as the words provided are typed correctly the 
script should work as intended."""

"""This function checks for questions that contain a certain word or words. Note that if multiple words are
provided, the function returns only the questions that contain all of them. The function returns a list of lists
whose 1st element is the episode's number, and the 2nd element is the question itself."""

def all_word_check (words):
    
    loc = []
    
    for i in range(len(jep)):
        
        """This funky-looking line here does all the checking; specifically, it checks if each word of those 
        provided are included within the individual questions. If the two numbers match, means that there are
        as many TRUE returns as words provided, so the question contains them all."""
        if len(words) == sum(words[word] in jep.iloc[i].question for word in range(len(words))): 
        
            loc.append([jep.iloc[i].show_number, jep.iloc[i].question])
                
    return (loc)

#print (len(all_word_check(["King", "England"])))

"""The folliwing function, unlike the previous one, will be checking if at least *one* of the words provided
are included in a question. Should multiple words be found within the same question, the script will still only 
return one list with the location and the question just like the previous function."""

def one_word_check(words):
    
    loc = []
    
    for i in range(len(jep)):
        
        if sum(words[word] in jep.iloc[i].question for word in range(len(words))) > 0: 
            
            loc.append([jep.iloc[i].show_number, jep.iloc[i].question])
    
    return (loc)

#print (len(one_word_check(["King", "England"])))

#CHECK ANSWERS

"""This following function checks which questions had the same answer. As the number of unique answers are 
a lot fewer than that of unique questions, it is expected that some answers will be featured more than once.
Unlike the previous functions that returned subsets of the dataset, this one returns only a list of 
locations."""

def answer_check(answer):

    loc = []    
    
    for i in range(len(jep)):
        if answer == jep.iloc[i].answer:
            loc.append(i)
    
    return(loc)

#print (jep.iloc[answer_check("Confucius")])