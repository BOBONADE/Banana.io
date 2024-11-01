import tkinter as tk
from PIL import Image, ImageTk  # Ensure Pillow is installed


def format_number(number):
    """Formats a large number to include M, B, T, etc., with up to one decimal."""
    if number >= 1_000_000_000_000:
        return f"{number / 1_000_000_000_000:.1f}T"
    elif number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.1f}B"
    elif number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"
    else:
        return str(int(number))


class ScrollableShop:
    def __init__(self, parent, on_upgrade_click):
        self.shop_frame = tk.Frame(parent, bg="#E6B34A")
        self.shop_frame.pack(side="left", padx=10, fill="y")

        # Title label for shop
        self.title_label = tk.Label(self.shop_frame, text="Upgrades Shop", font=("Arial", 18, "bold"),
                                    bg="#E6B34A", fg="black")
        self.title_label.pack(pady=10)

        # Scrollable canvas
        self.canvas = tk.Canvas(self.shop_frame, bg="#E6B34A", height=420, highlightthickness=0)
        self.scrollable_shop_frame = tk.Frame(self.canvas, bg="#E6B34A")
        self.scrollbar = tk.Scrollbar(self.shop_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollable_shop_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_shop_frame, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Pass the upgrade click handler from BananaGame
        self.on_upgrade_click = on_upgrade_click
        self.upgrade_labels = {}  # Track labels for dynamic cost updates
        self.owned_labels = {}  # Track labels for owned counts
        self.populate_upgrades()

    def populate_upgrades(self):
        # Upgrade configuration: initial cost, rate, image path, and owned count
        self.upgrade_shop = {
            1: {"cost": 15, "rate": 1, "image": "./imgs/pig.png", "owned": 0},
            2: {"cost": 100, "rate": 7, "image": "./imgs/dog.png", "owned": 0},
            3: {"cost": 1100, "rate": 19, "image": "./imgs/chicken.png", "owned": 0},
            4: {"cost": 12000, "rate": 69, "image": "./imgs/monkey.png", "owned": 0},
            5: {"cost": 130000, "rate": 260, "image": "./imgs/goat.png", "owned": 0},
            6: {"cost": 1400000, "rate": 1400, "image": "./imgs/horse.png", "owned": 0},
            7: {"cost": 20000000, "rate": 7800, "image": "./imgs/snake.png", "owned": 0},
            8: {"cost": 330000000, "rate": 44000, "image": "./imgs/dragon.png", "owned": 0},
            9: {"cost": 5100000000, "rate": 260000, "image": "./imgs/rabbit.png", "owned": 0},
            10: {"cost": 75000000000, "rate": 1600000, "image": "./imgs/tiger.png", "owned": 0},
            11: {"cost": 1000000000000, "rate": 10000000, "image": "./imgs/cow.png", "owned": 0},
            12: {"cost": 14000000000000, "rate": 65000000, "image": "./imgs/mouse.png", "owned": 0},
        }

        # Populate buttons for each upgrade
        for upgrade_num, upgrade_info in self.upgrade_shop.items():
            # Load and display the image for each upgrade
            try:
                image_path = upgrade_info["image"]
                upgrade_img = Image.open(image_path)
                upgrade_img_resized = upgrade_img.resize((200, 175), Image.LANCZOS)
                upgrade_image = ImageTk.PhotoImage(upgrade_img_resized)

                # Frame for each upgrade
                upgrade_frame = tk.Frame(self.scrollable_shop_frame, bg="#E6B34A")
                upgrade_frame.pack(pady=10, padx=47, fill="x")

                # Image label
                upgrade_label = tk.Label(upgrade_frame, image=upgrade_image, bg="#D8C56B", borderwidth=0)
                upgrade_label.image = upgrade_image  # Keep a reference to avoid garbage collection
                upgrade_label.pack()
                upgrade_label.bind("<Button-1>", lambda event, num=upgrade_num: self.on_upgrade_click(num))

                # Cost label below the image
                cost_label = tk.Label(
                    upgrade_frame,
                    text=f"Cost: {format_number(upgrade_info['cost'])}  |  +{upgrade_info['rate']} bananas/sec",
                    font=("Arial", 12, "italic"),
                    bg="#E6B34A", fg="black"
                )
                cost_label.pack(pady=(5, 0))

                # Owned label below the cost label
                owned_label = tk.Label(
                    upgrade_frame,
                    text=f"Owned: {upgrade_info['owned']}",
                    font=("Arial", 10),
                    bg="#E6B34A", fg="black"
                )
                owned_label.pack(pady=(2, 0))

                # Store labels for dynamic updates
                self.upgrade_labels[upgrade_num] = cost_label
                self.owned_labels[upgrade_num] = owned_label

            except Exception as e:
                print(f"Error loading image for upgrade {upgrade_num}: {e}")

    def update_cost_label(self, upgrade_num, new_cost, new_rate):
        """Updates the cost and rate label for the specified upgrade."""
        cost_label = self.upgrade_labels.get(upgrade_num)
        if cost_label:
            cost_label.config(text=f"Cost: {format_number(new_cost)}  |  +{new_rate} bananas/sec")

    def update_owned_label(self, upgrade_num, owned_count):
        """Updates the owned label for the specified upgrade."""
        owned_label = self.owned_labels.get(upgrade_num)
        if owned_label:
            owned_label.config(text=f"Owned: {owned_count}")

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")


class BananaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Banana.io")
        self.root.geometry("1200x800")
        self.root.configure(bg='#F5BD65')

        # Game state variables
        self.banana_count = 0
        self.auto_click_rate = 0
        self.upgrade_cost_increase = 1.15
        self.upgrade_rate_increase = 1.05

        # Load and resize the banana image (ensure it has a transparent background)
        self.banana_image = ImageTk.PhotoImage(file="./imgs/banana-png-27764.png")

        # Setup the game UI
        self.create_widgets()
        self.auto_click()

    def create_widgets(self):
        # Banana counter label
        self.banana_label = tk.Label(self.root, text="000", font=("Verdana", 40, "bold"), bg="#F5BD65", fg="black")
        self.banana_label.pack(pady=10)

        # Auto-click rate label below the banana counter
        self.auto_click_rate_label = tk.Label(
            self.root, text=f"{self.auto_click_rate:.1f} bananas/sec", font=("Verdana", 12), bg="#F5BD65", fg="black"
        )
        self.auto_click_rate_label.pack(pady=(0, 20))

        # Main frame for shop and banana button
        self.main_frame = tk.Frame(self.root, bg="#F5BD65")
        self.main_frame.pack(expand=True, fill="both", pady=10)

        # Shop panel on the left
        self.shop = ScrollableShop(self.main_frame, self.buy_upgrade)

        # Banana button on the right side of the screen
        self.banana_frame = tk.Frame(self.main_frame, bg="#F5BD65")
        self.banana_frame.pack(side="left", expand=True)

        # Banana button setup
        self.banana_label_button = tk.Label(
            self.banana_frame,
            image=self.banana_image,
            bg=self.root.cget("bg"),
            borderwidth=0
        )
        self.banana_label_button.bind("<Button-1>", lambda event: self.click_banana())
        self.banana_label_button.pack(pady=80)

    def click_banana(self):
        """Increases the banana count when the banana is clicked."""
        self.banana_count += 1
        self.update_banana_count()

    def update_banana_count(self):
        """Updates the banana count label."""
        if self.banana_count == 0:
            self.banana_label.config(text="000")
        else:
            self.banana_label.config(text=format_number(self.banana_count))

    def update_auto_click_rate_label(self):
        """Updates the auto-click rate label."""
        self.auto_click_rate_label.config(text=f"{self.auto_click_rate:.1f} bananas/sec")

    def buy_upgrade(self, upgrade_num):
        """Handles purchasing an upgrade."""
        upgrade = self.shop.upgrade_shop[upgrade_num]
        cost = upgrade['cost']

        if self.banana_count >= cost:
            self.banana_count -= cost
            # Increase the rate by 5% each time
            new_rate = int(upgrade['rate'] * self.upgrade_rate_increase)
            self.auto_click_rate += new_rate
            # Update the upgrade's rate and cost in the shop
            upgrade['rate'] = new_rate
            upgrade['cost'] = int(cost * self.upgrade_cost_increase)
            upgrade['owned'] += 1

            self.update_banana_count()
            self.update_auto_click_rate_label()
            self.shop.update_cost_label(upgrade_num, upgrade['cost'], new_rate)
            self.shop.update_owned_label(upgrade_num, upgrade['owned'])

    def auto_click(self):
        """Automatically adds bananas based on the auto-click rate."""
        self.banana_count += self.auto_click_rate
        self.update_banana_count()
        self.root.after(1000, self.auto_click)


# Run the game
root = tk.Tk()
game = BananaGame(root)
root.mainloop()






