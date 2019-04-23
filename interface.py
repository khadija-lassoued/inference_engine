import moteur 
from moteur import Chainage as ch
from moteur import File 
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os

class Root(tk.Tk):
    
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
        
		app=Application(self)
		menuBar=MenuBar(self,app)
		self.config(menu=menuBar)
		app.pack(side='top', fill='both', expand='True', padx=10, pady=10)
        
		StatusBar(self).pack(side='bottom', fill='x')
		
		
class MenuBar(tk.Menu):
	def __init__(self, root,app):
		tk.Menu.__init__(self, root)
		
		def about():
			top = tk.Toplevel()
			top.title("About this application...")

			msg = tk.Message(top, text="Ce programme est un logiciel libre, open source, facile a utiliser, pour generer un mini systeme expert. ")
			msg.pack()

			button = tk.Button(top, text="OK", command=top.destroy)
			button.pack()
		
		projectMenu = tk.Menu(self, tearoff=False)
		projectMenu.add_command(label="Nouveau",command=app.new)
		projectMenu.add_command(label="Ouvrir ...",command=app.open)
		projectMenu.add_command(label="Enregistrer sous ...",command=app.save_as)
		projectMenu.add_separator()
		projectMenu.add_command(label="Quitter", command=root.quit)
		self.add_cascade(label="Projet", menu=projectMenu)
		
		ruleMenu = tk.Menu(self, tearoff=False)
		ruleMenu.add_command(label="Nouveau",command=app.r.new)
		ruleMenu.add_command(label="Ouvrir ...",command=app.r.open)
		ruleMenu.add_command(label="Enregistrer",command=app.r.save)
		ruleMenu.add_command(label="Enregistrer sous ...",command=app.r.save_as)
		self.add_cascade(label="Regles", menu=ruleMenu)
		
		factMenu = tk.Menu(self, tearoff=False)
		factMenu.add_command(label="Nouveau",command=app.f.new)
		factMenu.add_command(label="Ouvrir ...",command=app.f.open)
		factMenu.add_command(label="Enregistrer",command=app.f.save)
		factMenu.add_command(label="Enregistrer sous ...",command=app.f.save_as)
		self.add_cascade(label="Faits", menu=factMenu)
		
		helpMenu = tk.Menu(self, tearoff=0)
		helpMenu.add_command(label="aide")
		helpMenu.add_command(label="a propos...",command=about)
		self.add_cascade(label="?", menu=helpMenu)
		
		
class Application(ttk.Notebook):
	def __init__(self, root):
		ttk.Notebook.__init__(self, root)
		
		self.projectName=""
		self.r=Regle(self)
		self.f=Fait(self)
		
		self.add(self.r, text = "Regle")
		self.add(self.f, text = "Fait")
		self.add(Chainage(self), text = "Chainage")
		
	def new(self):
		self.r.new()
		self.f.new()
		
	def open(self):
		self.projectName=filedialog.askopenfilename(initialdir = ".",title = "Select file",defaultextension=".py",filetypes =(("Text File", "*.py"),("All Files","*.*")))
		cmd="py "+self.projectName
		os.system(cmd)
		self.r.BR="BC.txt"
		self.f.BF="BF.txt"
		rules=(File(self.r.BR).extractRule())
		for r in rules:
			self.r.rules.append(r.numRegle+": si "+' et '.join(r.premisse)+" alors "+'et'.join(r.conclusion))
			self.r.list.insert(self.r.indice,r.numRegle)
			self.r.indice+=1
			self.r.label.config(text="")
		fact=(File(self.f.BF).extractFact())
		for f in fact:
			self.f.facts.append(f.fait)
			self.f.list.insert(self.f.indice,f.fait)
			self.f.indice+=1
			self.f.label.config(text="")
		
	def save_as(self):
		self.projectName=filedialog.asksaveasfilename(initialdir = ".",title = "Select file",defaultextension=".py",filetypes =(("Text File", "*.py"),("All Files","*.*")))
		if self.projectName!="":
			with open(self.projectName, 'w+') as f:
				f.write('BR=["')
				f.write('","'.join(self.r.rules))
				f.write("\"]\n")
				f.write('BF=["')
				f.write('","'.join(self.f.facts))
				f.write("\"]\nwith open(\"BC.txt\", 'w+') as f:")
				f.write("\n 	f.write('\\n'.join(BR))")
				f.write("\nwith open(\"BF.txt\", 'w+') as f:")
				f.write('\n 	f.write("BF:")')
				f.write("\n 	f.write(','.join(BF))")

class StatusBar(ttk.Frame):

	def __init__(self, master):
		ttk.Frame.__init__(self, master)
		self.label = ttk.Label(self, relief='sunken', anchor='w')
		self.label.pack(fill='x')

	def set(self, format, *args):
		self.label.config(text=format % args)
		self.label.update_idletasks()

	def clear(self):
		self.label.config(text="")
		self.label.update_idletasks()
            
class Regle(ttk.Frame):
	def __init__(self, root):
		ttk.Frame.__init__(self, root)
		
		self.rules=[]
		self.BR=""
		
		regle_update = ttk.Panedwindow(self, orient = "horizontal")
		regle_update.pack(fill='both', padx=10, pady=10)
		
		reglCtrl = ttk.Frame(regle_update)
		ttk.Label(reglCtrl, text="Base des regles").pack()
		self.list = tk.Listbox(reglCtrl)
		self.list.bind("<<ListboxSelect>>", self.affiche)
		
		self.indice=1
		self.MAJ=-1
		self.list.pack(side='top', fill='both', padx=10, pady=10)
		tk.Button(reglCtrl, text ='modifier',bg="#83AF98",command=self.update).pack(side='left', padx= 10, pady=5)
		tk.Button(reglCtrl, text ='Supprimer',bg="#83AF98",command=self.delete).pack(side='left', padx=10, pady=5)
		
		self.regleDef = ttk.Frame(regle_update)
		
		ttk.Label(self.regleDef, text="Regle").pack(anchor="w", padx=10)
		self.numReg=tk.Entry(self.regleDef)
		self.numReg.pack(anchor="w",padx=10,pady=5)
		ttk.Label(self.regleDef, text="Si").pack(anchor="nw", padx=10)
		self.premisse=tk.Text(self.regleDef,height=3)
		self.premisse.pack(anchor="nw",fill='both', padx=10,pady=5)
		ttk.Label(self.regleDef, text="Alors").pack(anchor="nw", padx=10)
		self.conclusion=tk.Text(self.regleDef,height=3,pady=5)
		self.conclusion.pack(anchor="nw",fill='both', padx=10)
		self.button=tk.Button(self.regleDef, text ='ajouter',bg="#d0af8e",command=self.insert)
		self.button.pack(anchor="n", padx=10,pady=20)
		self.numReg.bind('<Return>', lambda widget: self.premisse.focus_set(),'break')
		self.premisse.bind('<Return>', lambda widget: self.conclusion.focus_set(),'break')
		
		regle_update.add(reglCtrl)
		regle_update.add(self.regleDef)
		
		regle_final = ttk.Panedwindow(self, orient = "vertical")
		regle_final.pack(fill='both', padx=10, pady=10)
		self.label = ttk.Label(regle_final)
		
		regle_final.add(self.label)
		regle_final.add(tk.Button(regle_final, text ='ouvrir ...',bg="#c48d84",command=self.open))
		regle_final.add(tk.Button(regle_final, text ='Enregistrer',bg="#c48d84",command=self.save))
		regle_final.add(tk.Button(regle_final, text ='Enregistrer sous ...',bg="#c48d84",command=self.save_as))
		
		
		regle_update.pack(fill='both', padx=10, pady=10)
		regle_final.pack(fill='both', padx=10, pady=10)
		
	def insert(self,event=None):
		self.numReg.focus_set()
		regle=self.numReg.get()+": si "+self.premisse.get('1.0', 'end'+'-2c')+" alors "+self.conclusion.get('1.0', 'end'+'-1c')
		if self.MAJ==-1:
			self.list.insert(self.indice,self.numReg.get())
			self.indice += 1
			self.rules.append(regle)
		else:
			self.list.delete(self.MAJ)
			self.list.insert(self.MAJ,self.numReg.get())
			self.rules[self.MAJ]=regle
			self.label.config(text=self.rules[self.MAJ])
		self.numReg.delete(0, 'end')
		self.premisse.delete(0.0, 'end')
		self.conclusion.delete(0.0, 'end')
		
	def delete(self):
		self.rules.remove(self.rules[self.list.curselection()[0]])
		self.list.delete(self.list.curselection())
		
	def affiche(self,event):
		self.label.config(anchor='n',text=self.rules[self.list.curselection()[0]])
		
	def update(self):
		self.MAJ=self.list.curselection()[0]
		rule=self.rules[self.list.curselection()[0]]
		self.numReg.insert('1',rule.split(": si ")[0])
		self.premisse.insert('1.0',(rule.split(": si ")[1]).split("alors ")[0])
		self.conclusion.insert('1.0',(rule.split(": si ")[1]).split("alors ")[1])
		self.button.config(text="OK")
				
	def open(self):
		self.new()
		self.BR=filedialog.askopenfilename(initialdir = ".",title = "Select file",defaultextension=".txt",filetypes =(("Text File", "*.txt"),("All Files","*.*")))
		if self.BR!="":
			try:
				rules=(File(self.BR).extractRule())
				for r in rules:
					self.rules.append(r.numRegle+": si "+' et '.join(r.premisse)+" alors "+'et'.join(r.conclusion))
					self.list.insert(self.indice,r.numRegle)
					self.indice+=1
					self.label.config(text="")
			except ValueError as e:
				self.label.config(anchor='s',text="Echec d'importation: Impossiple d'ouvrir la base des regles. Veuillez d'entrer un fichier valide",foreground = "red")
				
	def save(self):
		if self.BR=="":
			self.save_as()
		else:
			with open(self.BR, 'w') as f:
				f.write('\n'.join(self.rules))
		
	def save_as(self):
		self.BR=filedialog.asksaveasfilename(initialdir = ".",title = "Select file",defaultextension=".txt",filetypes =(("Text File", "*.txt"),("All Files","*.*")))
		if self.BR!="":
			with open(self.BR, 'w+') as f:
				f.write('\n'.join(self.rules))
		
	def new(self):
		self.BR=""
		self.rules=[]
		self.list.delete(0, 'end')

class Fait(ttk.Frame):
	def __init__(self, root):
		ttk.Frame.__init__(self, root)
		
		self.facts=[]
		self.BF=""
		
		fait = ttk.Panedwindow(self, orient = "horizontal")
		fait.pack(fill='both', padx=10, pady=10)
		
		faitCtrl = ttk.Frame(fait)
		ttk.Label(faitCtrl, text="Base des faits").pack()
		self.list = tk.Listbox(faitCtrl)
		self.list.bind("<<ListboxSelect>>", self.affiche)
		self.indice=1
		self.list.pack(side='top', fill='both', padx=10, pady=10)
		tk.Button(faitCtrl, text ='Ajouter',bg="#83AF98",command=self.insert).pack(side='left', padx=10, pady=5)
		tk.Button(faitCtrl, text ='Supprimer',bg="#83AF98",command=self.delete).pack(side='left', padx=10, pady=5)
		
		faitDef = ttk.Frame(fait) 
		ttk.Label(faitDef,text="Fait").pack(side='top', fill='both', padx=10, pady=5)
		self.fact = tk.Text(faitDef,height=5)
		self.fact.bind('<Return>', self.insert)
		self.fact.pack(side='top', fill='both', padx=10, pady=5)
		
		
		fait.add(faitCtrl)
		fait.add(faitDef)
		
		fait_final = ttk.Panedwindow(self, orient = "vertical")
		fait_final.pack(fill='both', padx=10, pady=10)
		self.label = ttk.Label(fait_final)
		
		fait_final.add(self.label)
		fait_final.add(tk.Button(fait_final, text ='ouvrir ...',bg="#c48d84",command=self.open))
		fait_final.add(tk.Button(fait_final, text ='Enregistrer',bg="#c48d84",command=self.save))
		fait_final.add(tk.Button(fait_final, text ='Enregistrer sous ...',bg="#c48d84",command=self.save))
		
		fait.pack()
		fait_final.pack()
		
		self.root=root
	
	def insert(self,event=None):
		fait=self.fact.get('1.0', 'end'+'-1c')
		self.list.insert(self.indice,self.fact.get('1.0', 'end'+'-1c'))
		self.indice += 1
		self.fact.delete(0.0, 'end')
		self.facts.append(fait)

		
	def delete(self):
		self.list.delete(self.list.curselection())
		self.facts.remove(self.list.curselection())
		
	def open(self):
		self.new()
		self.BF=filedialog.askopenfilename(initialdir = ".",title = "Select file",defaultextension=".txt",filetypes =(("Text File", "*.txt"),("All Files","*.*")))	
		if self.BF!="":
			try:
				fact=(File(self.BF).extractFact())
				for f in fact:
					self.facts.append(f.fait)
					self.list.insert(self.indice,f.fait)
					self.indice+=1
			except ValueError as e:
				self.label.config(anchor='s',text="Echec d'importation: Impossiple d'ouvrir la base des faits. Veuillez d'entrer un fichier valide",foreground = "red")
	
	def save(self):
		if self.BF=="":
			self.save_as()
		else:
			with open(self.BF, 'w') as f:
				f.write('\n'.join(self.rules))
		
	def save_as(self):
		self.BF=filedialog.asksaveasfilename(initialdir = ".",title = "Select file",defaultextension=".txt",filetypes =(("Text File", "*.txt"),("All Files","*.*")))
		if self.BF!="":
			open(self.BF, 'a')
			with open(self.BF, 'w') as f:
				f.write("BF:")
				f.write(','.join(self.facts))
	
	def affiche(self,event):
		self.label.config(anchor='s',text=self.facts[self.list.curselection()[0]])
	
	def new(self):
		self.BF=""
		self.facts=[]
		self.list.delete(0, 'end')
		
class Chainage(ttk.Frame):
	def __init__(self, root):
		ttk.Frame.__init__(self, root)
		
		self.root=root
		
		type = ttk.Frame(self)
		ttk.Label(type, text ='Choisir le type de chainage:   ').grid(row =1, column =1, padx=10, pady=10,sticky="w")
		self.typeChainage =  tk.IntVar() 
		self.typeChainage.set(1)
		self.avant=ttk.Radiobutton(type, text="chainage AVANT AVEC CONFLITS (en largeur d'abbord)", variable=self.typeChainage, value=1)
		self.avant.grid(row =1, column =2, sticky="W")
		self.arriere=ttk.Radiobutton(type, text="chainage ARRIERE AVEC CONFLITS (regle ayant le nombre max de premisses)", variable=self.typeChainage, value=2)
		self.arriere.grid(row =2, column =2, sticky="W")
		ttk.Label(type,text="But a atteindre").grid(row =3, column =1, padx=10, pady=10,sticky="w")
		self.but = tk.Text(type,height=3)
		self.but.bind('<Return>', lambda widget : self.chainage())
		self.but.grid(row =3, column =2, padx=10, pady=10)
		
		self.resultat = Resultat(self)
		
		self.label = tk.Label(self, text="", width=20, anchor="w")
		
		type.pack(fill="both",padx=10,pady=10)
		tk.Button(self,text ='Lancer',bg="#83AF98",command=self.chainage).pack(anchor="s")
		self.resultat.pack(fill="both",padx=10,pady=10,expand='True')	
		

	def print_trace(self, message):
		def change_color(tag,color):
			self.resultat.trace.tag_config(tag,foreground=color)
			self.resultat.trace.insert("end", message[0]+'\n',tag)
			
		if "erreur" in message[0] or "n'est pas atteint" in message[0] or "ne permet pas" in message[0]:
			change_color('error','red')
		elif "declenchee et ajout" in message[0]:
			change_color('update','#ec6d18')
		elif "base des faits finale" in message[0] or "chainage" in message[0]:
			change_color('title','#db7b65')
		elif "conflit" in message[0] or "filtrage" in message[0]:
			change_color('conflit','#108070')
		elif "but atteint" in message[0]:
			change_color('but','#2e811d')
		else :
			self.resultat.trace.insert("end", message[0]+'\n')
			
		self.resultat.trace.see("end")
		if len(message) > 1:
			self.after(300, self.print_trace, message[1:])
			
	def error(self,i):
		top = tk.Toplevel()
		top.title("Erreur...")
		
		if i==1:
			errorMsg="Veuillez entrer votre base de connaissance"
		if i==2:
			errorMsg="Veuillez entrer votre base de regle"
		if i==3:
			errorMsg="Veuillez entrer votre base de fait"
		msg = tk.Message(top, text=errorMsg)
		msg.pack()

		button = tk.Button(top, text="OK", command=top.destroy)
		button.pack()
		
	def chainage(self):
		if self.root.r.BR=="" :
			self.error(1)
		elif self.root.r.BR=="":
			self.error(2)
		elif self.root.f.BF=="":
			self.error(3)
		else:
			if self.typeChainage.get()==1:
				self.chainage_avant()
			if self.typeChainage.get()==2:
				self.chainage_arriere()
	
	def chainage_avant(self):
		
		but = self.but.get('1.0', 'end'+'-1c')
		self.c = ch(File(self.root.r.BR),File(self.root.f.BF),but)	
		verif = self.c.chainageAvant(but)
		self.print_trace(self.c.tr.trace)
			
	def chainage_arriere(self):
		
		but = self.but.get('1.0', 'end'+'-1c')
		self.c = ch(File(self.root.r.BR),File(self.root.f.BF),but)	
		verif = self.c.chainageArriere(but)
		self.print_trace(self.c.tr.trace)
		
		
class Resultat(ttk.Labelframe):
	def __init__(self, root):
		ttk.Labelframe.__init__(self, root, text='resultat')
		
		self.root=root
		
		self.tr=[]
		self.trace = tk.Text(self)
		scroll=ttk.Scrollbar(self.trace, orient='vertical',command = self.trace.yview)
		scroll.pack( side = 'right', fill = 'y' )
		self.trace.pack(side='top', fill='both', expand='True', padx=20, pady=20)
		self.trace.configure(yscrollcommand=scroll.set)
		
		
		tk.Button(self, text ='Sauvgarder',bg="#c48d84",command=self.save).pack(side='left', padx=250, pady=20)
		tk.Button(self, text ='Supprimer',bg="#c48d84",command=self.delete).pack(side='right', padx=250, pady=20)
		
	
	def save(self):
		trace=filedialog.asksaveasfilename(initialdir = ".",title = "Select file",defaultextension=".txt",filetypes =(("Text File", "*.txt"),("All Files","*.*")))
		with open(trace, 'w') as f:
			f.write('\n'.join(self.root.c.tr.trace))
	
	def delete(self):
		self.trace.delete(0.0, 'end')
		
root = Root()
root.mainloop()