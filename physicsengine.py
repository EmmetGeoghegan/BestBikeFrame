from anastruct import SystemElements
ss = SystemElements()

ss.add_element(location=[[0, 0], [3, 4]])
ss.add_element(location=[[3, 4], [8, 4]])

ss.add_support_hinged(node_id=1)
ss.add_support_fixed(node_id=3)

ss.q_load(element_id=2, q=-10)
ss.solve()

ss.show_structure()
