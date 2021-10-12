# import numpy
import numpy
import random
import time

#runtime
start = time.time()

#group stage results (vals = total wins)
teams = ['Invictus Gaming','Virtus.Pro','OG','T1','Undying','Evil Geniuses','Team Aster','Alliance','Thunder Predator','PSG.LGD','Team Secret','Vici Gaming','Team Spirit','Beastcoast','Quincy Crew','Fnatic','Elephant','SG Esports']
results = {'Invictus Gaming':14,'Virtus.Pro':11,'OG':10,'T1':10,'Undying':9,'Evil Geniuses':9,'Team Aster':5,'Alliance':4,'Thunder Predator':0,'PSG.LGD':15,'Team Secret':10,'Vici Gaming':10,'Team Spirit':10,'Beastcoast':7,'Quincy Crew':6,'Fnatic':6,'Elephant':6,'SG Esports':2}

group_a = ['Invictus Gaming','Virtus.Pro','OG','T1','Undying','Evil Geniuses','Team Aster','Alliance','Thunder Predator']
group_b = ['PSG.LGD','Team Secret','Vici Gaming','Team Spirit','Beastcoast','Quincy Crew','Fnatic','Elephant','SG Esports']

eliminated_teams = ['Thunder Predator','SG Esports']
winners = []

#now set team elo scores by running group stage matches
elos= {}
for team in group_a:
	elos[team] = 1500
for team in group_b:
	elos[team] = 1500

def elo_calc(elos,winner,loser,elo1,elo2):
	#given winner and loser and elos return the updated elo results
	ratio = 400
	k = 40
	#expected score for elo1
	expected_score1 = 1/(1+10**((elo2-elo1)/ratio))
	#expected score for elo2
	expected_score2 = (1-expected_score1)
	elo1_new = elo1 + k*(1-expected_score1)
	elo2_new = elo2 + k*(0-expected_score2)
	elos[winner] = round(elo1_new,1)
	elos[loser] = round(elo2_new,2)

def calc_expected_score(team1,team2,elo1,elo2):
	#expected score for team1
	ratio = 400
	return(1/(1+10**((elo2-elo1)/ratio)))

#list out group stage results to add elo changes
group_matches = {}

#using this to get a printout of matches to fill in results by hand
for index,team in enumerate(group_a):
	for team2 in group_a[(index+1):]:
		group_matches[team+'-'+team2] = 0
for index,team in enumerate(group_b):
	for team2 in group_b[(index+1):]:
		group_matches[team+'-'+team2] = 0

group_matches = {'Invictus Gaming-Virtus.Pro': '2-0', 'Invictus Gaming-OG': '1-1', 'Invictus Gaming-T1': '2-0', 'Invictus Gaming-Undying': '1-1', 'Invictus Gaming-Evil Geniuses': '2-0', 'Invictus Gaming-Team Aster': '2-0', 'Invictus Gaming-Alliance': '2-0', 'Invictus Gaming-Thunder Predator': '2-0', 'Virtus.Pro-OG': '1-1', 'Virtus.Pro-T1': '0-2', 'Virtus.Pro-Undying': '2-0', 'Virtus.Pro-Evil Geniuses': '2-0', 'Virtus.Pro-Team Aster': '2-0', 'Virtus.Pro-Alliance': '2-0', 'Virtus.Pro-Thunder Predator': '2-0', 'OG-T1': '2-0', 'OG-Undying': '1-1', 'OG-Evil Geniuses': '1-1', 'OG-Team Aster': '0-2', 'OG-Alliance': '2-0', 'OG-Thunder Predator': '2-0', 'T1-Undying': '2-0', 'T1-Evil Geniuses': '0-2', 'T1-Team Aster': '2-0', 'T1-Alliance': '2-0', 'T1-Thunder Predator': '2-0', 'Undying-Evil Geniuses': '1-1', 'Undying-Team Aster': '2-0', 'Undying-Alliance': '2-0', 'Undying-Thunder Predator': '2-0', 'Evil Geniuses-Team Aster': '2-0', 'Evil Geniuses-Alliance': '1-1', 'Evil Geniuses-Thunder Predator': '2-0', 'Team Aster-Alliance': '1-1', 'Team Aster-Thunder Predator': '2-0', 'Alliance-Thunder Predator': '2-0', 'PSG.LGD-Team Secret': '1-1', 'PSG.LGD-Vici Gaming': '2-0', 'PSG.LGD-Team Spirit': '2-0', 'PSG.LGD-Beastcoast': '2-0', 'PSG.LGD-Quincy Crew': '2-0', 'PSG.LGD-Fnatic': '2-0', 'PSG.LGD-Elephant': '2-0', 'PSG.LGD-SG Esports': '2-0', 'Team Secret-Vici Gaming': '2-0', 'Team Secret-Team Spirit': '2-0', 'Team Secret-Beastcoast': '0-2', 'Team Secret-Quincy Crew': '2-0', 'Team Secret-Fnatic': '0-2', 'Team Secret-Elephant': '1-1', 'Team Secret-SG Esports': '2-0', 'Vici Gaming-Team Spirit': '2-0', 'Vici Gaming-Beastcoast': '1-1', 'Vici Gaming-Quincy Crew': '2-0', 'Vici Gaming-Fnatic': '1-1', 'Vici Gaming-Elephant': '2-0', 'Vici Gaming-SG Esports': '2-0', 'Team Spirit-Beastcoast': '2-0', 'Team Spirit-Quincy Crew': '2-0', 'Team Spirit-Fnatic': '2-0', 'Team Spirit-Elephant': '2-0', 'Team Spirit-SG Esports': '2-0', 'Beastcoast-Quincy Crew': '1-1', 'Beastcoast-Fnatic': '1-1', 'Beastcoast-Elephant': '0-2', 'Beastcoast-SG Esports': '2-0', 'Quincy Crew-Fnatic': '1-1', 'Quincy Crew-Elephant': '2-0', 'Quincy Crew-SG Esports': '2-0', 'Fnatic-Elephant': '1-1', 'Fnatic-SG Esports': '0-2', 'Elephant-SG Esports': '2-0'}

def calc_group_elo(group_matches,elos):
	#use group results to get post-group elos. also shuffle the dict so that matches are randomly played
	matches = list(group_matches.keys())
	random.shuffle(matches)
	for match in matches:
		#teams
		teams = match.split('-')
		#score
		scores = group_matches[match].split('-')
		if scores[0] == '2':
			elo_calc(elos,teams[0],teams[1],elos[teams[0]],elos[teams[1]])
			elo_calc(elos,teams[0],teams[1],elos[teams[0]],elos[teams[1]])
		elif scores[0] == '1':
			elo_calc(elos,teams[0],teams[1],elos[teams[0]],elos[teams[1]])
			elo_calc(elos,teams[1],teams[0],elos[teams[1]],elos[teams[0]])
		else:
			elo_calc(elos,teams[1],teams[0],elos[teams[1]],elos[teams[0]])
			elo_calc(elos,teams[1],teams[0],elos[teams[1]],elos[teams[0]])


#calculate the post-group elos
calc_group_elo(group_matches,elos)

#now simulate brackets but first write function to simulate a matchup
def simulate_match(team1,team2,elos,n):
	#simulate a match based on best of 1,3,5 games where n is number of wins needed(1,2,3)
	win1 = 0
	win2 = 0
	games = 0
	while True:
		expected_score = calc_expected_score(team1,team2,elos[team1],elos[team2])
		score = random.random()
		games +=1
		#team1 wins
		if score >= expected_score:
			elo_calc(elos,team1,team2,elos[team1],elos[team2])
			win1 +=1
		#team2 wins
		else:
			elo_calc(elos,team2,team1,elos[team2],elos[team1])
			win2 +=1
		if win1 == n:
			return(team1,games)
		elif win2 == n:
			return(team2,games)

#coding in the bracket system. there are 22 total matchups split amongst upper and lower bracket. losses in upper bracket drop teams to lower bracket and losses in lower bracket result in elimination
matchups = {}
for matchup in range(1,23):
	matchups[matchup] = ''

#now manually fill in initial bracket
matchups[1] = 'Invictus Gaming-Team Spirit'
matchups[2] = 'Team Secret-OG'
matchups[3] = 'PSG.LGD-T1'
matchups[4] = 'Vici Gaming-Virtus.Pro'
matchups[5] = 'Undying-Fnatic'
matchups[6] = 'Quincy Crew-Team Aster'
matchups[7] = 'Beastcoast-Alliance'
matchups[8] = 'Evil Geniuses-Elephant'

#manually run each matchup..... lower matchups first
sims = 100000
for i in range(5,9):
	teams = matchups[i].split('-')
	#simulate matches 2000 times to get accurate results
	result = [[teams[0],0],[teams[1],0]]
	for j in range(sims):
		winner,games = simulate_match(teams[0],teams[1],elos,1)
		if winner == teams[0]:
			result[0][1] += 1
		else:
			result[1][1] += 1
	if result[0][1] > result[1][1]:
		eliminated_teams.append(teams[1])
		matchups[i+4] = teams[0]
	else:
		eliminated_teams.append(teams[0])
		matchups[i+4] = teams[1]

#now initial upper bracket matchups
for i in range(1,3):
	teams = matchups[i].split('-')
	#simulate matches 2000 times to get accurate results
	result = [[teams[0],0],[teams[1],0]]
	for j in range(sims):
		winner,games = simulate_match(teams[0],teams[1],elos,2)
		if winner == teams[0]:
			result[0][1] += 1
		else:
			result[1][1] += 1
	if result[0][1] > result[1][1]:
		matchups[13] = matchups[13] + '-' + teams[0]
		if i == 1:
			matchups[9] = matchups[9] + '-' + teams[1]
		else:
			matchups[10] = matchups[10] + '-' + teams[1]
	else:
		matchups[13] = matchups[13] + '-' + teams[1]
		if i == 1:
			matchups[9] = matchups[9] + '-' + teams[0]
		else:
			matchups[10] = matchups[10] + '-' + teams[0]
#simple fix 
matchups[13] = matchups[13][1:]

for i in range(3,5):
	teams = matchups[i].split('-')
	#simulate matches 2000 times to get accurate results
	result = [[teams[0],0],[teams[1],0]]
	for j in range(sims):
		winner,games = simulate_match(teams[0],teams[1],elos,2)
		if winner == teams[0]:
			result[0][1] += 1
		else:
			result[1][1] += 1
	if result[0][1] > result[1][1]:
		matchups[14] = matchups[14] + '-' + teams[0]
		if i == 3:
			matchups[11] = matchups[11] + '-' + teams[1]
		else:
			matchups[12] = matchups[12] + '-' + teams[1]
	else:
		matchups[14] = matchups[14] + '-' + teams[1]
		if i == 3:
			matchups[11] = matchups[11] + '-' + teams[0]
		else:
			matchups[12] = matchups[12] + '-' + teams[0]
#simple fix 
matchups[14] = matchups[14][1:]

for i in range(9,11):
	teams = matchups[i].split('-')
	#simulate matches 2000 times to get accurate results
	result = [[teams[0],0],[teams[1],0]]
	for j in range(sims):
		winner,games = simulate_match(teams[0],teams[1],elos,2)
		if winner == teams[0]:
			result[0][1] += 1
		else:
			result[1][1] += 1
	if result[0][1] > result[1][1]:
		matchups[15] = matchups[15] + '-' + teams[0]
		eliminated_teams.append(teams[1])
	else:
		matchups[15] = matchups[15] + '-' + teams[1]
		eliminated_teams.append(teams[0])
matchups[15] = matchups[15][1:]

for i in range(11,13):
	teams = matchups[i].split('-')
	#simulate matches 2000 times to get accurate results
	result = [[teams[0],0],[teams[1],0]]
	for j in range(sims):
		winner,games = simulate_match(teams[0],teams[1],elos,2)
		if winner == teams[0]:
			result[0][1] += 1
		else:
			result[1][1] += 1
	if result[0][1] > result[1][1]:
		matchups[16] = matchups[16] + '-' + teams[0]
		eliminated_teams.append(teams[1])
	else:
		matchups[16] = matchups[16] + '-' + teams[1]
		eliminated_teams.append(teams[0])
matchups[16] = matchups[16][1:]

for i in range(13,15):
	teams = matchups[i].split('-')
	#simulate matches 2000 times to get accurate results
	result = [[teams[0],0],[teams[1],0]]
	for j in range(sims):
		winner,games = simulate_match(teams[0],teams[1],elos,2)
		if winner == teams[0]:
			result[0][1] += 1
		else:
			result[1][1] += 1

	if result[0][1] > result[1][1]:
		matchups[19] = matchups[19] + '-' + teams[0]
		matchups[i+4] = matchups[i+4] + '-' + teams[1]
	else:
		matchups[19] = matchups[19] + '-' + teams[1]
		matchups[i+4] = matchups[i+4] + '-' + teams[0]
matchups[17] = matchups[17][1:]
matchups[18] = matchups[18][1:]
matchups[19] = matchups[19][1:]

for i in range(15,17):
	teams = matchups[i].split('-')
	#simulate matches 2000 times to get accurate results
	result = [[teams[0],0],[teams[1],0]]
	for j in range(sims):
		winner,games = simulate_match(teams[0],teams[1],elos,2)
		if winner == teams[0]:
			result[0][1] += 1
		else:
			result[1][1] += 1
	if result[0][1] > result[1][1]:
		if i == 15:
			matchups[17] = matchups[17] + '-' + teams[0]
			eliminated_teams.append(teams[1])
		else:
			matchups[18] = matchups[18] + '-' + teams[0]
			eliminated_teams.append(teams[1])
	else:
		if i == 15:
			matchups[17] = matchups[17] + '-' + teams[0]
			eliminated_teams.append(teams[1])
		else:
			matchups[18] = matchups[18] + '-' + teams[0]
			eliminated_teams.append(teams[1])

for i in range(17,19):
	teams = matchups[i].split('-')
	#simulate matches 2000 times to get accurate results
	result = [[teams[0],0],[teams[1],0]]
	for j in range(sims):
		winner,games = simulate_match(teams[0],teams[1],elos,2)
		if winner == teams[0]:
			result[0][1] += 1
		else:
			result[1][1] += 1
	if result[0][1] > result[1][1]:
		matchups[20] = matchups[20] + '-' + teams[0]
		eliminated_teams.append(teams[1])
	else:
		matchups[20] = matchups[20] + '-' + teams[1]
		eliminated_teams.append(teams[0])
matchups[20] = matchups[20][1:]

for i in range(19,20):
	teams = matchups[i].split('-')
	#simulate matches 2000 times to get accurate results
	result = [[teams[0],0],[teams[1],0]]
	for j in range(sims):
		winner,games = simulate_match(teams[0],teams[1],elos,2)
		if winner == teams[0]:
			result[0][1] += 1
		else:
			result[1][1] += 1
	if result[0][1] > result[1][1]:
		matchups[22] = matchups[22] + teams[0]
		matchups[21] = matchups[21] + teams[1]
	else:
		matchups[22] = matchups[22] + teams[1]
		matchups[21] = matchups[21] + teams[0]

for i in range(20,21):
	teams = matchups[i].split('-')
	#simulate matches 2000 times to get accurate results
	result = [[teams[0],0],[teams[1],0]]
	for j in range(sims):
		winner,games = simulate_match(teams[0],teams[1],elos,2)
		if winner == teams[0]:
			result[0][1] += 1
		else:
			result[1][1] += 1
	if result[0][1] > result[1][1]:
		matchups[21] = matchups[21] + '-' + teams[0]
		eliminated_teams.append(teams[1])
	else:
		matchups[21] = matchups[21] + '-' + teams[1]
		eliminated_teams.append(teams[0])

for i in range(21,22):
	teams = matchups[i].split('-')
	#simulate matches 2000 times to get accurate results
	result = [[teams[0],0],[teams[1],0]]
	for j in range(sims):
		winner,games = simulate_match(teams[0],teams[1],elos,2)
		if winner == teams[0]:
			result[0][1] += 1
		else:
			result[1][1] += 1
	if result[0][1] > result[1][1]:
		matchups[22] = matchups[22] + '-' + teams[0]
		eliminated_teams.append(teams[1])
	else:
		matchups[22] = matchups[22] + '-' + teams[1]
		eliminated_teams.append(teams[0])

for i in range(22,23):
	teams = matchups[i].split('-')
	#simulate matches 2000 times to get accurate results
	result = [[teams[0],0],[teams[1],0]]
	for j in range(sims):
		winner,games = simulate_match(teams[0],teams[1],elos,3)
		if winner == teams[0]:
			result[0][1] += 1
		else:
			result[1][1] += 1
	if result[0][1] > result[1][1]:
		winners.append(teams[0])
		eliminated_teams.append(teams[1])
	else:
		winners.append(teams[1])
		eliminated_teams.append(teams[0])




print(matchups)
print(winners)
print(eliminated_teams)

end = time.time()
print(end-start)
