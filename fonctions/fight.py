#====================================COMBAT====================================
import random
import asyncio

async def fight(message):
  if len(message.content.split()) == 3:
    await message.channel.send("Merci de mettre 2 combattants !")
    return
  
  joueur1 = message.content.split()[1]
  joueur2 = message.content.split()[2]
  joueurs = [joueur1,joueur2]
  winner = random.choice(joueurs)
  if winner == joueurs[0]:
    loser = joueurs[1]
  else :
    loser = joueurs[0]

  await message.channel.send(f"Début du combat entre {joueur1} et {joueur2}, qui va gagner ce duel ?")

  phrases = [
    f"{winner} a gagné car {loser} est naze.",
    "Match nul, ils sont K.O tous les deux !",
    f"Victoire de {winner} par forfait.",
    f"Victoire de {winner} après un match très serré entre les deux joueurs.",
    f"{loser} perd le match après seulement 6 secondes de jeu, quel faible.",
    "Match incroyable entre les deux joueurs mais aucun gagnant.",
    f"{winner} a atomisé {loser} sans le moindre effort, quelle honte.",
    f"{winner} a cassé le petit orteil de {loser} et ressort gagnant de ce combat, ouille ouille ouille...",
    f"{loser} a fuit le combat...",
    f"{loser} s'est cassé la machoire en tentant une prise de karaté, victoire de {winner}.",
    f"Une boule de bowling est tombée malencontreusement sur le crâne de {loser} l'assommant et offrant la victoire à {winner}.",
    f"{winner} a mangé un kebab avant de venir sur le terrain et a battu son adversaire {loser} grâce à la technique suprême des kebabosaurus-rex.",      
    f"{loser} est en réalité un main Pyke, et comme tous les mains Pyke, il a été condamné à mort avant même le début du combat...",
    f"{winner} a gagné le combat en ramenant tous ses potes, quel faible... ",
    f"En route pour arriver sur le ring, {loser} s'est fait écraser par une bicyclette et est mort sur le coup, quelle malchance !",
     f"{winner} a pété tellement fort qu'il a intoxiqué toute la salle y compris {loser}.",
    f"\"Pourquoi se battre ?\" demandant {loser} naïvement avant de se faire piétiner par {winner} d'un élan de honte.",
    f"{winner} a brisé les tympans de {loser} en chantant la reine des neiges.",
    f"{loser} pensait avoir gagné le combat mais c'était qu'un rêve.",
    f"{loser} a été aggressé par des mouettes en costard et s'est fait picorer le visage avant d'arriver contre {winner}.",
    f"Le combat entre {winner} et {loser} se trouvait tout près d'un lac. Après un échange de coups intense, {loser} tomba dans l'eau et ne sachant pas nager, il mourra noyé.",
    f"{loser} a ramené son copain Bigfoot pour éclater la tronche de {winner}, mais, ne pouvant pas contrôler la bête elle se retourna contre {loser} et lui éclata la tronche.",
    f"{winner} a sauvagement démembré {loser} pour une experience sociale.",
    f"{winner} a vaincu son adversaire {loser} grâce à la technique \"mille an de souffrance\", maintenant, {loser} vie avec une chiasse permanente.",
    f"{winner} a écrit le nom de {loser} dans son death note, {loser} succomba donc d'une crise cardiaque...",
    f"Lors de leur combat, {winner} et {loser} virent une éruption volcanique. En essayant d'échapper à la lave, {loser} heurta un petit rat et tomba au sol. La lave le rattrapa et il finit grillé comme un kebab.",
    f"{loser} s'est transformé en cacahuète et s'est fait manger à l'apéro par {winner} inconsciemment.",
    f"{winner} a concocté une potion à la merguez contre son adversaire {loser}, après l'avoir jeté sur lui {loser} se transforma en merguez et se fit manger par un cochon... Quel cannibalisme...",
    f"{loser} est tombé amoureux de {winner}. À cause de cet amour passionnel et le devoir de se battre, {loser} fit un seppuku.",
    f"{winner} a mis un uppercut tellement puissant à {loser} qu'il a atteint l'exosphere avant de s'écraser au sol comme une merde...",
    f"{winner} a détruit son adversaire avant même qu'il n'ait eu le temps de bouger. Personne ne l'avait vu venir.",
    f"{winner} a littéralement terrassé son adversaire à l'aide d'un seul coup bien placé. {loser} va rester inconscient encore un petit moment.",
    f"Même avec les yeux bandés, {winner} n'a eu aucun mal à venir à bout de {loser}, qui s'est suicidé accablé de honte.",
    f"{winner} a cassé le nez de son adversaire avec une clé à molette, c'est pas très fairplay pour {loser} qui finit à l'hôpital en pleurs",
    f"Le stratège {winner} a aveuglé son adversaire avec du sable avant de le jeter du haut de la falaise. C'est une victoire écrasante, lol."]
  
  await asyncio.sleep(5)
  await message.channel.send(random.choice(phrases))
