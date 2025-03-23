import numpy as np

def flatten(mtx):
    mtx_flatten = []
    for row in mtx:
        mtx_flatten.extend(row)
    return mtx_flatten

class Group:
    def __init__(self, name, icon, existing_desks=[], n_new=0) -> None:
        self.name = name
        self.icon = icon
        self.existing_desks = set(existing_desks)
        self.n_new = n_new
        self.n = len(existing_desks) + n_new

class DesksClass:
    def __init__(self, desks_matrix, groups) -> None:
        self.desks = desks_matrix
        self.groups = groups
        self.n = sum([group.n for group in groups])
        desks_flatten = flatten(desks_matrix)
        self.desk_set = set(desks_flatten) - set([-1])
        self.adjacent_desk_graph = {desk: [] for desk in self.desk_set}
        self.h = len(desks_matrix)
        self.w = len(desks_matrix[0])
        for i in range(len(desks_matrix)):
            for j in range(len(desks_matrix[0])):
                for under, right in [[0, 1], [1, 0]]:
                    if i + under == self.h or j + right == self.w: continue
                    if desks_matrix[i][j] != -1 and desks_matrix[i + under][j + right] != -1:
                        self.adjacent_desk_graph[desks_matrix[i][j]].append(desks_matrix[i + under][j + right])
                        self.adjacent_desk_graph[desks_matrix[i + under][j + right]].append(desks_matrix[i][j])

    def get_loss(self, desk_groups):
        separate_loss = 0
        moving_loss = 0
        for desks, group in zip(desk_groups, self.groups):
            assert len(desks) == group.n
            moving_loss += len(group.existing_desks - set(desks)) ** 2
            n_island = 0
            while desks:
                n_island += 1
                q = [desks.pop()]
                while q:
                    q0 = q.pop()
                    for q1 in self.adjacent_desk_graph[q0]:
                        if q1 in desks:
                            q.append(q1)
                            desks.remove(q1)

            separate_loss += max(0, n_island - 1) ** 2

        return separate_loss, moving_loss

    def change(self, desk_groups, desk_set_remained):
        empty_desk = np.random.choice(desk_set_remained)
        desk_set_remained.remove(empty_desk)
        assert empty_desk not in desk_set_remained
        student = np.random.choice(self.n)
        for i_group in range(len(self.groups)):
            group = self.groups[i_group]
            if group.n <= student:
                student -= group.n
                continue

            desk_set_remained.append(desk_groups[i_group][student])
            desk_groups[i_group][student] = empty_desk
            break

        return desk_groups, desk_set_remained
