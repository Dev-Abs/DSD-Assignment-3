import unittest
import networkx as nx
from main import parse_circuit, get_delay, find_critical_path


class TestCriticalPathAnalysis(unittest.TestCase):

    def setUp(self):
        """
        Set up test circuits as strings to simulate file inputs.
        """
        self.test_circuit_1 = """
        # Circuit 1
        INPUT in1
        INPUT in2
        ADD add1 in1 in2
        MUL mul1 in1 add1
        REG reg1 mul1
        ADD add2 reg1 in2
        OUTPUT out1 add2
        """

        self.test_circuit_2 = """
        # Circuit 2
        INPUT a
        INPUT b
        MUL mult1 a b
        ADD add1 a mult1
        REG reg1 add1
        MUL mult2 reg1 b
        OUTPUT y mult2
        """

        self.test_circuit_3 = """
        # Circuit 3
        INPUT x1
        INPUT x2
        MUX mux1 x1 x2
        ADD add1 mux1 x2
        REG reg1 add1
        ADD add2 reg1 x1
        OUTPUT result add2
        """

        self.test_circuit_4 = """
        # Circuit Name: cir_4
        INPUT a
        INPUT b
        INPUT c
        ADD add1 a b
        MUL mul1 add1 c
        REG reg1 mul1
        ADD add2 reg1 a
        MUL mul2 add2 b
        OUTPUT out1 add2
        OUTPUT out2 mul2
        """

        self.test_circuit_5 = """
        # Circuit Name: cir_5
        INPUT x
        INPUT y
        INPUT z
        MUL mul1 x y
        ADD add1 mul1 z
        REG reg1 add1
        MUL mul2 reg1 x
        ADD add2 mul2 y
        REG reg2 add2
        ADD add3 reg2 z
        OUTPUT out add3
        """

    def test_get_delay(self):
        """
        Test the delay values for different node types.
        """
        self.assertEqual(get_delay("INPUT"), 0.0)
        self.assertEqual(get_delay("OUTPUT"), 0.0)
        self.assertEqual(get_delay("ADD"), 0.5)
        self.assertEqual(get_delay("MUL"), 0.5)
        self.assertEqual(get_delay("REG"), 0.1)
        self.assertEqual(get_delay("UNKNOWN"), 1.0)  # Default delay for unknown types

    def test_parse_circuit(self):
        """
        Test if the circuit graph is parsed correctly.
        """
        graph = parse_circuit(self.test_circuit_1)

        # Check if nodes are added correctly
        self.assertEqual(set(graph.nodes), {"in1", "in2", "add1", "mul1", "reg1", "add2", "out1"})

        # Check if edges are added correctly
        self.assertTrue(("in1", "add1") in graph.edges)
        self.assertTrue(("add1", "mul1") in graph.edges)
        self.assertTrue(("mul1", "reg1") in graph.edges)
        self.assertTrue(("reg1", "add2") in graph.edges)
        self.assertTrue(("add2", "out1") in graph.edges)

        # Check node attributes
        self.assertEqual(graph.nodes["add1"]["type"], "ADD")
        self.assertEqual(graph.nodes["add1"]["delay"], 0.5)

    def test_find_critical_path(self):
        """
        Test the critical path and its delay.
        """
        graph = parse_circuit(self.test_circuit_1)
        critical_path, total_delay = find_critical_path(graph)

        # Verify the critical path
        self.assertEqual(critical_path, ["in1", "add1", "mul1", "reg1", "add2", "out1"])

        # Verify the total delay
        self.assertAlmostEqual(total_delay, 1.6, places=2)

    def test_critical_path_with_registers(self):
        """
        Test a sequential circuit with registers in the path.
        """
        graph = parse_circuit(self.test_circuit_2)
        critical_path, total_delay = find_critical_path(graph)

        # Verify the critical path
        self.assertEqual(critical_path, ["a", "add1", "reg1", "mult2", "y"])

        # Verify the total delay
        self.assertAlmostEqual(total_delay, 1.6, places=2)

    def test_critical_path_with_complex_circuit(self):
        """
        Test a complex sequential circuit with multiple components.
        """
        graph = parse_circuit(self.test_circuit_5)
        critical_path, total_delay = find_critical_path(graph)

        # Verify the critical path
        self.assertEqual(critical_path, ["x", "mul1", "add1", "reg1", "mul2", "add2", "reg2", "add3", "out"])

        # Verify the total delay
        self.assertAlmostEqual(total_delay, 2.7, places=2)


if __name__ == "__main__":
    unittest.main()
