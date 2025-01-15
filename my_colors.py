# v0.7.1

import flet as ft

class MyColors:
    def __init__(self, put_page: ft.Page):
        self.put_page = put_page


    # prime colors
    @property
    def my_blue(self):
        return "#2439da"
    
    @property
    def my_background_black(self):
        return "#22272b"
    
    @property
    def my_background_soft_black(self):
        return "#2c333b"
    
    @property
    def my_soft_white(self):
        return "#adb5b8"
    

    # object colors
    @property
    def text_color(self):
        if self.put_page.client_storage.get("luden_settings_pagetheme") == "DARK":
            return self.my_soft_white
        elif self.put_page.client_storage.get("luden_settings_pagetheme") == "LIGHT":
            return self.my_background_soft_black
    
    @property
    def view_bg_color(self):
        if self.put_page.client_storage.get("luden_settings_pagetheme") == "DARK":
            return self.my_background_black
        elif self.put_page.client_storage.get("luden_settings_pagetheme") == "LIGHT":
            return "#fcfcfe"

    @property
    def view_bg_color_soft(self):
        if self.put_page.client_storage.get("luden_settings_pagetheme") == "DARK":
            return self.my_background_soft_black
        elif self.put_page.client_storage.get("luden_settings_pagetheme") == "LIGHT":
            return "#eff2fb"

    @property
    def search_text_color(self):
        if self.put_page.client_storage.get("luden_settings_pagetheme") == "DARK":
            return self.my_background_soft_black
        elif self.put_page.client_storage.get("luden_settings_pagetheme") == "LIGHT":
            return "#eff2fb"


    @property
    def shadow_color(self):
        if self.put_page.client_storage.get("luden_settings_pagetheme") == "DARK":
            return "black"
        elif self.put_page.client_storage.get("luden_settings_pagetheme") == "LIGHT":
            return ft.Colors.BLUE_GREY_300
    
    @property
    def get_title_color(self):
        if self.put_page.client_storage.get("luden_settings_pagetheme") == "DARK":
            return self.my_soft_white
        elif self.put_page.client_storage.get("luden_settings_pagetheme") == "LIGHT":
            return self.my_blue

    @property
    def get_ex_color(self):
        if self.put_page.client_storage.get("luden_settings_pagetheme") == "DARK":
            return "#98999c"
        elif self.put_page.client_storage.get("luden_settings_pagetheme") == "LIGHT":
            return self.my_background_soft_black

    @property
    def settings_icons(self):
        if self.put_page.client_storage.get("luden_settings_pagetheme") == "DARK":
            return ft.Colors.WHITE
        elif self.put_page.client_storage.get("luden_settings_pagetheme") == "LIGHT":
            return self.my_blue
    @property
    def settings_sun_or_moon(self):
        if self.put_page.client_storage.get("luden_settings_pagetheme") == "DARK":
            return ft.Colors.WHITE
        elif self.put_page.client_storage.get("luden_settings_pagetheme") == "LIGHT":
            return "#FFDF22"

    @property
    def clear_button_color(self):
        if self.put_page.client_storage.get("luden_settings_pagetheme") == "DARK":
            return self.my_soft_white
        elif self.put_page.client_storage.get("luden_settings_pagetheme") == "LIGHT":
            return ft.colors.GREY_700


    # Shadow
    @property
    def get_shadow(self):
        return ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=self.shadow_color,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER
        )