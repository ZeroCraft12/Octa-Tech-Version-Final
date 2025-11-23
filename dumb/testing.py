from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.screen import MDScreen


class Example(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        return (
            MDScreen(
                MDButton(
                    MDButtonIcon(
                        icon="plus",
                    ),
                    MDButtonText(
                        text="Elevated",
                    ),
                    style="elevated",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                ),
                md_bg_color=self.theme_cls.surfaceColor,
            )
        )


Example().run()