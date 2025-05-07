import requests

ville_id=169 # Blois
URL="https://www.historique-meteo.net/site/export.php"
# Attention : récupérer les cookie dans l'explorateur...
headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'cookie': r'Cookie: *************************',
         'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0',
         'Referer': 'https://www.historique-meteo.net/france/centre/blois/2024/05/',
         }
params={'ville_id':ville_id, 'annee': '2024', 'mois':'09'}

res = requests.get(URL, params=params, headers=headers)
print(res.status_code)
print(res.text)