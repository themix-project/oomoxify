# -*- coding: utf-8 -*-
import os

from gi.repository import Gtk

from oomox_gui.export_common import ExportConfig, FileBasedExportDialog
from oomox_gui.i18n import translate
from oomox_gui.plugin_api import OomoxExportPlugin

PLUGIN_DIR = os.path.dirname(os.path.realpath(__file__))
OOMOXIFY_SCRIPT_PATH = os.path.join(
    PLUGIN_DIR, "oomoxify.sh"
)


OPTION_SPOTIFY_PATH = 'spotify_path'
OPTION_FONT_NAME = 'font_name'
OPTION_FONT_OPTIONS = 'font_options'
VALUE_FONT_DEFAULT = 'default'
VALUE_FONT_NORMALIZE = 'normalize'
VALUE_FONT_CUSTOM = 'custom'


class SpotifyExportDialog(FileBasedExportDialog):

    export_config = None
    timeout = 120

    def do_export(self):
        self.export_config[OPTION_FONT_NAME] = self.font_name_entry.get_text()
        self.export_config[OPTION_SPOTIFY_PATH] = self.spotify_path_entry.get_text()
        self.export_config.save()

        export_args = [
            "bash",
            OOMOXIFY_SCRIPT_PATH,
            self.temp_theme_path,
            '--gui',
            '--spotify-apps-path', self.export_config[OPTION_SPOTIFY_PATH],
        ]
        if self.export_config[OPTION_FONT_OPTIONS] == VALUE_FONT_NORMALIZE:
            export_args.append('--font-weight')
        elif self.export_config[OPTION_FONT_OPTIONS] == VALUE_FONT_CUSTOM:
            export_args.append('--font')
            export_args.append(self.export_config[OPTION_FONT_NAME])

        self.command = export_args
        super().do_export()

    def on_font_radio_toggled(self, button, value):
        if button.get_active():
            self.export_config[OPTION_FONT_OPTIONS] = value
            self.font_name_entry.set_sensitive(value == VALUE_FONT_CUSTOM)

    def _init_radios(self):
        self.font_radio_default = \
            Gtk.RadioButton.new_with_mnemonic_from_widget(
                None,
                translate("Don't change _default font")
            )
        self.font_radio_default.connect(
            "toggled", self.on_font_radio_toggled, VALUE_FONT_DEFAULT
        )
        self.options_box.add(self.font_radio_default)

        self.font_radio_normalize = \
            Gtk.RadioButton.new_with_mnemonic_from_widget(
                self.font_radio_default,
                translate("_Normalize font weight")
            )
        self.font_radio_normalize.connect(
            "toggled", self.on_font_radio_toggled, VALUE_FONT_NORMALIZE
        )
        self.options_box.add(self.font_radio_normalize)

        self.font_radio_custom = Gtk.RadioButton.new_with_mnemonic_from_widget(
            self.font_radio_default,
            translate("Use custom _font:")
        )
        self.font_radio_custom.connect(
            "toggled", self.on_font_radio_toggled, VALUE_FONT_CUSTOM
        )
        self.options_box.add(self.font_radio_custom)

        self.font_name_entry = Gtk.Entry(text=self.export_config[OPTION_FONT_NAME])
        self.options_box.add(self.font_name_entry)

        self.font_name_entry.set_sensitive(
            self.export_config[OPTION_FONT_OPTIONS] == VALUE_FONT_CUSTOM
        )
        if self.export_config[OPTION_FONT_OPTIONS] == VALUE_FONT_NORMALIZE:
            self.font_radio_normalize.set_active(True)
        if self.export_config[OPTION_FONT_OPTIONS] == VALUE_FONT_CUSTOM:
            self.font_radio_custom.set_active(True)

    def __init__(self, transient_for, colorscheme, theme_name):
        super().__init__(
            transient_for=transient_for,
            headline=translate("Spotify Options"),
            colorscheme=colorscheme,
            theme_name=theme_name
        )
        self.label.hide()
        self.export_config = ExportConfig(
            config_name='spotify',
            default_config={
                OPTION_SPOTIFY_PATH: "/usr/share/spotify/Apps",
                OPTION_FONT_NAME: "sans-serif",
                OPTION_FONT_OPTIONS: VALUE_FONT_DEFAULT,
            }
        )

        export_options_headline = Gtk.Label()
        export_options_headline.set_markup('<b>' + translate("Font Options") + '</b>')
        export_options_headline.set_justify(Gtk.Justification.LEFT)
        export_options_headline.set_alignment(0.0, 0.0)
        self.options_box.add(export_options_headline)

        self._init_radios()

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        spotify_path_label = Gtk.Label(label=translate('Spotify _path:'),
                                       use_underline=True)
        self.spotify_path_entry = Gtk.Entry(text=self.export_config[OPTION_SPOTIFY_PATH])
        spotify_path_label.set_mnemonic_widget(self.spotify_path_entry)
        hbox.add(spotify_path_label)
        hbox.add(self.spotify_path_entry)

        self.options_box.add(hbox)

        self.box.add(self.options_box)
        self.options_box.show_all()
        self.box.add(self.apply_button)
        self.apply_button.show()


class Plugin(OomoxExportPlugin):

    name = 'spotify'
    display_name = 'Oomoxify'
    export_text = translate("Apply Spotif_y Theme…")
    about_text = translate('Apply the current theme to Spotify Desktop app.')
    about_links = [
        {
            'name': translate('Homepage'),
            'url': 'https://github.com/themix-project/oomoxify/',
        },
    ]

    export_dialog = SpotifyExportDialog

    theme_model_extra = [
        {
            'type': 'separator',
            'display_name': translate('Spotify')
        },
        {
            'key': 'SPOTIFY_PROTO_BG',
            'type': 'color',
            'fallback_key': 'HDR_BG',
            'display_name': translate('Background'),
        },
        {
            'key': 'SPOTIFY_PROTO_FG',
            'type': 'color',
            'fallback_key': 'HDR_FG',
            'display_name': translate('Foreground'),
        },
        {
            'key': 'SPOTIFY_PROTO_SEL',
            'type': 'color',
            'fallback_key': 'SEL_BG',
            'display_name': translate('Accent Color'),
        },
    ]
