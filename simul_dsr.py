# coding: utf-8
# régles de modulation = commune nouvelle 2018-2019 ; communes nouvelles avant 2017 ; variation 90/120 forfait
# garantie : forfait => 1/2 de n-1 ; cible => 1/2 par n sur 2 n

import csv

def get_dict_db(path):
	with open(path, newline='') as csvfile:	
			db = {}
			reader = csv.reader(csvfile,delimiter=";")
			header = None
			
			r_counter = 0
			for row in reader:
				if r_counter == 0:
					header = row
				else:
					counter = 0
					line_dict = {}
					for e in row:
						line_dict[header[counter].replace("\ufeffCode","Code")] = e
						counter+=1
					db[line_dict["Code INSEE de la commune"]] = line_dict
				r_counter +=1
	return db

class Commune:
	def __init__(self,base,insee):
		self.commune_data ={}
		self._get_params(base,insee)

	def _get_params(self,db,insee):

		commune_data = {"nom_commune":"Nom de la commune",
			"code_insee":"Code INSEE de la commune",
			"commune_pop_dgf":"Population DGF Année N'",
			"commune_effort_fiscal":"Effort fiscal",
			"commune_coeff_zrr":"Commune située en ZRR",
		
			"commune_nouvelle":None, #ne ressort pas du fichier DGCL
			"commune_nouvelle_date_creation":None, #ne ressort pas du fichier DGCL
		
			"commune_pop":"Population INSEE Année N ",
			"commune_bureau_centralisateur":"Bureaux centralisateurs",
			"commune_chef_lieu_arr":"Chef-lieu d'arrondissement au 31 décembre 2014",
		
			"canton_pop":"Pourcentage de la population communale dans le canton",
			"unite_urbaine_pop":"Population DGF des communes de l'agglomération",
			"unite_urbaine_pop_dep":"Population départementale de référence de l'agglomération",
			"unite_urbaine_ville_importante":None, #ne ressort pas du fichier DGCL
			"unite_urbaine_ville_chef_lieu_dep":"Chef-lieu de département agglo",
		
			"canton_chef_lieu_code":"Code commune chef-lieu de canton au 1er janvier 2014",
			"canton_chef_lieu_10k":None, #à déterminer en allant lire les données du chef lieu
			
			"commune_pfi_hab":"Potentiel financier par habitant",
			"commune_pfis":"Potentiel financier superficiaire",
		
			"annee_perte_eligibilite":None, #à récupérer de l'année précédente
			"montant_perte_eligibilite":None, #à récupérer de l'année précédente
		
			"commune_longueur_voirie":"Longueur de voirie en mètres",
			"commune_montagne":"Commune située en zone de montagne",
			"commune_insulaire":"Commune insulaire",
			"commune_pop_3a16":"Population 3 à 16 ans",
		
			"commune_ind_synt":"Indice synthétique",
			"commune_pfi_hab_strate": None, #à récupérer de la note DGCL
			"commune_rev_hab":"Revenu imposable des habitants de la commune"}

		for e in commune_data:
			if commune_data[e]:
				self.commune_data[e] = db[insee][commune_data[e]]


class Legislation:
	def __init__(self,code):
		self._get_params(code)

	def _get_params(self,code):

		L2334_20 = {"elig_seuil_pop_normal":("attribuée aux communes de moins de "," habitants et à certains "),
				"elig_seuil_chef_arr":("chefs-lieux d'arrondissement de moins de "," habitants pour tenir compte, d'une part, ")}

		#Frac 1
		L2334_21 ={"elig_frac_1_crit_pc_pop_canton":("attribuée aux communes dont la population représente au moins "," %"+" de la population du canton, aux communes sièges "),
				"elig_frac_1_agg_pc_pop_dep":("Représentant au moins "," % "+"de la population du département ou "),
				"elig_frac_1_agg_pop_tot":("département ou comptant plus de "," habitants ;"),
				"elig_frac_1_agg_commune_max_pop_presente":("Comptant une commune soit de plus de "," habitants, soit chef-lieu de département "),
				"elig_frac_1_chef_lieu_pop":("Situées dans un canton dont la commune chef-lieu compte plus de "," habitants, à l'exception des communes sièges "),
				"elig_frac_1_diff_pfi":("potentiel financier par habitant est supérieur au "," du potentiel financier moyen par habitant des communes de moins de "),
				# "elig_frac_1_chef_lieu_arr_pop_min":("fraction les chefs-lieux d'arrondissement au 31 décembre 2014, dont la population est comprise entre "," et "),
				# "elig_frac_1_chef_lieu_arr_pop_max":(" et "," habitants, qui n'entrent pas dans les cas prévus aux 1°"),
				# Pas computable à ce stade 
		
				"det_frac_1_pop_lim":("population prise en compte dans la limite de "," habitants ;"),
				"det_frac_1_ecart_pfi_pop_lim":("l'écart entre le potentiel financier moyen par habitant des communes de moins de "," habitants et le potentiel financier par habitant "),
				"det_frac_1_eff_fisc_lim":("l'effort fiscal pris en compte dans la limite de "," ;"),
				"det_frac_1_coeffmaj_zrr":("D'un coefficient multiplicateur égal à "," pour les communes situées en zones de revitalisation rurale telles "),
				"det_frac_1_garantie":("garantie non renouvelable, une attribution égale "," de celle qu'elle a perçue l'année précédente"),
				"det_frac_1_frein_min":("l'attribution d'une commune éligible ne peut être ni inférieure à "," %"),
				"det_frac_1_frein_max":("ni supérieure à "," %")}

		
		#Franc 2
		L2334_22 ={"elig_frac_2_diff_pfi":("dont le potentiel financier par habitant, tel qu'il est défini à l'article L. 2334-4, est inférieur au "," du potentiel financier moyen par habitant des communes "),
		
				"rep_frac_2_env_1":("1° Pour "," %"),
				"rep_frac_2_env_2":("appartenant au même groupe démographique ainsi que par l'effort fiscal plafonné à "," ;"),
				"rep_frac_2_env_3":("2° Pour "," %"),
				"rep_frac_2_env_4":("4° Pour "," %"),
		
				"det_frac_2_env_1_plafond_eff_fisc":("entre le potentiel financier par hectare de la commune et le potentiel financier moyen par hectare des communes de moins de "," habitants."),
		
				"det_frac_2_env_2_maj_mont_ins":("situées en zone de montagne ou pour les communes insulaires, la longueur de la voirie est ",". Pour l'application du présent article"),
		
				"det_frac_2_env_4_pop_max":("en fonction de l'écart entre le potentiel financier par hectare de la commune et le potentiel financier moyen par hectare des communes de moins de "," habitants."),
		
				"det_frac_2_frein_min":("l'attribution au titre de cette fraction d'une commune éligible ne peut être ni inférieure à "," % ni supérieure à"),
				"det_frac_2_frein_max":("% ni supérieure à "," %")}

		#Frac3
		L2334_22_1 = {"elig_frac_3_nb_communes":("La troisième fraction de la dotation de solidarité rurale est attribuée aux "," premières communes"),
				"elig_frac_3_pop_communes":("premières communes de moins de ","10 000 habitants, parmi celles éligibles au moins "),
				"det_frac_3_pc_a":("aux a et b en pondérant le premier par "," %"),
				"det_frac_3_pc_b":("et le deuxième par "," %")}

		#lire L2334_20
		self.L2334_20_code = {}
		
		for e in L2334_20:
			self.L2334_20_code[e] = code["L2334_20"].split(L2334_20[e][0])[-1].split(L2334_20[e][1])[0]

		#lire L2334_21
		self.L2334_21_code = {}
		
		for e in L2334_21:
			self.L2334_21_code[e] = code["L2334_21"].split(L2334_21[e][0])[-1].split(L2334_21[e][1])[0]

		#lire L2334_22
		self.L2334_22_code = {}
		
		for e in L2334_22:
			self.L2334_22_code[e] = code["L2334_22"].split(L2334_22[e][0])[-1].split(L2334_22[e][1])[0]

		#lire L2334_22_1
		self.L2334_22_1_code = {}
		
		for e in L2334_22_1:
			self.L2334_22_1_code[e] = code["L2334_22_1"].split(L2334_22_1[e][0])[-1].split(L2334_22_1[e][1])[0]


c = {}

for e in ["L2334_20","L2334_21","L2334_22","L2334_22_1"]:
	c[e] = open(e+".txt").read()

a = Legislation(c)


db_raw = get_dict_db(input(">> "))
db_communes = []


for e in db_raw:
	db_communes.append(Commune(db_raw,e))






# valeur_point_forfait = None
# valeur_point_perequation_tiers_1 = None
# valeur_point_perequation_tiers_2 = None
# valeur_point_perequation_tiers_3 = None
# valeur_point_perequation_10pc = None

# valeur_point_cible_tiers_1 = None
# valeur_point_cible_tiers_2 = None
# valeur_point_cible_tiers_3 = None
# valeur_point_cible_10pc = None


# Fraction bourg-centre


# nat_pfi_m_10k = "Potentiel financier -10 000"


# # Fraction péréquation
# commune_pfi_hab = None


# nat_pfis_10k = None


# # Fraction cible
# commune_eligible_fraction_bc_p = None
# commune_pop = None

# nat_rev_hab_strate = None

# # Formule répartition bourg-centre

class Simulation:
	def __init__(self, data_communes, legislation_source, legislation_amdt):
		self.data_communes = data_communes
		self.legislation_source = legislation_source
		self.legislation_amdt = legislation_amdt


	def _simulation_generale(self):
		#source
		simulation_source = {}

		for commune in self.data_communes:
			if self._eligible_generale(commune,self.legislation_source.L2334_20_code):
				print(commune.commune_data["nom_commune"]," est éligible")
			else:
				pass


	def _eligible_generale(self,commune,legislation_applicable):
		try:
			if int(commune.commune_data["code_insee"][0:2])<96:
				cinsee = True
			else:
				cinsee = False
		except:
			cinsee = True

		if cinsee:
			if int(commune.commune_data["commune_pop"].replace(" ","")) > int(legislation_applicable["elig_seuil_pop_normal"].replace(" ","")):
				if commune.commune_data["commune_chef_lieu_arr"] != "NON":
					if int(commune.commune_data["commune_pop"].replace(" ","")) > int(legislation_applicable["elig_seuil_chef_arr"].replace(" ","")):
						return False
					else:
						return True
				else:
					return True
			else:
				return True
		else:
			return False

	def _eligible_frac_1(self,commune,legislation_applicable):
		try:
			if int(commune.commune_data["code_insee"][0:2])<96:
				cinsee = True
			else:
				cinsee = False
		except:
			cinsee = True

		if cinsee:
			if int(commune.commune_data["unite_urbaine_pop_dep"]) > int(legislation_applicable["elig_frac_1_agg_pc_pop_dep"]):
				return False
			if int(commune.commune_data["unite_urbaine_pop"].replace(" ","")) > int(legislation_applicable["elig_frac_1_agg_pop_tot"].replace(" ","")):
				return False
			if int(self.data_communes[commune.commune_data["unite_urbaine_ville_chef_lieu_dep"]].commune_data["commune_pop"].replace(" ","")) > legislation_applicable["elig_frac_1_chef_lieu_pop"]:
				return False
			




		

		else:
			return False




	def _calc_dsr_bc(self):
		
		rapport_pfi = 1 + ((nat_pfi_m_10k-commune_pfi_hab)/nat_pfi_m_10k)
		return commune_pop_dgf * rapport_pfi * commune_effort_fiscal * commune_coeff_zrr * valeur_point_forfait

	# Formule répartition fraction péréquation

	def _calc_dsr_perequation(self):
		
		rapport_pfi = 1 + ((nat_pfi_m_10k-commune_pfi_hab)/nat_pfi_m_10k)
		envl_1 = commune_pop_dgf * rapport_pfi * commune_effort_fiscal * valeur_point_perequation_tiers_1

		commune_longueur_voirie_maj = 1
		if commune_montagne :
			commune_longueur_voirie_maj = 2
		if commune_insulaire :
			commune_longueur_voirie_maj = 2

		envl_2 = commune_longueur_voirie * commune_longueur_voirie_maj * valeur_point_perequation_tiers_2

		envl_3 = commune_pop_3a16 * commune_point_perequation_tiers_3

		rapport_pfis = 1 + ((nat_pfis_10k-commune_pfis)/nat_pfis_10k)
		envl_4 = commune_pop_dgf * rapport_pfis * valeur_point_perequation_10pc

		return envl_1 + envl_2 + envl_3 + envl_4


	def _calc_dsr_cible(self):
		rapport_pfi = 1 + ((nat_pfi_m_10k-commune_pfi_hab)/nat_pfi_m_10k)
		envl_1 = commune_pop_dgf * rapport_pfi * commune_effort_fiscal * valeur_point_cible_tiers_1

		commune_longueur_voirie_maj = 1
		if commune_montagne :
			commune_longueur_voirie_maj = 2
		if commune_insulaire :
			commune_longueur_voirie_maj = 2

		envl_2 = commune_longueur_voirie * commune_longueur_voirie_maj * valeur_point_cible_tiers_2

		envl_3 = commune_pop_3a16 * commune_point_perequation_tiers_3

		rapport_pfis = 1 + ((nat_pfis_10k-commune_pfis)/nat_pfis_10k)
		envl_4 = commune_pop_dgf * rapport_pfis * valeur_point_cible_10pc

		return envl_1 + envl_2 + envl_3 + envl_4




s = Simulation(db_communes,a,None)
s._simulation_generale()







