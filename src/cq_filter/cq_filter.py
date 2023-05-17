import itertools
from typing import Callable, Iterable, TypeVar

import cadquery as cq
from cadquery.cq import CQObject

T = TypeVar("T", bound="CQFilterMixin")


class CQFilterMixin:
    """
    Mixin class for cq.Workplane that provides extra filtering,
    sorting and grouping capabilities for workplane objects
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._cq_filter_groups = None
        self._snapshot_objs = None
        self._snapshot_f = None

    def __getitem__(self, item):
        if self._cq_filter_groups is None:
            objs = self.objects[item]
        else:
            objs = self._cq_filter_groups[item]
            try:
                # Attempt to flatten a list of lists
                # e.g. when we're selecting a range of groups
                objs = [obj for obj_group in objs for obj in obj_group]
            except TypeError:
                pass

        try:
            iter(objs)
        except TypeError:
            objs = [objs]

        return self.newObject(objs)

    def newObject(self: T, objlist: Iterable[CQObject]) -> T:
        rv = super().newObject(objlist)
        rv._cq_filter_groups = None
        return rv

    def filter(self: T, f: Callable[[CQObject], bool]) -> T:
        objs = filter(f, self.objects)
        return self.newObject(objs)

    def sort(self: T, key: Callable[[CQObject], bool]) -> T:
        objs = sorted(self.objects, key=key)
        return self.newObject(objs)

    def group(self: T, key: Callable[[CQObject], bool]) -> T:
        if isinstance(key, Cluster):
            sort_key = key.f
        else:
            sort_key = key

        objs = sorted(self.objects, key=sort_key)
        cq_filter_groups = []
        for _, g in itertools.groupby(objs, key):
            cq_filter_groups.append(list(g))

        rv = self.newObject(objs)
        rv._cq_filter_groups = cq_filter_groups
        return rv

    def snapshot_faces(self: T):
        self._snapshot_f = "faces"
        self._snapshot_objs = self.faces().objects

    def created_faces(self):
        pass


class Workplane(CQFilterMixin, cq.Workplane):
    pass


class Cluster:
    """Cluster objects based on a tolerance"""

    def __init__(self, f: Callable[[CQObject], bool], tol=1e-4):
        self.f = f
        self.tol = tol
        self.cluster_value = None

    def __call__(self, elem: CQObject):
        value = self.f(elem)
        if (
            self.cluster_value is not None
            and abs(value - self.cluster_value) < self.tol
        ):
            return self.cluster_value
        self.cluster_value = value
        return value
