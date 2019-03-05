#This is a quick and dirty program to give sample tests based on Dr. Smith's practice question pools. 
#A command line flag specifies the quiz number
#if the quiz hasn't already been downloaded it will be, and then it will be parsed into two lists
#The question list contains each question and multiple choice answers, and an answer list which has...the answers
#A second flag lets the user choose between a short or full quiz, defaulting to short. 
#Once the quiz is finished, any questions that were answered incorrectly will be saved to a file named out for additional study

import random
import re
import sys
import os
from string import maketrans

url = "http://faculty.etsu.edu/SMITHBJ/s2019/qs/practice_quiz"

if len(sys.argv) < 2:
	print "Usage: python quiz.py <quizNumber> <s/f>"
	sys.exit(1)

if re.match("^[0-9]+",sys.argv[1]):
	print "You picked quiz " + str(sys.argv[1])
	quizNo = str(sys.argv[1])
	url += quizNo+".html"
else:
	print "Usage: python quiz.py <quizNumber> <s/f>"
	sys.exit(1)

shortQuiz = True
if len(sys.argv) > 2:
	if sys.argv[2] == 'f':
		shortQuiz = False



#check to see if file has already been downloaded and stripped
exists = os.path.isfile("./quiz"+quizNo+".txt")

if exists == False:
	a = os.system("wget " + url + " -O quiz"+quizNo+".html") #it was easier to use the system wget to get check for 404
	if a != 0: #if the file doesn't exist, report and exit
		print "Quiz does not exist, check course website\n"
		sys.exit(2)

	os.system("sed -e 's/<[^>]*>//g' quiz"+quizNo+".html > quiz"+quizNo+".txt") #strip the html tags out and save as a text file
	os.remove("./quiz"+quizNo+".html") #delte the html file


quizIn = open("quiz"+quizNo+".txt","r")

line = ""
question = ""
questions = list()
answers = list()
missed = list()

while(True): #loop to read until we get to the first question
	line = quizIn.readline().lstrip()
	if len(line) == 0:
		continue
	if re.match('^[0-9]+\.',line):
		question += line #prime the first iteration of the next loop
		break

qlines = 0
while(True): #loop to read questions
	line = quizIn.readline().lstrip()
	if len(line) == 0:
		continue
	if re.match('([0-9]+[a-z], )+',line) or re.match('^Answers',line): #if we have a match, we've hit the answer portion
		print line
		questions.append(question)
		break
	if re.match('^[0-9]+\.',line) and qlines > 2:#check to see if were at the start of the next quesiton
		questions.append(question)
		qlines = 0
		question = line
	else:
		qlines += 1
		question += line	



trantab = maketrans(".",",") #some question pools have typos where a period saperates answers rather than a comma
if re.match('^Answers',line):
	line = line[8:].lstrip()
print line
ans = line.split(',')
while(len(answers) < len(questions)):
	for a in ans:
		for c in a:
			if(c.isalpha()):
				answers.append(c)
				break
	line = quizIn.readline().lstrip()
	line = line.translate(trantab)
	ans = line.split(',')


if len(answers) != len(questions):
	print("\033[91m\nQuestions and answer lists not equal length.\n\033[0m")
else:
	print("\033[94m\nQuestions and answer lists equal length.\n\033[0m")
correct = 0
if shortQuiz == True:
	for x in range(20):
		qn = random.randint(0,len(questions))
		print(questions[qn])
		ua = raw_input("Answer: ")
		if ua.lower() == answers[qn].lower():
			print("\033[94m You selected: " + ua + " the answer was " + answers[qn] + '\033[0m')
			correct += 1
		else:
			print("\033[91m You selected: " + ua + " the answer was " + answers[qn] + '\033[0m')
			missed.append(qn)
	print "You answered " + str(correct) + " of 20 questions correctly"
	score = correct * 5
	print "You scored a " + str(score)
else:
	for x in range(len(questions)):
		print(questions[x])
		ua = raw_input("Answer: ")
		if ua.lower() == answers[x].lower():
			print("\033[94m You selected: " + ua + " the answer was " + answers[x] + '\033[0m')
			correct += 1
		else:
			print("\033[91m You selected: " + ua + " the answer was " + answers[x] + '\033[0m')
			missed.append(x)
	print "You answered " + str(correct) + " of " + str(len(questions))+ " questions correctly"
	score = correct * (100.0 / len(questions))
	print "You scored a " + str(score)

print "Writing study guide\n"
fileout = open("StudyQuide","w")
for q in missed:
	fileout.write(questions[q] + "\n")

fileout.close()

print "Done\n"

