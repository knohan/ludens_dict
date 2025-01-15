# v0.7.1
# Random word search function is added
# alert_loading is directly handled in click_search func now 

import flet as ft
from string import ascii_lowercase
import requests
import difflib
import random

from style_result import DictionaryAPI
from my_colors import MyColors


url_letters_api = "https://raw.githubusercontent.com/knohan/ludens_dict/main/letters_api/letters"
#first_letters_check = ""
def github_wordlist(input_word: str, list_selected: list) -> None:
    get_first_letters = input_word[0:2]
    first_letters_check = ""
    wordlist = []
    word = ""

    print("first_letters_check: ", first_letters_check)
    #print(get_first_letters + "done")

    if get_first_letters != first_letters_check:
        if get_first_letters[1:2] != " ":     ##### This if-else is for queries such as "a "(space)
            data = requests.get(rf"{url_letters_api}/{get_first_letters}.txt").text   
        else:                                 ##### 
            data = requests.get(rf"{url_letters_api}/{get_first_letters[0]}%20.txt").text

        for letter in data:
            word += letter if letter != "\n" else ""
            if letter == "\n": wordlist.append(word.replace("\r", "")); word = ""

        zero_letter = input_word[0]
        for i in wordlist:
            first_letter = i[0].lower()
            if first_letter == zero_letter.lower():
                list_selected.append(i.strip())


        first_letters_check = get_first_letters[0:2]


########################
# for get_definition() #
########################
def add_histroy(put_page: ft.Page, history_key: str, history_value: str) -> None:
    put_page.client_storage.set(f"{history_key}", f"{history_value}")


def set_result_text(put_page: ft.Page, var: ft.Column, result_list: list) -> None:
    var.controls.clear()
    for i in result_list:
        var.controls.append(i)

    put_page.session.set("luden_result_text", result_list)



url_freedict_api = "https://api.dictionaryapi.dev/api/v2/entries/en/"
def get_definition(
        put_page: ft.Page, 
        put_user_input: ft.TextField, 
        put_result_text: ft.TextField, 
        put_container_05: ft.Container,
        put_click_search
    ) -> None:
    my_color = MyColors(put_page=put_page)

    put_user_input_low = put_user_input.value.lower()

    if put_user_input_low != "":
        try:
            dict_response = requests.get(f"{url_freedict_api}{put_user_input_low}")
            dict_response_json = dict_response.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.JSONDecodeError) as error: 
            match type(error).__name__:
                case "ConnectionError":
                    print("knk connection error var")  ###sil
                    message = [ft.Text("Connection error. Please check your internet connection", color=my_color.text_color)]
                    set_result_text(put_page, put_result_text, message)
                case "JSONDecodeError":
                    print("knk jsondecode error var")  ###sil
                    message = [ft.Text("Unexpected error. Please try again (JSONDecodeError)", color=my_color.text_color)]
                    set_result_text(put_page, put_result_text, message)
                case _:
                    print("knk bi error var")  ###sil
                    print(type(error).__name__, ":", error)
                    message = [ft.Text(f"Unexpected error. Please try again ({type(error).__name__}: {error})", color=my_color.text_color)]
                    set_result_text(put_page, put_result_text, message)
            return

        match dict_response.status_code:
            case 200:
                word = DictionaryAPI(input_json=dict_response_json)

                containers = []
                col_for_data = ft.Column(expand=True, scroll=ft.ScrollMode.HIDDEN)


                ## Audio, Flag and Text operations ##
                flags = {
                    "uk": ft.Container(
                        content=ft.Image(
                            src="assets/flag-uk.png", 
                            height=30,
                            width=30,
                        ),
                    ),
                    "us": ft.Container(
                        content=ft.Image(
                            src="assets/flag-us.png", 
                            height=30,
                            width=30,
                        ),
                    ),
                    "au": ft.Container(
                        content=ft.Image(
                            src="assets/flag-au.png", 
                            height=30,
                            width=30,
                        ),
                    ),
                }

                def pronunciation():
                    if len(word.audio) == 0:
                        return ft.Icon(ft.Icons.VOLUME_OFF, color=my_color.get_title_color)
                    elif len(word.audio) > 0:
                        return ft.Icon(ft.Icons.VOLUME_UP, color=my_color.get_title_color)
                top_panel_flags = ft.Row(controls=[pronunciation()])

                top_panel_text = ft.Row(
                            controls=[
                                ft.Text(f"{word.name}  -", color=my_color.text_color, weight=ft.FontWeight.BOLD), 
                                ft.Text(word.phonetic, color=my_color.text_color, weight=ft.FontWeight.BOLD, selectable=True),
                            ]
                        )
                
                top_panel = ft.Row(
                    controls=[
                        top_panel_text,
                        top_panel_flags, 
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                top_panel_container = ft.Container(  # using container for margin property
                    content=top_panel[0],  # IDK why but it percieves top_panel as a tuple, thats why it's "[0]"
                    margin=ft.margin.only(left=13, right=13)
                )
                

                for i in put_page.overlay:  # Clearing the auidos first from page.overlay
                    if isinstance(i, ft.core.audio.Audio):
                        put_page.overlay.remove(i)  # Audios are stacking if not cleared
                    print(type(i))

                for i in word.audio:
                    audio_link = word.audio[i]
                    print(i, audio_link)
                    match i:
                        case "uk":
                            audio_uk = ft.Audio(src=audio_link)
                            put_page.overlay.append(audio_uk)
                            flags["uk"].on_click = lambda x: audio_uk.play()
                            audio_uk.release_mode=ft.audio.ReleaseMode.STOP
                            top_panel_flags.controls.append(flags["uk"])
                        case "us":
                            audio_us = ft.Audio(src=audio_link)
                            put_page.overlay.append(audio_us)
                            flags["us"].on_click = lambda x: audio_us.play()
                            audio_us.release_mode=ft.audio.ReleaseMode.STOP
                            top_panel_flags.controls.append(flags["us"])
                        case "au":
                            audio_au = ft.Audio(src=audio_link)
                            put_page.overlay.append(audio_au)
                            flags["au"].on_click = lambda x: audio_au.play()
                            audio_au.release_mode=ft.audio.ReleaseMode.STOP
                            top_panel_flags.controls.append(flags["au"])

                containers.append(top_panel_container)


                ## Meaning and definiton operations ##
                for data in word.meanings_dict_list:
                    cache_data_container = ft.Container(
                        #border=ft.border.all(2, ft.Colors.WHITE), 
                        padding=15,
                        margin=0,
                        bgcolor=my_color.view_bg_color,
                        border_radius=20,
                    )
                    cache_data_col = ft.Column()

                    for meaning in data.items():
                        part_of_speech = meaning[0]

                        pos_check = True
                        def_count = 1
                        for def_ex in meaning[1]:
                            if pos_check == True:
                                cache_data_col.controls.append(
                                    ft.Text(f"{part_of_speech[0:-1]}", italic=True, weight=ft.FontWeight.W_400)
                                )
                            if def_ex[1] != "noEx":
                                cache_data_col.controls.append(
                                    ft.Text(
                                        spans=[
                                            ft.TextSpan(f"{def_count}. ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                            ft.TextSpan(f"{def_ex[0]}", style=ft.TextStyle(weight=ft.FontWeight.W_400)),
                                            ft.TextSpan(f"\n     • ", style=ft.TextStyle(weight=ft.FontWeight.W_400, color=my_color.get_ex_color, size=13)),
                                            ft.TextSpan(f"{def_ex[1]}", style=ft.TextStyle(weight=ft.FontWeight.W_400, color=my_color.get_ex_color, size=13)),
                                        ],
                                        selectable=True
                                    )
                                )
                            elif def_ex[1] == "noEx":
                                cache_data_col.controls.append(
                                    ft.Text(
                                        spans=[
                                            ft.TextSpan(f"{def_count}. ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                            ft.TextSpan(f"{def_ex[0]}", style=ft.TextStyle(weight=ft.FontWeight.W_400)),
                                        ],
                                        selectable=True
                                    )
                                )
                            pos_check = False
                            def_count += 1
                        cache_data_col.controls.append(ft.Divider())
                        cache_data_container.content = cache_data_col
                    col_for_data.controls.append(cache_data_container)

                containers.append(
                    ft.Container(
                        col_for_data, 
                        bgcolor=my_color.view_bg_color,
                        expand=True,
                        border_radius=ft.border_radius.vertical(20, 0)
                    )
                )
                #containers.append(ft.Divider())
                print("containers: ", containers)
                set_result_text(put_page, put_result_text, containers)
                # add history #
                if put_page.client_storage.get("luden_settings_history_onoff_bool") == True:
                    add_histroy(put_page, f"luden_history_{put_user_input_low}", f"{put_user_input_low}")
            case 404:
                #message = ft.Text("The Word Not Found")
                #######################################

                get_first_letters = put_user_input_low[0]
                wordlist = []
                list_for_ddumean = []
                word = ""

                data = requests.get(rf"{url_letters_api}/{get_first_letters}.txt").text
                for letter in data:
                    word += letter if letter != "\n" else ""
                    if letter == "\n": wordlist.append(word.replace("\r", "")); word = ""
                for i in wordlist:
                    list_for_ddumean.append(i)

                get_ddumean = difflib.get_close_matches(put_user_input_low, list_for_ddumean, 14, cutoff=0.7)

                message = ft.Text(f"{get_ddumean}", color=my_color.text_color)#d
                
                suggest_column = ft.Column(
                    spacing=0, 
                    expand=True, 
                    scroll=ft.ScrollMode.ALWAYS, 
                    #height=(put_page.height/1.60)
                    height=(put_page.height)
                )
                suggest_container = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Word not found. Did you mean:", weight=ft.FontWeight.BOLD, color=my_color.text_color),
                            suggest_column,
                        ]
                    ),
                    expand=True
                )

                def click_list_item(word_item):
                    put_user_input.value = word_item
                    put_click_search("_", x=False)  # "_" is a placeholder here
                    put_container_05.visible = False
                    put_page.update()
                for i in get_ddumean:
                    item = i
                    suggest_column.controls.append(ft.ListTile(
                            title=ft.Text(item, color=my_color.text_color), 
                            on_click=lambda _, x=item: click_list_item(x), 
                            dense=True, 
                            #shape=ft.StadiumBorder(),
                            bgcolor=my_color.view_bg_color
                    ))

                if len(suggest_column.controls) > 0:
                    message = [
                        #ft.Text("Word not found. Did you mean:", weight=ft.FontWeight.BOLD, color=my_color.text_color), 
                        suggest_container
                    ]
                    set_result_text(put_page, put_result_text, message)
                else:
                    message = [ft.Text(
                        "Sorry, the word you entered is not found and there is no suggestion. \U0001F615",
                        color=my_color.text_color
                    )]
                    set_result_text(put_page, put_result_text, message)

                #######################################
                #set_result_text(put_page, put_result_text, message)
            case 429:
                message = [ft.Text("Too many search attempts. Please wait and try again later.", color=my_color.text_color)]
                set_result_text(put_page, put_result_text, message)
            case _:
                message = [ft.Text(f"Unexpected error! Code: {dict_response.status_code}", color=my_color.text_color)]
                set_result_text(put_page, put_result_text, message)

    #put_page.close(put_alert_for_loading)


######################
# For Radom Word Cat #  should get random word list a.txt, b.txt, c.txt etc. not aa.txt, ab.txt, ac.txt...! adjust it 
######################
def get_random_word() -> str:
    url_letters_api = "https://raw.githubusercontent.com/knohan/ludens_dict/main/letters_api/letters"

    while True:
        ran_1st = random.randint(0, 25)
        ran_2nd = random.randint(0, 25)

        data = requests.get(rf"{url_letters_api}/{ascii_lowercase[ran_1st]}{ascii_lowercase[ran_2nd]}.txt")

        if data.status_code == 200: break


    wordlist = []
    word = ""
    data_txt = data.text

    for letter in data_txt:
                word += letter if letter != "\n" else ""
                if letter == "\n": wordlist.append(word.replace("\r", "")); word = ""


    return random.choice(wordlist)