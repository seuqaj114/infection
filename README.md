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
import total_infection
import limited_infection

from schema import set_collection
from utils import load_default_data, visualize_collection
```

Create a ```collection``` from ```hierarchy.json```

```python
collection = set_collection(load_default_data())
```

Spread infections as you wish using ```total_infection.spread_infection``` and ```limited_infection.spread_limited_infection``` according to 
the source code, and ```visualize_collection``` to visualize your network's infections.

## Examples

If we use the standard ```hierarchy.json``` we get the following networks

```python
>>> collection = set_collection(load_default_data())
>>> visualize_collection(collection)
{
    "ema v1.0": {
        "peter v1.0": {
            "able v1.0": null, 
            "bel v1.0": null, 
            "mana v1.0": null, 
            "mia v1.0": null
        }, 
        "guy v1.0": {
            "fred v1.0": null
        }
    }, 
    "mike v1.0": {
        "jane v1.0": {
            "john v1.0": null
        }, 
        "paul v1.0": null, 
        "jack v1.0": null
    }
}
```

We have two main networks, led by ema and mike.

Now lets make some infections!

### Total infection

If we want to infect mike's network with version 2.0, we simply run the command:

```python
>>> total_infection.spread_infection("mike",2.0,collection)
Users infected: ['mike', u'jane', u'john', u'paul', u'jack']
['mike', u'jane', u'john', u'paul', u'jack']
>>> visualize_collection(collection)
{
    "ema v1.0": {
        "peter v1.0": {
            "able v1.0": null, 
            "bel v1.0": null, 
            "mana v1.0": null, 
            "mia v1.0": null
        }, 
        "guy v1.0": {
            "fred v1.0": null
        }
    }, 
    "mike v2.0": {
        "jack v2.0": null, 
        "paul v2.0": null, 
        "jane v2.0": {
            "john v2.0": null
        }
    }
}
```

As we can seen, all of mike's network is now under version 2.0. 

To infect mike's network we could start from any user in it. If we want to infect this network with version 3.0, we can also start from jane, for example:

```python
>>> total_infection.spread_infection("jane",3.0,collection)
Users infected: ['jane', u'john', u'mike', u'paul', u'jack']
['jane', u'john', u'mike', u'paul', u'jack']
>>> visualize_collection(collection)
{
    "ema v1.0": {
        "peter v1.0": {
            "able v1.0": null, 
            "bel v1.0": null, 
            "mana v1.0": null, 
            "mia v1.0": null
        }, 
        "guy v1.0": {
            "fred v1.0": null
        }
    }, 
    "mike v3.0": {
        "jane v3.0": {
            "john v3.0": null
        }, 
        "paul v3.0": null, 
        "jack v3.0": null
    }
}
```

### Limited infection and exact limited infection

For the ```limited_infection```,  if we wanted to infect close to 3 users with version 4.0, running the following command would give us

```python
>>> limited_infection.spread_limited_infection(3,4.0,collection)
Users infected: [u'jane']
[u'jane']
>>> visualize_collection(collection)
{
    "ema v1.0": {
        "peter v1.0": {
            "able v1.0": null, 
            "bel v1.0": null, 
            "mana v1.0": null, 
            "mia v1.0": null
        }, 
        "guy v1.0": {
            "fred v1.0": null
        }
    }, 
    "mike v3.0": {
        "jane v4.0": {
            "john v4.0": null
        }, 
        "paul v3.0": null, 
        "jack v3.0": null
    }
}
```

As we can see, there is no sub-network containing exactly 3 users, and so the algorithm went on and found jane's network, which contains 2 users, and infected it.

In fact, if we ran the previous command with ```exact=True``` we'd get:
```python
>>> limited_infection.spread_limited_infection(3,4.0,collection,True)
exact_set = False
Exact infection impossible!
```

To show one more example of the exact limited infection, if we wanted to infect exactly 4 users with the version 5.0, running the following command yields:
```python
>>> limited_infection.spread_limited_infection(4,5.0,collection,True)
Users infected: [u'jane', u'guy']
[u'jane', u'guy']
>>> visualize_collection(collection)
{
    "ema v1.0": {
        "guy v5.0": {
            "fred v5.0": null
        }, 
        "peter v1.0": {
            "able v1.0": null, 
            "bel v1.0": null, 
            "mana v1.0": null, 
            "mia v1.0": null
        }
    }, 
    "mike v3.0": {
        "paul v3.0": null, 
        "jane v5.0": {
            "john v5.0": null
        }, 
        "jack v3.0": null
    }
}
```
As we can see, the algorithm found out a combination of 2 networks containing 2 users each, guy's and jane's, thus infecting exactly 4 users. 

Running exact limited infection for more users than the ones available in the networks will always fail, while running the approximate limited infection in this scenario would just cause it to infect every user.

### Adding more users

Because in a real-life situation not all users may be logged in by the time the network is created (the guy who's late for class should not stay out of the infection!), it is important to be able to add users to a network *a posteriori*.
For example, to add a user named "bale", coached by "guy", just import ```python from schema import add_user``` and use the command:
```python
add_user("bale","guy",collection)
```
The new user will have version of its coach.

## Benchmarks

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
