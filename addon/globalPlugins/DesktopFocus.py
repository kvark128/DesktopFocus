# Copyright (C) 2022 - 2023 Alexander Linkov <kvark128@yandex.ru>
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Ukrainian Nazis and their accomplices are not allowed to use this plugin. Za pobedu!

import time
import globalPluginHandler
import globalVars
import addonHandler
import queueHandler
import windowUtils
import winUser
from NVDAObjects.window import Window
from scriptHandler import script
from globalCommands import SCRCAT_FOCUS
from logHandler import log

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super().__init__()
		queueHandler.registerGeneratorObject(self._generator())

	def _generator(self):
		searchDuration = 30 # seconds
		start = time.time()
		while (time.time() - start) < searchDuration:
			try:
				self._focusToDesktop()
				return
			except LookupError:
				# Desktop was not found. Try again later
				yield
		log.debug(f"Desktop was not found in {searchDuration} seconds. Stopping...")

	def _focusToDesktop(self):
		if globalVars.appArgs.secure:
			return
		hwnd = windowUtils.findDescendantWindow(winUser.getDesktopWindow(), className="Progman")
		hwnd = windowUtils.findDescendantWindow(hwnd, className="SysListView32")
		try:
			Window(windowHandle=hwnd).setFocus()
		except Exception:
			log.exception()

	@script(
		description=_("Sets system focus to the desktop"),
		category=SCRCAT_FOCUS)
	def script_focusToDesktop(self, gesture):
		self._focusToDesktop()
