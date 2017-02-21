import sublime
import sublime_plugin
import os
import subprocess
from subprocess import call
from subprocess import PIPE
import sys

class runprogramCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		currentWindow = self.view.window()
		currentWindow.show_input_panel("Arguments: ", "", self.on_done, None, None)

	def on_done(self, text):

		filepath = self.view.file_name()
		folderpath, filename = head, tail = os.path.split(filepath)
		
		print(text)

		compileCmd = "javac " + filepath
		runCmd = "java -classpath " + folderpath + " " + filename.rstrip(".java") + " " + text
		delCmd = filepath.rstrip("java") + "class"
		
		compileOut = subprocess.Popen(compileCmd, shell=True, stderr=PIPE).communicate()[1]
		html = "<div style='overflow:auto; width:400px; height:400px; white-space:pre-wrap;'>output</div>"

		if len(compileOut)>0:
			self.view.show_popup(html.replace("output",compileOut.decode("utf-8").replace("\n","<br />")), max_width=512, on_navigate=lambda x: copy(self.view, x))
		else:
			runOut = subprocess.Popen(runCmd, shell=True, stdout=PIPE).communicate()[0]
			self.view.show_popup(html.replace("output",runOut.decode("utf-8").replace("\n","<br />")), max_width=512, on_navigate=lambda x: copy(self.view, x))
			os.remove(delCmd)