import math


class Sudoku(object):

    def __init__(self, slots_init):
        # 属性初始化
        self.slots = {}
        self.slots_shadow = {}
        self.rows = {}
        self.columns = {}
        self.blocks = {}

        # 分配空的行/列/块
        for i in range(1, 10):
            self.rows[str(i)] = Row(id=i)
            self.columns[str(i)] = column(id=i)
            self.blocks[str(i)] = Block(id=i)

        # 将所有已知格子装入字典
        for slot in slots_init:
            if str(slot.row) not in self.slots:
                self.slots[str(slot.row)] = {}
            self.slots[str(slot.row)][str(slot.column)] = slot

        # 将每个格子装进所属的行/列/块
        for slot in slots_init:
            self.rows[str(slot.row)].numbers.append(slot.value)
            self.columns[str(slot.column)].numbers.append(slot.value)
            self.blocks[str(slot.block)].numbers.append(slot.value)

        # 为每一个待填数字的格子分配一个“影子格子”
        for id_row in range(1, 10):
            for id_column in range(1, 10):
                found = False
                if str(id_row) not in self.slots:
                    pass
                else:
                    if str(id_column) not in self.slots[str(id_row)]:
                        pass
                    else:
                        found = True
                if not found:
                    if str(id_row) not in self.slots_shadow:
                        self.slots_shadow[str(id_row)] = {}
                    self.slots_shadow[str(id_row)][str(id_column)] = Slot_shadow(id_row, id_column, 0)

        # 显示初始状态
        print("初始状态：")
        self.print_sudoku()
        # print("初始影子状态：")
        # self.print_sudoku(shadow=True)
        x.print_number_row()
        x.print_number_column()
        x.print_number_block()

        # 更新所有行/列/块的可能性列表
        self.__update_possible_value_rcb()

        # 更新每个影子格子的可能性列表
        self.__update_possible_value_slot_shadow()

    def __update_possible_value_slot_shadow(self):
        print("\n----------- 影子格子可能性列表更新 -----------")
        for row in self.slots_shadow:
            for column in self.slots_shadow[row]:
                slot_shadow = self.slots_shadow[row][column]
                _row = self.rows[row]
                _column = self.columns[column]
                _block = self.blocks[str(slot_shadow.block)]
                for i in range(1, 10):
                    if (i in _row.numbers) or (i in _column.numbers) or (i in _block.numbers):
                        slot_shadow.possible_value.pop(str(i))
                print("第%s行第%s格：%s" % (row, column, slot_shadow.possible_value.keys()))

    def __update_possible_value_rcb(self):
        for row in self.slots:
            for column in self.slots[row]:
                slot = self.slots[row][column]
                self.rows[str(slot.row)].possible_value.pop(str(slot.value))
                self.columns[str(slot.column)].possible_value.pop(str(slot.value))
                self.blocks[str(slot.block)].possible_value.pop(str(slot.value))

    def __update_possible_value_add(self, slot):
        self.rows[str(slot.row)].possible_value.pop(str(slot.value))
        print(self.rows[str(slot.row)].possible_value)
        self.columns[str(slot.column)].possible_value.pop(str(slot.value))
        print(self.columns[str(slot.column)].possible_value)
        self.blocks[str(slot.block)].possible_value.pop(str(slot.value))
        print(self.blocks[str(slot.block)].possible_value)

    def print_sudoku(self, shadow=False):
        element = self.slots
        if shadow:
            element = self.slots_shadow

        print("*---*---*---*---*---*---*---*---*---*")
        for id_row in range(1, 10):
            print("|", end="")
            for id_column in range(1, 10):
                if id_column not in [3, 6, 9]:
                    sep = "*"
                else:
                    sep = "|"
                printed = False
                if str(id_row) in element:
                    if str(id_column) in element[str(id_row)]:
                        if id_column == 9:
                            print(" %s %s" % (element[str(id_row)][str(id_column)].value, sep))
                        else:
                            print(" %s %s" % (element[str(id_row)][str(id_column)].value, sep), end="")
                        printed = True
                if not printed:
                    if id_column == 9:
                        print("   %s" % sep)
                    else:
                        print("   %s" % sep, end="")

            if id_row not in [3, 6, 9]:
                print("* * * * * * * * * * * * * * * * * * *")
            else:
                print("*---*---*---*---*---*---*---*---*---*")

    def print_number_row(self):
        print("\n------------------ 行信息 ------------------")
        for row in self.rows.keys():
            print("第 %s 行：%s" % (row, self.rows[row].numbers))

    def print_number_column(self):
        print("\n------------------ 列信息 ------------------")
        for column in self.columns.keys():
            print("第 %s 列：%s" % (column, self.columns[column].numbers))

    def print_number_block(self):
        print("\n------------------ 块信息 ------------------")
        for block in self.blocks.keys():
            print("第 %s 块：%s" % (block, self.blocks[block].numbers))

class Slot(object):

    def __init__(self, row, column, value):
        self.row = row
        self.column = column

        # block
        block_row = math.ceil(float(row) / 3)
        block_column = math.ceil(float(column) / 3)
        self.block = 3 * (block_row - 1) + block_column
        self.value = value

class Slot_shadow(Slot):

    def __init__(self, row, column, value):
        super().__init__(row, column, value)
        self.possible_value = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9}

class Group_slot(object):

    def __init__(self, id):
        self.id = id
        self.numbers = []
        self.possible_value = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9}

class Row(Group_slot):

    def __init__(self, id):
        super().__init__(id)

class column(Group_slot):

    def __init__(self, id):
        super().__init__(id)

class Block(Group_slot):

    def __init__(self, id):
        super().__init__(id)


slots = [Slot(1, 1, 2), Slot(1, 4, 3), Slot(2, 1, 8), Slot(2, 3, 4), Slot(2, 5, 6), Slot(2, 6, 2), Slot(2, 9, 3),
         Slot(3, 2, 1), Slot(3, 3, 3), Slot(3, 4, 8), Slot(3, 7, 2), Slot(4, 5, 2), Slot(4, 7, 3), Slot(4, 8, 9),
         Slot(5, 1, 5), Slot(5, 3, 7), Slot(5, 7, 6), Slot(5, 8, 2), Slot(5, 9, 1), Slot(6, 2, 3), Slot(6, 3, 2),
         Slot(6, 6, 6), Slot(7, 2, 2), Slot(7, 6, 9), Slot(7, 7, 1), Slot(7, 8, 4), Slot(8, 1, 6), Slot(8, 3, 1),
         Slot(8, 4, 2), Slot(8, 5, 5), Slot(8, 7, 8), Slot(8, 9, 9), Slot(9, 6, 1), Slot(9, 9, 2), ]
x = Sudoku(slots)

