import os
import re
import sys
from ollama import chat


def ask_ollama(model_name, prompt):
  response = chat(
      model=model_name, messages=[{"role": "user", "content": prompt}]
  )
  return response["message"]["content"]


def run_agent_system(user_prompt):
  print(f"\n🚀 [Orchestrateur] Analyse de la demande : '{user_prompt}'")

  # Étape 1 : L'Orchestrateur analyse la demande
  prompt_orchestrateur = f"""
    Tu es un orchestrateur système intelligent.
    Demande utilisateur : "{user_prompt}"
    
    Si tu as besoin de lire un fichier existant, écris la commande sous ce format :
    [READ: chemin/du/fichier]
    
    Analyse la demande et indique quel fichier cibler.
    """

  reponse_orch = ask_ollama("qwen2.5:7b", prompt_orchestrateur)
  print(f"\n--- Réponse Orchestrateur ---\n{reponse_orch}\n")

  # Étape 2 : Python extrait le fichier cible (soit via [READ:], soit cherché dans le prompt utilisateur)
  file_path = None
  if "[READ:" in reponse_orch:
    try:
      start = reponse_orch.find("[READ:") + 6
      end = reponse_orch.find("]", start)
      file_path = reponse_orch[start:end].strip()
    except:
      pass

  # Si aucun [READ] n'a été trouvé, on cherche un chemin de fichier dans le prompt utilisateur (ex: test/factorielle.py)
  if not file_path:
    mots = user_prompt.split()
    for mot in mots:
      if "/" in mot or mot.endswith((".py", ".js", ".txt", ".json", ".md")):
        file_path = mot.strip(".,'\"")
        break

  contexte_fichiers = ""
  if file_path and os.path.exists(file_path):
    print(f"📂 [Python] Lecture automatique de : {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
      contenu = f.read()
    contexte_fichiers = (
        f"\n\nContenu actuel du fichier {file_path}:\n```python\n{contenu}\n```"
    )
  else:
    print(
        "ℹ️ Aucun fichier existant ciblé pour la lecture (création de code de"
        " zéro ?)"
    )

  # Étape 3 : Délégation au Coder si la demande implique du code
  code_genere = ""
  if any(
      kw in user_prompt.lower()
      for kw in ["corrige", "écris", "code", "crée", "modifie", "factorielle"]
  ):
    print("💻 [Coder] Délégation de la production de code à Qwen-Coder...")
    prompt_coder = f"""
        Contexte technique :{contexte_fichiers}
        
        Instructions de l'utilisateur : {user_prompt}
        
        Rédige uniquement le code source propre, robuste et complet au format markdown python. N'ajoute pas de blabla.
        """
    print(f"\n--- Prompt envoyé au Coder ---\n{prompt_coder}\n------------------------------")

    code_genere = ask_ollama("qwen2.5-coder:7b", prompt_coder)
    print(f"\n--- Code généré par le Coder ---\n{code_genere}\n") 

  # Étape 4 : Écriture automatique dans le fichier cible s'il a été identifié
  if code_genere and file_path:
    print(f"💾 [Python] Enregistrement automatique dans : {file_path}")

    # Nettoyage propre du code (extraction du bloc markdown)
    clean_code = code_genere
    if "```python" in clean_code:
      clean_code = clean_code.split("```python")[1].split("```")[0].strip()
    elif "```" in clean_code:
      clean_code = clean_code.split("```")[1].split("```")[0].strip()

    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
      f.write(clean_code)
    print(f"✅ Fichier {file_path} mis à jour et enregistré avec succès !")
  else:
    print("⚠️ Aucun fichier de destination identifié pour sauvegarder le code.")


if __name__ == "__main__":
  if len(sys.argv) > 1:
    user_prompt = " ".join(sys.argv[1:])
    run_agent_system(user_prompt)
  else:
    print("❌ Veuillez fournir une instruction.")