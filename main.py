# Version==0.7.1
# some minor cleaning of comments


import flet as ft
import difflib
import os
import time

import util_funcs  #
from my_colors import MyColors

APP_VERSION = "0.7.1"


img_cat = ft.Image(
        src=f"assets/mainpage-cat.png",
        width=320,
        height=320,
    )


#### MAIN APP ####
def main(page: ft.Page):
    page.title = "dict"
    #page.vertical_alignment = ft.MainAxisAlignment.START
    #page.window.width = 390   # removed
    #page.window.height = 816  # removed
    if page.client_storage.get("luden_settings_pagetheme") is None:
        page.client_storage.set("luden_settings_pagetheme", "LIGHT")  # DARK'TI
        page.client_storage.set("luden_settings_pagetheme_bool", True)
    page.theme_mode = page.client_storage.get("luden_settings_pagetheme")
    #page.theme = ft.Theme(color_scheme_seed="#7f79f7")

    print(page.height, page.height, page.height, page.window.height)

    #page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
    #page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)


    my_color = MyColors(page)

    ### Page Start ###
    # some variables
    global page_go_history_check, check_auto_focus, main_page_cat_checker
    page_go_history_check = False
    check_auto_focus = False  # To solve the issue about keyboard popping up when entered in other views like settings, history etc.
    main_page_cat_checker = True  # To set the cute cat only at the starting phase of the app
    def page_build(r):

        global check_auto_focus, main_page_cat_checker

        #### FIRST DEFS ###
        def click_search(e, is_random=False):
            global main_page_cat_checker
            history_button.focus()  # To hide keyboard

            page.open(alert_loading)  # Alert is opened in the start, and closed at the end

            if is_random is True:
                random_word = util_funcs.get_random_word()
                search_text.value = random_word

                util_funcs.get_definition(
                page, 
                ft.Text(f"{random_word}"), 
                result_text,  
                container_05, 
                lambda _, x: click_search(_, x)
            )
            elif is_random is False:
                util_funcs.get_definition(
                    page, 
                    search_text, 
                    result_text,  
                    container_05, 
                    lambda _, x: click_search(_, x)
                )


            container_05.visible = False
            # search_text.border adjusting
            if container_05.visible == True:
                print("girdimmm")
                search_text.border_radius = ft.border_radius.vertical(25, 0)
            else:
                search_text.border_radius = 25
            search_button.disabled = True
            page.update()

            page.session.set("luden_temp_search_text", search_text.value)

            main_page_cat_checker = False

            page.close(alert_loading)


        def delete_text(e):
            container_05.visible = False
            # search_text.border adjusting
            if container_05.visible == True:
                print("girdimmm")
                search_text.border_radius = ft.border_radius.vertical(25, 0)
            else:
                search_text.border_radius = 25
            container_05.update()
            search_text.value = ""
            search_text.focus()
            search_text.update()
            clear_button.visible = False
            clear_button.update()


        global words_start_with_permenant, check_x, check_first_letter, check_bool
        words_start_with_permenant = []
        check_x = []
        check_first_letter = ""
        check_bool = True
        def add_suggested_word(e):
            global words_start_with_permenant, check_x, check_first_letter, check_bool
            st_str = str(search_text.value).lower()

            # validate search button availability
            search_button.disabled = False if st_str else True
            clear_button.visible = True if st_str else False

            # change search_button icon color
            if search_button.disabled == True:
                search_button.icon_color = "#6d747e"
            else:
                search_button.icon_color = my_color.get_title_color


            page.session.set("luden_temp_search_text", search_text.value)

            try:
                if st_str[0:2] != check_first_letter[0:2] or st_str == "":
                    print("------------------------------------------------")
                    check_bool = True
                    check_first_letter = st_str
                """elif st_str[0] == check_first_letter[0]:  # Bura üstteki if'le çelişiyo
                    check_bool = True"""

                if st_str[0] == check_first_letter[0] and len(st_str) > 1 and check_bool == True:
                    words_start_with_permenant = []
                    print("ife girdim ife ife ife ife")
                    check_bool = False
                    util_funcs.github_wordlist(st_str, words_start_with_permenant)

            except IndexError:
                print("indexerror - here - indexerror")
                check_bool = True
                check_first_letter = " "



            print("words_start_with_permenant uzunluk: ", len(words_start_with_permenant))
            get_suggestion = difflib.get_close_matches(st_str, words_start_with_permenant, 8, cutoff=0.6)
            print("suggestionim", get_suggestion)
            def click_list_item(z):
                search_text.value = z
                click_search(e)
                container_05.visible = False
                # search_text.border adjusting
                if container_05.visible == True:
                    search_text.border_radius = ft.border_radius.vertical(25, 0)
                else:
                    search_text.border_radius = 25
                page.update()
            container_listTile.controls.clear()
            for i in get_suggestion:
                item = i
                container_listTile.controls.append(
                    ft.ListTile(
                        title=ft.Text(item, color=my_color.text_color), 
                        on_click=lambda _, x=item: click_list_item(x), 
                        dense=True,
                        bgcolor=ft.Colors.with_opacity(0, "red")  ###################### redi black falan yap
                    )
                )  # dense=True ise container heighy 40 oluyo min_vertical_padding=0, title_text_style=ft.TextStyle(size=13.5)
               
                container_05.height = (len(get_suggestion) * 48) if len(get_suggestion) < 6 else 240  # 40* because dense=True (on mobile it's 48, on pc it's 40)
                #container_05.height = 240  # üstteki gibiydi # tekrar üsttekini açtım, ui içind aha iyi diye

            container_05.visible = False if len(st_str) < 2 else True

            # search_text.border adjusting
            if container_05.visible == True:
                search_text.border_radius = ft.border_radius.vertical(25, 0)
            else:
                search_text.border_radius = 25
            page.update()


        ########################################################################################################################


        # History storage functions
        def delete_all_history(e):
            for i in reversed(client_history):
                #history_element = page.client_storage.get(f"{i}")
                page.client_storage.remove(i)
            page.close(alert_history)
            page.open(alert_delete_feedback)


        # Sections of the page
        def make_vis_container_05(e):
            print("dsafadfafsdşsamş")
            container_05.visible = True
            page.update()
        search_text = ft.TextField(
            value = page.session.get("luden_temp_search_text"),
            hint_text="Search",
            autofocus=False if check_auto_focus == True else True, 
            border_width=2,  # gereksiz ha 
            on_change=add_suggested_word, 
            on_submit=lambda e: click_search(e),  # does this has to be a lambda?
            on_click=make_vis_container_05, 
            keyboard_type=ft.KeyboardType.NAME,
            bgcolor=my_color.search_text_color,
            color=my_color.text_color,
            border_radius=25,
            border_color=ft.Colors.with_opacity(0, ft.Colors.BLACK),
            height=40,  # used to be 35
            hint_style=ft.TextStyle(height=1),  # for phone 1, for pc 1.4
            cursor_height=18,
            cursor_color=my_color.get_title_color,
            multiline=False,
        )
        search_text_responsive = ft.ResponsiveRow(
            controls=[search_text]
        )
            
        search_button = ft.IconButton(
            ft.Icons.SEARCH, on_click=lambda e: click_search(e), 
            disabled=True,
            selected_icon_color="#3647c9",
            disabled_color="#6d747e",
            
        )
        
        clear_button = ft.IconButton(
            ft.Icons.CLEAR, 
            on_click=delete_text, 
            visible=False if search_text.value == "" else True, 
            icon_color=my_color.clear_button_color  ### code smth specific for this
        )

        if main_page_cat_checker == True:
            result_text = ft.Column(
                controls=[
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                ft.Column(
                                    controls=[
                                        ft.Container(img_cat, on_click=lambda _, x=True: click_search(_, x)),
                                        ft.Text("    Click Me\n        For\nRandom Word!", style=ft.TextStyle(weight=ft.FontWeight.W_300), color=my_color.get_title_color),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=0,
                                    expand=True,
                                    scroll=ft.ScrollMode.ALWAYS
                                ), 
                                expand=True,
                            )
                        ],
                        expand=True
                    )
                ],
            )
        else:
            result_text = ft.Column(controls=page.session.get("luden_result_text"))

        ## Alerts ##
        alert_rateus = ft.AlertDialog(
            title=(ft.Text("Directing to Google Play")), 
            content=(ft.Text("You are being directed to Google Play Store to rate this app. Do you confirm?")), 
            modal=True,
        )
        alert_rateus.actions = [
            ft.TextButton("yes", on_click=lambda e, x="https://google.com": page.launch_url(x)),  # For now its google.com
            ft.TextButton("no", on_click=lambda e, x=alert_rateus: page.close(x))
        ]


        alert_history = ft.AlertDialog(
            content=(ft.Text("Do you really wish to clear all history?")), 
            modal=True
        )
        alert_history.actions = [
            ft.TextButton("yes", on_click=delete_all_history), 
            ft.TextButton("no", on_click=lambda e, x=alert_history: page.close(x))
        ]


        alert_delete_feedback = ft.AlertDialog(
            content=(ft.Text("History is cleared.")), 
            modal=True
        )
        alert_delete_feedback.actions = [
            ft.TextButton("ok", on_click=lambda e, x=alert_delete_feedback: page.close(x))
        ]

        def alert_erase_feedback(e, erased_word):
            alrt = ft.AlertDialog(
                content=(ft.Text(f'"{erased_word}" is erased from history')), 
                modal=False,
            )
            alrt.actions = [
                ft.TextButton("ok", on_click=lambda e, x=alrt: page.close(x))
            ]
            return alrt


        alert_loading = ft.AlertDialog(
            title=(ft.ProgressRing()), 
            title_padding=120, 
            bgcolor=ft.Colors.with_opacity(0.0, "grey"), 
            modal=True
        )  # title_padding=120 ideal for mobile. 130 makes it too wide on mobile

        ## about history ##
        client_history = page.client_storage.get_keys("luden_history_")
        history_page = ft.Column(scroll=ft.ScrollMode.HIDDEN, expand=True)

        def history_search(e, word_history):
            global page_go_history_check, history_word, main_page_cat_checker
            main_page_cat_checker = False  # To get the cat in the beggining in session storage
            view_back(e)
            page_go_history_check = True
            history_word = word_history
            page.session.set("luden_temp_search_text", word_history)

        def del_hstry_item(e: ft.ControlEvent, word_item):
            page.open(alert_erase_feedback(e, word_item))
            page.client_storage.remove(f"luden_history_{word_item}")

        for i in reversed(client_history):
            history_element = page.client_storage.get(f"{i}")
            history_page.controls.append(
                ft.Dismissible(
                    content=ft.Container(
                        content=ft.ListTile(
                            title=ft.Text(f"{history_element}"), 
                            dense=True, 
                            on_click=lambda _, item=history_element: history_search(_, item),
                            title_alignment=ft.ListTileTitleAlignment.TITLE_HEIGHT,
                            title_text_style=ft.TextStyle(
                                weight=ft.FontWeight.W_600, 
                                color=my_color.text_color,
                                ),
                            bgcolor=my_color.view_bg_color,
                        ),
                        bgcolor=my_color.view_bg_color,
                        border_radius=10,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=5,
                            color=my_color.shadow_color,
                            blur_style=ft.ShadowBlurStyle.OUTER
                        ),
                        margin=ft.margin.only(right=10, left=10, top=7),
                    ), 
                    dismiss_direction=ft.DismissDirection.HORIZONTAL,
                    on_dismiss=lambda _, item=history_element: del_hstry_item(_, item),
                    dismiss_thresholds={
                            ft.DismissDirection.END_TO_START: 0.7,
                            ft.DismissDirection.START_TO_END: 0.7,
                        },
                )
            )
        global page_go_history_check, container_05
        if page_go_history_check == True:
            search_text.value = history_word
            util_funcs.get_definition(
                page, 
                search_text, 
                result_text,  
                container_05, 
                lambda _, x: click_search(_, x)
            )
            page_go_history_check = False

        # about history on/off #
        if page.client_storage.get("luden_settings_history_onoff_bool") is None: 
            page.client_storage.set("luden_settings_history_onoff_bool", True)

        def history_onoff(e):
            if page.client_storage.get("luden_settings_history_onoff_bool") == False:
                page.client_storage.set("luden_settings_history_onoff_bool", True)
            else: 
                page.client_storage.set("luden_settings_history_onoff_bool", False)

        switch_history_onoff = ft.Switch(
            on_change=history_onoff,
            value = True if page.client_storage.get("luden_settings_history_onoff_bool") is True or None else False,
            active_color=my_color.settings_icons
        )

        # about theme
        def change_theme(e: ft.ControlEvent):
            global main_page_cat_checker
            main_page_cat_checker = True  # when theme is changed, cat is revealed
            page.session.set("luden_temp_search_text", "")  # when theme is changed search_text is cleared

            page.theme_mode = "LIGHT" if page.theme_mode == "DARK" else "DARK"

            if page.theme_mode == "LIGHT":
                page.client_storage.set("luden_settings_pagetheme_bool", False)
            else: 
                page.client_storage.set("luden_settings_pagetheme_bool", True)

            page.client_storage.set("luden_settings_pagetheme", page.theme_mode)

            view_back(e)
            #page.update()  # buna gerek yok gibi

        def sun_or_moon(p):
            match p:
                case "icon":
                    if page.client_storage.get("luden_settings_pagetheme_bool") == True:
                        return ft.Icons.MODE_NIGHT_OUTLINED
                    else: 
                        return ft.Icons.WB_SUNNY_OUTLINED
                case "selected_icon":
                    if page.client_storage.get("luden_settings_pagetheme_bool") == True:
                        return ft.Icons.WB_SUNNY_OUTLINED
                    else: 
                        return ft.Icons.MODE_NIGHT_OUTLINED

        switch_page_theme = ft.IconButton(
            icon=sun_or_moon("icon"), 
            selected_icon=sun_or_moon("selected_icon"),
            on_click=change_theme,
            icon_color=my_color.settings_icons
        )

        # Appbar section elements
        history_button = ft.IconButton(
            icon=ft.Icons.HISTORY, 
            on_click=lambda _: page.go("/history"), 
            icon_color=my_color.get_title_color
        )

        popup_menu = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(
                    content=ft.Row(controls=[ft.Icon(ft.Icons.SETTINGS, color=my_color.get_title_color), ft.Text("Settings")]),
                    on_click=lambda e: page.go("/settings"),
                ),
                ft.PopupMenuItem(
                    content=ft.Row(controls=[ft.Icon(ft.Icons.INFO_OUTLINE, color=my_color.get_title_color), ft.Text("About")]),
                    on_click=lambda e: page.go("/about"),
                ),
                ft.PopupMenuItem(
                    content=ft.Row(controls=[ft.Icon(ft.Icons.RATE_REVIEW_OUTLINED, color=my_color.get_title_color), ft.Text("Rate Us :)")]),
                    on_click=lambda e, x=alert_rateus: page.open(x),
                ),
            ],
            width=45,
            on_open=lambda _: history_button.focus(),
            icon_color=my_color.get_title_color
        )

        # Containers
        container_listTile = ft.Column(spacing=0, scroll=ft.ScrollMode.ALWAYS)
        
        container_05 = ft.Container(
            container_listTile, 
            visible=False, 
            bgcolor=ft.Colors.with_opacity(0.3, my_color.view_bg_color),
            blur=15,
            border_radius=ft.border_radius.vertical(0, 25),
        )


        container_1_stack = ft.ResponsiveRow(
            controls=[
                ft.Stack(
                    controls=[
                        search_text_responsive, 
                        ft.Row(
                            controls=[
                            search_button,
                            clear_button, 
                            ], 
                            spacing=-100,
                            rtl=True,
                            right=8
                        ),
                    ], 
                    alignment=ft.alignment.Alignment(0.9, 0)
                ),
            ]
        )

        container_1 = ft.Column(
            controls=[
                ft.Container(
                    content=ft.ResponsiveRow(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Text(
                                            "Luden's Dict",
                                            color=my_color.get_title_color,
                                            style=ft.TextStyle(weight=ft.FontWeight.W_900),
                                            size=28
                                            ),
                                            ft.Row(
                                                controls=[
                                                    history_button,
                                                    popup_menu
                                                ],
                                                spacing=0
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ), 
                                    container_1_stack
                                ],
                                expand=True,
                                spacing=25
                            )
                        ],
                    ),
                    padding=ft.padding.only(top=10, right=10, bottom=20, left=10),
                    margin=ft.margin.only(top=-10, right=-10, bottom=0, left=-10),
                    bgcolor=my_color.view_bg_color,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=my_color.shadow_color,
                        offset=ft.Offset(0, 0),
                        blur_style=ft.ShadowBlurStyle.OUTER
                    ),
                    height=135,
                ),
                container_05
            ],
            spacing=1
        )


        def ct_2_onclick(e):
            history_button.focus()
            container_05.visible = False
            # search_text.border adjusting
            if container_05.visible == True:
                print("girdimmm")
                search_text.border_radius = ft.border_radius.vertical(25, 0)
            else:
                search_text.border_radius = 25
            page.update()
        container_2 = ft.Container(
            result_text, 
            expand=True, 
            on_click=ct_2_onclick,
            padding=15,
            margin=ft.margin.only(top=140, right=-30, bottom=-30, left=-30),
            bgcolor = my_color.view_bg_color_soft
        )


    
        #### Here starts the building stage ####
        page.views.clear()
        # This is the main page
        page.views.append(
            ft.View(
                route="/",
                controls=[
                    ft.AppBar(toolbar_height=0),
                    ft.Stack([container_2, container_1], expand=True),
                ],
                bgcolor=my_color.view_bg_color_soft
            )
        )

        # These are subpages
        if page.route == "/settings":
            page.views.append(
                ft.View(
                    route="/settings",
                    controls=[
                        ft.AppBar(title=ft.Text("Luden's Settings", color="#eff2fb"), bgcolor="#3647c9", automatically_imply_leading=False, leading=ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS_NEW, icon_color="#eff2fb", on_click=view_back)),
                        ft.Container(
                            ft.Column(
                                controls=[
                                    ft.Row([ft.Text("Enable/Disable History"), switch_history_onoff], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    ft.Row([ft.Text("Clear All History"), ft.IconButton(icon=ft.Icons.DELETE_FOREVER, on_click=lambda e: page.open(alert_history), icon_color=my_color.settings_icons)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    ft.Row([ft.Text("Dark/Light Mode"), switch_page_theme], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                ],
                                expand=True,
                                scroll=ft.ScrollMode.ALWAYS
                            ), 
                            padding=15,
                            expand=True,
                        )
                    ],
                    bgcolor=my_color.view_bg_color_soft
                )
            )
        elif page.route == "/about":
            page.views.append(
                ft.View(
                    route="/about", 
                    controls=[
                        ft.AppBar(title=ft.Text("Luden's Info", color="#eff2fb"), bgcolor="#3647c9", automatically_imply_leading=False, leading=ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS_NEW, icon_color="#eff2fb", on_click=view_back)),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("About", selectable=True, weight=ft.FontWeight.BOLD),
                                    ft.Text(
                                        value="This app was developed with a focus on educational purposes and is " \
                                        "completely free to use. It benefits from the dictionaryapi.dev as its " \
                                        "primary API for retrieving definitions, with wiktionary.org serving as the " \
                                        "underlying source of information." 
                                        
                                    ),
                                    ft.Text(f"You can visit these webpages: "),
                                    ft.Text(spans=[
                                        ft.TextSpan(
                                            text="https://dictionaryapi.dev", 
                                            url="https://dictionaryapi.dev/", 
                                            style=ft.TextStyle(color="blue")
                                        )
                                    ]),
                                    ft.Text(spans=[
                                        ft.TextSpan(
                                            text="https://www.wiktionary.org", 
                                            url="https://www.wiktionary.org/", 
                                            style=ft.TextStyle(color="blue")
                                        )
                                    ]),
                                    ft.Text(f"App version: {APP_VERSION}"),
                                ],
                                expand=True,
                                scroll=ft.ScrollMode.ALWAYS
                            ),
                            expand=True
                        ),
                        
                    ],
                    bgcolor=my_color.view_bg_color_soft
                )
            )
        elif page.route == "/history":
            page.views.append(
                ft.View(
                    route="/history", 
                    controls=[
                        ft.AppBar(title=ft.Text("Luden's History", color="#eff2fb"), bgcolor="#3647c9", automatically_imply_leading=False, leading=ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS_NEW, icon_color="#eff2fb", on_click=view_back)),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("\nSwipe right or left to remove item:", style=ft.TextStyle(weight=ft.FontWeight.W_600)),
                                    ft.Divider(),
                                ]
                            ),
                        ),
                        history_page
                    ],
                    bgcolor=my_color.view_bg_color_soft
                )
            )
        page.update()
        check_auto_focus = True
        
        print(page.height)
        print("BURABURABURABURABA", page.client_storage.get("luden_settings_pagetheme"))

    def view_back(v):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    
    def resize_handler(e):
        """
        should put something that would make it more comfortable on the
        rotated, wide phone screen...
        """   
    #page.on_resized = resize_handler
    

    ## Starting the structure ##
    page.on_route_change = page_build
    page.on_view_pop = view_back
    page.go("/")




if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
