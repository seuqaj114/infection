#	Khan Academy Project Interview

## Instructions

Dowload the zip or clone the repo and navigate to the 'infection' directory.

Change ```hierarchy.json``` to create your own relationship tree. For example, in the tree below,
"mike" coaches "jane", "paul" and "jack", and "jane" coaches "john". "ema" does not coach anyone and is not coached either.
I used names but you can use any combination of numbers and letters, as long as each ID is UNIQUE. 

```javascript
{
    "mike": {
        "jane": {
            "john": null
        }, 
        "paul": null, 
        "jack": null
    }, 
    "ema": null
}
```

Open a Python shell (Python 2.7).

Import the following functions

```python

from schema import set_collection
from total_infection import spread_infection
from limited_infection import spread_limited_infection
from utils import load_default_data

```

Create a ```collection``` from ```hierarchy.json```

```python

collection = set_collection(load_default_data)
```

Spread infections as you wish!


## Tests

The algorithm built to execute the exact limited infection is actually quite fast. Below are some benchmarks,
done using an ordered test list of 1 million elements, with each element ranging between 0 and 200 million.

The second argument of the 'time_get_exact_set' is the number of users to infect and the time elapsed is given in seconds.

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
