# Guide de référence : lire les 3 états financiers comme un analyste

*Phase 2 du parcours : analyse fondamentale. Cas pratique : Dollarama, exercice 2026 (clos le 1er février 2026).*
*Rédigé le 20 novembre 2026. Montants en millions de dollars canadiens (M$) sauf mention contraire.*

> Ce guide sert à apprendre. Ce n'est pas une recommandation d'acheter ou de vendre Dollarama ni aucun autre titre, et je ne suis pas conseiller financier.

---

## Sommaire

0. [Les deux pièges de ta dernière séance](#0-les-deux-pièges-de-ta-dernière-séance)
1. [Les 3 états en une page](#1-les-3-états-en-une-page)
2. [Quels chiffres surveiller, état par état](#2-quels-chiffres-surveiller-état-par-état)
3. [Quand regarder : le calendrier des publications](#3-quand-regarder--le-calendrier-des-publications)
4. [Comment analyser la santé d'une entreprise : la méthode en 8 étapes](#4-comment-analyser-la-santé-dune-entreprise--la-méthode-en-8-étapes)
5. [Les signaux d'alerte (*red flags*)](#5-les-signaux-dalerte-red-flags)
6. [Les scores : Piotroski et Altman, et leurs limites](#6-les-scores--piotroski-et-altman-et-leurs-limites)
7. [Cas complet : Dollarama, exercice 2026](#7-cas-complet--dollarama-exercice-2026)
8. [À toi de jouer (Excel ou Google Sheets)](#8-à-toi-de-jouer-excel-ou-google-sheets)
9. [Mini-quiz](#9-mini-quiz)
10. [Sources](#10-sources)

---

## 0. Les deux pièges de ta dernière séance

Tu as eu 3/5 sur les états de Dollarama. Les deux erreurs sont classiques, et une fois corrigées elles ne reviennent plus.

### Piège 1 : le bilan est une **photo**, les flux sont un **film**

- **Bilan** (*balance sheet*, en IFRS « état de la situation financière ») : ce que l'entreprise possède et doit **à une date précise**. Chez Dollarama : « au 1er février 2026 ». C'est un **stock**.
- **État des flux de trésorerie** (*cash flow statement*) : l'argent qui est **entré et sorti pendant l'exercice**, du 3 février 2025 au 1er février 2026. C'est un **flux**.
- **Analogie** : ton compte bancaire. Le solde affiché le 1er février, c'est le bilan. Ton relevé de l'année (paies, loyer, épicerie), c'est l'état des flux.

**Le pont entre les deux** : la variation de trésorerie dans l'état des flux explique exactement le passage d'un bilan à l'autre.

| | M$ |
|---|---:|
| Encaisse au bilan du 2 février 2025 (photo 1) | 122,7 |
| + Variation de trésorerie pendant l'exercice (film) | + 208,9 |
| = Encaisse au bilan du 1er février 2026 (photo 2) | **331,6** |

Même logique pour les stocks : au bilan, ils passent de 921 à 1 103 M$ (+182). Mais l'état des flux n'affiche que −54 M$ pour les stocks. Pourquoi ? Parce que 128 M$ de stocks sont **arrivés avec l'achat de The Reject Shop** en Australie, payés dans la section investissement (« acquisition d'une entreprise »). Deux photos ne disent pas *comment* on est passé de l'une à l'autre : c'est le rôle du film.

### Piège 2 : l'amortissement **augmente** le flux d'exploitation, il ne le réduit pas

L'amortissement (*depreciation and amortization*) est une charge **sans sortie d'argent** : l'argent est sorti le jour où on a acheté l'équipement (dans la section investissement). Dans la méthode indirecte, on part du bénéfice net et on **rajoute** l'amortissement. Il pousse donc le flux d'exploitation **au-dessus** du bénéfice.

Ce qui tire le flux d'exploitation **sous** le bénéfice, c'est surtout une **hausse du fonds de roulement** (*working capital*) : des stocks qui gonflent, des clients qui paient plus lentement, des fournisseurs payés plus vite. Le profit est comptabilisé, mais l'argent est immobilisé dans les tablettes ou chez les clients.

> **Règle à retenir** : flux d'exploitation ≈ bénéfice net **+** amortissement (et autres charges hors caisse) **−** hausse du fonds de roulement.

**Précision importante sur Dollarama 2026.** Les chiffres réels montrent que le flux d'exploitation (**1 761 M$**) est en fait **supérieur** au bénéfice net (**1 309 M$**), un ratio de 1,34. Le fonds de roulement a bien consommé de l'argent (−56 M$, surtout des stocks à −54 M$), mais l'amortissement (+460 M$) et le rajout des frais financiers (+184 M$) l'emportent largement. La bonne façon de le dire est donc :
- quand le flux d'exploitation est **inférieur** au bénéfice, la première cause à chercher est la **hausse du fonds de roulement**, jamais l'amortissement ;
- chez Dollarama 2026, le fonds de roulement a **réduit** le flux de 56 M$, mais pas assez pour le faire passer sous le bénéfice.

Le pont complet est à la [section 7.3](#73-flux-de-trésorerie--le-pont-bénéfice--cash).

---

## 1. Les 3 états en une page

| État | Question à laquelle il répond | Nature | Lignes clés |
|---|---|---|---|
| **État des résultats** (*income statement*) | L'entreprise est-elle rentable **sur la période** ? | Flux (exercice) | Ventes, marge brute, résultat d'exploitation, bénéfice net, BPA |
| **Bilan** (*balance sheet*) | Que possède-t-elle et que doit-elle **à une date** ? | Stock (photo) | Encaisse, stocks, immobilisations, dette, obligations locatives, capitaux propres |
| **Flux de trésorerie** (*cash flow statement*) | D'où vient l'argent et où est-il allé **sur la période** ? | Flux (exercice) | Exploitation, investissement, financement |

**Comment ils s'emboîtent :**
- le bénéfice net (résultats) est la première ligne des flux d'exploitation (méthode indirecte) et alimente les bénéfices non répartis (bilan) ;
- les variations des postes du bilan (stocks, clients, fournisseurs) apparaissent dans le fonds de roulement des flux ;
- la variation de trésorerie (flux) = encaisse de fin moins encaisse de début (bilan).

**Le principe derrière tout ça** : la comptabilité d'exercice (*accrual accounting*). On enregistre une vente quand elle est faite, pas quand elle est encaissée. C'est pour ça que le bénéfice et le cash divergent, et que comparer les deux est le test le plus utile de toute l'analyse.

---

## 2. Quels chiffres surveiller, état par état

Les seuils ci-dessous sont des **ordres de grandeur indicatifs**, pas des règles. Ils varient beaucoup selon le secteur. Compare toujours d'abord l'entreprise **à elle-même dans le temps**, puis **à ses pairs directs**.

### 2.1 État des résultats

| Indicateur | Formule | Ordres de grandeur | Limites et pièges |
|---|---|---|---|
| **Croissance des ventes** | Ventes N / Ventes N−1 − 1 | Mature : 2 à 6 %. Croissance : 10 à 20 %+ | Séparer organique et acquisitions, effet de change, semaine supplémentaire (53 semaines). En commerce de détail, regarder les **ventes des magasins comparables** (*same-store sales*) |
| **Marge brute** (*gross margin*) | Marge brute / ventes | Épicerie 25 à 30 %, magasins à un dollar 35 à 45 %, luxe 60 %+, logiciel 70 à 85 % | Surtout utile **dans le temps** : une marge stable indique un pouvoir de fixation des prix. Ce qu'on met dans le « coût des ventes » varie d'une entreprise à l'autre |
| **Marge d'exploitation** (*operating margin*) | Résultat d'exploitation / ventes | Détail 3 à 10 %, très bon détaillant 10 %+, logiciel 20 à 40 % | Vérifier ce qui est inclus (quote-part d'entreprises associées, gains ponctuels) |
| **Marge BAIIA** (*EBITDA margin*) | BAIIA / ventes | Varie énormément | Le BAIIA ignore le capex et, sous IFRS 16, il ignore aussi **les loyers**. Il gonfle chez les détaillants |
| **Marge nette** | Bénéfice net / ventes | 2 à 20 % selon le secteur | Touchée par les impôts, les intérêts et les éléments non récurrents |
| **BPA dilué** (*diluted EPS*) et sa croissance | Bénéfice net / actions diluées | | Le BPA peut croître plus vite que le bénéfice grâce aux rachats d'actions. Comparer les deux croissances |
| **Taux d'impôt effectif** | Impôts / bénéfice avant impôts | Canada : ~26,5 % (taux combiné fédéral et provincial typique) | Un taux anormalement bas peut ne pas durer (ex. impôt minimum mondial « Pilier Deux ») |
| **Éléments non récurrents** | | | Gains de réévaluation, frais d'acquisition, dépréciations. Les isoler pour estimer le bénéfice « normal » |

### 2.2 Bilan

| Indicateur | Formule | Ordres de grandeur | Limites |
|---|---|---|---|
| **Ratio de liquidité générale** (*current ratio*) | Actif à court terme / passif à court terme | 1 à 2 courant. Détaillants souvent ~1 | Un détaillant qui encaisse comptant et paie ses fournisseurs à 30-60 jours peut vivre avec moins de 1 |
| **Ratio de liquidité immédiate** (*quick ratio*) | (Encaisse + placements + clients) / passif CT | > 1 confortable en industrie | Peu pertinent pour un détaillant (actif CT = surtout des stocks) |
| **Jours de stocks** (DIO, *days inventory outstanding*) | Stock moyen / coût des ventes × 365 | Épicerie 20 à 40 j, magasins à un dollar 80 à 110 j, mode 100 j+ | La **tendance** compte plus que le niveau. Utiliser le stock **moyen**. Attention aux acquisitions en cours d'année |
| **Jours de comptes clients** (DSO, *days sales outstanding*) | Clients moyens / ventes × 365 | Détail : ~0 à 5 j. B2B : 30 à 60 j | Un DSO qui grimpe plus vite que les ventes = signal d'alerte |
| **Jours fournisseurs** (DPO, *days payables outstanding*) | Fournisseurs moyens / coût des ventes × 365 | 30 à 60 j | Un DPO qui s'allonge gonfle le cash **une seule fois** et peut cacher des tensions |
| **Cycle de conversion de trésorerie** (*cash conversion cycle*) | DIO + DSO − DPO | Plus bas = mieux | Négatif chez Costco ou Amazon : les fournisseurs financent l'entreprise |
| **Dette nette / BAIIA** (*net debt / EBITDA*) | (Dette − encaisse) / BAIIA 12 mois | < 1x faible, 1 à 2,5x modéré, > 3 à 4x élevé (sauf services publics, FPI, infrastructures) | **Toujours être cohérent avec IFRS 16** (voir 2.4) |
| **Couverture des intérêts** (*interest coverage*) | Résultat d'exploitation (BAII) / charges d'intérêts | > 8x confortable, 3 à 5x à surveiller, < 2x risqué | Utiliser les intérêts **bruts**, et retirer les revenus non encaissés si on veut être prudent |
| **Goodwill / capitaux propres** | | > 50 % : à creuser | Le goodwill (*écart d'acquisition*) n'est pas amorti en IFRS, seulement déprécié. Une grosse dépréciation signale qu'on a payé trop cher |
| **Capitaux propres tangibles** | CP − goodwill − incorporels | | Peut être faible ou négatif chez les entreprises qui rachètent beaucoup d'actions, sans être un problème en soi |

### 2.3 Flux de trésorerie

| Indicateur | Formule | Ordres de grandeur | Limites |
|---|---|---|---|
| **Conversion du bénéfice en cash** | Flux d'exploitation / bénéfice net | ≥ 1 sur plusieurs années. < 0,8 de façon répétée = alerte | Vérifier où sont classés les **intérêts** (en IFRS, on peut les mettre en financement : le flux d'exploitation paraît alors plus gros) |
| **Capex** (*capital expenditures*) | Achats d'immobilisations + incorporels | Capex / amortissement : ~1 = maintien, > 1 = croissance | Distinguer capex de maintien et de croissance (rarement publié) |
| **Flux de trésorerie disponible** (FCF, *free cash flow*) | Flux d'exploitation − capex | Marge FCF > 10 % = excellente | **Sous IFRS 16, soustraire aussi les paiements de baux** (capital + intérêts) pour comparer avec une entreprise qui possède ses locaux |
| **Accruals de Sloan** | (Bénéfice net − flux d'exploitation) / actif moyen | Négatif = bon. > +10 % = qualité douteuse | Indicateur classique de la qualité des bénéfices (Sloan, 1996) |
| **Utilisation du FCF** | (Dividendes + rachats) / FCF | ≤ 100 % soutenable | > 100 % pendant plusieurs années = financé par la dette |
| **Dilution** | Variation du nombre d'actions diluées | Baisse = rachats. Hausse > 2 %/an = à surveiller | La rémunération en actions (*stock-based compensation*) est une vraie charge même si elle est rajoutée dans les flux |

### 2.4 Deux sujets transversaux à maîtriser

**IFRS 16 et les baux.** Depuis 2019, une entreprise IFRS inscrit presque tous ses baux au bilan : un **actif « droit d'utilisation »** (*right-of-use asset*) et une **obligation locative** (*lease liability*), qui ressemble à une dette. Conséquences :
- le loyer disparaît des charges d'exploitation et devient **amortissement + intérêts**. Le BAIIA gonfle donc mécaniquement ;
- dans les flux, la partie « capital » du loyer passe en **financement**. Le flux d'exploitation gonfle aussi ;
- **règle de cohérence** : soit (dette nette + baux) / BAIIA IFRS 16, soit dette nette / (BAIIA − loyers payés). Jamais dette nette sans baux divisée par un BAIIA qui exclut les loyers : ça flatte l'entreprise ;
- les entreprises américaines (US GAAP, ASC 842) inscrivent aussi les baux au bilan, mais gardent le loyer en charge d'exploitation : les comparaisons Canada/États-Unis demandent des ajustements.

**Les rachats d'actions qui gonflent le ROE.** Le ROE (*return on equity*) = bénéfice net / capitaux propres. Quand une entreprise rachète ses actions au-dessus de leur valeur comptable, elle réduit ses capitaux propres. Le dénominateur fond, le ROE explose, sans que l'entreprise soit plus rentable. Décompose avec **DuPont** : ROE = marge nette × rotation de l'actif × levier (actif / CP). Si le ROE vient surtout du levier, regarde plutôt le **ROA** (bénéfice / actif) ou le **ROIC** (rendement du capital investi, dette comprise).

---

## 3. Quand regarder : le calendrier des publications

### 3.1 Les documents et leurs délais

| Document | Canada (SEDAR+) | États-Unis (EDGAR) | Contenu |
|---|---|---|---|
| **Communiqué de résultats** (*earnings release*) | Le jour même, souvent avant l'ouverture | Formulaire 8-K | Chiffres clés, parfois sans l'état des flux complet |
| **États financiers trimestriels** | Dans les **45 jours** après la fin du trimestre (émetteurs non émergents, Règlement 51-102) | **10-Q** dans les 40 à 45 jours selon la taille | États résumés, non audités (examen limité) |
| **États financiers annuels audités** | Dans les **90 jours** après la fin de l'exercice | **10-K** dans les 60 à 90 jours selon la taille | États complets, notes, rapport de l'auditeur |
| **Rapport de gestion** (MD&A, *management's discussion and analysis*) | Avec chaque série d'états | Section du 10-Q / 10-K | La direction explique les chiffres, les mesures non-IFRS, la liquidité, les risques |
| **Notice annuelle** (AIF, *annual information form*) | Peu après les états annuels | Partie I du 10-K | Description de l'entreprise, facteurs de risque détaillés |
| **Circulaire de sollicitation de procurations** (*proxy circular*) | Avant l'assemblée annuelle | DEF 14A | Rémunération des dirigeants (et leurs critères de bonus !) |
| **Conférence téléphonique** (*earnings call*) | Le jour des résultats | | Questions des analystes : souvent plus révélatrices que le communiqué |

Où chercher : la section « Investisseurs » du site de l'entreprise, **SEDAR+** (sedarplus.ca) au Canada, **EDGAR** (sec.gov/edgar) aux États-Unis. Les délais ci-dessus sont les maximums réglementaires ; les grandes entreprises publient souvent bien avant.

### 3.2 Le rythme chez Dollarama

Exercice de 52 semaines clos le dimanche le plus proche du 31 janvier (53 semaines certaines années, comme l'exercice 2025). Pour l'exercice 2026 :
- **24 mars 2026** : résultats du T4 et de l'exercice, états audités et rapport de gestion (rapport de l'auditeur daté du 23 mars) ;
- **avril 2026** : notice annuelle (datée du 14 avril 2026) et documents de procuration ;
- **11 juin 2026** : T1 de l'exercice 2027 ;
- les T2 et T3 sortent en général en septembre et en décembre. Vérifie les dates exactes sur la page « Investisseurs ».

### 3.3 Quoi regarder à chaque publication

**Chaque trimestre (30 minutes) :**
1. Ventes et ventes des magasins comparables, en **année sur année** (même trimestre l'an dernier) : le commerce de détail est saisonnier, donc comparer le T4 au T3 n'a pas de sens.
2. Marge brute et marge d'exploitation : variation en points de base.
3. Stocks et jours de stocks : grimpent-ils plus vite que les ventes ?
4. Flux d'exploitation **cumulés depuis le début de l'exercice** (un trimestre seul est bruité par le fonds de roulement).
5. Dette nette et ratio d'endettement publié par la société.
6. Changement de prévisions (*guidance*) et commentaires de la direction.

**Chaque année (2 à 3 heures) :**
1. Rapport de l'auditeur : opinion sans réserve ? Questions clés de l'audit (*key audit matters*) ?
2. Notes : méthodes comptables, changements d'estimation, baux, dette (échéances, taux), regroupements d'entreprises, éventualités.
3. Les ratios des sections 2.1 à 2.3 sur **5 à 10 ans** : on cherche des tendances, pas un chiffre isolé.
4. Rapprochement des mesures non-IFRS avec les chiffres IFRS.
5. Comparaison avec 2 ou 3 **pairs** (pour Dollarama : Dollar Tree, Dollar General, Walmart, Costco, en ajustant pour IFRS / US GAAP).

| Comparaison | Sert à | Piège |
|---|---|---|
| Trimestre sur trimestre (T/T) | Repérer une rupture brutale | Saisonnalité |
| Année sur année (A/A) | La comparaison standard | Semaine supplémentaire, acquisitions |
| 5 à 10 ans | Voir le cycle complet et la tendance de fond | Changements de normes (IFRS 16 en 2019) |
| Pairs | Juger si une marge est « bonne » | Normes et modèles d'affaires différents |

---

## 4. Comment analyser la santé d'une entreprise : la méthode en 8 étapes

1. **Comprendre le modèle d'affaires** (avant tout chiffre). Comment l'entreprise gagne-t-elle de l'argent ? Qui paie, combien, à quelle fréquence ? Quels sont les coûts principaux ?
2. **Croissance** : ventes sur 5 ans, organique vs acquisitions, volume vs prix. Chez un détaillant : magasins comparables + nouveaux magasins.
3. **Rentabilité** : marges brute, d'exploitation, nette, stables ou en tendance ? ROIC supérieur au coût du capital (~8 à 10 %) ?
4. **Qualité des bénéfices** : flux d'exploitation / bénéfice ≥ 1 sur plusieurs années ? Accruals négatifs ? Éléments non récurrents ? Bénéfices comptables non encaissés (quote-part d'entreprises associées, gains de réévaluation) ?
5. **Fonds de roulement** : DIO, DSO, DPO et leur tendance comparée aux ventes.
6. **Solidité financière** : dette nette + baux / BAIIA, couverture des intérêts, échéances de la dette, liquidité, notation de crédit.
7. **Utilisation du cash** : capex (maintien vs croissance), acquisitions, dividendes, rachats. Le tout est-il financé par le FCF ou par la dette ? Les rachats se font-ils à un prix raisonnable ?
8. **Signaux d'alerte et scores** : passe la checklist de la section 5, calcule Piotroski et Altman en gardant leurs limites en tête, puis écris en 5 lignes ta conclusion sur la santé de l'entreprise (pas sur son prix, qui est une autre question : l'évaluation vient plus loin dans le parcours).

> **Biais à surveiller** : le **biais de confirmation**. Quand on aime une entreprise, on cherche les chiffres qui nous donnent raison. Commence toujours par chercher ce qui pourrait aller mal.

---

## 5. Les signaux d'alerte (*red flags*)

| Signal | Pourquoi c'est inquiétant | Où le voir |
|---|---|---|
| **Bénéfice en hausse, flux d'exploitation en baisse** (plusieurs trimestres) | Le profit n'est pas encaissé : ventes à crédit agressives, stocks invendus, estimations optimistes | Résultats vs flux |
| **Stocks qui croissent plus vite que les ventes** | Produits qui ne se vendent pas, risque de soldes et de dépréciation | Bilan, DIO |
| **Comptes clients qui croissent plus vite que les ventes** | Ventes « poussées » ou clients qui ne paient pas | Bilan, DSO |
| **DPO qui s'allonge fortement** | Gonfle le cash une fois. Peut cacher une difficulté à payer | Bilan, DPO |
| **Goodwill élevé** et acquisitions en série | Croissance achetée, risque de dépréciation, comparaisons difficiles | Bilan, notes sur les regroupements |
| **Ajustements non-IFRS abusifs** | « BAIIA ajusté » qui exclut chaque année des charges dites « exceptionnelles », exclusion de la rémunération en actions | Rapport de gestion : rapprochement |
| **Éléments non récurrents… récurrents** | Restructurations tous les ans = coût normal de l'activité | Résultats, notes |
| **Changement de méthode comptable ou d'auditeur**, retard de publication | Peut annoncer des problèmes | Notes, rapport de l'auditeur |
| **Dividendes + rachats > FCF** plusieurs années de suite | Financés par la dette, pas soutenable indéfiniment | Flux de financement |
| **Dette qui monte plus vite que le BAIIA**, échéances concentrées | Risque de refinancement, surtout si les taux montent | Notes sur la dette |
| **Dilution forte** | Rémunération en actions qui transfère de la valeur aux employés | Nombre d'actions diluées |
| **Bénéfices comptables non encaissés** | Quote-part d'entreprises associées, gains de juste valeur | Résultats vs flux |
| **Capex durablement inférieur à l'amortissement** | Sous-investissement qui gonfle le FCF à court terme | Flux d'investissement |

Un signal seul n'est **pas** une preuve. C'est une question à poser. L'exemple des stocks de Dollarama (section 7.4) montre qu'un signal apparent peut avoir une explication parfaitement saine.

---

## 6. Les scores : Piotroski et Altman, et leurs limites

### 6.1 Piotroski F-Score (2000)

Neuf tests binaires (1 point chacun) sur la rentabilité, l'endettement et l'efficacité :

| # | Test | Groupe |
|---|---|---|
| 1 | Bénéfice net > 0 | Rentabilité |
| 2 | Flux d'exploitation > 0 | Rentabilité |
| 3 | ROA en hausse | Rentabilité |
| 4 | Flux d'exploitation > bénéfice net | Qualité |
| 5 | Dette à long terme / actif en baisse | Endettement |
| 6 | Ratio de liquidité en hausse | Liquidité |
| 7 | Pas d'émission d'actions | Dilution |
| 8 | Marge brute en hausse | Efficacité |
| 9 | Rotation de l'actif en hausse | Efficacité |

Lecture : 8-9 = solide, 0-2 = fragile. **Limites** : conçu en 2000 pour trier des actions **« value »** (ratio valeur comptable / cours élevé), donc des entreprises bon marché et souvent en difficulté. Les tests sont binaires (45,0 % contre 45,1 % de marge brute coûte un point), et une acquisition ou IFRS 16 font bouger l'actif sans rien dire de la santé réelle.

### 6.2 Altman Z-Score (1968)

Prédit le risque de faillite à 2 ans avec 5 ratios :

**Z = 1,2 X1 + 1,4 X2 + 3,3 X3 + 0,6 X4 + 1,0 X5**

- X1 = fonds de roulement / actif total
- X2 = bénéfices non répartis / actif total
- X3 = BAII / actif total
- X4 = capitalisation boursière / passif total
- X5 = ventes / actif total

Zones : > 2,99 « sûre », 1,81 à 2,99 « grise », < 1,81 « détresse ».
Variante **Z''** pour les entreprises non manufacturières : Z'' = 6,56 X1 + 3,26 X2 + 6,72 X3 + 1,05 X4'' (X4'' = capitaux propres **comptables** / passif), zones > 2,60 et < 1,10.

**Limites** : calibré sur 66 manufacturières américaines des années 1950-60. Le X4 dépend du cours de bourse (une action chère « sauve » le score). Le X2 est détruit par les rachats d'actions et les dividendes (bénéfices non répartis faibles ou négatifs sans difficulté réelle). Il ignore les baux hors bilan dans sa version d'origine. Il n'est pas fait pour les banques, les assureurs ou les FPI.

> Les scores sont des **filtres**, pas des verdicts. Ils servent à repérer quoi creuser.

---

## 7. Cas complet : Dollarama, exercice 2026

**Contexte.** Dollarama (TSX : DOL), Mont-Royal (Québec). Magasins à prix fixes jusqu'à 5 $. Au 1er février 2026 : **1 691 magasins au Canada** et **402 en Australie** (The Reject Shop, acheté le 21 juillet 2025). Participation dans **Dollarcity** en Amérique latine (60,1 % de CARS, comptabilisée à la valeur de consolidation, donc une simple quote-part du bénéfice dans les résultats). Exercice 2026 = 52 semaines, contre **53 semaines** pour l'exercice 2025.

Tous les calculs sont dans [calculs_dollarama.py](calculs_dollarama.py), résultats bruts dans [resultats_calculs.txt](resultats_calculs.txt).

### 7.1 État des résultats

| M$ | Ex. 2026 | Ex. 2025 | Ex. 2024 |
|---|---:|---:|---:|
| Ventes | 7 255,8 | 6 413,1 | 5 867,3 |
| Croissance des ventes | 13,1 % | 9,3 % | 16,1 % |
| Ventes des magasins comparables (Canada) | +4,2 % | +4,6 % | |
| Marge brute | 45,0 % | 45,1 % | 44,5 % |
| Frais généraux (VGA) / ventes | 15,1 % | 14,5 % | 14,4 % |
| BAIIA (publié) | 2 408,2 | 2 121,8 | 1 861,2 |
| Marge BAIIA | 33,2 % | 33,1 % | 31,7 % |
| Résultat d'exploitation | 1 937,9 | 1 710,7 | 1 495,7 |
| Marge d'exploitation | 26,7 % | 26,7 % | 25,5 % |
| Bénéfice net | 1 309,4 | 1 168,5 | 1 010,5 |
| Marge nette | 18,0 % | 18,2 % | 17,2 % |
| BPA dilué | 4,73 $ | 4,16 $ | 3,56 $ |
| Taux d'impôt effectif | 25,8 % | 24,5 % | |

**Lecture :**
- **Croissance** : +13,1 % malgré une semaine de moins que l'an dernier. Mais l'Australie apporte 454,8 M$ de ventes sur 6,5 mois. Sans elle, les ventes canadiennes (6 800,9 M$) progressent d'environ 6 %. La croissance organique se décompose en magasins comparables +4,2 % (2,4 % de transactions en plus, panier moyen +1,7 %) et 75 nouveaux magasins nets au Canada.
- **Marges** : la marge brute est remarquablement stable à 45 %, très élevée pour du commerce de détail. Les frais VGA montent de 0,6 point, en partie parce que The Reject Shop a un modèle moins rentable (marge brute d'environ 37 %, résultat d'exploitation de 5,7 M$ seulement sur 454,8 M$ de ventes).
- **Attention au BAIIA** : la marge de 33 % est gonflée par IFRS 16. Les loyers des magasins n'y sont pas déduits (ils sont devenus amortissement + intérêts). Après loyers payés (390 M$), le BAIIA tombe à environ 2 018 M$, soit **~27,8 %** des ventes.
- **Éléments à isoler** :
  - **quote-part de Dollarcity** : 191,5 M$, soit **9,9 % du résultat d'exploitation**. C'est un bénéfice comptable : Dollarama n'a reçu que **106,6 M$ en cash** (distributions) ;
  - **gain non réalisé** de 10,3 M$ sur un dérivé lié à Dollarcity (option d'achat), non récurrent, environ 0,03 $ de BPA ;
  - **taux d'impôt** en hausse (25,8 % contre 24,5 %), en partie dû à une provision pour l'impôt minimum mondial (Pilier Deux) selon le rapport de gestion.
- **BPA vs bénéfice** : le bénéfice net croît de 12,1 %, le BPA de 13,7 %. L'écart vient des **rachats d'actions** (−1,5 % d'actions diluées en moyenne).

### 7.2 Bilan

| M$ | 1er févr. 2026 | 2 févr. 2025 |
|---|---:|---:|
| Encaisse | 331,6 | 122,7 |
| Stocks | 1 103,2 | 921,1 |
| Actif à court terme | 1 522,0 | 1 201,3 |
| Droits d'utilisation (baux) | 2 397,2 | 2 109,4 |
| Immobilisations corporelles | 1 258,5 | 1 046,4 |
| Goodwill | 801,7 | 727,8 |
| Participations (Dollarcity) | 1 285,1 | 1 131,7 |
| **Actif total** | **7 558,4** | **6 482,6** |
| Passif à court terme | 1 348,2 | 1 014,3 |
| Dette totale (CT + LT) | 2 625,1 | 2 282,7 |
| Obligations locatives (CT + LT) | 2 770,5 | 2 427,0 |
| **Capitaux propres** | **1 455,9** | **1 188,3** |
| Bénéfices non répartis | 128,9 | −225,3 |

| Ratio | 2026 | 2025 | Lecture |
|---|---:|---:|---|
| Liquidité générale | 1,13 | 1,18 | Normal pour un détaillant qui vend comptant |
| Liquidité immédiate | 0,27 | 0,17 | Peu pertinent ici (actif CT = surtout des stocks) |
| Dette nette | 2 293,6 | 2 160,0 | |
| Dette nette / BAIIA (sans baux) | 0,95x | 1,02x | **Incohérent** : à ne pas utiliser |
| Dette nette / (BAIIA − loyers payés) | 1,14x | 1,20x | Cohérent, modéré |
| (Dette nette + baux) / BAIIA | 2,10x | 2,16x | Cohérent. La société publie **2,07x** (elle ajoute 6 mois de BAIIA australien d'avant l'achat) |
| Couverture : résultat d'exploitation / frais financiers nets | 10,5x | 10,4x | Confortable |
| Couverture prudente : (résultat d'exploitation − quote-part Dollarcity) / intérêts bruts | 8,3x | 8,2x | Toujours confortable |
| Goodwill / capitaux propres | 55 % | 61 % | Élevé, mais vient surtout du rachat par Bain Capital en 2004, pas d'acquisitions en série |
| Capitaux propres tangibles | 475,9 | 279,8 | Faibles à cause des rachats (voir 7.5) |

**Lecture** : l'endettement est réel mais maîtrisé, et doit inclure les baux puisque presque tous les magasins sont loués. Les intérêts sont bien couverts. La société a émis 600 M$ d'obligations à 3,85 % et remboursé 250 M$ à 5,084 % pendant l'année.

### 7.3 Flux de trésorerie : le pont bénéfice → cash

C'est l'état qui manquait dans le communiqué. Le voici, tiré des états audités :

| Flux d'exploitation 2026 | M$ | Pourquoi |
|---|---:|---|
| Bénéfice net | 1 309,4 | Point de départ |
| + Amortissement total | **+460,0** | Charge sans sortie d'argent (inclut 31 M$ d'amortissement des entrepôts logé dans le coût des ventes) |
| + Rémunération en actions | +16,0 | Charge payée en actions, pas en cash |
| + Frais financiers nets | **+184,0** | Rajoutés ici parce que Dollarama classe les intérêts payés **en financement** (choix permis en IFRS) |
| − Impôts différés | −8,8 | |
| − Gain non réalisé (dérivé) | −10,3 | Gain comptable, pas de cash |
| − Quote-part de Dollarcity | **−191,5** | Bénéfice comptable non encaissé (les distributions reçues sont en investissement) |
| + Intérêts reçus | +25,6 | |
| + Autres | +32,7 | Surtout la provision Pilier Deux |
| **− Hausse du fonds de roulement** | **−55,9** | Stocks −54,3, frais payés d'avance −21,9, impôts −17,3, fournisseurs +37,9 |
| **= Flux d'exploitation** | **1 761,2** | |

**Ce que ça t'apprend sur ton piège 2** : l'amortissement (+460) pousse le flux **vers le haut**. Le fonds de roulement (−56) le tire **vers le bas**. Ici le premier l'emporte, d'où un flux de 1,34 fois le bénéfice.

**Mais attention au classement des intérêts.** Dollarama met tous ses intérêts payés en financement. Pour comparer avec une entreprise qui les met en exploitation, retire-les :

| Mesure | 2026 | 2025 |
|---|---:|---:|
| Flux d'exploitation / bénéfice net | 1,34x | 1,41x |
| (Flux d'exploitation − intérêts payés sur dette et baux) / bénéfice net | **1,18x** | 1,24x |

### 7.4 Fonds de roulement : un « signal d'alerte » qui n'en est pas un

À première vue : **stocks +19,8 %**, ventes +13,1 %. Les stocks croissent plus vite que les ventes : c'est un des signaux de la section 5. Creusons.

| | M$ |
|---|---:|
| Stocks au 2 février 2025 | 921,1 |
| + Stocks reçus avec The Reject Shop (21 juillet 2025, note 6) | +127,8 |
| + Hausse « organique » (= la ligne stocks de l'état des flux) | +54,3 |
| = Stocks au 1er février 2026 | 1 103,2 |

Hors acquisition, les stocks montent de **5,9 %**, soit moins que les ventes. Le signal est expliqué.

| Ratio | 2026 | 2025 |
|---|---:|---:|
| Jours de stocks (stock moyen) | 93 j | 95 j |
| Jours de stocks (stock de fin) | 101 j | 96 j |
| Jours de stocks (fin, coût des ventes australien annualisé, approx.) | ~95 j | |
| Rotation des stocks | 3,9x | 3,8x |
| Jours de comptes clients (DSO) | 2 j | |
| Jours fournisseurs (DPO, inclut charges à payer) | 37 j | |
| Cycle de conversion de trésorerie | ~57 j | |

**Leçon** : le DIO de fin d'année (101 j) est faussé parce qu'on divise un stock **complet** de l'Australie par seulement **6,5 mois** de coût des ventes australien. C'est exactement le piège « photo vs film » : le bilan (photo) contient toute l'Australie, l'état des résultats (film) n'en contient qu'une moitié. Un DSO de 2 jours est normal : les clients paient à la caisse.

### 7.5 FCF, rachats et ROE gonflé

| M$ | 2026 | 2025 |
|---|---:|---:|
| Flux d'exploitation | 1 761,2 | 1 644,1 |
| − Capex (immobilisations + incorporels) | −272,8 | −243,4 |
| **= FCF « simple »** | **1 488,4** | 1 400,7 |
| − Paiements de baux (capital 291,2 + intérêts 99,1) | −390,3 | −317,8 |
| − Intérêts payés sur la dette | −114,5 | −108,5 |
| **= FCF ajusté (comparable à une entreprise propriétaire de ses locaux)** | **983,5** | 974,4 |
| FCF ajusté / bénéfice net | 0,75x | 0,83x |
| Marge FCF ajusté | 13,6 % | 15,2 % |
| Dividendes + rachats | 977,6 | 1 188,0 |
| (Dividendes + rachats) / FCF ajusté | **99 %** | 122 % |

**Lecture** :
- Le FCF « simple » (1 488 M$) surestime le cash vraiment disponible, parce qu'il oublie les loyers et les intérêts. L'écart entre 1 488 et 984 M$ (−34 %), c'est **l'effet IFRS 16 + classement des intérêts**.
- Capex / amortissement = 0,59x. Ce n'est pas forcément du sous-investissement : l'amortissement inclut celui des droits d'utilisation (les baux), qui n'est pas du capex. Il faut donc comparer le capex à l'amortissement des **immobilisations corporelles** seulement.
- Dollarama redistribue presque **100 % de son FCF ajusté** (surtout en rachats : 834 M$ pour 4,4 millions d'actions à ~192 $ en moyenne). En 2025, elle a redistribué 122 % : la différence vient de la dette. L'achat de The Reject Shop (182 M$) et l'apport à Dollarcity Mexique (50 M$) ont été financés par la hausse nette de la dette (+350 M$).

**Le ROE de 99 % : décomposition DuPont**

| Composante | 2026 |
|---|---:|
| Marge nette | 18,0 % |
| × Rotation de l'actif (ventes / actif moyen) | 1,03x |
| × Levier (actif moyen / capitaux propres moyens) | **5,31x** |
| = ROE | **99 %** |
| ROA | 18,7 % |
| ROIC approx. (dette + baux inclus) | 22 % |

Le ROE de 99 % vient surtout du **levier**. Depuis 2012, Dollarama a payé **8 027 M$ de plus que la valeur comptable** pour racheter ses actions (rapport de gestion). Ces sommes ont été retirées des capitaux propres. Si on les rajoutait, le ROE serait d'environ **14 %**. Le ROA (18,7 %) et le ROIC (~22 %) restent excellents : l'entreprise est très rentable, mais **le chiffre de 99 % exagère** sa rentabilité. C'est aussi pourquoi les bénéfices non répartis étaient négatifs jusqu'en 2025 : pas à cause de pertes, mais des rachats.

### 7.6 Scores

**Piotroski F-Score 2026 : 5 / 9**

| Test | Point | Détail |
|---|:---:|---|
| 1. Bénéfice net > 0 | 1 | 1 309 M$ |
| 2. Flux d'exploitation > 0 | 1 | 1 761 M$ |
| 3. ROA en hausse | 0 | 20,2 % contre 22,2 % (actif gonflé par l'acquisition et les baux australiens) |
| 4. Flux > bénéfice | 1 | 1 761 > 1 309 |
| 5. Dette LT / actif en baisse | 1 | 31,7 % contre 34,2 % |
| 6. Liquidité en hausse | 0 | 1,13 contre 1,18 |
| 7. Pas d'émission nette d'actions | 1 | −1,5 % d'actions |
| 8. Marge brute en hausse | 0 | 45,0 % contre 45,1 % (écart insignifiant) |
| 9. Rotation de l'actif en hausse | 0 | 1,12 contre 1,22 (même cause qu'au test 3) |

Un 5/9 « moyen » pour une entreprise aux marges stables et très rentable : c'est la **limite** du score. Deux des quatre points perdus viennent mécaniquement de l'acquisition australienne (actif qui grossit d'un coup), et un autre d'un écart de 0,1 point de marge.

**Altman Z-Score 2026** (cours approximatif de 195 $ fin janvier 2026, soit une capitalisation d'environ 53 G$)

| Version | Score | Zone |
|---|---:|---|
| Z original (manufacturières, cours de bourse) | **7,09** | « Sûre » |
| Z'' (non manufacturières, valeur comptable) | **2,18** | « Grise » |

Le même bilan donne « très sûr » avec une formule et « zone grise » avec l'autre. Pourquoi ?
- dans le Z original, **74 % du score** vient de X4 (capitalisation boursière / passif) : c'est le marché qui « vote » pour l'entreprise ;
- dans le Z'', X2 (bénéfices non répartis / actif = 0,017) et X4'' (capitaux propres comptables / passif = 0,24) sont **écrasés par les rachats d'actions** ;
- aucune des deux versions n'a été conçue pour un détaillant sous IFRS 16 avec 2,8 G$ d'obligations locatives.

Conclusion : pour Dollarama, les ratios directs (couverture des intérêts de 8 à 10x, dette + baux / BAIIA d'environ 2x, flux d'exploitation stable) disent plus de choses sur le risque que l'un ou l'autre Z-Score.

### 7.7 Synthèse santé (pas une recommandation)

| Axe | Constat | Ce qu'il faudrait suivre |
|---|---|---|
| Croissance | Organique ~6 % au Canada, plus l'Australie | Magasins comparables T par T, rentabilité australienne |
| Rentabilité | Marges stables et élevées, ROIC ~22 % | Frais VGA en hausse, marge australienne |
| Qualité des bénéfices | Bonne : flux > bénéfice, accruals négatifs (−6,4 %) | Part croissante de Dollarcity (non encaissée en totalité) |
| Fonds de roulement | Sain une fois l'acquisition retirée | Jours de stocks moyens au prochain exercice complet |
| Solidité | Dette + baux ~2x le BAIIA, intérêts couverts 8 à 10x | Refinancements, taux |
| Utilisation du cash | ~100 % du FCF ajusté redistribué, surtout en rachats | Rachats financés par la dette, prix payé |
| Signaux à creuser | Taux d'impôt (Pilier Deux), goodwill de l'Australie (allocation du prix encore provisoire) | Dépréciation éventuelle |

---

## 8. À toi de jouer (Excel ou Google Sheets)

Reprends les données de la [section 7](#7-cas-complet--dollarama-exercice-2026) dans un tableur.

1. **Pont du flux d'exploitation.** En A1:A11, mets les lignes du tableau 7.3. En B11 : `=SOMME(B1:B10)`. Tu dois retrouver 1 761,2.
2. **Jours de stocks.** Stock moyen : `=(921,1+1103,2)/2`. DIO : `=stock_moyen/3987,1*365`. Attendu : environ 93 j.
3. **FCF ajusté.** `=1761,2-272,8-390,3-114,5`. Attendu : 983,6 (983,5 sans arrondi).
4. **ROE et DuPont.** ROE : `=1309,4/((1188,3+1455,9)/2)`. Puis vérifie que `marge × rotation × levier` donne le même chiffre.
5. **Défi** : refais le Z'' en remplaçant les bénéfices non répartis (128,9) par les bénéfices non répartis ajustés publiés par Dollarama (8 155,9). Le score change-t-il de zone ? Qu'est-ce que ça te dit sur la variable X2 ?

---

## 9. Mini-quiz

**1.** Le bilan de Dollarama affiche une encaisse de 331,6 M$. Ce chiffre représente :
- A) l'argent généré par l'exploitation pendant l'exercice 2026
- B) l'argent en banque **au 1er février 2026**
- C) la variation de trésorerie de l'exercice
- D) le flux de trésorerie disponible

**2.** Une entreprise affiche un bénéfice net de 100 M$, un amortissement de 30 M$ et une hausse de ses stocks de 50 M$ (aucun autre ajustement). Son flux d'exploitation est de :
- A) 180 M$
- B) 120 M$
- C) 80 M$
- D) 20 M$

**3.** Chez Dollarama 2026, les stocks au bilan augmentent de 182 M$, mais l'état des flux n'indique que 54 M$ d'argent absorbé par les stocks. Pourquoi ?
- A) L'amortissement des stocks est rajouté
- B) 128 M$ de stocks sont arrivés avec l'achat de The Reject Shop, payé dans la section investissement
- C) L'entreprise a payé ses fournisseurs plus lentement
- D) C'est une erreur dans les états financiers

**4.** Le ROE de Dollarama est d'environ 99 %. La meilleure interprétation est :
- A) Dollarama est 5 fois plus rentable que la moyenne du secteur
- B) Le ROE est gonflé surtout par le levier : des capitaux propres très faibles après des années de rachats d'actions
- C) La marge nette est de 99 %
- D) L'entreprise ne paie pas d'impôts

**5.** Pour comparer l'endettement de Dollarama (IFRS 16) de façon cohérente, quel ratio faut-il utiliser ?
- A) Dette nette / BAIIA IFRS 16 (0,95x)
- B) (Dette nette + obligations locatives) / BAIIA IFRS 16 (~2,1x)
- C) Dette totale / ventes
- D) Encaisse / dette

<details>
<summary><strong>Réponses et explications</strong> (essaie d'abord !)</summary>

1. **B.** Le bilan est une photo à une date. A et D sont des flux (le film de l'année). C (208,9 M$) est l'écart entre deux photos, qu'on trouve dans l'état des flux.
2. **C : 80 M$.** 100 + 30 (amortissement **rajouté**, aucune sortie d'argent) − 50 (hausse des stocks : argent immobilisé) = 80. Le flux est inférieur au bénéfice **à cause du fonds de roulement**, pas de l'amortissement, qui l'aurait au contraire augmenté. Piège : la réponse A additionne la hausse des stocks au lieu de la soustraire.
3. **B.** Les stocks repris lors d'une acquisition ne passent pas par le fonds de roulement : ils sont inclus dans le prix d'achat (section investissement). Hors acquisition, les stocks n'ont crû que de 5,9 %, moins que les ventes.
4. **B.** DuPont : marge nette 18 % × rotation 1,03 × levier 5,3. Le ROA (18,7 %) et le ROIC (~22 %) sont excellents, mais le ROE de 99 % vient du dénominateur réduit par 8 G$ de primes de rachat depuis 2012.
5. **B.** Le BAIIA IFRS 16 exclut les loyers. Il faut donc ajouter les obligations locatives à la dette (ou retirer les loyers du BAIIA, ce qui donne ~1,1x). A mélange une dette sans baux et un BAIIA sans loyers : il flatte l'entreprise.

</details>

---

## 10. Sources

**Documents de Dollarama (exercice 2026, clos le 1er février 2026)** :
- États financiers consolidés audités, exercices clos le 1er février 2026 et le 2 février 2025 (rapport de PwC daté du 23 mars 2026) : [proxyvote.com, FINST_633103.PDF](https://materials.proxyvote.com/Approved/25675T/20260416/FINST_633103.PDF), aussi publié sur [dollarama.com, Q4FY26-DOL-FS-EN-web.pdf](https://www.dollarama.com/en-CA/corp/wp-content/uploads/2025/06/Q4FY26-DOL-FS-EN-web.pdf). Utilisés : bilan, résultats, flux de trésorerie, notes 6 (The Reject Shop), 14 (rachats), 20 (charges par nature), 22 (fonds de roulement et financement).
- Rapport de gestion de l'exercice 2026, daté du 24 mars 2026 : [proxyvote.com, MDA_633101.PDF](https://materials.proxyvote.com/Approved/25675T/20260416/MDA_633101.PDF). Utilisés : faits saillants, magasins comparables, données sectorielles, BAIIA, dette nette, ratio dette nette ajustée / BAIIA, bénéfices non répartis ajustés.
- Notice annuelle 2026 (14 avril 2026) : [dollarama.com](https://www.dollarama.com/en-CA/corp/wp-content/uploads/2026/04/2026-Annual-Information-Form-EN.pdf).
- Page « Information financière » : [dollarama.com/en-CA/corp/financial-reporting](https://www.dollarama.com/en-CA/corp/financial-reporting).
- Rapport de gestion T1 exercice 2027 : [dollarama.com](https://www.dollarama.com/en-CA/corp/wp-content/uploads/2026/09/Q1FY27-DOL-MDA-ENG-vF-website.pdf).

**Cours de l'action (approximatif, utilisé seulement pour l'Altman Z)** : ~196 $ mi-janvier 2026 ([MarketScreener](https://ca.marketscreener.com/quote/stock/DOLLARAMA-INC-5640759/)), 198,07 $ le 15 janvier 2026 ([Simply Wall St](https://simplywall.st/company/id/27b093da-6ddf-4f87-bff0-7056607673d6)), ~192 $ début février 2026 ([Motley Fool Australia](https://fool.com.au/tickers/tsx-dol)). Hypothèse retenue : 195 $. Le cours exact du 30 janvier 2026 n'a pas été vérifié.

**Références méthodologiques** :
- Piotroski, J. (2000), « Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers », *Journal of Accounting Research*.
- Altman, E. (1968), « Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy », *Journal of Finance*. Version Z'' : Altman (2000/2005).
- Sloan, R. (1996), « Do Stock Prices Fully Reflect Information in Accruals and Cash Flows about Future Earnings? », *The Accounting Review*.
- IFRS 16 *Contrats de location* ; IAS 7 *Tableau des flux de trésorerie* (choix de classement des intérêts payés).
- Délais de dépôt : Règlement 51-102 sur les obligations d'information continue (Canada) ; règles de la SEC pour les formulaires 10-K et 10-Q (États-Unis). Ce sont des règles générales : vérifie la catégorie de l'émetteur.

**Calculs** : [calculs_dollarama.py](calculs_dollarama.py) (Python), résultats dans [resultats_calculs.txt](resultats_calculs.txt).

---

*Prochain concept du parcours : les ratios d'évaluation (P/E, EV/EBITDA) et le FCF comme base du DCF.*
