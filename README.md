# CadQuery object filtering framework


cq-filter adds a few new workplane methods that take a function argument
of type `f: Callable[[CQObject], bool]`:

* `filter(f)`: filters Workplane objects
* `sort(f)`: orders Workplane objects
* `group(f)`: groups Workplane objects
* `last`: selects newly created faces
* `toWires`: select wires from selected faces

Additionally, it adds subscription support to the Workplane, allowing 
selection of objects quickly.

## Rationale

Manipulating object selections in cadquery isn't currently possible without breaking out of the fluent API.


## Using filter

Following example filters all faces with an Area of more than 100

```python
wp = (
    wp
    .faces(">Z")
    .filter(lambda face: face.Area() > 100)
)
```

⚠️ values in cq/occt are often not as exact as you'd expect. For example you might expect a certain 
face to have an area of exactly 100 and be included when you filter the area against `>= 100`, but upon
closer inspection it turns out the area is actually just slightly below 100 (99.999999997). Consider rounding to some
sane precision, like `round(face.Area(), 4)`

## Using sort and subscription

Following example sorts all faces by area and selects the three biggest ones

```python
wp = (
    wp
    .faces(">Z")
    .sort(lambda face: face.Area())[-3:]
)
```

## Using group and clustering


Select the smallest faces that are within 10 units of each other

```python
wp = (
    wp
    .faces(">Z")
    .group(Cluster(lambda face: face.Area(), tol=10)[0])
)
```

* ⚠️`group()` call will not yet select new objects, but it will create a new workplane object.
Selection should be done immediatelly after the grouping. Grouping data will be erased by 
next manipulation of workplane.

* selecting a range of groups (`[0:2]`) works as expected

* Cluster() defaults to a tolerance of `1e-4`

## Using `last` to select newly created faces

A call to `.last(everything=False)` attempts to select newly created faces. When `everything = False` it will only
select faces that share all their edges with other new faces. In other words: probably the face you'd want to focus on
after some operation like extrude, cut or revolve will be selected. 

Supplying `everything = True` will select all faces that are new.

```python
from cq_filter import Workplane

wp = (
    Workplane()
    .rect(5, 5)
    .extrude(2)
    .last()
    .workplane()
)
```

* ⚠️ `last` will not select faces that were modified 


## Usage 

You may want to create your own workplane class if you have multiple mixins

```python 
from cq_filter import CQFilterMixin

class Workplane(CQFilterMixin, cq.Workplane):
   pass
```

If you don't have multiple mixins, then the above class can also be directly imported 

```python 
from cq_filter import Workplane
```