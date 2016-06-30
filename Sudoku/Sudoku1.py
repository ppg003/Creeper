import math


class Sudoku(object):
    def __init__(self, slots_init):
        # 属性初始化
        self.slots = {
            "1": {},
            "2": {},
            "3": {},
            "4": {},
            "5": {},
            "6": {},
            "7": {},
            "8": {},
            "9": {},
        }
        self.slots_shadow = {
            "1": {},
            "2": {},
            "3": {},
            "4": {},
            "5": {},
            "6": {},
            "7": {},
            "8": {},
            "9": {},
        }
        self.rows = {}
        self.columns = {}
        self.blocks = {}

        # 分配空的行/列/块
        for i in range(1, 10):
            self.rows[str(i)] = Row(id=i)
            self.columns[str(i)] = Column(id=i)
            self.blocks[str(i)] = Block(id=i)

        # 将所有已知格子装入字典
        for slot in slots_init:
            self.slots[str(slot.row)][str(slot.column)] = slot

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
                    self.slots_shadow[str(id_row)][str(id_column)] = Slot_shadow(id_row, id_column, 0)

        # 将每个格子装进所属的行/列/块
        for slot in slots_init:
            self.rows[str(slot.row)].numbers.append(slot.value)
            self.rows[str(slot.row)].numbers_possible.remove(slot.value)
            self.rows[str(slot.row)].slots.append(slot)

            self.columns[str(slot.column)].numbers.append(slot.value)
            self.columns[str(slot.column)].numbers_possible.remove(slot.value)
            self.columns[str(slot.column)].slots.append(slot)

            self.blocks[str(slot.block)].numbers.append(slot.value)
            self.blocks[str(slot.block)].numbers_possible.remove(slot.value)
            self.blocks[str(slot.block)].slots.append(slot)

        # 将每个影子格子装进所属的行/列/块
        for row in self.slots_shadow:
            for column in self.slots_shadow[row]:
                slot_shadow = self.slots_shadow[row][column]
                self.rows[str(slot_shadow.row)].slots_shadow.append(slot_shadow)
                self.columns[str(slot_shadow.column)].slots_shadow.append(slot_shadow)
                self.blocks[str(slot_shadow.block)].slots_shadow.append(slot_shadow)

        # 显示初始状态
        print("初始状态：")
        self.print_sudoku()
        # print("初始影子状态：")
        # self.print_sudoku(shadow=True)
        self.print_number_row()
        self.print_number_column()
        self.print_number_block()

        # 更新每个影子格子的可能性列表
        self.__update_possible_value_slot_shadow()

    def do_sudoku(self):
        change = True  # 如果有变化则继续循环，无变化时停止
        count = 0  # 循环次数
        while change:
            count += 1
            print("-------- 第%s次循环 --------" % count)
            print("搜索行...")
            change_row = self.__uniqueness_row()
            print("搜索列...")
            change_column = self.__uniqueness_column()
            print("搜索块...")
            change_block = self.__uniqueness_block()
            change = change_row or change_column or change_block
            if not change:
                print("--------- 循环结束 ---------")
        self.print_sudoku()
        self.verification()

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

    def __uniqueness_row(self):
        found = False
        for id in self.rows:
            row = self.rows[id]
            for number_possible in row.numbers_possible:
                count = 0
                for slot_shadow in row.slots_shadow:
                    for value in slot_shadow.possible_value:
                        # print("%s - %s : %s" % (id, value, number_possible))
                        if slot_shadow.possible_value[value] == number_possible:
                            count += 1
                if count == 1:
                    found = True
                    for slot_shadow in row.slots_shadow:
                        for value in slot_shadow.possible_value:
                            if slot_shadow.possible_value[value] == number_possible:
                                # print("found - number_possible")
                                self.__add_slot(Slot(slot_shadow.row, slot_shadow.column, number_possible))
        if found:
            print("有更新！")
            self.print_sudoku()
        return found

    def __uniqueness_column(self):
        found = False
        for id in self.columns:
            column = self.columns[id]
            for number_possible in column.numbers_possible:
                count = 0
                for slot_shadow in column.slots_shadow:
                    for value in slot_shadow.possible_value:
                        # print("%s - %s : %s" % (id, value, number_possible))
                        if slot_shadow.possible_value[value] == number_possible:
                            count += 1
                if count == 1:
                    found = True
                    for slot_shadow in column.slots_shadow:
                        for value in slot_shadow.possible_value:
                            if slot_shadow.possible_value[value] == number_possible:
                                # print("found - number_possible")
                                self.__add_slot(Slot(slot_shadow.row, slot_shadow.column, number_possible))
        if found:
            print("有更新！")
            self.print_sudoku()
        return found

    def __uniqueness_block(self):
        found = False
        for id in self.blocks:
            block = self.blocks[id]
            for number_possible in block.numbers_possible:
                count = 0
                for slot_shadow in block.slots_shadow:
                    for value in slot_shadow.possible_value:
                        # print("%s - %s : %s" % (id, value, number_possible))
                        if slot_shadow.possible_value[value] == number_possible:
                            count += 1
                if count == 1:
                    found = True
                    for slot_shadow in block.slots_shadow:
                        for value in slot_shadow.possible_value:
                            if slot_shadow.possible_value[value] == number_possible:
                                # print("found - number_possible")
                                self.__add_slot(Slot(slot_shadow.row, slot_shadow.column, number_possible))
        if found:
            print("有更新！")
            self.print_sudoku()
        return found

    def __conflit_row_column(self):
        pass

    def __add_slot(self, slot):
        print("第%s行 | 第%s列 | 值：%s" % (slot.row, slot.column, slot.value))
        self.slots[str(slot.row)][str(slot.column)] = slot
        self.slots_shadow[str(slot.row)].pop(str(slot.column))
        self.rows[str(slot.row)].add_slot(slot)
        self.columns[str(slot.column)].add_slot(slot)
        self.blocks[str(slot.block)].add_slot(slot)

    def verification(self):
        count_slot = 0
        for row in self.slots:
            for column in range(1, 10):
                if str(column) in self.slots[row]:
                    count_slot += 1
        if count_slot == 81:
            print("所有空格填充完毕。")
        else:
            print("有未填充空格。")
    #     ffffffffffffffffffffffffffffffffffffffffffffff




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
        self.slots = []
        self.slots_shadow = []
        self.numbers = []
        self.numbers_possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # self.possible_value = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9}

    def add_slot(self, slot):
        # self.slots 添加新格子
        self.slots.append(slot)

        # self.slots_shadow 删除转换为格子的影子格子并更新相关影子格子的可能性列表
        for slot_shadow in self.slots_shadow:
            if slot_shadow.row == slot.row and slot_shadow.column == slot.column:
                self.slots_shadow.remove(slot_shadow)
            else:
                if str(slot.value) in slot_shadow.possible_value:
                    slot_shadow.possible_value.pop(str(slot.value))

        # numbers 增加新值
        self.numbers.append(slot.value)

        # numbers_possible 减去新值
        self.numbers_possible.remove(slot.value)

class Row(Group_slot):
    def __init__(self, id):
        super().__init__(id)


class Column(Group_slot):
    def __init__(self, id):
        super().__init__(id)


class Block(Group_slot):
    def __init__(self, id):
        super().__init__(id)


sudoku1 = [Slot(1, 1, 2), Slot(1, 4, 3), Slot(2, 1, 8), Slot(2, 3, 4), Slot(2, 5, 6), Slot(2, 6, 2), Slot(2, 9, 3),
           Slot(3, 2, 1), Slot(3, 3, 3), Slot(3, 4, 8), Slot(3, 7, 2), Slot(4, 5, 2), Slot(4, 7, 3), Slot(4, 8, 9),
           Slot(5, 1, 5), Slot(5, 3, 7), Slot(5, 7, 6), Slot(5, 8, 2), Slot(5, 9, 1), Slot(6, 2, 3), Slot(6, 3, 2),
           Slot(6, 6, 6), Slot(7, 2, 2), Slot(7, 6, 9), Slot(7, 7, 1), Slot(7, 8, 4), Slot(8, 1, 6), Slot(8, 3, 1),
           Slot(8, 4, 2), Slot(8, 5, 5), Slot(8, 7, 8), Slot(8, 9, 9), Slot(9, 6, 1), Slot(9, 9, 2), ]

sudoku2 = [
    Slot(1, 1, 7),
    Slot(1, 3, 1),
    Slot(1, 7, 2),
    Slot(1, 9, 5),
    Slot(2, 2, 6),
    Slot(2, 3, 5),
    Slot(2, 7, 8),
    Slot(3, 5, 1),
    Slot(3, 7, 9),
    Slot(4, 5, 7),
    Slot(4, 6, 6),
    Slot(4, 9, 1),
    Slot(5, 3, 7),
    Slot(5, 5, 3),
    Slot(5, 8, 6),
    Slot(6, 4, 2),
    Slot(7, 3, 3),
    Slot(7, 5, 6),
    Slot(7, 6, 8),
    Slot(8, 4, 9),
    Slot(8, 6, 3),
    Slot(8, 8, 8),
    Slot(9, 2, 8),
    Slot(9, 5, 5),
    Slot(9, 8, 7),
]

sudoku3 = [
    Slot(1,1,1),
    Slot(1,3,5),
    Slot(1,4,7),
    Slot(1,5,8),
    Slot(1,6,9),
    Slot(1,8,4),
    Slot(2,1,3),
    Slot(2,5,2),
    Slot(2,8,9),
    Slot(3,2,6),
    Slot(3,7,7),
    Slot(3,9,2),
    Slot(4,1,6),
    Slot(4,2,1),
    Slot(4,4,8),
    Slot(4,5,5),
    Slot(4,8,7),
    Slot(5,1,5),
    Slot(5,3,2),
    Slot(5,6,3),
    Slot(5,7,4),
    Slot(6,3,8),
    Slot(6,5,6),
    Slot(6,7,1),
    Slot(6,8,3),
    Slot(7,1,9),
    Slot(7,3,1),
    Slot(7,4,2),
    Slot(7,7,6),
    Slot(7,8,8),
    Slot(7,9,3),
    Slot(8,4,5),
    Slot(8,8,2),
    Slot(8,9,4),
    Slot(9,3,4),
    Slot(9,5,9),
    Slot(9,8,1),
    Slot(9,9,7),
]
x = Sudoku(sudoku3)
x.do_sudoku()
# for slot_shadow in x.rows["2"].slots_shadow:
#     print(slot_shadow.possible_value.keys())
#
# for row in x.slots_shadow:
#     for column in x.slots_shadow[row]:
#         print(x.slots_shadow[row][column].possible_value.keys())