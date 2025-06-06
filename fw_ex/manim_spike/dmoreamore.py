# pyright: reportWildcardImportFromLibrary=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalOperand=false
# pyright: reportArgumentType=false

# ruff: noqa: F405
# ruff: noqa: F403
from manim import *


class DoMoreAskMore(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = ORANGE
        LEFT_SIDE = self.camera.frame_width * LEFT / 2
        RIGHT_SIDE = self.camera.frame_width * RIGHT / 2
        # print(LEFT)
        print(LEFT_SIDE)
        # print(RIGHT)
        print(RIGHT_SIDE)
        # Title and Author
        title = Text("Make It Positive", font_size=30, weight=BOLD, color=BLACK)
        title.to_corner(UL)

        author = Text("KamalRaj", font_size=30, weight=BOLD, color=BLACK)
        author.to_corner(DR)

        # Bottom Left Text (Moved above the bottom line)
        made_with_python = Text(
            "Built with Python", font_size=30, weight=BOLD, color=BLACK
        )

        # Top line (Starts from right edge of title and extends to right side of frame)
        top_line = Line(LEFT_SIDE, RIGHT_SIDE, color=BLACK)
        top_line.to_edge(UP, buff=0.3)

        # Bottom line (Full width)
        bottom_line = Line(LEFT_SIDE, RIGHT_SIDE, color=BLACK)
        bottom_line.to_edge(DOWN, buff=0.3)

        # Position "Made with Python" above bottom line
        made_with_python.next_to(bottom_line, UP, buff=0.1).to_edge(LEFT, buff=0.3)

        # Main text
        text_kwargs = {"font_size": 80, "color": BLACK, "weight": BOLD}
        do_more = Text("Do More", **text_kwargs)
        ask_more = Text("Ask More", **text_kwargs)

        do_more.move_to(UP * 0.8)
        ask_more.move_to(DOWN * 0.8)

        # Animations
        self.play(Create(top_line), Create(bottom_line), run_time=1.5)
        self.wait(1.5)

        self.add(title, author, made_with_python)

        self.play(GrowFromCenter(do_more), GrowFromCenter(ask_more), run_time=2.5)
        self.wait(2.5)
