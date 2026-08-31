from espn_api.football import League

# --- CONFIG ---
LEAGUE_ID = 412178
SWID = '{EA2BDE03-CAE1-48B9-A7FA-29E8ABBFD0D6}'
ESPN_S2 = 'AECXGiM0XeKHfPyYlxU3A0pW%2BId9JLUXDHvIhuehNtViX9BJdaK1aDq5OnlSW6ZjMqhUCiXFC6Tlgoh8AXoOAfxSzHeFKaTHbeeOXwq%2Bcq7ME2k7KS9edm5ETpehUpbdG84%2FC4x4qaqhuDccxQgNPribn5ZrJ5zcLbtioCN9%2BZdBRm6ztHCAQJqYIuw0nA0Ul6HnuI3jY%2F%2F%2FGcHGfoZXORP908ycj0aoj5IXZ6u5Zw7ELfW4x3FdCOXh84Yj%2BFLcZmqSysYrONA6hRTqY5LjKXIUFReBVHhZx2WGUzqq40eMFg%3D%3D'

# Verified Historical Baseline (2006 - 2025) with Titles/Championships
# NOTE: Update the 'titles' numbers below to match your league history!
all_time_stats = {
    "Justin Popehn":    {"wins": 144, "losses": 116, "pf": 26291.4, "titles": 2},
    "Nick Wittrock":    {"wins": 142, "losses": 118, "pf": 26691.0, "titles": 2},
    "Grant Salzl":      {"wins": 139, "losses": 121, "pf": 25512.0, "titles": 1},
    "Jake Childers":    {"wins": 134, "losses": 126, "pf": 26336.2, "titles": 2},
    "Scott Schroeder":  {"wins": 132, "losses": 128, "pf": 26240.0, "titles": 1},
    "Adam Backes":      {"wins": 122, "losses": 125, "pf": 24758.2, "titles": 1},
    "Jay Kiess":        {"wins": 120, "losses": 140, "pf": 25267.4, "titles": 1},
    "Bill Loesch":      {"wins": 111, "losses": 123, "pf": 23345.1, "titles": 1},
    "Dustin Schlangen": {"wins": 111, "losses": 149, "pf": 24563.4, "titles": 1},
    "Adam Willard":     {"wins": 104, "losses": 117, "pf": 21791.0, "titles": 1},
    "Cole Schmitz":     {"wins": 19,  "losses": 7,   "pf": 2448.0,  "titles": 0},
    "Steve Benda":      {"wins": 9,   "losses": 17,  "pf": 2354.0,  "titles": 0}
}

NAME_MAPPING = {
    "justin popehn": "Justin Popehn",
    "nick wittrock": "Nick Wittrock",
    "grant salzl": "Grant Salzl",
    "jake childers": "Jake Childers",
    "scott schroeder": "Scott Schroeder",
    "jay kiess": "Jay Kiess",
    "jason kiess": "Jay Kiess",
    "bill loesch": "Bill Loesch",
    "william loesch": "Bill Loesch",
    "adam willard": "Adam Willard",
    "adam backes": "Adam Backes",
    "dustin schlangen": "Dustin Schlangen",
    "steve benda": "Steve Benda",
    "cole schmitz": "Cole Schmitz"
}

def clean_name(name):
    if not isinstance(name, str): return ""
    norm = name.strip().lower()
    return NAME_MAPPING.get(norm, name.strip().title())

print("Fetching 2026 live stats from ESPN...")
try:
    league = League(LEAGUE_ID, 2026, ESPN_S2, SWID)
    for team in league.teams:
        owner = "Unknown"
        if hasattr(team, 'owners') and team.owners:
            first = team.owners[0]
            if isinstance(first, dict):
                owner = clean_name(f"{first.get('firstName', '')} {first.get('lastName', '')}")
            elif isinstance(first, str):
                owner = clean_name(first)
        if owner not in all_time_stats:
            all_time_stats[owner] = {"wins": 0, "losses": 0, "pf": 0.0, "titles": 0}
        all_time_stats[owner]["wins"] += team.wins
        all_time_stats[owner]["losses"] += team.losses
        all_time_stats[owner]["pf"] += getattr(team, 'points_for', 0.0)
except Exception as e:
    print(f"ESPN sync note: {e}")

print("Generating styled HTML with Titles...")
html_output = """<!DOCTYPE html>
<html>
<head>
<style>
  body { background-color: transparent; color: #ffffff; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; margin: 0; padding: 10px; }
  table { width: 100%; border-collapse: collapse; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
  th, td { padding: 14px 15px; text-align: left; border-bottom: 1px solid #333; }
  th { background-color: #0055ff; color: white; text-transform: uppercase; font-weight: 800; letter-spacing: 1px; cursor: pointer; user-select: none; position: relative; }
  th:hover { background-color: #0040cc; }
  th::after { content: " ↕"; font-size: 11px; opacity: 0.6; }
  tr:nth-child(even) { background-color: #1a1a1a; }
  tr:nth-child(odd) { background-color: #0d0d0d; }
  tr:hover { background-color: #2a2a2a; }
</style>
</head>
<body>
<table id="sortableTable">
  <thead>
    <tr>
      <th onclick="sortTable(0)">Rank</th>
      <th onclick="sortTable(1)">Owner</th>
      <th onclick="sortTable(2)">Titles</th>
      <th onclick="sortTable(3)">Wins</th>
      <th onclick="sortTable(4)">Losses</th>
      <th onclick="sortTable(5)">Win %</th>
      <th onclick="sortTable(6)">Points For</th>
    </tr>
  </thead>
  <tbody>
"""

rank = 1
# Sort primarily by titles (descending), then wins (descending), then points for
for owner, stats in sorted(all_time_stats.items(), key=lambda x: (x[1]['titles'], x[1]['wins'], x[1]['pf']), reverse=True):
    total = stats['wins'] + stats['losses']
    pct = round((stats['wins'] / total * 100), 1) if total > 0 else 0
    win_pct_str = f"{pct}%"
    titles = stats.get('titles', 0)
    html_output += f"    <tr><td>{rank}</td><td>{owner}</td><td>{titles}</td><td>{stats['wins']}</td><td>{stats['losses']}</td><td>{win_pct_str}</td><td>{round(stats['pf'], 2)}</td></tr>\n"
    rank += 1

html_output += """  </tbody>
</table>

<script>
function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("sortableTable");
  switching = true;
  dir = "asc";
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      var xVal = x.innerHTML.replace('%', '').trim();
      var yVal = y.innerHTML.replace('%', '').trim();
      var xNum = parseFloat(xVal);
      var yNum = parseFloat(yVal);
      var cmpX = isNaN(xNum) ? xVal.toLowerCase() : xNum;
      var cmpY = isNaN(yNum) ? yVal.toLowerCase() : yNum;
      
      if (dir == "asc") {
        if (cmpX > cmpY) { shouldSwitch = true; break; }
      } else if (dir == "desc") {
        if (cmpX < cmpY) { shouldSwitch = true; break; }
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      switchcount++;
    } else {
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}
</script>
</body>
</html>
"""

with open("leaderboard.html", "w") as f:
    f.write(html_output)

print("SUCCESS! Generated updated leaderboard.html with Titles.")
