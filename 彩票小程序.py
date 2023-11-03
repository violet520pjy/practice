from random import choice
import tkinter as tk


class LotteryTicket:
    def __init__(self, *numbers):
        self.numbers = list(numbers)

    def winner(self):
        return choice(self.numbers)


# 创建Tkinter窗口
root = tk.Tk()
root.title("Lottery Game")

results_winner = []  # 用来存储结果的列表
results_you = []


def run_lottery():
    results_winner.clear()
    results_you.clear()
    for _ in range(4):
        result = one_test.winner()
        results_winner.append(result)

    for _ in range(4):
        result = one_test.winner()
        results_you.append(result)

    winner_label.config(text="Winner's Result: " + str(results_winner))
    you_label.config(text="Your Result: " + str(results_you))

    if results_winner == results_you:
        result_label.config(text="Congratulations! You win!")
    else:
        result_label.config(text="Sorry, you lose.")


one_test = LotteryTicket(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'f', 'g', 'w', 'e', 'v')

# 在窗口中显示抽奖结果
winner_label = tk.Label(root, text="Winner's Result: ")
winner_label.pack()

you_label = tk.Label(root, text="Your Result: ")
you_label.pack()

result_label = tk.Label(root, text="")
result_label.pack()

# 添加运行按钮
run_button = tk.Button(root, text="Run Lottery", command=run_lottery)
run_button.pack()

# 启动窗口的主循环
root.mainloop()
