# CadQuery object filtering framework


cq-filter adds a few new workplane methods that take a function argument
of type `f: Callable[[CQObject], bool]`:

* `filter(f)`: filters Workplane objects
* `order(f)`: orders Workplane objects
* `group(f)`: groups Workplane objects

Additionally, it adds subscription support to the Workplane, allowing 
selection of objects quickly.

## Rationale

Manipulating object selections in cadquery isn't currently possible without breaking out of the fluent API.


## Using filter

Following example filters all faces with an Area of more than 100

```python
wp = (wp
     .faces(">Z")
     .filter(lambda face: face.Area() > 100)
     )
```

⚠️ values in cq/occt are often not as exact as you'd expect. For example you might expect a certain 
face to have an area of exactly 100 and be included when you filter the area against `>= 100`, but upon
closer inspection it turns out the area is actually just slightly below 100 (99.999999997). Consider rounding to some
sane precision, like `round(face.Area(), 4)`

## Using order and subscription

Following example orders all faces by area and selects the three biggest ones

```python
wp = (wp
     .faces(">Z")
     .order(lambda face: face.Area())[-3:]
     )
```

## Using group and clustering


Select the smallest faces that are within 10 units of each other

```python
wp = (wp
.faces(">Z")
.group(Cluster(lambda face: face.Area(), tol=10)[0]
)
```

* ⚠️`group()` call will not yet select new objects, but it will create a new workplane object.
Selection should be done immediatelly after the grouping. Grouping data will be erased by 
next manipulation of workplane.

* selecting a range of groups (`[0:2]`) works as expected

* Cluster() defaults to a tolerance of `1e-4`

## Usage 

You'll probably want to create your own workplane class

```python 
class Workplane(CQFilterMixin, cq.Workplane):
   pass
```
