# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import layout, bar, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy
# from libqtile.extension import *

from libqtile.widget import Spacer

#mod4 or mod = super key
super = "mod4"  # mod
alt = "alt"  # mod1
mod2 = "control"  # mod2
home = os.path.expanduser('~')

# Default Applications
web_browser = 'brave'
code_editor = 'code'
text_editor = 'subl'
music_player = ''
file_manager = 'pcmanfm'
terminal = 'alacritty'


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


myTerm = "alacritty"  # My terminal of choice

keys = [

    # SUPER + FUNCTION KEYS
    Key([super], "f", lazy.window.toggle_fullscreen()),
    Key([super], "q", lazy.window.kill()),
    Key([super], "t", lazy.spawn(myTerm)),
    # Volume Control
    # Key([mod], "v", lazy.spawn('pavucontrol')),
    Key([super], "d", lazy.spawn('nwggrid -p -o 0.4')),
    Key([super], "a",
        lazy.spawn(
            "dmenu_run -i -nb '#2B303B' -nf '#C0C5CE' -sb '#C0C5CE' -sf '#2B303B' -fn 'NotoMonoRegular:bold:pixelsize=14'"
        )),
    Key([super], "Return", lazy.spawn(terminal)),
    Key([super], "KP_Enter", lazy.spawn(terminal)),
    Key([super], "w", lazy.spawn(web_browser)),
    Key([super], "e", lazy.spawn(file_manager)),
    Key([super], "c", lazy.spawn(code_editor)),
    Key([super], "s", lazy.spawn(text_editor)),

    # SUPER + SHIFT KEYS
    Key([super, "shift"], "q", lazy.window.kill()),
    Key([super, "shift"], "r", lazy.restart()),
    # Key([super, "control"], "r", lazy.restart()),

    # CONTROL + ALT KEYS
    Key(["mod1", "control"], "o",
        lazy.spawn(home + '/.config/qtile/scripts/picom-toggle.sh')),
    # Key(["mod1", "control"], "u", lazy.spawn('pavucontrol')),

    # ALT + ... KEYS
    Key(["mod1"], "p", lazy.spawn('rofi -show window')),
    Key(["mod1"], "l", lazy.spawn('rofi -show run')),

    # CONTROL + SHIFT KEYS
    Key([mod2, "shift"], "Escape", lazy.spawn('lxtask')),

    # SCREENSHOTS
    Key([], "Print", lazy.spawn('flameshot full -p ' + home + '/Pictures')),
    Key([mod2], "Print",
        lazy.spawn('flameshot full -p ' + home + '/Pictures')),

    # MULTIMEDIA KEYS

    # INCREASE/DECREASE BRIGHTNESS
    # Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5")),
    # Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5")),

    # INCREASE/DECREASE/MUTE VOLUME
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),
    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
    Key([], "XF86AudioNext", lazy.spawn("mpc next")),
    Key([], "XF86AudioPrev", lazy.spawn("mpc prev")),
    Key([], "XF86AudioStop", lazy.spawn("mpc stop")),

    # QTILE LAYOUT KEYS
    Key([super], "n", lazy.layout.normalize()),
    Key([super], "space", lazy.next_layout()),

    # CHANGE FOCUS
    Key([super], "Up", lazy.layout.up()),
    Key([super], "Down", lazy.layout.down()),
    Key([super], "Left", lazy.layout.left()),
    Key([super], "Right", lazy.layout.right()),
    Key([super], "k", lazy.layout.up()),
    Key([super], "j", lazy.layout.down()),
    Key([super], "h", lazy.layout.left()),
    Key([super], "l", lazy.layout.right()),

    # RESIZE UP, DOWN, LEFT, RIGHT
    Key(
        [super, "control"],
        "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        [super, "control"],
        "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        [super, "control"],
        "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        [super, "control"],
        "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        [super, "control"],
        "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        [super, "control"],
        "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        [super, "control"],
        "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
    Key(
        [super, "control"],
        "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),

    # FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([super, "shift"], "f", lazy.layout.flip()),

    # FLIP LAYOUT FOR BSP
    Key([super, "mod1"], "k", lazy.layout.flip_up()),
    Key([super, "mod1"], "j", lazy.layout.flip_down()),
    Key([super, "mod1"], "l", lazy.layout.flip_right()),
    Key([super, "mod1"], "h", lazy.layout.flip_left()),

    # MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([super, "shift"], "k", lazy.layout.shuffle_up()),
    Key([super, "shift"], "j", lazy.layout.shuffle_down()),
    Key([super, "shift"], "h", lazy.layout.shuffle_left()),
    Key([super, "shift"], "l", lazy.layout.shuffle_right()),

    ### Treetab controls
    Key([super, "control"],
        "k",
        lazy.layout.section_up(),
        desc='Move up a section in treetab'),
    Key([super, "control"],
        "j",
        lazy.layout.section_down(),
        desc='Move down a section in treetab'),

    # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([super, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([super, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([super, "shift"], "Left", lazy.layout.swap_left()),
    Key([super, "shift"], "Right", lazy.layout.swap_right()),

    # TOGGLE FLOATING LAYOUT
    Key([super, "shift"], "space", lazy.window.toggle_floating()),
]

groups = []

# FOR QWERTY KEYBOARDS
group_names = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
]

group_labels = [
    "1 ",
    "2 ",
    "3 ",
    "4 ",
    "5 ",
    "6 ",
    "7 ",
    "8 ",
    "9 ",
    "0",
]
#group_labels = ["", "", "", "", "", "", "", "", "", "",]
#group_labels = ["", "", "", "", "",]
#group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

group_layouts = [
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "treetab",
    "floating",
]
#group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

        #CHANGE WORKSPACES
        Key([super], i.name, lazy.group[i.name].toscreen()),
        Key([super], "Tab", lazy.screen.next_group()),
        Key([super, "shift"], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        Key([super, "shift"], i.name, lazy.window.togroup(i.name)),
        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        # Key([super, "shift"], i.name, lazy.window.togroup(i.name),
        # lazy.group[i.name].toscreen()),
    ])


def init_layout_theme():
    return {
        "margin": 0,
        "border_width": 2,
        "border_focus": "#C0C5CE",
        "border_normal": "#2B303B"
    }


layout_theme = init_layout_theme()

layouts = [
    layout.MonadTall(margin=0,
                     border_width=2,
                     border_focus="#8FA1B3",
                     border_normal="#2B303B"),
    layout.MonadWide(margin=0,
                     border_width=2,
                     border_focus="#8FA1B3",
                     border_normal="#2B303B"),
    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme),
    layout.Columns(**layout_theme),
    layout.Stack(**layout_theme),
    layout.Tile(**layout_theme),
    layout.TreeTab(sections=['FIRST', 'SECOND'],
                   bg_color='#141414',
                   active_bg='#0000ff',
                   inactive_bg='#1e90ff',
                   padding_y=5,
                   section_top=10,
                   panel_width=280),
    layout.VerticalTile(**layout_theme),
    layout.Zoomy(**layout_theme)
]

# COLORS FOR THE BAR

test_color = ["#fc9803", "#fc5a03"]
ocean_colors = {
    "BG": "#2B303B",
    "FG": "#C0C5CE",
    "red": "#BF616A",
    "green": "#A3BE8C",
    "yellow": "#EBCB8B",
    "blue": "#8FA1B3",
    "magenta": "#B48EAD",
    "cyan": "#8FA1B3",
    "white": "#EFF1F5",
    "grey": "#65737E"
}


def init_colors():
    return [
        ["#2F343F", "#2F343F"],  # color 0
        ["#2F343F", "#2F343F"],  # color 1
        ["#c0c5ce", "#c0c5ce"],  # color 2
        ["#e75480", "#e75480"],  # color 3
        ["#f4c2c2", "#f4c2c2"],  # color 4
        ["#ffffff", "#ffffff"],  # color 5
        ["#ff0000", "#ff0000"],  # color 6
        ["#62FF00", "#62FF00"],  # color 7
        ["#000000", "#000000"],  # color 8
        ["#c40234", "#c40234"],  # color 9
        ["#6790eb", "#6790eb"],  # color 10
        ["#ff00ff", "#ff00ff"],  #11
        ["#4c566a", "#4c566a"],  #12 
        ["#282c34", "#282c34"],  #13
        ["#212121", "#212121"],  #14
        ["#98c379", "#98c379"],  #15 
        ["#b48ead", "#b48ead"],  #16 
        ["#abb2bf", "#abb2bf"],  # color 17
        ["#81a1c1", "#81a1c1"],  #18 
        ["#56b6c2", "#56b6c2"],  #19 
        ["#c678dd", "#c678dd"],  #20 
        ["#e06c75", "#e06c75"],  #21
        ["#fb9f7f", "#fb9f7f"],  #22
        ["#ffd47e", "#ffd47e"]
    ]  #23


colors = init_colors()


def base(fg='text', bg='dark'):
    # return {'foreground': colors[14],'background': colors[15]}
    return {'foreground': ocean_colors["FG"], 'background': ocean_colors["BG"]}


# WIDGETS FOR THE BAR


def init_widgets_defaults():
    return dict(font="Noto Sans",
                fontsize=14,
                padding=2,
                background=ocean_colors["BG"])
    # background=colors[1])


widget_defaults = init_widgets_defaults()


def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
        widget.Sep(linewidth=1,
                   padding=10,
                   foreground=ocean_colors["BG"],
                   background=ocean_colors["BG"]),
        widget.Image(
            filename="~/.config/qtile/icons/garuda-red.png",
            iconsize=9,
            #    background = ocean_colors["BG"],
            mouse_callbacks={'Button1':
                             lambda: qtile.cmd_spawn('jgmenu_run')}),
        widget.Sep(linewidth=1,
                   padding=10,
                   foreground=ocean_colors["BG"],
                   background=ocean_colors["BG"]),
        widget.GroupBox(**base(),
                        font='UbuntuMono Nerd Font',
                        fontsize=14,
                        margin_y=3,
                        margin_x=0,
                        padding_y=5,
                        padding_x=4,
                        borderwidth=3,
                        active=ocean_colors["magenta"],
                        inactive=ocean_colors["FG"],
                        block_highlight_text_color=ocean_colors["BG"],
                        rounded=False,
                        highlight_method='block',
                        urgent_alert_method='block',
                        urgent_border=ocean_colors["red"],
                        this_current_screen_border=ocean_colors["FG"],
                        this_screen_border=ocean_colors["grey"],
                        other_current_screen_border=ocean_colors["FG"],
                        other_screen_border=ocean_colors['grey'],
                        disable_drag=True),
        widget.Sep(linewidth=1,
                   padding=10,
                   foreground=ocean_colors["BG"],
                   background=ocean_colors["BG"]),
        widget.TaskList(
            highlight_method='block',  # or block
            icon_size=17,
            max_title_width=250,
            rounded=False,
            padding_x=10,
            padding_y=0,
            margin_y=0,
            fontsize=14,
            border=ocean_colors["grey"],
            foreground=ocean_colors["FG"],
            margin=0,
            txt_floating='🗗',
            txt_minimized='>_ ',
            borderwidth=1,
            # background=colors[20],
            #unfocused_border = 'border'
        ),
        widget.CurrentLayoutIcon(
            custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
            foreground=ocean_colors["FG"],
            #    background = colors[3],
            padding=0,
            scale=0.7),
        widget.CurrentLayout(
            # font = "Noto Sans Bold",
            fontsize=14,
            foreground=ocean_colors["FG"],
            #   background = ocean_colors["BG"]
        ),
        widget.Net(
            font="Noto Sans",
            fontsize=14,
            # Here enter your network name
            interface=["wlp6s0"],
            format='{down} ↓↑ {up}',
            foreground=colors[5],
            background=colors[19],
            padding=0,
        ),
        widget.Sep(linewidth=1,
                   padding=10,
                   foreground=ocean_colors["grey"],
                   background=ocean_colors["BG"]),
        widget.CPU(
            font="Noto Sans",
            #format = '{MemUsed}M/{MemTotal}M',
            update_interval=1,
            fontsize=14,
            foreground=ocean_colors["FG"],
            # background = colors[22],
            mouse_callbacks={
                'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')
            },
        ),
        widget.Sep(linewidth=1,
                   padding=10,
                   foreground=ocean_colors["grey"],
                   background=ocean_colors["BG"]),
        widget.Memory(
            font="Noto Sans",
            format='{MemUsed: .0f}M/{MemTotal: .0f}M',
            update_interval=1,
            fontsize=14,
            measure_mem='M',
            foreground=ocean_colors["FG"],
            # background = colors[16],
            mouse_callbacks={
                'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')
            },
        ),
        widget.Sep(linewidth=1,
                   padding=10,
                   foreground=ocean_colors["grey"],
                   background=ocean_colors["BG"]),
        widget.Clock(
            # foreground = colors[9],
            foreground=ocean_colors["FG"],
            # background = test_color,
            fontsize=14,
            format="%Y-%m-%d %H:%M"),
        widget.Sep(linewidth=1,
                   padding=10,
                   foreground=ocean_colors["grey"],
                   background=ocean_colors["BG"]),
        widget.Systray(
            #    background=colors[10],
            icon_size=17,
            padding=5),
        widget.Sep(linewidth=1,
                   padding=10,
                   foreground=ocean_colors["BG"],
                   background=ocean_colors["BG"]),
    ]
    return widgets_list


widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2


widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [
        Screen(top=bar.Bar(widgets=init_widgets_screen1(),
                           size=20,
                           opacity=1.00,
                           background=ocean_colors["BG"])),
        Screen(top=bar.Bar(widgets=init_widgets_screen2(),
                           size=20,
                           opacity=1.00,
                           background=ocean_colors["BG"]))
    ]


screens = init_screens()

# MOUSE CONFIGURATION
mouse = [
    Drag([super],
         "Button1",
         lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([super],
         "Button3",
         lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ##################
#########################################################
# @hook.subscribe.client_new
# def assign_app_group(client):
#     d = {}
#     #########################################################
#     ################ assgin apps to groups ##################
#     #########################################################
#     d["1"] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser",
#               "navigator", "firefox", "vivaldi-stable", "vivaldi-snapshot", "chromium", "google-chrome", "brave", "brave-browser", ]
#     d["2"] = [ "Atom", "Subl3", "Geany", "Brackets", "Code-oss", "Code", "TelegramDesktop", "Discord",
#                "atom", "subl3", "geany", "brackets", "code-oss", "code", "telegramDesktop", "discord", ]
#     d["3"] = ["Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",
#               "inkscape", "nomacs", "ristretto", "nitrogen", "feh", ]
#     d["4"] = ["Gimp", "gimp" ]
#     d["5"] = ["Meld", "meld", "org.gnome.meld" "org.gnome.Meld" ]
#     d["6"] = ["Vlc","vlc", "Mpv", "mpv" ]
#     d["7"] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer",
#               "virtualbox manager", "virtualbox machine", "vmplayer", ]
#     d["8"] = ["pcmanfm", "Nemo", "Caja", "Nautilus", "org.gnome.Nautilus", "Pcmanfm", "Pcmanfm-qt",
#               "pcmanfm", "nemo", "caja", "nautilus", "org.gnome.nautilus", "pcmanfm", "pcmanfm-qt", ]
#     d["9"] = ["Evolution", "Geary", "Mail", "Thunderbird",
#               "evolution", "geary", "mail", "thunderbird" ]
#     d["0"] = ["Spotify", "Pragha", "Clementine", "Deadbeef", "Audacious",
#               "spotify", "pragha", "clementine", "deadbeef", "audacious" ]
#     ##########################################################
#     wm_class = client.window.get_wm_class()[0]
#
#     for i in range(len(d)):
#         if wm_class in list(d.values())[i]:
#             group = list(d.keys())[i]
#             client.togroup(group)
#             client.group.cmd_toscreen()

# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME

main = None


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])


@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])


@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True


floating_types = ["notification", "toolbar", "splash", "dialog"]

follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),
    Match(wm_class='makebranch'),
    Match(wm_class='maketag'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(title='branchdialog'),
    Match(title='Open File'),
    Match(title='pinentry'),
    Match(wm_class='ssh-askpass'),
    Match(wm_class='lxpolkit'),
    Match(wm_class='Lxpolkit'),
    Match(wm_class='yad'),
    Match(wm_class='Yad'),
    Match(wm_class='Cairo-dock'),
    Match(wm_class='cairo-dock'),
],
                                  fullscreen_border_width=0,
                                  border_width=0)
auto_fullscreen = True

focus_on_window_activation = "focus"  # or smart

wmname = "LG3D"
