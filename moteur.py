import re

#Préparation et implémentation des primitives d’accès à la base de connaissances
#déclaration des classes

class Fait:
	def __init__(self, fait, numRegle):
		self.fait = fait
		self.numRegle = numRegle
	
class Regle:
	def __init__(self, numRegle, premisse, conclusion):
		self.numRegle= numRegle
		self.premisse= premisse
		self.conclusion= conclusion
		
	def affichage(self):
		return(self.numRegle+": "+", ".join(self.premisse)+" --> "+",".join(self.conclusion))
	
class File:
	def __init__(self, filename):
		self.filename = filename
		
	#la fonction extractFact extrait les faits de la base de faits dans une liste facts
	def extractFact(self):
		facts=[]
		i=0
		with open(self.filename,'r') as f:
			content = f.read()
			if content[0] != "B":
				raise ValueError('Bad Fact File description')
			content = content.split(":")
			faits = content[1].split(",")
			for f in faits:
				fait = Fait (faits[i],-1)
				facts.append(fait)
				i+=1
		return(facts)
		
	#la fonction extractRule extrait les regles de la base de connaissances dans une liste rules
	def extractRule(self):
		rules=[]
		with open(self.filename,'r') as f:
			content = f.read()
			line = content.split("\n") 
			for l in line:
				numRegle, premisse, conclusion = re.split(' si | alors ',l)
				conclusion = conclusion.split(" et ")
				premisse = premisse.split(" et ")
				numRegle = numRegle [numRegle.index("R") : numRegle.index(":")]
				reg = Regle(numRegle,premisse,conclusion)
				rules.append(reg)
		return(rules)
	
#La fonction logique "not"
def non(f):
	if "non " in f:
		newf=f.split("non ")
		f=newf[1]
	else:
		f="non "+f
	return f

#La fonction notExist qui verifie l'existence d'un fait dans la base des faits
def notExist(concl,baseFait):
	not_exist=True
	for f in baseFait:
		if (concl==f.fait or non(concl)==f.fait):
			not_exist=False
	return not_exist

class Trace:
	def __init__(self):
		self.trace=[]
#La fonction saveTrace demande a l'utilisateur si il veut sauvegarder la trace et si oui le faire dans un fichier trace.txt	
	def saveTrace(self):
		msg=input("\nvoulez vous sauvegarder la trace des inferences ? (O/N)  ")
		if msg=="O" or msg=="o":
			with open('trace.txt', 'a') as f:
				f.write("--------\n")
				for t in self.trace:
					f.write(t+'\n')
				
#La fonction afficherBaseFinale affiche a l'utilisateur la base des faits finale
	def afficherBaseFinale(self,facts):
		tr="\nbase des faits finale:"
		self.trace.append(tr)
		i=0
		for f in facts:
			i+=1
			if str(f.numRegle)=="-1":
				fourni="par l'utilisateur"
			else:
				fourni="par la regle "+str(f.numRegle)		
			tr=str(i)+"."+f.fait+": // fourni "+fourni
			self.trace.append(tr)
					
def maximum (conflit):
	max=0
	for r in conflit:
		if len(r.premisse)>max:
			max=len(r.premisse)
			regMax=r
	return(r)

class Chainage: 
	def __init__(self,BR,BF,but):
		self.rules=BR.extractRule()
		self.facts=BF.extractFact()
		self.but=but
		self.tr = Trace()

	def ajoutAuBF(self,regleDeclenche):
		for r in regleDeclenche:
			for c in r.conclusion:
				if not(notExist(c,self.facts)):
					tr="***** erreur : la negation existe dans la base *****\n"
					self.tr.trace.append(tr)
					break
				else:
					newFait= Fait(c,r.numRegle)
					self.facts.append(newFait)
					tr="  "+r.numRegle+" declenchee et ajout du fait **"+newFait.fait+"** a la base des faits"
					self.tr.trace.append(tr)
					if c==self.but:
						tr="  but atteint: "+c+"\n"
						self.tr.trace.append(tr)
						self.tr.afficherBaseFinale(self.facts)
						#self.tr.saveTrace()
						#exit() 
			self.rules.remove(r)
	
		
	def chainageArriere(self,but):
		if (but==""):
			tr="\n ***** erreur: veillez entrer le but *****"
			self.tr.trace.append(tr)
			return(False)
		if (but==self.but):
			tr="\n chainage arriere, but : %s \n"%but
			self.tr.trace.append(tr)
		conflit=[]
		while (self.rules):
			verif=False
			regleDeclenche=[]
			for r in self.rules:
				for c in r.conclusion:
					if but==c:
						conflit.append(r)
						tr="    ---conflit--- "+r.affichage()
						self.tr.trace.append(tr)
						verif=True
						break
			#il n'y a aucune regle qui a notre but comme conclusion
			if (not verif):
				tr=" ***** erreur: il n'y a aucune regle qui a notre but comme conclusion *****"
				self.tr.trace.append(tr)
				return(verif)
			while (len(conflit)!=0):
				regleDeclenche=[]
				verif=True
				reg = maximum(conflit)
				tr="  la regle ayant le nombre max de premisses est "+reg.numRegle
				self.tr.trace.append(tr)
				conflit.remove(reg)
				for p in reg.premisse:
					if (notExist(p,self.facts)):
						if(not self.chainageArriere(p)):
							tr="  on peut pas declencher la regle "+reg.numRegle
							self.tr.trace.append(tr)
							verif=False
							break
				if (len(conflit)==0 and verif==False):
					tr="\n la base de fait ne permet pas de declencher aucune regle"
					self.tr.trace.append(tr)
					return(False)
				if(verif):
					regleDeclenche.append(reg)
					tr="  ajout de la regle **"+reg.numRegle+"** a la BRD"
					self.tr.trace.append(tr)
					self.ajoutAuBF(regleDeclenche)
					return (True)
		return(False)
			
				
				
	def chainageAvant(self,but):
		#controle sur l'existence du but ou sa negation dans la base des faits initiale
		tr="\n chainage avant, but : %s\n"%but
		self.tr.trace.append(tr)
		for f in self.facts:
			if but==f.fait:
				tr="but atteint: "+but+"\n"
				self.tr.trace.append(tr)
				affiche()
				save()
			#exit()
			if non(but)==f.fait:
				tr="erreur : la negation du but existe deja dans la base des faits\n"
				self.tr.trace.append(tr)
				save()
				#exit()
		#conflit
		base_regle_dec=[1]
		while (self.rules and base_regle_dec):
			if but not in self.facts:
				tr="    ---filtrage---"
				self.tr.trace.append(tr)
			base_regle_dec=[]
			for r in self.rules:
				c=0
				for p in r.premisse:
					for f in self.facts:
						if p==f.fait:
							c+=1
				if c==len(r.premisse):
					base_regle_dec.append(r)
					tr="ajout de la regle **"+r.numRegle+"** a la BRD"
					self.tr.trace.append(tr)
			self.ajoutAuBF(base_regle_dec)			
		if but not in f.fait:
			tr="le but n'est pas atteint, la base des faits ne permet pas la déduction de but"
			self.tr.trace.append(tr)
			self.tr.afficherBaseFinale(self.facts)
		if but =="":
			self.tr.afficherBaseFinale(self.facts)
			
def main():
	#Initialisation des listes a utiliser
	rules = []
	facts = []
	trace = []

#affichage des base de connaissances a l'utilisateur
# with open("BC1.txt", 'r') as f:
    # print("\nBase connaissance 1:")
    # print (f.read())
# with open("BC2.txt", 'r') as f:
    # print("\nBase connaissance 2:")
    # print (f.read())
	
#saisie du but et de base de connaissance
  
main()
