# Rogue
A dungeon crawling game based on the Rogue-Like genre.

This game is very much in progress, and still has a lot of work to be done on it.

Rogue features a system that creates randomly-generated floors, to allow players to experience a new dungeon every time they play.

This is how it works:
<ol>
  <li>A 2D list is created to represent the floor, initially filled with all walls.</li>
  <li>A random starting location is chosen within the list, and that location is turned into a walkable floor space.</li>
  <li>The generator chooses a random direction, and moves 1 space in that direction, turning that into a floor as well.</li>
  <li>This is repeated over and over until a dungeon is created.</li>
  <li>Finally a start location is chosen, as well as an exit location that must be a certain distance from the start.</li>
</ol>

<em>But why do it this way?</em>
By creating the floors this way, it allows for extremely different types of floors to be created. From long hallways to giant, wide open rooms. This system also makes sure there is a connection to every part of the map, in order to avoid any places that are impossible to get to so the most exploration is possible. 

<h3>TODO:</h3>
<ul>
  <li>Finish enemy pathfinding</li>
  <li>Add combat</li>
  <li>Add fog of war</li>
  <li>Add progression system</>
</ul>
