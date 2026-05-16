#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de suppression des tests DD02, DD04, DD03 de la section Immobilisations
dans le PROGRAMME DE CONTRÔLE pour E-revision

Auteur: Assistant IA
Date: 16 Mai 2026
Contexte: Mise à jour du menu Démarrer E-revision - Suppression des tests comptables Immobilisations
"""

import re
import sys
from pathlib import Path

def remove_immobilisations_tests_dd02_dd04_dd03(file_path: str) -> bool:
    """
    Supprime les tests DD02, DD04, DD03 de la section Immobilisations du PROGRAMME DE CONTRÔLE
    pour E-revision dans DemarrerMenu.tsx
    
    Tests à supprimer:
    - DD02: Travaux analytiques -Immo (avec tous les modes)
    - DD02: Feuilles maîtresses-IMMOBILISATIONS (avec tous les modes)
    - DD04: Revue des techniques comptables (avec tous les modes)
    - DD03: Revue du Contrôle interne (avec tous les modes)
    
    Args:
        file_path: Chemin vers le fichier DemarrerMenu.tsx
        
    Returns:
        bool: True si la modification a réussi, False sinon
    """
    try:
        # Lire le fichier
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        content = ''.join(lines)
        
        # Vérifier que nous sommes dans la bonne section
        if 'e-revision' not in content.lower():
            print("❌ Erreur: Section E-revision non trouvée dans le fichier")
            return False
        
        if 'immobilisations' not in content.lower():
            print("❌ Erreur: Section Immobilisations non trouvée")
            return False
        
        # Trouver les indices de début et fin pour chaque test à supprimer
        tests_to_remove = []
        
        # Chercher DD02 Feuilles maîtresses
        for i, line in enumerate(lines):
            if "id: 'immobilisations-dd02'" in line and "immobilisations-dd02-travaux" not in line:
                # Trouver la fin du bloc (jusqu'à la fermeture des modes)
                start_idx = i
                bracket_count = 0
                found_start = False
                for j in range(i, len(lines)):
                    if '{' in lines[j]:
                        bracket_count += lines[j].count('{')
                        found_start = True
                    if '}' in lines[j]:
                        bracket_count -= lines[j].count('}')
                    if found_start and bracket_count == 0:
                        tests_to_remove.append(('DD02 Feuilles maîtresses', start_idx, j + 1))
                        break
        
        # Chercher DD02 Travaux analytiques
        for i, line in enumerate(lines):
            if "id: 'immobilisations-dd02-travaux'" in line:
                start_idx = i
                bracket_count = 0
                found_start = False
                for j in range(i, len(lines)):
                    if '{' in lines[j]:
                        bracket_count += lines[j].count('{')
                        found_start = True
                    if '}' in lines[j]:
                        bracket_count -= lines[j].count('}')
                    if found_start and bracket_count == 0:
                        tests_to_remove.append(('DD02 Travaux analytiques', start_idx, j + 1))
                        break
        
        # Chercher DD03
        for i, line in enumerate(lines):
            if "id: 'immobilisations-dd03'" in line:
                start_idx = i
                bracket_count = 0
                found_start = False
                for j in range(i, len(lines)):
                    if '{' in lines[j]:
                        bracket_count += lines[j].count('{')
                        found_start = True
                    if '}' in lines[j]:
                        bracket_count -= lines[j].count('}')
                    if found_start and bracket_count == 0:
                        tests_to_remove.append(('DD03 Revue CI', start_idx, j + 1))
                        break
        
        # Chercher DD04
        for i, line in enumerate(lines):
            if "id: 'immobilisations-dd04'" in line:
                start_idx = i
                bracket_count = 0
                found_start = False
                for j in range(i, len(lines)):
                    if '{' in lines[j]:
                        bracket_count += lines[j].count('{')
                        found_start = True
                    if '}' in lines[j]:
                        bracket_count -= lines[j].count('}')
                    if found_start and bracket_count == 0:
                        tests_to_remove.append(('DD04 Revue techniques', start_idx, j + 1))
                        break
        
        print(f"\n📊 Tests trouvés: {len(tests_to_remove)}")
        for test_name, start, end in tests_to_remove:
            print(f"   - {test_name}: lignes {start+1} à {end}")
        
        if not tests_to_remove:
            print("\n⚠️  Aucun test à supprimer trouvé")
            return False
        
        # Supprimer les tests en ordre inverse pour ne pas décaler les indices
        tests_to_remove.sort(key=lambda x: x[1], reverse=True)
        
        for test_name, start, end in tests_to_remove:
            # Vérifier s'il y a une virgule avant le bloc
            if start > 0 and ',' in lines[start - 1]:
                # Supprimer aussi la virgule précédente
                del lines[start - 1:end]
                print(f"✅ Test {test_name} supprimé (avec virgule précédente)")
            else:
                # Supprimer juste le bloc
                del lines[start:end]
                # Vérifier s'il y a une virgule après
                if start < len(lines) and lines[start].strip().startswith(','):
                    lines[start] = lines[start].lstrip(',').lstrip()
                print(f"✅ Test {test_name} supprimé")
        
        # Écrire le fichier modifié
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print(f"\n✅ Fichier modifié avec succès: {file_path}")
        print(f"\n📝 Résumé des suppressions:")
        print(f"   - DD02 Travaux analytiques -Immo: Supprimé (avec tous les modes)")
        print(f"   - DD02 Feuilles maîtresses-IMMOBILISATIONS: Supprimé (avec tous les modes)")
        print(f"   - DD04 Revue des techniques comptables: Supprimé (avec tous les modes)")
        print(f"   - DD03 Revue du Contrôle interne: Supprimé (avec tous les modes)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la modification du fichier: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Fonction principale"""
    print("=" * 80)
    print("SUPPRESSION DES TESTS DD02, DD04, DD03 - SECTION IMMOBILISATIONS")
    print("E-revision - Programme de contrôle")
    print("=" * 80)
    
    # Chemin vers le fichier DemarrerMenu.tsx
    file_path = Path("src/components/Clara_Components/DemarrerMenu.tsx")
    
    if not file_path.exists():
        print(f"❌ Erreur: Fichier non trouvé: {file_path}")
        sys.exit(1)
    
    print(f"\n📂 Fichier cible: {file_path}")
    print(f"\n🎯 Tests à supprimer:")
    print(f"   1. DD02 - Travaux analytiques -Immo (avec tous les modes)")
    print(f"   2. DD02 - Feuilles maîtresses-IMMOBILISATIONS (avec tous les modes)")
    print(f"   3. DD04 - Revue des techniques comptables (avec tous les modes)")
    print(f"   4. DD03 - Revue du Contrôle interne (avec tous les modes)")
    
    # Exécuter la suppression
    success = remove_immobilisations_tests_dd02_dd04_dd03(str(file_path))
    
    if success:
        print("\n" + "=" * 80)
        print("✅ SUPPRESSION TERMINÉE AVEC SUCCÈS")
        print("=" * 80)
        print("\n📋 Prochaines étapes:")
        print("   1. Vérifier le fichier DemarrerMenu.tsx")
        print("   2. Tester l'application")
        print("   3. Commit les changements")
        sys.exit(0)
    else:
        print("\n" + "=" * 80)
        print("❌ ÉCHEC DE LA SUPPRESSION")
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
