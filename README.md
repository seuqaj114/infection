# Tests

The algorithm built to execute the exact limited infection is actually quite fast, and some benchmarks are below, \
done using an ordered test list of 1 million elements, with each element ranging between 0 and 200 million. 
The second argument of the 'time_get_exact_set' is the number of users to infect.

```python

>>> ord_list = [(randint(0,200000000),)*2 for i in range(1000000)]
>>> ord_list.sort(key=lambda x: -x[1])
>>> time_get_exact_set(ord_list,1000001)
exact_set = [(996657, 996657), (1460, 1460), (1289, 1289), (254, 254), (214, 214), (127, 127)]
Time elapsed: 0.476819038391
>>> time_get_exact_set(ord_list,100000001)
exact_set = [(99998917, 99998917), (830, 830), (254, 254)]
Time elapsed: 0.924282073975
>>> time_get_exact_set(ord_list,1000000001)
exact_set = [(199999611, 199999611), (199999502, 199999502), (199998634, 199998634), (199998573, 199998573), (199998382, 199998382), (3281, 3281), (1423, 1423), (254, 254), (214, 214), (127, 127)]
Time elapsed: 0.745213031769
>>> time_get_exact_set(ord_list,10001)
exact_set = [(6848, 6848), (1855, 1855), (830, 830), (254, 254), (214, 214)]
Time elapsed: 0.460386991501

```