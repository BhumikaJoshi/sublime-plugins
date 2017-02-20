import sublime
import sublime_plugin
import os
import subprocess
from subprocess import call
from subprocess import PIPE
import sys

class runprogramCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		#print(self.view.file_name())
		filepath = self.view.file_name()
		#folderPath = self.get_folder_path(javaFilepath)
		folderpath, filename = head, tail = os.path.split(filepath)
		
		compileCmd = "javac " + filepath
		runCmd = "java -classpath " + folderpath + " " + filename.rstrip(".java")
		delCmd = filepath.rstrip("java") + "class"
		
		compileOut = subprocess.Popen(compileCmd, shell=True, stderr=PIPE).communicate()[1]
		html = "<div style='overflow:auto; width:400px; height:400px; white-space:pre-wrap;'>output</div>"

		if len(compileOut)>0:
			self.view.show_popup(html.replace("output",compileOut.decode("utf-8").replace("\n","<br />")), max_width=512, on_navigate=lambda x: copy(self.view, x))
		else:
			runOut = subprocess.Popen(runCmd, shell=True, stdout=PIPE).communicate()[0]
			self.view.show_popup(html.replace("output",runOut.decode("utf-8").replace("\n","<br />")), max_width=512, on_navigate=lambda x: copy(self.view, x))
			os.remove(delCmd)