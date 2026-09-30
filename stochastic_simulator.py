import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class StochasticSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Stochastic Simulation System")
        self.root.geometry("1100x750")
        self.root.minsize(950, 650)

        self.bg = "#10131a"
        self.card = "#191e27"
        self.text = "#f4f4f5"
        self.muted = "#9ca3af"
        self.accent = "#8b5cf6"
        self.success = "#22c55e"
        self.danger = "#ef4444"

        self.root.configure(bg=self.bg)

        self.build_interface()

    def build_interface(self):
        # ================= HEADER =================
        header = tk.Frame(self.root, bg=self.bg)
        header.pack(fill="x", padx=30, pady=(25, 10))

        title = tk.Label(
            header,
            text="STOCHASTIC SIMULATION",
            font=("Segoe UI", 24, "bold"),
            fg=self.text,
            bg=self.bg
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            header,
            text="Monte Carlo analysis using the Gambler's Ruin model",
            font=("Segoe UI", 11),
            fg=self.muted,
            bg=self.bg
        )
        subtitle.pack(anchor="w", pady=(4, 0))

        # ================= MAIN AREA =================
        main = tk.Frame(self.root, bg=self.bg)
        main.pack(fill="both", expand=True, padx=30, pady=15)

        # ---------- LEFT PANEL ----------
        controls = tk.Frame(main, bg=self.card, width=300)
        controls.pack(side="left", fill="y", padx=(0, 15))
        controls.pack_propagate(False)

        tk.Label(
            controls,
            text="SIMULATION SETTINGS",
            font=("Segoe UI", 12, "bold"),
            fg=self.text,
            bg=self.card
        ).pack(anchor="w", padx=20, pady=(20, 20))

        self.starting_capital = self.create_input(
            controls,
            "Starting Capital",
            "50"
        )

        self.goal = self.create_input(
            controls,
            "Target Capital",
            "100"
        )

        self.win_probability = self.create_input(
            controls,
            "Win Probability (%)",
            "50"
        )

        self.simulations = self.create_input(
            controls,
            "Number of Simulations",
            "1000"
        )

        self.max_rounds = self.create_input(
            controls,
            "Maximum Rounds",
            "500"
        )

        # Run button
        self.run_button = tk.Button(
            controls,
            text="RUN SIMULATION",
            command=self.run_simulation,
            font=("Segoe UI", 11, "bold"),
            bg=self.accent,
            fg="white",
            activebackground="#7c3aed",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=12
        )
        self.run_button.pack(fill="x", padx=20, pady=(25, 10))

        self.clear_button = tk.Button(
            controls,
            text="CLEAR RESULTS",
            command=self.clear_results,
            font=("Segoe UI", 10),
            bg="#272d38",
            fg=self.text,
            activebackground="#343b48",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=10
        )
        self.clear_button.pack(fill="x", padx=20)

        # ---------- RIGHT PANEL ----------
        right = tk.Frame(main, bg=self.bg)
        right.pack(side="right", fill="both", expand=True)

        # Results cards
        cards = tk.Frame(right, bg=self.bg)
        cards.pack(fill="x")

        self.win_card = self.create_result_card(
            cards,
            "SUCCESS RATE",
            "—"
        )

        self.loss_card = self.create_result_card(
            cards,
            "RUIN RATE",
            "—"
        )

        self.average_card = self.create_result_card(
            cards,
            "AVERAGE ROUNDS",
            "—"
        )

        # Graph
        graph_frame = tk.Frame(
            right,
            bg=self.card
        )
        graph_frame.pack(
            fill="both",
            expand=True,
            pady=(15, 0)
        )

        self.figure, self.ax = plt.subplots(
            figsize=(7, 4.5),
            dpi=100
        )

        self.figure.patch.set_facecolor(self.card)
        self.ax.set_facecolor(self.card)

        self.ax.set_title(
            "Simulation Results",
            color=self.text,
            fontsize=13,
            pad=15
        )

        self.ax.tick_params(
            colors=self.muted
        )

        for spine in self.ax.spines.values():
            spine.set_color("#374151")

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=graph_frame
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Status bar
        self.status = tk.Label(
            self.root,
            text="Ready to run simulation",
            font=("Segoe UI", 9),
            fg=self.muted,
            bg=self.bg
        )
        self.status.pack(
            anchor="w",
            padx=30,
            pady=(0, 15)
        )

    # ==========================================================
    # INPUT FIELD
    # ==========================================================

    def create_input(self, parent, label, default):
        container = tk.Frame(parent, bg=self.card)
        container.pack(fill="x", padx=20, pady=8)

        tk.Label(
            container,
            text=label,
            font=("Segoe UI", 9),
            fg=self.muted,
            bg=self.card
        ).pack(anchor="w")

        entry = tk.Entry(
            container,
            font=("Segoe UI", 11),
            bg="#11151c",
            fg=self.text,
            insertbackground="white",
            relief="flat"
        )

        entry.insert(0, default)
        entry.pack(
            fill="x",
            pady=(5, 0),
            ipady=7
        )

        return entry

    # ==========================================================
    # RESULT CARD
    # ==========================================================

    def create_result_card(self, parent, title, value):
        card = tk.Frame(
            parent,
            bg=self.card,
            width=170,
            height=95
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 8, "bold"),
            fg=self.muted,
            bg=self.card
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 0)
        )

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 20, "bold"),
            fg=self.text,
            bg=self.card
        )

        value_label.pack(
            anchor="w",
            padx=15,
            pady=(5, 0)
        )

        return value_label

    # ==========================================================
    # SIMULATION
    # ==========================================================

    def run_simulation(self):
        try:
            start = int(self.starting_capital.get())
            goal = int(self.goal.get())
            probability = float(self.win_probability.get()) / 100
            simulations = int(self.simulations.get())
            max_rounds = int(self.max_rounds.get())

            if start <= 0:
                raise ValueError("Starting capital must be greater than 0.")

            if goal <= start:
                raise ValueError(
                    "Target capital must be greater than starting capital."
                )

            if not 0 <= probability <= 1:
                raise ValueError(
                    "Win probability must be between 0 and 100."
                )

            if simulations <= 0:
                raise ValueError(
                    "Number of simulations must be greater than 0."
                )

            if max_rounds <= 0:
                raise ValueError(
                    "Maximum rounds must be greater than 0."
                )

        except ValueError as error:
            messagebox.showerror(
                "Invalid Input",
                str(error)
            )
            return

        self.status.config(
            text="Running simulation..."
        )

        self.root.update_idletasks()

        successful_runs = 0
        ruined_runs = 0
        rounds_completed = []

        # Store a sample of paths for visualization
        sample_paths = []

        sample_size = min(20, simulations)

        for simulation in range(simulations):

            capital = start
            path = [capital]
            rounds = 0

            while (
                capital > 0
                and capital < goal
                and rounds < max_rounds
            ):

                # Fair/simple betting:
                # win = +1
                # loss = -1
                if np.random.random() < probability:
                    capital += 1
                else:
                    capital -= 1

                rounds += 1
                path.append(capital)

            if capital >= goal:
                successful_runs += 1

            elif capital <= 0:
                ruined_runs += 1

            rounds_completed.append(rounds)

            if simulation < sample_size:
                sample_paths.append(path)

        # ================= RESULTS =================

        success_rate = (
            successful_runs / simulations
        ) * 100

        ruin_rate = (
            ruined_runs / simulations
        ) * 100

        average_rounds = np.mean(
            rounds_completed
        )

        self.win_card.config(
            text=f"{success_rate:.1f}%"
        )

        self.loss_card.config(
            text=f"{ruin_rate:.1f}%"
        )

        self.average_card.config(
            text=f"{average_rounds:.1f}"
        )

        # ================= GRAPH =================

        self.ax.clear()

        self.ax.set_facecolor(self.card)

        for i, path in enumerate(sample_paths):
            self.ax.plot(
                path,
                linewidth=1.2,
                alpha=0.55
            )

        self.ax.axhline(
            goal,
            linestyle="--",
            linewidth=1.5,
            label="Target"
        )

        self.ax.axhline(
            0,
            linestyle="--",
            linewidth=1.5,
            label="Ruin"
        )

        self.ax.set_title(
            "Sample Capital Paths",
            color=self.text,
            fontsize=13,
            pad=15
        )

        self.ax.set_xlabel(
            "Round",
            color=self.muted
        )

        self.ax.set_ylabel(
            "Capital",
            color=self.muted
        )

        self.ax.tick_params(
            colors=self.muted
        )

        self.ax.grid(
            alpha=0.12
        )

        self.ax.legend(
            facecolor=self.card,
            labelcolor=self.text
        )

        for spine in self.ax.spines.values():
            spine.set_color("#374151")

        self.figure.tight_layout()

        self.canvas.draw()

        self.status.config(
            text=(
                f"Completed {simulations:,} simulations • "
                f"{successful_runs:,} reached the target • "
                f"{ruined_runs:,} reached ruin"
            )
        )

    # ==========================================================
    # CLEAR
    # ==========================================================

    def clear_results(self):
        self.win_card.config(text="—")
        self.loss_card.config(text="—")
        self.average_card.config(text="—")

        self.ax.clear()

        self.ax.set_facecolor(self.card)

        self.ax.set_title(
            "Simulation Results",
            color=self.text,
            fontsize=13,
            pad=15
        )

        self.ax.tick_params(
            colors=self.muted
        )

        for spine in self.ax.spines.values():
            spine.set_color("#374151")

        self.canvas.draw()

        self.status.config(
            text="Results cleared"
        )

# ==============================================================
# RUN APPLICATION
# ==============================================================

if __name__ == "__main__":
    root = tk.Tk()

    app = StochasticSimulator(root)

    root.mainloop()