import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ComplementVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("1's and 2's Complement Visualizer")

        self.operation = tk.StringVar(value='1s')

        self.input_string = ""
        self.output_string = ""
        self.current_index = None
        self.current_state = 'q0'

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()

        control_frame = tk.Frame(master)
        control_frame.pack(pady=5)

        tk.Label(control_frame, text="Input binary string:").grid(row=0, column=0)
        self.input_entry = tk.Entry(control_frame)
        self.input_entry.grid(row=0, column=1)
        tk.Button(control_frame, text="Start Simulation", command=self.start_simulation).grid(row=0, column=2)

        op_frame = tk.Frame(master)
        op_frame.pack(pady=5)
        tk.Label(op_frame, text="Select Operation:").pack(side=tk.LEFT)
        tk.Radiobutton(op_frame, text="1's Complement", variable=self.operation, value='1s', command=self.reset_ui).pack(side=tk.LEFT)
        tk.Radiobutton(op_frame, text="2's Complement", variable=self.operation, value='2s', command=self.reset_ui).pack(side=tk.LEFT)

        self.next_button = tk.Button(control_frame, text="Next Step", command=self.next_step, state=tk.DISABLED)
        self.next_button.grid(row=0, column=3)

        self.status_label = tk.Label(master, text="Status: Please enter input and select operation.")
        self.status_label.pack()
        self.output_label = tk.Label(master, text="Output: ")
        self.output_label.pack()

        self.build_fa_graph()
        self.draw_graph()

    def reset_ui(self):
        self.status_label.config(text="Status: Operation changed. Please enter input and start simulation.")
        self.output_label.config(text="Output: ")
        self.next_button.config(state=tk.DISABLED)
        self.input_entry.delete(0, tk.END)
        self.output_string = ""
        self.input_string = ""
        self.current_index = None
        self.current_state = 'q0'
        self.build_fa_graph()
        self.draw_graph()

    def build_fa_graph(self):
        self.graph = nx.MultiDiGraph()
        self.pos = {}
        if self.operation.get() == '1s':
            self.graph.add_node('q0', label="Flip every bit")
            self.graph.add_edge('q0', 'q0', label='0/1')
            self.graph.add_edge('q0', 'q0', label='1/0')
            self.pos = {'q0': (0, 0)}
        else:
            # 2's complement states
            self.graph.add_node('q0', label="Copy until 1")
            self.graph.add_node('q1', label="Flip bits")
            self.graph.add_edge('q0', 'q0', label='0/0')
            self.graph.add_edge('q0', 'q1', label='1/1')
            self.graph.add_edge('q1', 'q1', label='0/1')
            self.graph.add_edge('q1', 'q1', label='1/0')
            # Fix positions horizontally aligned for clarity
            self.pos = {'q0': (-1, 0), 'q1': (1, 0)}

    def draw_graph(self, highlight_transition=None, current_state=None):
        self.ax.clear()

        node_colors = []
        for n in self.graph.nodes:
            node_colors.append('lightgreen' if n == current_state else 'lightblue')

        nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax, node_color=node_colors, node_size=1600)
        labels = {n: f"{n}\n{self.graph.nodes[n]['label']}" for n in self.graph.nodes}
        nx.draw_networkx_labels(self.graph, self.pos, labels=labels, ax=self.ax)

        edge_colors = []
        widths = []
        for u, v, k, d in self.graph.edges(keys=True, data=True):
            if highlight_transition and (u, v, d['label']) == highlight_transition:
                edge_colors.append('red')
                widths.append(3)
            else:
                edge_colors.append('black')
                widths.append(1)

        nx.draw_networkx_edges(self.graph, self.pos, ax=self.ax, edge_color=edge_colors,
                               connectionstyle='arc3, rad=0.2', width=widths)

        edge_labels = {(u, v, k): d['label'] for u, v, k, d in self.graph.edges(keys=True, data=True)}
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=edge_labels, ax=self.ax)

        self.ax.set_axis_off()
        self.fig.tight_layout()
        self.canvas.draw()

    def start_simulation(self):
        s = self.input_entry.get().strip()
        if not s:
            messagebox.showerror("Error", "Please enter a binary string.")
            return
        if any(c not in ('0', '1') for c in s):
            messagebox.showerror("Error", "Input string must be binary (0 or 1).")
            return

        self.input_string = s
        self.output_string = ""

        if self.operation.get() == '1s':
            self.current_index = 0  # left to right
        else:
            self.current_index = len(s) - 1  # right to left for 2's complement

        self.current_state = 'q0'
        self.status_label.config(text=f"Status: Simulation started for {self.operation.get()} complement. Processing {'left to right' if self.operation.get()=='1s' else 'right to left'}.")
        self.output_label.config(text="Output: ")
        self.next_button.config(state=tk.NORMAL)
        self.draw_graph(current_state=self.current_state)

    def next_step(self):
        if (self.operation.get() == '1s' and self.current_index >= len(self.input_string)) or \
           (self.operation.get() == '2s' and self.current_index < 0):
            self.status_label.config(text=f"Status: Processing complete. Final output: {self.output_string}")
            self.output_label.config(text=f"Output: {self.output_string}")
            self.next_button.config(state=tk.DISABLED)
            self.draw_graph()
            return

        bit = self.input_string[self.current_index]

        if self.operation.get() == '1s':
            # flip every bit, move forward
            out_bit = '1' if bit == '0' else '0'
            transition_label = f"{bit}/{out_bit}"
            self.current_state = 'q0'
            self.output_string += out_bit
            self.current_index += 1  # move left to right

        else:
            # 2's complement
            if self.current_state == 'q0':
                if bit == '1':
                    out_bit = '1'
                    self.current_state = 'q1'
                else:
                    out_bit = '0'
            else:  # q1, flip bits
                out_bit = '1' if bit == '0' else '0'

            transition_label = f"{bit}/{out_bit}"
            self.output_string = out_bit + self.output_string  # prepend output
            self.current_index -= 1  # right to left

        self.status_label.config(text=f"Step {abs(self.current_index - (len(self.input_string) if self.operation.get()=='1s' else -1))}/{len(self.input_string)}: input='{bit}', output='{out_bit}', state={self.current_state}")
        self.output_label.config(text=f"Output: {self.output_string}")

        highlight = None
        for u, v, k, d in self.graph.edges(keys=True, data=True):
            if u == self.current_state and d['label'] == transition_label:
                highlight = (u, v, transition_label)
                break

        self.draw_graph(highlight_transition=highlight, current_state=self.current_state)

def main():
    root = tk.Tk()
    app = ComplementVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
