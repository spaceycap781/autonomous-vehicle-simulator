import unittest
from main import astar

class TestAStar(unittest.TestCase):
    def test_shortest_route(self):
        path = astar((0,0),(2,2),set(),3,3)
        self.assertEqual(len(path)-1,4)
        self.assertEqual((path[0],path[-1]),((0,0),(2,2)))

    def test_obstacle_avoidance(self):
        obstacles = {(0,1),(1,1)}
        path = astar((0,0),(0,2),obstacles,3,3)
        self.assertTrue(path)
        self.assertFalse(set(path) & obstacles)

    def test_unreachable(self):
        self.assertEqual(astar((0,0),(2,2),{(0,1),(1,0)},3,3),[])

    def test_start_equals_goal(self):
        self.assertEqual(astar((1,1),(1,1),set(),3,3),[(1,1)])

if __name__ == '__main__':
    unittest.main()
